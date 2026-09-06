import Challenge
import Reduction

import Lean
import Lean.Util.CollectAxioms
open Lean Meta in
run_meta do
  let env ← getEnv
  let getType := fun (n : Name) => do
    let some info := env.find? n | throwError "missing declaration {n}"
    unless info.levelParams.length ≤ 1 do
      throwError "multiple universe parameters need an explicit map: {n}"
    pure (info.type.instantiateLevelParams info.levelParams (info.levelParams.map fun _ => Level.param `audit_u))
  let mut expected ← getType `HarrisReplay.harris
  for child in (#[`HarrisReplay.iterated_nonneg, `HarrisReplay.inner_expansion] : Array Name).reverse do
    expected := mkForall `_ BinderInfo.default (← getType child) expected
  let some (.thmInfo proof) := env.find? `harris_reduction
    | throwError "reduction must be a theorem"
  unless ← isDefEq (← getType `harris_reduction) expected do
    throwError "reduction does not prove the specified child-to-parent implication"
  for ax in (← collectAxioms `harris_reduction) do
    unless #[`propext, `Quot.sound, `Classical.choice].contains ax do
      throwError "unproved or forbidden dependency: {ax}"

  logInfo "REDUCTION_CHECKED_cda448f3d8f243dab3e76ad00fbdcd15"
