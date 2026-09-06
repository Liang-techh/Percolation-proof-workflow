import Solution
import Lean.Util.CollectAxioms

open Lean in
run_meta do
  let env ← getEnv
  let mut rows : Array String := #[]
  for (name, ci) in env.constants.toList do
    unless (match ci with | .thmInfo _ => true | .opaqueInfo _ => true | _ => false) do
      continue
    let some idx := env.getModuleIdxFor? name | continue
    let some mod := env.header.moduleNames[idx.toNat]? | continue
    unless (`Percolation).isPrefixOf mod || mod == `Solution do continue
    let some range ← findDeclarationRanges? name | continue
    let typ ← withOptions (fun opts => opts.setBool `pp.all true) do
      Lean.Meta.ppExpr ci.type
    let axioms ← collectAxioms name
    let row := Json.mkObj [
      ("name", toJson name.toString),
      ("module", toJson mod.toString),
      ("type", toJson typ.pretty),
      ("levelParams", toJson (ci.levelParams.map Name.toString)),
      ("axioms", toJson (axioms.map Name.toString)),
      ("startLine", toJson range.range.pos.line)]
    rows := rows.push row.compress
  IO.FS.writeFile "../../../artifacts/percolation/elaborated_types.jsonl"
    (String.intercalate "\n" rows.toList)
  logInfo s!"wrote {rows.size} elaborated types and axiom sets"
