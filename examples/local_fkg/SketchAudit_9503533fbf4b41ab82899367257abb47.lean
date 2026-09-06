import LocalFKGChallenge
import LocalFKGReduction
import LocalFKGObligations
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
  let mut expected ← getType `Percolation.Literature.harris_fkg_local
  for child in (#[`Percolation.Literature.LocalFKG.finite_bernoulli_positive_correlation, `Percolation.Literature.LocalFKG.local_event_cube_expectation] : Array Name).reverse do
    expected := mkForall `_ BinderInfo.default (← getType child) expected
  let some (.thmInfo proof) := env.find? `Percolation.Literature.LocalFKG.harris_fkg_local_of_children
    | throwError "reduction must be a theorem"
  unless ← isDefEq (← getType `Percolation.Literature.LocalFKG.harris_fkg_local_of_children) expected do
    throwError "reduction does not prove the specified child-to-parent implication"
  for ax in (← collectAxioms `Percolation.Literature.LocalFKG.harris_fkg_local_of_children) do
    unless #[`propext, `Quot.sound, `Classical.choice].contains ax do
      throwError "unproved or forbidden dependency: {ax}"

  let bannedModules : Array String := #["Percolation.Literature.HarrisLocal", "Percolation.Literature.HarrisInequality", "Percolation.Literature.InequalitiesProofs", "Mathlib.Combinatorics.SetFamily.FourFunctions", "Percolation", "Solution", "Challenge"]
  for mod in env.header.moduleNames do
    if bannedModules.contains mod.toString then
      throwError "forbidden transitive import: {mod}"
  let bannedProofs : Array String := #["harris_fkg_local", "harris_fkg_holds", "infinitePi_harris", "infinitePi_harris_dependsOn", "real_eq_sum_of_determinedBy"]
  let targetName := "Percolation.Literature.LocalFKG.harris_fkg_local_of_children".toName
  let mut visited : Std.HashSet Name := {}
  let mut pending := [targetName]
  while h : pending ≠ [] do
    let n := pending.head h
    pending := pending.tail
    if visited.contains n then continue
    visited := visited.insert n
    let userName := ((privateToUserName? n).getD n).toString
    if n != targetName && bannedProofs.any (fun b => userName == b || userName.endsWith ("." ++ b)) then
      throwError "forbidden proof dependency: {n}"
    let some ci := env.find? n | throwError "missing dependency: {n}"
    let values := match ci with
      | .thmInfo t => t.value.getUsedConstants
      | .defnInfo d => d.value.getUsedConstants
      | .opaqueInfo o => o.value.getUsedConstants
      | _ => #[]
    pending := (ci.type.getUsedConstants ++ values).toList ++ pending

  logInfo "REDUCTION_CHECKED_b52ebc5a64f44bd0abf7e0dd5d349800"
