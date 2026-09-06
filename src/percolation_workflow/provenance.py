"""Lean-environment provenance checks for reconstruction experiments, not proof validity."""
import json
from pathlib import Path
import re
import hashlib


def lean_checks(contract: dict, target: str) -> str:
    """Insert into run_meta after `let env ← getEnv`; imports are checked transitively.

    Exact module names distinguish the forbidden aggregate `Percolation` from allowed
    foundational submodules. Traverse definitions, opaque and generated helper proofs;
    renaming a wrapper does not hide its forbidden dependencies.
    """
    if not contract.get('forbidden_modules') and not contract.get('forbidden_existing_proofs'):
        return ''
    modules = ', '.join(json.dumps(n) for n in contract.get('forbidden_modules', []))
    names = ', '.join(json.dumps(n) for n in contract.get('forbidden_existing_proofs', []))
    return f'''
  let bannedModules : Array String := #[{modules}]
  for mod in env.header.moduleNames do
    if bannedModules.contains mod.toString then
      throwError "forbidden transitive import: {{mod}}"
  let bannedProofs : Array String := #[{names}]
  let targetName := {json.dumps(target)}.toName
  let mut visited : Std.HashSet Name := {{}}
  let mut pending := [targetName]
  while h : pending ≠ [] do
    let n := pending.head h
    pending := pending.tail
    if visited.contains n then continue
    visited := visited.insert n
    let userName := ((privateToUserName? n).getD n).toString
    if n != targetName && bannedProofs.any (fun b => userName == b || userName.endsWith ("." ++ b)) then
      throwError "forbidden proof dependency: {{n}}"
    let some ci := env.find? n | throwError "missing dependency: {{n}}"
    let values := match ci with
      | .thmInfo t => t.value.getUsedConstants
      | .defnInfo d => d.value.getUsedConstants
      | .opaqueInfo o => o.value.getUsedConstants
      | _ => #[]
    pending := (ci.type.getUsedConstants ++ values).toList ++ pending
'''


def write_audit(project: Path, module: str, target: str, contract: dict):
    checks = lean_checks(contract, target)
    if not checks:
        return None
    if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)*', module):
        raise ValueError('unsupported solution module')
    identity = hashlib.sha256((module + '\n' + checks).encode()).hexdigest()
    marker = 'PROVENANCE_CHECKED_' + identity
    source = project / ('ProvenanceAudit_' + identity + '.lean')
    content = (f'import {module}\nimport Lean\nopen Lean in\nrun_meta do\n'
               '  let env ← getEnv\n' + checks + f'  logInfo "{marker}"\n')
    if source.exists():
        if source.read_text(encoding='utf-8') != content:
            raise ValueError('existing provenance audit was modified')
    else:
        source.write_text(content, encoding='utf-8')
    return source, marker
