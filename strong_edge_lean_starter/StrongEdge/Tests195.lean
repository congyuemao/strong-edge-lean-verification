module

public import StrongEdge.MinimalPacking195
public import StrongEdge.Tests

@[expose] public section

namespace StrongEdge.Tests195

open Finset

/-- K20 satisfies all five high-degree bounds vacuously. This regression
prevents dropping the independent no-twenty-clique premise. -/
theorem complete20_thresholds : CliqueBounds195 (⊤ : SimpleGraph (Fin 20)) := by
  have hdeg : ∀ x : Fin 20, (⊤ : SimpleGraph (Fin 20)).degree x = 19 := by
    intro x
    simp
  have hempty (k : ℕ) (hk : 20 ≤ k) (Q : Finset (Fin 20))
      (hd : ∀ x ∈ Q, k ≤ (⊤ : SimpleGraph (Fin 20)).degree x) : Q = ∅ := by
    apply eq_empty_iff_forall_notMem.mpr
    intro x hx
    have := hd x hx
    rw [hdeg x] at this
    omega
  constructor <;> intro Q _ hd
  · simp [hempty 20 (by omega) Q hd]
  · simp [hempty 21 (by omega) Q hd]
  · simp [hempty 22 (by omega) Q hd]
  · simp [hempty 23 (by omega) Q hd]
  · simp [hempty 24 (by omega) Q hd]

theorem complete20_has_no_packing195 :
    ¬ ∃ M : Finset (Fin 20), (⊤ : SimpleGraph (Fin 20)).IsIndepSet (M : Set (Fin 20)) ∧
      2 * 20 ≤ 39 * M.card := by
  rintro ⟨M, hM, hcount⟩
  have hc : M.card ≤ 1 := by
    apply card_le_one.mpr
    intro x hx y hy
    by_contra hxy
    exact hM hx hy hxy hxy
  omega

/-- Empty candidates are covered without a nonempty-graph assumption. -/
theorem empty_candidates
    {W : Type*} [Fintype W] [DecidableEq W] (H : SimpleGraph W)
    [DecidableRel H.Adj] (hd : ∀ x, H.degree x ≤ 24) (hb : CliqueBounds195 H) :
    ∃ M : Finset W, M ⊆ ∅ ∧ H.IsIndepSet (M : Set W) ∧ 2 * (∅ : Finset W).card ≤ 39 * M.card := by
  apply subset_packing195_of_clique_bounds H hd hb ∅
  intro Q hs _
  have hQ : Q = ∅ := subset_empty.mp hs
  simp [hQ]

end StrongEdge.Tests195
