module

public import PaperRoute.Library.Bounds.High20

@[expose] public section

/-!
Formal additions for Sections 2 and 3 of the paper-first manuscript.
Definitions and elementary lemmas are shared with StrongEdge. The exact
identities and the threshold-parametric load bound below are new statements;
they are not inferred by invoking either final packing theorem.
-/
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

variable [DecidableRel (conflictGraph G).Adj]

theorem degree_le_twenty_of_triangle (hΔ : ∀ x, G.degree x ≤ 4)
    {u v w : V} (e : G.edgeSet) (he : e.val = s(u, v))
    (huw : G.Adj u w) (hvw : G.Adj v w) :
    (conflictGraph G).degree e ≤ 20 := by
  have hi := conflict_degree_add_inside_eq_sum G e he
  have hc := endpointNeighbourCover_card_le_five_of_triangle G hΔ
    (G.mem_edgeSet.mp (he ▸ e.property)) huw hvw
  have hs := sum_le_sum (s := endpointNeighbourCover G u v) (fun x _ => hΔ x)
  simp only [sum_const, smul_eq_mul] at hs
  omega

omit [DecidableRel (conflictGraph G).Adj] in
/-- The unspecialized incidence bound from manuscript (3.4). -/
theorem multiple_type_sum_le_three_neighbors (hΔ : ∀ x, G.degree x ≤ 4) (r : V) :
    (∑ x ∈ multipleTips G r, (rootType G r x).card) ≤
      3 * (G.neighborFinset r).card := by
  rw [root_type_card_sum_eq_label_sum]
  have hs := sum_le_sum (s := G.neighborFinset r) (fun a ha =>
    root_label_multiple_card_le_three G hΔ ((G.mem_neighborFinset r a).mp ha))
  simpa only [sum_const, smul_eq_mul, Nat.mul_comm] using hs

omit [DecidableRel (conflictGraph G).Adj] in
theorem star_subset_meeting (Q : Finset G.edgeSet) (r : V) :
    edgeIncidences G Q r ⊆ edgesMeeting G Q (G.neighborFinset r) := by
  intro e he
  obtain ⟨heQ, hre⟩ := mem_filter.mp he
  obtain ⟨a, hea⟩ := Sym2.mem_iff_exists.mp hre
  have hra : G.Adj r a := G.mem_edgeSet.mp (hea ▸ e.property)
  exact mem_filter.mpr ⟨heQ, a, (G.mem_neighborFinset r a).mpr hra,
    hea.symm ▸ Sym2.mem_mk_right r a⟩

omit [DecidableRel (conflictGraph G).Adj] in
/-- Manuscript (3.1): exact partition, stronger than the old covering inequality. -/
theorem selected_card_eq_star_root_outer (Q : Finset G.edgeSet) (r : V) :
    Q.card = (edgeIncidences G Q r).card + (rootEdges G Q r).card +
      (outerEdges G Q r).card := by
  classical
  have hstar : (edgesMeeting G Q (G.neighborFinset r)).filter
      (fun e => r ∈ e.val) = edgeIncidences G Q r := by
    ext e
    constructor
    · intro he
      obtain ⟨hem, hre⟩ := mem_filter.mp he
      exact mem_filter.mpr ⟨(mem_filter.mp hem).1, hre⟩
    · intro he
      exact mem_filter.mpr ⟨star_subset_meeting G Q r he, (mem_filter.mp he).2⟩
  have houter : Q.filter (fun e => ¬ ∃ a ∈ G.neighborFinset r, a ∈ e.val) =
      outerEdges G Q r := by
    ext e
    simp only [outerEdges, mem_filter]
    constructor
    · rintro ⟨heQ, hn⟩
      refine ⟨heQ, ?_, ?_⟩
      · intro hre
        exact hn (mem_filter.mp (star_subset_meeting G Q r (mem_filter.mpr ⟨heQ, hre⟩))).2
      · intro a hae hra
        exact hn ⟨a, (G.mem_neighborFinset r a).mpr hra, hae⟩
    · rintro ⟨heQ, _, hn⟩
      refine ⟨heQ, ?_⟩
      rintro ⟨a, ha, hae⟩
      exact hn a hae ((G.mem_neighborFinset r a).mp ha)
  have h1 := card_filter_add_card_filter_not
    (s := edgesMeeting G Q (G.neighborFinset r)) (p := fun e => r ∈ e.val)
  have h2 := card_filter_add_card_filter_not
    (s := Q) (p := fun e => ∃ a ∈ G.neighborFinset r, a ∈ e.val)
  rw [hstar] at h1
  rw [houter] at h2
  change _ + (rootEdges G Q r).card = _ at h1
  change (edgesMeeting G Q (G.neighborFinset r)).card + _ = _ at h2
  omega

omit [DecidableRel (conflictGraph G).Adj] in
theorem root_incidence_eq_star_add_root (Q : Finset G.edgeSet) (r : V)
    (hN : G.IsIndepSet (G.neighborSet r)) :
    (∑ a ∈ G.neighborFinset r, (edgeIncidences G Q a).card) =
      (edgeIncidences G Q r).card + (rootEdges G Q r).card := by
  have hi : edgesInside G Q (G.neighborFinset r) = ∅ := by
    apply eq_empty_iff_forall_notMem.mpr
    intro e he
    obtain ⟨_, hh⟩ := mem_filter.mp he
    obtain ⟨a, b, hab⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = e.val from ⟨e.val, rfl⟩)
    have ha := hh a (hab ▸ Sym2.mem_mk_left a b)
    have hb := hh b (hab ▸ Sym2.mem_mk_right a b)
    have hadj : G.Adj a b := G.mem_edgeSet.mp (hab ▸ e.property)
    exact hN ((G.mem_neighborFinset r a).mp ha) ((G.mem_neighborFinset r b).mp hb)
      hadj.ne hadj
  have hs := incidence_sum_eq_meeting_add_inside G Q (G.neighborFinset r)
  have hstar : (edgesMeeting G Q (G.neighborFinset r)).filter
      (fun e => r ∈ e.val) = edgeIncidences G Q r := by
    ext e
    constructor
    · intro he
      exact mem_filter.mpr ⟨(mem_filter.mp (mem_filter.mp he).1).1, (mem_filter.mp he).2⟩
    · intro he
      exact mem_filter.mpr ⟨star_subset_meeting G Q r he, (mem_filter.mp he).2⟩
  have hp := card_filter_add_card_filter_not
    (s := edgesMeeting G Q (G.neighborFinset r)) (p := fun e => r ∈ e.val)
  rw [hstar] at hp
  change _ + (rootEdges G Q r).card = _ at hp
  rw [hi, card_empty, Nat.add_zero] at hs
  omega

end PaperRoute
