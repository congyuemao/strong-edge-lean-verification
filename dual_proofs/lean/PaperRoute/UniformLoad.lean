module

public import PaperRoute.RootPrimitives

@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

variable [DecidableRel (conflictGraph G).Adj]

/-- Manuscript (3.5): one threshold-parametric proof, not four special cases. -/
theorem root_load_budget_disjoint (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet) {t : ℕ}
    (ht : ∀ e ∈ Q, t ≤ (conflictGraph G).degree e)
    {r a : V} (hdis : Disjoint ((G.neighborFinset r).erase a) ((G.neighborFinset a).erase r))
    (ha : a ∈ rootLabels G Q r) :
    (∑ x ∈ (G.neighborFinset a).erase r, ((rootType G r x).erase a).card) + t ≤ 24 := by
  obtain ⟨_, e, heQ, he⟩ := mem_filter.mp ha
  rw [← fourCycleOpposites_card_eq_root_load]
  have hc : (fourCycleOpposites G r a).card ≤
      (edgesInside G univ (endpointNeighbourCover G r a)).card := by
    apply card_le_via_relation _ _ (fun p f => f.val = s(p.1, p.2))
    · intro p hp
      obtain ⟨hp, hpAdj⟩ := mem_filter.mp hp
      obtain ⟨hx, hy⟩ := mem_product.mp hp
      refine ⟨⟨s(p.1, p.2), hpAdj⟩, mem_filter.mpr ⟨mem_univ _, ?_⟩, rfl⟩
      exact Sym2.forall_mem_pair.mpr ⟨mem_union_left _ hx, mem_union_right _ hy⟩
    · intro p hp q hq f hpf hqf
      obtain ⟨hp, _⟩ := mem_filter.mp hp
      obtain ⟨hq, _⟩ := mem_filter.mp hq
      obtain ⟨hxp, _⟩ := mem_product.mp hp
      obtain ⟨_, hyq⟩ := mem_product.mp hq
      rcases Sym2.eq_iff.mp (hpf.symm.trans hqf) with h | h
      · exact Prod.ext h.1 h.2
      · exact (disjoint_left.mp hdis hxp (h.1.symm ▸ hyq)).elim
  have hb := inside_cover_budget G hΔ e he (ht e heQ)
  omega

/-- Manuscript (3.5): one threshold-parametric proof, not four special cases. -/
theorem root_load_budget (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet) {t : ℕ}
    (ht : ∀ e ∈ Q, t ≤ (conflictGraph G).degree e)
    {r a : V} (hN : G.IsIndepSet (G.neighborSet r))
    (ha : a ∈ rootLabels G Q r) :
    (∑ x ∈ (G.neighborFinset a).erase r, ((rootType G r x).erase a).card) + t ≤ 24 := by
  obtain ⟨haN, e, heQ, he⟩ := mem_filter.mp ha
  have hra := (G.mem_neighborFinset r a).mp haN
  have hdis : Disjoint ((G.neighborFinset r).erase a)
      ((G.neighborFinset a).erase r) := by
    apply disjoint_left.mpr
    intro x hx hy
    exact hN hra ((G.mem_neighborFinset r x).mp (mem_erase.mp hx).2)
      (mem_erase.mp hx).1.symm ((G.mem_neighborFinset a x).mp (mem_erase.mp hy).2)
  exact root_load_budget_disjoint G hΔ Q ht hdis ha

theorem root_load_budget_sub (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet) {t : ℕ}
    (ht : ∀ e ∈ Q, t ≤ (conflictGraph G).degree e)
    {r a : V} (hN : G.IsIndepSet (G.neighborSet r))
    (ha : a ∈ rootLabels G Q r) :
    (∑ x ∈ (G.neighborFinset a).erase r, ((rootType G r x).erase a).card) ≤ 24-t := by
  have := root_load_budget G hΔ Q ht hN ha
  omega


end PaperRoute
