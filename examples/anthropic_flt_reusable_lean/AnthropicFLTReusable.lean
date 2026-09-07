import Lean

/-!
Minimal, non-number-theoretic adapter sidecar for the Anthropic FLT P2M utility.

Source provenance:
  repository: https://github.com/anthropics/anthropic-fermats-last-theorem
  commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
  source path: P2M/Util.lean
  upstream toolchain: Lean 4.33.1
  upstream Mathlib revision: db584cd6d46c92f209a44c0f1c829460d327499d

This file intentionally copies/adapts only the proof-card elaboration seam and a
small type-equality gate. It contains no FLT or other number-theoretic theorem.
-/

open Lean Elab Tactic Meta in
elab "p2m_exact_reverting " e:term : tactic => do
  let g ← getMainGoal
  let lctx := (← g.getDecl).lctx
  let fvars := lctx.foldl (init := #[]) fun acc d =>
    if d.isImplementationDetail then acc else acc.push d.fvarId
  let (_, g') ← g.revert fvars (preserveOrder := true)
  g'.withContext do
    let tgt ← g'.getType
    let v ← Term.withSynthesize <| elabTermEnsuringType e tgt
    let v ← instantiateMVars v
    if v.hasExprMVar then
      throwError "p2m_exact_reverting: unassigned metavariables remain"
    g'.assign v
  replaceMainGoal []

open Lean Elab Command Meta in
elab "#p2m_type_eq " a:ident b:ident : command => liftTermElabM do
  let some ia := (← getEnv).find? a.getId |
    throwError m!"#p2m_type_eq: unknown constant {a.getId}"
  let some ib := (← getEnv).find? b.getId |
    throwError m!"#p2m_type_eq: unknown constant {b.getId}"
  let la ← ia.levelParams.mapM fun _ => mkFreshLevelMVar
  let lb ← ib.levelParams.mapM fun _ => mkFreshLevelMVar
  let ta := ia.type.instantiateLevelParams ia.levelParams la
  let tb := ib.type.instantiateLevelParams ib.levelParams lb
  if ← isDefEq ta tb then
    logInfo m!"P2M_TYPE_EQ {a.getId} {b.getId}"
  else
    throwError m!"P2M_TYPE_MISMATCH\n  {a.getId} : {ta}\n  {b.getId} : {tb}"

namespace AnthropicFLTReusable

theorem reusableStatement (x : Nat) (_h : x = x) : x = x := by
  p2m_exact_reverting (fun _ _ => rfl)

theorem reusableProof (x : Nat) (_h : x = x) : x = x := by
  exact rfl

theorem exact_reverting_example (x : Nat) (_h : x = x) : x = x := by
  p2m_exact_reverting (fun _ _ => rfl)

end AnthropicFLTReusable

#p2m_type_eq AnthropicFLTReusable.reusableStatement AnthropicFLTReusable.reusableProof
