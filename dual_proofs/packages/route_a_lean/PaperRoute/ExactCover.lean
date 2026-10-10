module

public import PaperRoute.Library.Bounds.EdgeCounting

@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Reverse implication missing from the original one-sided cover lemma. -/
theorem meets_cover_conflict {u v : V} {e f : G.edgeSet}
    (he : e.val = s(u, v))
    (hf : ∃ w ∈ endpointNeighbourCover G u v, w ∈ f.val) :
    StrongConflict G e f := by
  obtain ⟨w, hw, hwf⟩ := hf
  have hne : e ≠ f := by
    intro h
    have hwe : w ∈ e.val := h.symm ▸ hwf
    rw [he, Sym2.mem_iff] at hwe
    rcases hwe with hwu | hwv
    · exact left_notMem_endpointNeighbourCover G u v (hwu ▸ hw)
    · exact right_notMem_endpointNeighbourCover G u v (hwv ▸ hw)
  have join {a : V} (hae : a ∈ e.val) (haw : G.Adj a w) :
      StrongConflict G e f := by
    let g : G.edgeSet := ⟨s(a, w), haw⟩
    have hag : a ∈ g.val := Sym2.mem_mk_left _ _
    have hwg : w ∈ g.val := Sym2.mem_mk_right _ _
    by_cases heg : e = g
    · exact ⟨hne, Or.inl (SimpleGraph.lineGraph_adj_iff_exists.mpr
        ⟨hne, w, heg.symm ▸ hwg, hwf⟩)⟩
    by_cases hgf : g = f
    · exact ⟨hne, Or.inl (SimpleGraph.lineGraph_adj_iff_exists.mpr
        ⟨hne, a, hae, hgf ▸ hag⟩)⟩
    exact ⟨hne, Or.inr ⟨g,
      SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨heg, a, hae, hag⟩,
      SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hgf, w, hwg, hwf⟩⟩⟩
  rcases mem_union.mp hw with hw | hw
  · exact join (he.symm ▸ Sym2.mem_mk_left u v)
      ((G.mem_neighborFinset u w).mp (mem_erase.mp hw).2)
  · exact join (he.symm ▸ Sym2.mem_mk_right u v)
      ((G.mem_neighborFinset v w).mp (mem_erase.mp hw).2)

theorem conflict_iff_meets_cover {u v : V} {e f : G.edgeSet}
    (he : e.val = s(u, v)) :
    StrongConflict G e f ↔
      ∃ w ∈ endpointNeighbourCover G u v, w ∈ f.val :=
  ⟨strongConflict_meets_cover G he, meets_cover_conflict G he⟩

variable [DecidableRel (conflictGraph G).Adj]

theorem conflict_neighbors_eq_meeting {u v : V} (e : G.edgeSet)
    (he : e.val = s(u, v)) :
    (conflictGraph G).neighborFinset e =
      edgesMeeting G univ (endpointNeighbourCover G u v) := by
  ext f
  simp only [SimpleGraph.mem_neighborFinset, edgesMeeting, mem_filter,
    mem_univ, true_and]
  exact conflict_iff_meets_cover G he

/-- Manuscript (2.1), stated additively to avoid truncated natural subtraction. -/
theorem conflict_degree_add_inside_eq_sum {u v : V} (e : G.edgeSet)
    (he : e.val = s(u, v)) :
    (conflictGraph G).degree e +
      (edgesInside G univ (endpointNeighbourCover G u v)).card =
      ∑ w ∈ endpointNeighbourCover G u v, G.degree w := by
  have hi := incidence_sum_eq_meeting_add_inside G univ (endpointNeighbourCover G u v)
  simp only [edgeIncidences_univ_card] at hi
  rw [← conflict_neighbors_eq_meeting G e he,
    SimpleGraph.card_neighborFinset_eq_degree] at hi
  exact hi.symm

theorem conflict_degree_eq_sum_sub_inside {u v : V} (e : G.edgeSet)
    (he : e.val = s(u, v)) :
    (conflictGraph G).degree e =
      (∑ w ∈ endpointNeighbourCover G u v, G.degree w) -
        (edgesInside G univ (endpointNeighbourCover G u v)).card := by
  have := conflict_degree_add_inside_eq_sum G e he
  omega

theorem inside_cover_budget (hΔ : ∀ x, G.degree x ≤ 4)
    {u v : V} (e : G.edgeSet) (he : e.val = s(u, v))
    {t : ℕ} (ht : t ≤ (conflictGraph G).degree e) :
    (edgesInside G univ (endpointNeighbourCover G u v)).card + t ≤ 24 := by
  have hi := conflict_degree_add_inside_eq_sum G e he
  have hs := sum_le_sum (s := endpointNeighbourCover G u v) (fun x _ => hΔ x)
  have hc := endpointNeighbourCover_card_le_six G
    (G.mem_edgeSet.mp (he ▸ e.property)) hΔ
  simp only [sum_const, smul_eq_mul] at hs
  omega


end PaperRoute
