import StrongEdge
import OriginalSharpness
import Lean

open Lean Elab Command in
run_elab do
  let env ← getEnv
  let roots := [``StrongEdge.induced_matching_packing20,
    ``OriginalSharpness.twenty_is_necessary_real]
  for root in roots do
    let mut todo := [root]
    let mut seen : NameSet := {}
    let mut axioms : List String := []
    let mut unsafeNames : List String := []
    let mut project : List Json := []
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
      if ci.isAxiom then axioms := toString name :: axioms
      if ci.isUnsafe then unsafeNames := toString name :: unsafeNames
      let n := toString name
      if n.startsWith "PaperRoute" || n.startsWith "StrongEdge" ||
          n.startsWith "IndependentAudit" || n.startsWith "OriginalSharpness" then
        project := Json.mkObj [
          ("name", toJson n), ("dependencies", toJson (deps.map toString))] :: project
    for ax in axioms do
      unless ["propext", "Classical.choice", "Quot.sound"].contains ax do
        throwError "Unexpected axiom in {root}: {ax}"
    unless unsafeNames.isEmpty do
      throwError "Unsafe declarations in {root}: {unsafeNames}"
    let names := seen.toList.map toString
    if (toString root).startsWith "PaperRoute" then
      if names.any (fun n => n.startsWith "StrongEdge") then
        throwError "Paper route depends on original StrongEdge declarations"
    if (toString root) == "StrongEdge.induced_matching_packing20" then
      if names.any (fun n => n.startsWith "PaperRoute") then
        throwError "Original route depends on PaperRoute"
    if (toString root) == "PaperRoute.induced_matching_packing20" then
      for forbidden in [
        "PaperRoute.Library.induced_matching_packing20",
        "PaperRoute.Library.high20_clique_card_le_nineteen",
        "PaperRoute.Library.high21_clique_card_le_eighteen",
        "PaperRoute.Library.high22_clique_card_le_seventeen",
        "PaperRoute.Library.high23_clique_card_le_sixteen",
        "PaperRoute.Library.high24_clique_card_le_thirteen"] do
        if names.contains forbidden then throwError "Forbidden shortcut: {forbidden}"
      for required in [
        "PaperRoute.conflict_degree_add_inside_eq_sum",
        "PaperRoute.root_load_budget",
        "PaperRoute.root_load_budget_disjoint",
        "PaperRoute.selected_card_eq_star_root_outer",
        "PaperRoute.root_incidence_eq_star_add_root",
        "PaperRoute.multiple_type_sum_le_three_neighbors",
        "PaperRoute.outer_subset_card_le_four",
        "PaperRoute.small_type_clique_bound",
        "PaperRoute.clique_card_le_seventeen_of_type_four"] do
        unless names.contains required do throwError "Missing paper dependency: {required}"
    let record := Json.mkObj [
      ("root", toJson (toString root)), ("declarations", toJson names.length),
      ("axioms", toJson axioms), ("unsafe", toJson unsafeNames),
      ("project", toJson project)]
    logInfo m!"ROUTE_AUDIT {record.compress}"

#check StrongEdge.induced_matching_packing20
#print axioms StrongEdge.induced_matching_packing20

#check OriginalSharpness.twenty_is_necessary_real
#print axioms OriginalSharpness.twenty_is_necessary_real
