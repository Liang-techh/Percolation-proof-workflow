"""Trusted coordinator entry point for final-target verification and registration."""
from pathlib import Path
import hashlib
import json
from pathlib import PurePosixPath
from .comparator import load_config, run_comparator, validate_source_files
from .strict_admission import audit_strict_admission
from .lean import run_lean
from .model import EvidenceStage, WorkflowState
from .store import StateStore
from .statements import index_statements
from .provenance import write_audit


def source_snapshot(project: Path, *, declared_source_files=()) -> dict[str, str]:
    """Bind local Lean sources and project manifests; dependency revisions are in lake-manifest.

    This is not a sandbox against concurrent hostile writers or modified dependency caches.
    Run verification in a coordinator-owned isolated checkout.
    """
    required = ['lean-toolchain', 'lake-manifest.json', 'comparator.json']
    for name in required:
        if not (project / name).is_file():
            raise ValueError(f'missing verification input: {name}')
    paths = [p for p in project.rglob('*.lean') if '.lake' not in p.relative_to(project).parts
             and '.git' not in p.relative_to(project).parts]
    paths.extend(project / name for name in required)
    paths.extend(p for p in (project / 'lakefile.toml', project / 'lakefile.lean') if p.is_file())
    for value in validate_source_files(declared_source_files):
        relative = PurePosixPath(value)
        path = (project / Path(*relative.parts)).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError(f'missing comparator source input: {value}')
        paths.append(path)
    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths))}


