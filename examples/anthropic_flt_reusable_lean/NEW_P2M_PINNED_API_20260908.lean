import Lean

/-!
OPEN_UNCOMPILED; no execution or admission receipt.
Apache-2.0. Adapted from Anthropic, PBC (Copyright 2026), P2M/Util.lean:
https://github.com/anthropics/fermats-last-theorem
commit aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
blob 0a73367f78bc165bb5d35e42ca14f5055252e7f6
Target Lean: v4.33.1. No Mathlib import or runtime dependency.
Preserve the intake LICENSE/NOTICE/ATTRIBUTION provenance.
Changes: fresh syntax names and diagnostic prefixes. Retain upstream
clearAuxDeclsInsteadOfRevert and statement-universe generality check.
-/

set_option autoImplicit false

open Lean Elab Tactic Meta in
elab "p2m_pinned_exact_reverting " e:term : tactic => do
  let g ← getMainGoal
  let lctx := (← g.getDecl).lctx
  let fvars := lctx.foldl (init := #[]) fun acc d =>
    if d.isImplementationDetail then acc else acc.push d.fvarId
  let (_, g') ← g.revert fvars (preserveOrder := true)
    (clearAuxDeclsInsteadOfRevert := true)
  g'.withContext do
    let tgt ← g'.getType
    let v ← Term.withSynthesize <| elabTermEnsuringType e tgt
    let v ← instantiateMVars v
    if v.hasExprMVar then
      throwError "P2M_PINNED_UNASSIGNED: expression metavariables remain"
    g'.assign v
  replaceMainGoal []

open Lean Elab Command Meta in
elab "#p2m_pinned_type_eq " a:ident b:ident : command => liftTermElabM do
  let some ia := (← getEnv).find? a.getId |
    throwError m!"P2M_PINNED_UNKNOWN: {a.getId}"
  let some ib := (← getEnv).find? b.getId |
    throwError m!"P2M_PINNED_UNKNOWN: {b.getId}"
  let la ← ia.levelParams.mapM fun _ => mkFreshLevelMVar
  let lb ← ib.levelParams.mapM fun _ => mkFreshLevelMVar
  let ta := ia.type.instantiateLevelParams ia.levelParams la
  let tb := ib.type.instantiateLevelParams ib.levelParams lb
  if ← isDefEq ta tb then
    let mut pinned : Array String := #[]
    let mut seen : Array Level := #[]
    for l in la, nm in ia.levelParams do
      let l' ← instantiateLevelMVars l
      match l' with
      | .mvar _ =>
          if seen.contains l' then
            pinned := pinned.push s!"{nm} (identified with another)"
          else
            seen := seen.push l'
      | _ => pinned := pinned.push s!"{nm} := {l'}"
    if pinned.isEmpty then
      logInfo m!"P2M_PINNED_TYPE_EQ {a.getId} {b.getId}"
    else
      throwError m!"P2M_PINNED_UNDERGENERAL: statement universes {pinned}"
  else
    throwError m!"P2M_PINNED_TYPE_MISMATCH: {a.getId} {b.getId}"
