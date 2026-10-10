import StrongEdge
import Lean

open Lean Elab Command in
run_elab do
  let env ← getEnv
  let mut todo := [``StrongEdge.induced_matching_packing20]
  let mut seen : NameSet := {}
  while !todo.isEmpty do
    let name := todo.head!
    todo := todo.tail!
    if seen.contains name then continue
    seen := seen.insert name
    let some ci := env.find? name | throwError "Missing declaration {name}"
    let mut refs := ci.type.getUsedConstantsAsSet
    if let some value := ci.value? (allowOpaque := true) then
      refs := refs ∪ value.getUsedConstantsAsSet
    let deps := refs.toList
    todo := deps ++ todo
    let modName := match env.getModuleIdxFor? name with
      | some idx => toString env.header.moduleNames[idx.toNat]!
      | none => "<current>"
    let record := Json.mkObj [
      ("name", toJson (toString name)), ("module", toJson modName),
      ("axiom", toJson ci.isAxiom), ("unsafe", toJson ci.isUnsafe),
      ("dependencies", toJson (deps.map toString))]
    logInfo m!"AUDIT_DEP {record.compress}"
