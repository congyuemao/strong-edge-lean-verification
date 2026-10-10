import AuditSemantic
import StrongEdge.Tests

namespace IndependentAudit.Regression

open StrongEdge.Tests

theorem path_conflict_in_full_graph :
    IndependentAudit.directStrongConflict path4 path01 path23 := by
  refine ⟨0, 1, 2, 3, rfl, rfl, ?_⟩
  decide

theorem path_candidates_still_conflict :
    (StrongEdge.candidateConflictGraph path4 candidates).Adj
      ⟨path01, by simp [candidates]⟩ ⟨path23, by simp [candidates]⟩ := by
  exact (IndependentAudit.conflict_iff_direct path4 path01 path23 (by decide)).mpr
    path_conflict_in_full_graph

theorem deleting_middle_edge_removes_conflict :
    ¬ (StrongEdge.conflictGraph separated).Adj sep01 sep23 := by
  intro h
  have hw := (IndependentAudit.conflict_iff_endpointWitness separated sep01 sep23 (by decide)).mp h
  have hn : ¬ IndependentAudit.endpointWitness separated sep01 sep23 := by
    unfold IndependentAudit.endpointWitness
    decide
  exact hn hw

def doubleC5 : SimpleGraph (Fin 10) where
  Adj x y := (x.val / 2 + 1) % 5 = y.val / 2 ∨ (y.val / 2 + 1) % 5 = x.val / 2
  symm := ⟨fun _ _ h => h.symm⟩
  loopless := ⟨by decide⟩

instance : DecidableRel doubleC5.Adj := fun _ _ => inferInstanceAs (Decidable (_ ∨ _))

theorem doubleC5_ten_vertices : Fintype.card (Fin 10) = 10 := by decide
theorem doubleC5_degree_four : ∀ v, doubleC5.degree v = 4 := by decide
theorem doubleC5_twenty_edges : Fintype.card doubleC5.edgeSet = 20 := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 4000000 in
theorem doubleC5_endpoint_test : ∀ a b c d : Fin 10,
    doubleC5.Adj a b → doubleC5.Adj c d →
    (a = c ∨ a = d ∨ b = c ∨ b = d ∨
      doubleC5.Adj a c ∨ doubleC5.Adj a d ∨ doubleC5.Adj b c ∨ doubleC5.Adj b d) := by
  decide

theorem doubleC5_all_edges_conflict (e f : doubleC5.edgeSet) (hne : e ≠ f) :
    (StrongEdge.conflictGraph doubleC5).Adj e f := by
  apply (IndependentAudit.conflict_iff_direct doubleC5 e f hne).mpr
  obtain ⟨a, b, he⟩ := Sym2.exists.mp (show ∃ z, z = e.val from ⟨e.val, rfl⟩)
  obtain ⟨c, d, hf⟩ := Sym2.exists.mp (show ∃ z, z = f.val from ⟨f.val, rfl⟩)
  have hab : doubleC5.Adj a b := by have h := e.property; rwa [← he] at h
  have hcd : doubleC5.Adj c d := by have h := f.property; rwa [← hf] at h
  exact ⟨a, b, c, d, he.symm, hf.symm, doubleC5_endpoint_test a b c d hab hcd⟩

theorem doubleC5_matching_card_le_one (M : Finset doubleC5.edgeSet)
    (hM : StrongEdge.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet)) : M.card ≤ 1 := by
  apply Finset.card_le_one.mpr
  intro e he f hf
  by_contra hne
  exact hM he hf hne (doubleC5_all_edges_conflict e f hne)

theorem twenty_is_necessary (c : ℕ)
    (h : ∃ M : Finset doubleC5.edgeSet,
      StrongEdge.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet) ∧
      Fintype.card doubleC5.edgeSet ≤ c * M.card) : 20 ≤ c := by
  obtain ⟨M, hm, hc⟩ := h
  have hcard := doubleC5_matching_card_le_one M hm
  have hmul := Nat.mul_le_mul_left c hcard
  rw [doubleC5_twenty_edges] at hc
  omega

theorem empty_graph_packing (F : Finset (⊥ : SimpleGraph (Fin 0)).edgeSet) :
    ∃ M : Finset (⊥ : SimpleGraph (Fin 0)).edgeSet, M ⊆ F ∧
      IndependentAudit.endpointInducedMatching ⊥ (M : Set (⊥ : SimpleGraph (Fin 0)).edgeSet) ∧
      F.card ≤ 20 * M.card := by
  exact IndependentAudit.endpoint_packing20 ⊥ (by intro v; exact Fin.elim0 v) F

theorem isolated_vertices_packing (F : Finset (⊥ : SimpleGraph (Fin 5)).edgeSet) :
    ∃ M : Finset (⊥ : SimpleGraph (Fin 5)).edgeSet, M ⊆ F ∧
      IndependentAudit.endpointInducedMatching ⊥ (M : Set (⊥ : SimpleGraph (Fin 5)).edgeSet) ∧
      F.card ≤ 20 * M.card := by
  exact IndependentAudit.endpoint_packing20 ⊥ (by intro v; simp) F

theorem nonregular_path_packing (F : Finset path4.edgeSet) :
    ∃ M : Finset path4.edgeSet, M ⊆ F ∧
      IndependentAudit.endpointInducedMatching path4 (M : Set path4.edgeSet) ∧
      F.card ≤ 20 * M.card :=
  IndependentAudit.endpoint_packing20 path4 (by decide) F

theorem triangle_packing (F : Finset (⊤ : SimpleGraph (Fin 3)).edgeSet) :
    ∃ M : Finset (⊤ : SimpleGraph (Fin 3)).edgeSet, M ⊆ F ∧
      IndependentAudit.endpointInducedMatching ⊤ (M : Set (⊤ : SimpleGraph (Fin 3)).edgeSet) ∧
      F.card ≤ 20 * M.card :=
  IndependentAudit.endpoint_packing20 ⊤ (by decide) F

def cycle4 : SimpleGraph (Fin 4) where
  Adj x y := (x.val + 1) % 4 = y.val ∨ (y.val + 1) % 4 = x.val
  symm := ⟨fun _ _ h => h.symm⟩
  loopless := ⟨by decide⟩

instance : DecidableRel cycle4.Adj := fun _ _ => inferInstanceAs (Decidable (_ ∨ _))

theorem four_cycle_packing (F : Finset cycle4.edgeSet) :
    ∃ M : Finset cycle4.edgeSet, M ⊆ F ∧
      IndependentAudit.endpointInducedMatching cycle4 (M : Set cycle4.edgeSet) ∧
      F.card ≤ 20 * M.card :=
  IndependentAudit.endpoint_packing20 cycle4 (by decide) F

end IndependentAudit.Regression

#print axioms IndependentAudit.Regression.path_candidates_still_conflict
#print axioms IndependentAudit.Regression.deleting_middle_edge_removes_conflict
#print axioms IndependentAudit.Regression.doubleC5_degree_four
#print axioms IndependentAudit.Regression.doubleC5_twenty_edges
#print axioms IndependentAudit.Regression.doubleC5_endpoint_test
#print axioms IndependentAudit.Regression.doubleC5_all_edges_conflict
#print axioms IndependentAudit.Regression.twenty_is_necessary
#print axioms IndependentAudit.Regression.empty_graph_packing
#print axioms IndependentAudit.Regression.isolated_vertices_packing
#print axioms IndependentAudit.Regression.nonregular_path_packing
#print axioms IndependentAudit.Regression.triangle_packing
#print axioms IndependentAudit.Regression.four_cycle_packing
