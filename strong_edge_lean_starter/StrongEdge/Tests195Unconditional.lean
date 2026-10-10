module

public import StrongEdge.TightComponents

@[expose] public section

namespace StrongEdge.Tests195Unconditional

set_option synthInstance.maxSize 1000

open Finset

/-- Ten vertices, with independent pairs replacing the five cycle vertices. -/
def cycleDouble : SimpleGraph (Fin 5 × Fin 2) where
  Adj x y := x.1 + 1 = y.1 ∨ y.1 + 1 = x.1
  symm := ⟨fun _ _ h => h.symm⟩
  loopless := ⟨by
    have h : ∀ i : Fin 5, ¬ (i + 1 = i ∨ i + 1 = i) := by decide
    intro x
    exact h x.1⟩

instance : DecidableRel cycleDouble.Adj := fun _ _ => inferInstanceAs (Decidable (_ ∨ _))

def cyclePart (i : Fin 5) : Finset (Fin 5 × Fin 2) := univ.filter (fun x => x.1 = i)

theorem cycleDouble_degree_four : ∀ x, cycleDouble.degree x = 4 := by decide

theorem cycleDouble_edge_count : (univ : Finset cycleDouble.edgeSet).card = 20 := by decide

theorem cycleDouble_component_certificate : IsFiveCycleBlowupComponent cycleDouble univ := by
  refine ⟨cyclePart 0, cyclePart 1, cyclePart 2, cyclePart 3, cyclePart 4, ?_⟩
  simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, forall_eq_or_imp,
    false_implies, implies_true, List.Pairwise.nil, and_true]
  repeat' apply And.intro
  all_goals decide

theorem cycleDouble_is_original_component :
    ∃ c : cycleDouble.ConnectedComponent, c.supp = Set.univ := by
  simpa only [coe_univ] using five_cycle_blowup_is_connected_component cycleDouble univ
    cycleDouble_component_certificate

theorem cycleDouble_all_edges_strong_clique :
    (conflictGraph cycleDouble).IsClique (Set.univ : Set cycleDouble.edgeSet) := by
  intro e _ f _ hef
  change StrongConflict cycleDouble e f
  have h : ∀ e f : cycleDouble.edgeSet, e ≠ f → StrongConflict cycleDouble e f := by
    simp only [StrongConflict, SimpleGraph.lineGraph_adj_iff_exists]
    decide
  exact h e f hef

theorem cycleDouble_needs_correction :
    ¬ ∃ M : Finset cycleDouble.edgeSet, IsInducedMatching cycleDouble (M : Set cycleDouble.edgeSet) ∧
      2 * (univ : Finset cycleDouble.edgeSet).card ≤ 39 * M.card := by
  rintro ⟨M, hM, hb⟩
  have hc : M.card ≤ 1 := by
    apply card_le_one.mpr
    intro e he f hf
    by_contra hef
    exact hM he hf hef (cycleDouble_all_edges_strong_clique (Set.mem_univ _) (Set.mem_univ _) hef)
  rw [cycleDouble_edge_count] at hb
  omega

end StrongEdge.Tests195Unconditional
