import Solution
import Lean.Util.CollectAxioms

open Lean in
run_meta do
  let env ← getEnv
  for mod in env.header.moduleNames do
    if (`Percolation).isPrefixOf mod then
      throwError "Forbidden original proof module: {mod}"
  let some (.thmInfo theoremInfo) := env.find? `HarrisReplay.harris
    | throwError "Missing Harris theorem"
  let used := theoremInfo.value.getUsedConstants
  for child in #[`HarrisReplay.iterated_nonneg, `HarrisReplay.inner_expansion] do
    unless used.contains child do
      throwError "Parent does not use required child: {child}"
  for name in #[`HarrisReplay.harris, `HarrisReplay.iterated_nonneg, `HarrisReplay.inner_expansion] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Quot.sound, `Classical.choice].contains ax do
        throwError "Unexpected axiom in {name}: {ax}"
    logInfo m!"{name}: permitted axioms {axioms}"
  logInfo "Harris dependency and axiom audit accepted"
