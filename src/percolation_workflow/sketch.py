"""Check a reduction as an axiom-free implication before opening its child frontier.

Children are explicit assumptions, never admitted theorems. This is a local analogue
of SKETCH_ACCEPTED, not a proof of the parent. A single universe parameter is renamed
consistently across targets; multiple universe parameters require an explicit future map.
"""
import hashlib
import json
from pathlib import Path
import re
import uuid
from .lean import run_lean
from .statements import index_statements
from .store import StateStore
from .provenance import lean_checks
from .model import now
from .freshness import bind_freshness


def _name(value):
    if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)*', value):
        raise ValueError('unsupported Lean identifier in sketch audit')
    return value


def _snapshot(project):
    paths = [p for p in project.rglob('*') if p.is_file()
             and '.lake' not in p.relative_to(project).parts
             and (p.suffix == '.lean' or p.name in
                  {'lean-toolchain', 'lakefile.toml', 'lake-manifest.json'})]
    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def check_sketch(store: StateStore, parent_id: str, project: str | Path, *,
                 challenge_module: str, reduction_module: str, reduction_name: str,
                 obligation_modules: list[str] | None = None) -> bool:
    """Trusted coordinator supplies immutable Challenge and isolated project modules."""
    project = Path(project).resolve()
    obligation_modules = obligation_modules or []
    for value in (challenge_module, reduction_module, reduction_name, *obligation_modules):
        _name(value)
    state = store.load()
    state.validate()
    parent = state.nodes[parent_id]
    if parent.status != 'open':
        raise ValueError('parent must be open for sketch checking')
    proposal = parent.metadata['reduction_proposals'][-1]
    if proposal['status'] != 'proposed':
        raise ValueError('latest proposal is not pending')
    children = proposal['children']
    records = {}
    for module in dict.fromkeys([challenge_module, *obligation_modules]):
        for record in index_statements(project.joinpath(*module.split('.')).with_suffix('.lean')):
            if record.qualified_name in records:
                raise ValueError('ambiguous statement declaration across obligation modules')
            records[record.qualified_name] = record.source
    for node_id in [parent_id, *children]:
        node = state.nodes[node_id]
        _name(node.name)
        if records.get(node.name) != node.statement:
            raise ValueError('sketch node differs from its trusted Challenge statement')
    names = ', '.join('`' + state.nodes[c].name for c in children)
    marker = 'REDUCTION_CHECKED_' + uuid.uuid4().hex
    provenance = lean_checks(state.nodes[state.root_id].metadata.get('contract', {}), reduction_name)
    audit = project / ('SketchAudit_' + uuid.uuid4().hex + '.lean')
    obligation_imports = '\n'.join('import ' + module for module in obligation_modules)
    audit.write_text(f'''import {challenge_module}
import {reduction_module}
{obligation_imports}
import Lean
import Lean.Util.CollectAxioms
open Lean Meta in
run_meta do
  let env ← getEnv
  let getType := fun (n : Name) => do
    let some info := env.find? n | throwError "missing declaration {{n}}"
    unless info.levelParams.length ≤ 1 do
      throwError "multiple universe parameters need an explicit map: {{n}}"
    pure (info.type.instantiateLevelParams info.levelParams (info.levelParams.map fun _ => Level.param `audit_u))
  let mut expected ← getType `{parent.name}
  for child in (#[{names}] : Array Name).reverse do
    expected := mkForall `_ BinderInfo.default (← getType child) expected
  let some (.thmInfo proof) := env.find? `{reduction_name}
    | throwError "reduction must be a theorem"
  unless ← isDefEq (← getType `{reduction_name}) expected do
    throwError "reduction does not prove the specified child-to-parent implication"
  for ax in (← collectAxioms `{reduction_name}) do
    unless #[`propext, `Quot.sound, `Classical.choice].contains ax do
      throwError "unproved or forbidden dependency: {{ax}}"
{provenance}
  logInfo "{marker}"
''', encoding='utf-8')
    before = _snapshot(project)
    state.event('sketch_check_started', parent_id=parent_id, children=children, audit=str(audit))
    store.save(state)
    build = run_lean(project, ['lake', 'build', challenge_module, reduction_module, *obligation_modules])
    result = run_lean(project, ['lake', 'env', 'lean', str(audit)]) if build.ok else build
    accepted = result.ok and marker in result.stdout.splitlines() and before == _snapshot(project)
    state = store.load()
    latest = state.nodes[parent_id].metadata['reduction_proposals'][-1]
    if latest != proposal:
        raise ValueError('decomposition changed during sketch checking')
    state.event('sketch_check_finished', parent_id=parent_id, accepted=accepted,
                build_command=build.command, build_stdout=build.stdout, build_stderr=build.stderr,
                command=result.command, stdout=result.stdout, stderr=result.stderr,
                exit_code=result.exit_code, source_hashes=before)
    if accepted:
        olean_paths = [p.relative_to(project).as_posix() for p in project.rglob('*.olean')
                       if p.is_file()]
        latest.update(status='sketch_checked', reduction_name=reduction_name,
                      source_hashes=before, audit=str(audit),
                      audit_marker=marker,
                      freshness=bind_freshness(project, before, olean_paths=olean_paths),
                      reduction_status='accepted', accepted_at=now(),
                      manifest_sha256=(state.manifest.get('sha256') if state.manifest else None))
        for child in children:
            state.nodes[child].metadata['statement_status'] = 'indexed'
        state.event('sketch_frontier_opened', parent_id=parent_id, children=children)
    store.save(state)
    return accepted
