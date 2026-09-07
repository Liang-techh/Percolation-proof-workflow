"""Automatic closure of Prove2Me-style reductions after child verification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .lean import run_lean
from .model import EvidenceStage, NodeStatus
from .store import StateStore
from .freshness import audit_freshness


def reduction_snapshot(project: Path, *, declared_source_files=()) -> dict[str, str]:
    """Hash the reduction project's source and pinned build inputs."""
    paths = [p for p in project.rglob('*') if p.is_file()
             and '.lake' not in p.relative_to(project).parts
             and (p.suffix == '.lean' or p.name in
                  {'lean-toolchain', 'lake-manifest.json', 'lakefile.toml', 'lakefile.lean'})]
    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}


def close_verified_reductions(store: StateStore) -> list[str]:
    """Promote accepted reductions whose exact children are all registry-verified.

    This is the Prove2Me cascade: the reduction audit proves the parent from its
    child statements, and child registry evidence discharges those assumptions.
    The ordinary root comparator still runs after the cascade, so automatic
    closure never bypasses the final statement/kernel gate.
    """
    state = store.load()
    closed: list[str] = []
    for parent in list(state.nodes.values()):
        if parent.status != NodeStatus.OPEN:
            continue
        proposals = parent.metadata.get('reduction_proposals', [])
        proposal = next((item for item in reversed(proposals)
                         if item.get('status') == 'sketch_checked'
                         and item.get('reduction_status') == 'accepted'), None)
        if proposal is None or not proposal.get('audit_marker'):
            continue
        if any(state.nodes[child].status != NodeStatus.VERIFIED
               or child not in state.registry
               or state.registry[child].get('statement') != state.nodes[child].statement
               for child in proposal.get('children', [])):
            continue
        audit = Path(proposal.get('audit', ''))
        project = audit.parent
        if not audit.is_file() or not project.is_dir():
            state.event('reduction_reuse_unavailable', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'), audit=str(audit))
            store.save(state)
            continue
        try:
            before = reduction_snapshot(project)
        except OSError as exc:
            state.event('reduction_reuse_unavailable', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'), error=repr(exc))
            store.save(state)
            continue
        if before != proposal.get('source_hashes'):
            state.event('reduction_reuse_refused', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'), reason='source snapshot changed')
            store.save(state)
            continue
        fresh, reasons = audit_freshness(project, proposal.get('freshness'))
        if not fresh:
            state.event('reduction_reuse_refused', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'),
                        reason='verification inputs are stale', freshness_reasons=list(reasons))
            store.save(state)
            continue

        attempt_id = state.begin_attempt(parent.id, 'reduction-coordinator', str(audit))
        store.save(state)
        command = ['lake', 'env', 'lean', str(audit)]
        try:
            result = run_lean(project, command)
        except Exception as exc:
            state = store.load()
            current = state.attempts.get(attempt_id)
            if current is not None and current.finished_at is None:
                state.finish_attempt(attempt_id, status='verification_error', command=command,
                                     stdout='', stderr=repr(exc), exit_code=125)
                state.event('reduction_cascade_error', node_id=parent.id,
                            proposal_id=proposal.get('proposal_id'), command=command,
                            error=repr(exc), recovered_for_repair=True)
                store.save(state)
            continue
        state = store.load()
        accepted = result.ok and proposal.get('audit_marker') in result.stdout.splitlines()
        if accepted and before == reduction_snapshot(project):
            state.event('reduction_cascade_verified', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'), children=proposal['children'],
                        command=command, stdout=result.stdout, stderr=result.stderr)
            state.finish_attempt(attempt_id, status='passed', command=command,
                                 stdout=result.stdout, stderr=result.stderr, exit_code=0)
            state.set_evidence_stage(parent.id, EvidenceStage.LEAN_VERIFIED)
            receipt = {
                'verification_kind': 'reduction',
                'attempt_id': attempt_id,
                'source_hashes': before,
                'source_digest': hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
                'reduction_command': command,
                'reduction_stdout': result.stdout,
                'reduction_stderr': result.stderr,
                'reduction_name': proposal['reduction_name'],
                'reduction_audit': str(audit),
                'reduction_marker': proposal['audit_marker'],
                'child_registries': {
                    child: state.registry[child]['verification_receipt'].get('source_digest', child)
                    for child in proposal['children']
                },
                'statement_identity': {
                    'module': 'reduction-audit', 'name': parent.name,
                    'statement_sha256': hashlib.sha256(parent.statement.encode()).hexdigest(),
                },
                'manifest': state.manifest or {},
            }
            required_ids = list(parent.metadata.get('required_node_ids', []))
            if required_ids:
                receipt['required_input_registries'] = {
                    required_id: state.registry[required_id]['verification_receipt'].get(
                        'source_digest', required_id)
                    for required_id in required_ids
                    if required_id in state.registry
                }
            state._register_verified(parent.id, str(project), receipt=receipt)
            store.save(state)
            closed.append(parent.id)
        else:
            state.finish_attempt(attempt_id, status='verification_error', command=command,
                                 stdout=result.stdout, stderr=result.stderr or
                                 'reduction audit rejected or source changed', exit_code=1)
            state.event('reduction_cascade_rejected', node_id=parent.id,
                        proposal_id=proposal.get('proposal_id'), command=command,
                        stdout=result.stdout, stderr=result.stderr, exit_code=result.exit_code)
            store.save(state)
    return closed


__all__ = ['close_verified_reductions', 'reduction_snapshot']
