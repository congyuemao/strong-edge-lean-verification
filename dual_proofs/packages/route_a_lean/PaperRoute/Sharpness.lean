module
public import PaperRoute.Semantics
public import Mathlib.Basic.Real.Basic
@[expose] public section
namespace PaperRoute.Sharpness

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
    (PaperRoute.Library.conflictGraph doubleC5).Adj e f := by
  apply (PaperRoute.Semantics.conflict_iff_direct doubleC5 e f hne).mpr
  obtain ⟨a, b, he⟩ := Sym2.exists.mp (show ∃ z, z = e.val from ⟨e.val, rfl⟩)
  obtain ⟨c, d, hf⟩ := Sym2.exists.mp (show ∃ z, z = f.val from ⟨f.val, rfl⟩)
  have hab : doubleC5.Adj a b := by have h := e.property; rwa [← he] at h
  have hcd : doubleC5.Adj c d := by have h := f.property; rwa [← hf] at h
  exact ⟨a, b, c, d, he.symm, hf.symm, doubleC5_endpoint_test a b c d hab hcd⟩

theorem doubleC5_matching_card_le_one (M : Finset doubleC5.edgeSet)
    (hM : PaperRoute.Library.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet)) : M.card ≤ 1 := by
  apply Finset.card_le_one.mpr
  intro e he f hf
  by_contra hne
  exact hM he hf hne (doubleC5_all_edges_conflict e f hne)

theorem twenty_is_necessary (c : ℕ)
    (h : ∃ M : Finset doubleC5.edgeSet,
      PaperRoute.Library.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet) ∧
      Fintype.card doubleC5.edgeSet ≤ c * M.card) : 20 ≤ c := by
  obtain ⟨M, hm, hc⟩ := h
  have hcard := doubleC5_matching_card_le_one M hm
  have hmul := Nat.mul_le_mul_left c hcard
  rw [doubleC5_twenty_edges] at hc
  omega


/-- The manuscript claims sharpness against arbitrary real constants. -/
theorem twenty_is_necessary_real (c : ℝ)
    (h : ∃ M : Finset doubleC5.edgeSet,
      PaperRoute.Library.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet) ∧
      (Fintype.card doubleC5.edgeSet : ℝ) ≤ c * (M.card : ℝ)) : 20 ≤ c := by
  obtain ⟨M, hm, hc⟩ := h
  have hn := doubleC5_matching_card_le_one M hm
  rw [doubleC5_twenty_edges] at hc
  have hp : M.card ≠ 0 := by
    intro hz
    simp only [hz, Nat.cast_zero, mul_zero] at hc
    norm_num at hc
  have he : M.card = 1 := by omega
  norm_num [he] at hc
  exact hc

end PaperRoute.Sharpness
