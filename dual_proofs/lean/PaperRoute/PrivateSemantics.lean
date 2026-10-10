module
public import PaperRoute.Packing
@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
variable {W : Type*} [Fintype W] [DecidableEq W]
variable (H : SimpleGraph W) [DecidableRel H.Adj]

omit [Fintype W] in
/-- Exact translation of the manuscript's closed-neighbourhood definition. -/
theorem private_iff_closed_intersection (I : Finset W) {v x : W} (hv : v ∈ I) :
    IsPrivate H I v x ↔ I.filter (fun w => x = w ∨ H.Adj x w) = {v} := by
  constructor
  · intro h
    ext w
    simp only [mem_filter, mem_singleton]
    constructor
    · rintro ⟨hw, hc⟩
      by_contra hwv
      exact hc.elim (h.2 w hw hwv).1 (h.2 w hw hwv).2
    · intro hwv
      subst w
      exact ⟨hv, h.1⟩
  · intro h
    have hh : v ∈ I.filter (fun w => x = w ∨ H.Adj x w) := by rw [h]; simp
    refine ⟨(mem_filter.mp hh).2, ?_⟩
    intro w hw hwv
    have hn : ¬ (x = w ∨ H.Adj x w) := by
      intro hc
      have hh : w ∈ I.filter (fun z => x = z ∨ H.Adj x z) := mem_filter.mpr ⟨hw, hc⟩
      rw [h] at hh
      exact hwv (mem_singleton.mp hh)
    exact ⟨fun hx => hn (Or.inl hx), fun hx => hn (Or.inr hx)⟩

end PaperRoute
