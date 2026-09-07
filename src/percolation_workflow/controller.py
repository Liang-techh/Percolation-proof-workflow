"""Persistent frontier-driven verification; proof generation is supplied by Codex agents."""
import hashlib
import json
from pathlib import Path
from .store import StateStore
from .model import EvidenceStage, NodeStatus
from .registry import audit_registry
from .verification import verify_and_register, source_snapshot
from .lean import run_lean
from .comparator import load_config, run_comparator
from .statements import index_statements
from .provenance import write_audit
from .strict_admission import audit_strict_admission
from .bundles import stage_bundle
from .manifest import bind_manifest, load_verification_manifest
from .reduction import close_verified_reductions


def final_project_check(store, state, project, comparator_command, *, manifest_identity=None):
    # This function is also callable directly, so do not rely on verify_frontier
    # having established the admission preconditions for us.  In particular,
    # a comparator success is not theorem verification when the root has no
    # registry receipt or an explicit Lean-verified stage.
    root = state.nodes.get(state.root_id)
    admission_reasons = []
    if root is None:
        admission_reasons.append('missing workflow root')
    else:
        if root.status != NodeStatus.VERIFIED:
            admission_reasons.append('root is not VERIFIED')
        if root.id not in state.registry:
            admission_reasons.append('root is absent from verified registry')
        if state.evidence_stage(root.id) not in {
                EvidenceStage.LEAN_VERIFIED, EvidenceStage.GLOBAL_CLOSED}:
            admission_reasons.append('root lacks LEAN_VERIFIED/GLOBAL_CLOSED stage')
    if state.nodes and any(node.status != NodeStatus.VERIFIED for node in state.nodes.values()):
        admission_reasons.append('all theorem-DAG nodes are not VERIFIED')
    if set(state.registry) != {node.id for node in state.nodes.values()
                               if node.status == NodeStatus.VERIFIED}:
        admission_reasons.append('verified-node set and registry disagree')
    declared_gate = state.global_closure.get('formal_certificate_allowed')
    if declared_gate is not True:
        admission_reasons.append('formal_certificate_allowed is not explicitly true')
    if admission_reasons:
        state.event('controller_final_admission', accepted=False,
                    reasons=admission_reasons, comparator_skipped=True)
        store.save(state)
        return 'needs_repair'
    project = Path(project).resolve()
    config = load_config(project / 'comparator.json')
    root = state.nodes[state.root_id]
    if root.name not in config.theorem_names or not config.enable_nanoda or (
            set(config.permitted_axioms) - {'propext', 'Quot.sound', 'Classical.choice'}):
        raise ValueError('final comparator must cover the root with the standard kernel gates')
    records = [r for r in index_statements(
        project.joinpath(*config.challenge_module.split('.')).with_suffix('.lean'))
        if r.qualified_name == root.name]
    if len(records) != 1 or records[0].source != root.statement:
        raise ValueError('final Challenge differs from the root statement')
    contract = root.metadata.get('contract', {})
    audit = write_audit(project, config.solution_module, root.name, contract) if contract else None
    before = source_snapshot(project,
                             declared_source_files=getattr(config, 'source_files', ()))
    module_targets = sorted({config.challenge_module, config.solution_module} | {
        p.stem for p in project.glob('*.lean')
        if not p.stem.startswith(('ProvenanceAudit', 'SketchAudit'))})
    build_command = ['lake', 'build', *module_targets]
    result = run_lean(project, build_command)
    state.event('controller_full_build', exit_code=result.exit_code,
                stdout=result.stdout, stderr=result.stderr, command=result.command,
                manifest=manifest_identity)
    store.save(state)
    if not result.ok:
        return 'needs_repair'
    if audit:
        result = run_lean(project, ['lake', 'env', 'lean', str(audit[0])])
        accepted = result.ok and audit[1] in result.stdout.splitlines()
        state.event('controller_final_provenance', accepted=accepted, stdout=result.stdout,
                    stderr=result.stderr, exit_code=result.exit_code, command=result.command)
        store.save(state)
        if not accepted:
            return 'needs_repair'
    if getattr(config, 'strict_admission', False):
        strict = audit_strict_admission(
            project, config.theorem_names,
            solution_module=config.solution_module,
            challenge_module=config.challenge_module)
        state.event('controller_strict_admission',
                    accepted=strict.accepted, reasons=strict.reasons,
                    axioms=strict.axioms, toolchain=strict.toolchain,
                    toolchain_sha256=strict.toolchain_sha256,
                    lake_manifest_sha256=strict.lake_manifest_sha256,
                    command=list(strict.command), stdout=strict.stdout,
                    stderr=strict.stderr)
        store.save(state)
        if not strict.accepted:
            return 'needs_repair'
    accepted, stdout, stderr = run_comparator(project, comparator_command)
    unchanged = before == source_snapshot(
        project, declared_source_files=getattr(config, 'source_files', ()))
    state.event('controller_final_comparator', accepted=accepted, source_unchanged=unchanged,
                stdout=stdout, stderr=stderr, command=comparator_command, source_hashes=before,
                manifest=manifest_identity)
    store.save(state)
    return 'verified' if accepted and unchanged else 'needs_repair'


