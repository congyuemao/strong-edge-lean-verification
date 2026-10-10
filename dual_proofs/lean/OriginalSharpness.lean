import AuditRegression
import Mathlib.Basic.Real.Basic

namespace OriginalSharpness
open IndependentAudit.Regression

/-- Supplemental sharpness theorem; the original StrongEdge files are unchanged. -/
theorem twenty_is_necessary_real (c : ℝ)
    (h : ∃ M : Finset doubleC5.edgeSet,
      StrongEdge.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet) ∧
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

end OriginalSharpness
#print axioms OriginalSharpness.twenty_is_necessary_real
