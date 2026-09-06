"""Artifact freshness and explicit dependency invalidation for theorem reuse."""
import copy
import os
from pathlib import Path
from .model import WorkflowState, NodeStatus
from .store import StateStore
from .verification import source_snapshot
from .reduction import reduction_snapshot


def audit_registry(state: WorkflowState) -> dict[str, dict[str, str]]:
    results = {}
    for node_id, entry in state.registry.items():
        node = state.nodes.get(node_id)
        receipt = entry.get('verification_receipt', {})
        artifact = entry.get('artifact', '')
        projects = [Path(artifact)]
        # Backward-compatible read-only view for receipts created by the Linux
        # verifier before artifact_aliases was introduced. The evidence remains
        # the original Linux snapshot; this only locates it from Windows.
        if os.name == 'nt' and artifact.startswith('/home/'):
            projects.append(Path('\\\\wsl.localhost\\Ubuntu' + artifact.replace('/', '\\')))
        projects.extend(Path(p) for p in receipt.get('artifact_aliases', []))
        if node is None or node.status != NodeStatus.VERIFIED or entry.get('statement') != node.statement:
            results[node_id] = {'status': 'stale', 'reason': 'node and registry disagree'}
            continue
        if state.manifest and receipt.get('manifest', {}).get('sha256') != state.manifest.get('sha256'):
            results[node_id] = {'status': 'stale', 'reason': 'verification manifest identity differs'}
            continue
        if not receipt.get('source_hashes') or not entry.get('artifact'):
            results[node_id] = {'status': 'unavailable', 'reason': 'missing source evidence'}
            continue
        project = next((p for p in projects if p.is_dir()), None)
        if project is None:
            results[node_id] = {'status': 'unavailable', 'reason': 'artifact environment unavailable'}
            continue
        try:
            snapshot = reduction_snapshot if receipt.get('verification_kind') == 'reduction' else source_snapshot
            current = snapshot(
                project, declared_source_files=receipt.get('source_files', ()))
        except (OSError, ValueError) as exc:
            results[node_id] = {'status': 'unavailable', 'reason': str(exc)}
            continue
        results[node_id] = {'status': 'current' if current == receipt['source_hashes'] else 'stale',
                            'reason': 'source snapshot compared'}
    return results


def invalidate_dependents(state: WorkflowState, node_ids: list[str], *, reason: str,
                          store: StateStore | None = None) -> set[str]:
    """Reopen stale nodes and all parents; archive receipts instead of erasing history.

    Running attempts require explicit coordination first. Missing access to an artifact
    is not evidence that its contents changed and must not trigger this function.
    """
    if not reason.strip() or not set(node_ids) <= state.nodes.keys():
        raise ValueError('invalidation needs existing targets and a reason')
    state.validate()
    impacted = set(node_ids)
    reverse = {node_id: set() for node_id in state.nodes}
    for parent in state.nodes.values():
        for child in parent.dependencies:
            reverse[child].add(parent.id)
    work = list(impacted)
    while work:
        for parent in reverse[work.pop()] - impacted:
            impacted.add(parent)
            work.append(parent)
    if any(state.nodes[node_id].status == NodeStatus.IN_PROGRESS for node_id in impacted):
        raise ValueError('cannot invalidate while an affected attempt is running')
    candidate = copy.deepcopy(state)
    for node_id in sorted(impacted):
        node = candidate.nodes[node_id]
        entry = candidate.registry.pop(node_id, None)
        if entry is not None:
            node.metadata.setdefault('previous_verifications', []).append(entry)
        node.status = NodeStatus.OPEN
        node.verified_artifact = None
    candidate.event('verification_invalidated', roots=node_ids, affected=sorted(impacted), reason=reason)
    if store:
        store.save(candidate)
        state.revision = candidate.revision
    state.nodes, state.registry, state.events = candidate.nodes, candidate.registry, candidate.events
    return impacted