def verify_frontier(store: StateStore, project: str | Path, comparator_command: list[str],
                    *, max_steps: int = 100,
                    node_projects: dict[str, str | Path] | None = None,
                    manifest_identity: dict | None = None) -> str:
    """Verify available artifacts in dependency order without hard-coded theorem names.

    Returns needs_repair on a rejected artifact, awaiting_work if no eligible frontier,
    and paused on the step limit. Existing in-progress attempts are never restarted.
    The caller owns the checkout and state writer; concurrent controllers are unsupported.
    node_projects is a trusted coordinator mapping to isolated per-node verification
    bundles, each with its own Challenge, Solution and comparator config. The project
    argument remains the final assembled project, never a substitute leaf bundle.
    """
    if not store.path.is_file() or max_steps < 1:
        raise ValueError('existing state and positive step bound required')
    state = store.load()
    state.validate()
    if node_projects is not None and set(node_projects) != set(state.nodes):
        raise ValueError('per-node project mapping must cover exactly the current theorem DAG')
    if {n.id for n in state.nodes.values() if n.status == 'verified'} != set(state.registry):
        state.event('controller_reuse_refused', reason='verified nodes and registry disagree')
        store.save(state)
        return 'needs_revalidation'
    freshness = audit_registry(state)
    if any(item['status'] != 'current' for item in freshness.values()):
        state.event('controller_reuse_refused', freshness=freshness)
        store.save(state)
        return 'needs_revalidation'
    for _ in range(max_steps):
        close_verified_reductions(store)
        state = store.load()
        if state.nodes and all(node.status == 'verified' for node in state.nodes.values()):
            return final_project_check(store, state, project, comparator_command,
                                       manifest_identity=manifest_identity)
        frontier = [node for node in state.frontier() if node.metadata.get('statement_status') == 'indexed']
        if not frontier:
            state.event('controller_awaiting_work', in_progress=[n.id for n in state.nodes.values()
                        if n.status == 'in_progress'])
            store.save(state)
            return 'awaiting_work'
        node = frontier[0]
        node_project = node_projects[node.id] if node_projects is not None else project
        state.event('controller_frontier_selected', node_id=node.id, project=str(node_project))
        store.save(state)
        kwargs = {'store': store}
        if manifest_identity is not None:
            kwargs['manifest_identity'] = manifest_identity
        if not verify_and_register(state, node.id, node_project, comparator_command, **kwargs):
            return 'needs_repair'
    state.event('controller_paused', max_steps=max_steps)
    store.save(state)
    return 'paused'


def verify_manifest_frontier(store: StateStore, manifest_path: str | Path,
                             dependency_project: str | Path, bundle_root: str | Path,
                             comparator_command: list[str], *, max_steps: int = 100) -> str:
    """Stage every manifest-described node and drive the ordinary frontier controller.

    Paths to the pinned dependency, bundle cache and comparator executable remain runtime
    overlays; theorem/module/source selection and state identity come from the manifest.
    """
    manifest = load_verification_manifest(manifest_path)
    if store.path.resolve() != manifest.state_path.resolve():
        raise ValueError('manifest state_path does not match the supplied state store')
    bind_manifest(store, manifest)
    state = store.load()
    root = state.nodes.get(state.root_id)
    if root is None or (manifest.target_root and root.name != manifest.target_root):
        raise ValueError('manifest target root does not match research state')
    if manifest.contract_path is not None:
        if not manifest.contract_path.is_file():
            raise ValueError('manifest target.contract does not exist')
        contract = json.loads(manifest.contract_path.read_text(encoding='utf-8'))
        if not isinstance(contract, dict):
            raise ValueError('manifest target.contract must contain an object')
        if manifest.target_root and contract.get('target') != manifest.target_root:
            raise ValueError('manifest contract target does not match manifest target')
        existing = root.metadata.get('contract')
        if existing is not None and existing != contract:
            raise ValueError('manifest contract differs from the bound research contract')
        if existing is None:
            root.metadata['contract'] = contract
            root.metadata['contract_path'] = manifest.contract_path.name
    state.event('manifest_runtime_selected', manifest=manifest.identity_for_state(),
                target_root=manifest.target_root, dependency_name=manifest.dependency_name,
                dependency_profile=manifest.dependency_profile, toolchain=manifest.toolchain,
                contract_sha256=(hashlib.sha256(manifest.contract_path.read_bytes()).hexdigest()
                                 if manifest.contract_path is not None else None),
                verification_profile=manifest.verification.get('comparator_profile'))
    store.save(state)
    projects = {}
    for node in state.nodes.values():
        spec = manifest.for_node(node.name)
        projects[node.id] = stage_bundle(
            manifest.path.parent, bundle_root, node_name=node.name,
            challenge_module=spec.challenge_module, solution_module=spec.solution_module,
            source_files=spec.source_files, dependency_project=dependency_project,
            dependency_name=manifest.dependency_name,
            manifest_identity=manifest.identity_for_state())
    # The root bundle is the assembled, content-addressed final project. Keep
    # the last full build/comparator inside that isolated environment rather
    # than falling back to the mutable manifest source directory.
    return verify_frontier(store, projects[state.root_id], comparator_command,
                           max_steps=max_steps, node_projects=projects,
                           manifest_identity=manifest.identity_for_state())