def verify_and_register(state: WorkflowState, node_id: str, project: str | Path,
                        comparator_command: list[str], *, store: StateStore,
                        artifact_aliases: list[str | Path] | None = None,
                        manifest_identity: dict | None = None) -> bool:
    """Execute both gates, reject source drift, then register a named comparator target.

    comparator_command must be supplied by the trusted coordinator, not by a proof agent.
    It must run the pinned upstream comparator with the project's comparator.json.
    """
    project = Path(project).resolve()
    state.validate()
    node = state.nodes[node_id]
    state.set_evidence_stage(node_id, EvidenceStage.SOURCE_COMPARATOR_PENDING)
    config = load_config(project / 'comparator.json')
    if node.name not in config.theorem_names:
        raise ValueError('node is not a comparator target')
    if set(config.permitted_axioms) - {'propext', 'Quot.sound', 'Classical.choice'}:
        raise ValueError('nonstandard permitted axioms')
    if not config.enable_nanoda:
        raise ValueError('final acceptance requires nanoda')
    challenge = project.joinpath(*config.challenge_module.split('.')).with_suffix('.lean')
    if not challenge.resolve().is_relative_to(project):
        raise ValueError('Challenge must be inside the isolated project')
    matches = [record for record in index_statements(challenge) if record.qualified_name == node.name]
    if len(matches) != 1 or node.metadata.get('statement_status') != 'indexed' or node.statement != matches[0].source:
        raise ValueError('node statement is not bound to the trusted Challenge declaration')
    identity = {'module': config.challenge_module, 'name': node.name,
                'challenge_sha256': hashlib.sha256(challenge.read_bytes()).hexdigest(),
                'statement_sha256': hashlib.sha256(node.statement.encode()).hexdigest()}
    if any(state.nodes[dep].status != 'verified' for dep in node.dependencies):
        raise ValueError('open dependencies prevent registry promotion')
    audit = write_audit(project, config.solution_module, node.name,
                        state.nodes[state.root_id].metadata.get('contract', {}))
    declared_source_files = getattr(config, 'source_files', ())
    before = source_snapshot(project, declared_source_files=declared_source_files)
    attempt = state.begin_attempt(node_id, 'verification-coordinator')
    store.save(state)
    result = run_lean(project, ['lake', 'build', config.solution_module])
    state.event('verification_lean_finished', attempt_id=attempt, exit_code=result.exit_code,
                command=result.command, stdout=result.stdout, stderr=result.stderr)
    store.save(state)
    if not result.ok:
        state.set_evidence_stage(node_id, EvidenceStage.OPEN)
        state.finish_attempt(attempt, status='compile_error', command=result.command,
            stdout=result.stdout, stderr=result.stderr, exit_code=result.exit_code)
        store.save(state)
        return False
    if audit:
        checked = run_lean(project, ['lake', 'env', 'lean', str(audit[0])])
        provenance_ok = checked.ok and audit[1] in checked.stdout.splitlines()
        state.event('verification_provenance_finished', attempt_id=attempt,
                    accepted=provenance_ok, command=checked.command,
                    stdout=checked.stdout, stderr=checked.stderr, exit_code=checked.exit_code)
        if not provenance_ok:
            state.set_evidence_stage(node_id, EvidenceStage.OPEN)
            state.finish_attempt(attempt, status='provenance_rejected', command=checked.command,
                                 stdout=checked.stdout, stderr=checked.stderr, exit_code=1)
            store.save(state)
            return False
    strict_result = None
    if getattr(config, 'strict_admission', False):
        strict_result = audit_strict_admission(
            project, config.theorem_names,
            solution_module=config.solution_module,
            challenge_module=config.challenge_module)
        state.event('strict_admission_finished', node_id=node_id,
                    accepted=strict_result.accepted,
                    reasons=strict_result.reasons,
                    axioms=strict_result.axioms,
                    toolchain=strict_result.toolchain,
                    toolchain_sha256=strict_result.toolchain_sha256,
                    lake_manifest_sha256=strict_result.lake_manifest_sha256,
                    command=list(strict_result.command),
                    stdout=strict_result.stdout, stderr=strict_result.stderr)
        store.save(state)
        if not strict_result.accepted:
            state.set_evidence_stage(node_id, EvidenceStage.OPEN)
            state.finish_attempt(
                attempt, status='strict_admission_rejected',
                command=list(strict_result.command), stdout=strict_result.stdout,
                stderr='\n'.join(strict_result.reasons) + '\n' + strict_result.stderr,
                exit_code=1)
            store.save(state)
            return False
    state.set_evidence_stage(node_id, EvidenceStage.LEAN_VERIFIED)
    try:
        accepted, stdout, stderr = run_comparator(project, comparator_command)
        after = source_snapshot(project, declared_source_files=declared_source_files)
    except Exception as exc:
        state.set_evidence_stage(node_id, EvidenceStage.OPEN)
        state.finish_attempt(attempt, status='verification_error', command=comparator_command,
                             stdout='', stderr=repr(exc), exit_code=1)
        store.save(state)
        return False
    state.event('comparator_finished', node_id=node_id, command=comparator_command,
                accepted=accepted, stdout=stdout, stderr=stderr)
    store.save(state)
    if not accepted or before != after:
        state.set_evidence_stage(node_id, EvidenceStage.SOURCE_COMPARATOR_PENDING)
        state.finish_attempt(attempt, status='verification_rejected', command=comparator_command,
                             stdout=stdout, stderr=stderr, exit_code=1)
        state.event('verification_rejected', node_id=node_id,
                    comparator_accepted=accepted, source_changed=before != after)
        store.save(state)
        return False
    state.finish_attempt(attempt, status='passed', command=comparator_command,
                         stdout=stdout, stderr=stderr, exit_code=0)
    receipt = {'attempt_id': attempt, 'source_hashes': before,
               'source_digest': hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
               'comparator_command': comparator_command, 'comparator_stdout': stdout,
               'comparator_stderr': stderr, 'config': 'comparator.json', 'statement_identity': identity,
               'source_files': list(declared_source_files),
               'artifact_aliases': [str(p) for p in (artifact_aliases or [])]}
    if strict_result is not None:
        receipt['strict_admission'] = {
            'accepted': strict_result.accepted,
            'theorem_names': list(strict_result.theorem_names),
            'axioms': {name: list(values) for name, values in strict_result.axioms.items()},
            'toolchain': strict_result.toolchain,
            'toolchain_sha256': strict_result.toolchain_sha256,
            'lake_manifest_sha256': strict_result.lake_manifest_sha256,
            'command': list(strict_result.command),
            'stdout': strict_result.stdout,
            'stderr': strict_result.stderr,
        }
    if manifest_identity is not None:
        receipt['manifest'] = manifest_identity
    state._register_verified(node_id, str(project), receipt=receipt)
    store.save(state)
    return True
