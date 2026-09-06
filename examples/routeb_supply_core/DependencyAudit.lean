import Solution
import Lean

/- Read the actual compiled environment; traverse definition and opaque bodies.
This supplements, and does not replace, the upstream comparator and kernels. -/
open Lean in
run_meta do
  let env ← getEnv
  for mod in env.header.moduleNames do
    let s := mod.toString
    if s == "Challenge" || s.startsWith "Challenge." then
      throwError "forbidden Challenge dependency: {mod}"
  let target := `RouteBSupplyComparison.explicit_supply_bound
  let allowed := #[`propext, `Classical.choice, `Quot.sound]
  let mut visited : Std.HashSet Name := {}
  let mut pending := [target]
  let mut opaqueCount : Nat := 0
  let mut axioms : Array Name := #[]
  while h : pending ≠ [] do
    let n := pending.head h
    pending := pending.tail
    if visited.contains n then continue
    visited := visited.insert n
    let some ci := env.find? n | throwError "missing dependency: {n}"
    if let .axiomInfo _ := ci then
      unless allowed.contains n do throwError "unpermitted axiom: {n}"
      axioms := axioms.push n
    if let .opaqueInfo _ := ci then opaqueCount := opaqueCount + 1
    let values := (ci.value? (allowOpaque := true)).map Expr.getUsedConstants |>.getD #[]
    pending := (ci.type.getUsedConstants ++ values).toList ++ pending
    match ci with
    | .inductInfo info => pending := info.ctors ++ info.all ++ pending
    | .ctorInfo info => pending := info.induct :: pending
    | .recInfo info =>
      for rule in info.rules do
        pending := rule.ctor :: rule.rhs.getUsedConstants.toList ++ pending
    | _ => pure ()
  for required in #[`RouteBSupplyCore.pointwise_supply_bound,
      `RouteBSupplyCore.vector_completion_identity] do
    unless visited.contains required do throwError "missing intended proof dependency: {required}"
  logInfo m!"Dependency closure: {visited.size} declarations; opaque bodies: {opaqueCount}"
  logInfo m!"Reachable axioms: {axioms}"
  logInfo "ROUTEB_DEPENDENCY_AUDIT_OK"
