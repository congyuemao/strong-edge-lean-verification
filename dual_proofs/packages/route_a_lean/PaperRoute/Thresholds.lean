module

public import PaperRoute.Foundations
public import PaperRoute.Library.Bounds.High24
public import PaperRoute.Library.Bounds.High23
public import PaperRoute.Library.Bounds.High22
@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

variable [DecidableRel (conflictGraph G).Adj]

theorem outer_card_le_one_of_type_four
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (conflictGraph G).degree e)
    {r : V} (hN : G.IsIndepSet (G.neighborSet r))
    (hR : (rootLabels G Q r).card = 4)
    {x : V} (hxr : x ≠ r) (hx : 4 ≤ (rootType G r x).card) :
    (outerEdges G Q r).card ≤ 1 := by
  have hfull : rootLabels G Q r = G.neighborFinset r :=
    eq_of_subset_of_card_le (rootLabels_subset_neighbors G Q r)
      (by simpa only [hR, SimpleGraph.card_neighborFinset_eq_degree] using hΔ r)
  let O := (outerEdges G Q r).filter (fun e => x ∉ e.val)
  have hO : O.card ≤ 1 := by
    apply card_le_one.mpr
    intro e he f hf
    obtain ⟨heo, hxe⟩ := mem_filter.mp he
    obtain ⟨hfo, hxf⟩ := mem_filter.mp hf
    obtain ⟨u, v, hev⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = e.val from ⟨e.val, rfl⟩)
    obtain ⟨p, q, hfq⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = f.val from ⟨f.val, rfl⟩)
    have hs := high20_multipleTips_subset_four_outer_endpoints G hΔ Q hQ h20 hN hR hxr hx
      e heo hev.symm hxe
    have hends := outerEdges_endpoints G Q r f hfq.symm hfo
    have hpx : p ≠ x := fun h => hxf (hfq ▸ h ▸ Sym2.mem_mk_left p q)
    have hqx : q ≠ x := fun h => hxf (hfq ▸ h ▸ Sym2.mem_mk_right p q)
    have hp := high20_other_type_le_two_of_four G hΔ Q h20 hN hfull hxr hx hends.2.1 hpx
    have hq := high20_other_type_le_two_of_four G hΔ Q h20 hN hfull hxr hx hends.2.2.1 hqx
    have hc := (card_le_card (outer_edge_types_cover_root_labels G Q hQ r f hfq.symm hfo)).trans
      (card_union_le _ _)
    have hpm := hs (mem_filter.mpr ⟨mem_univ _, hends.2.1, by omega⟩)
    have hqm := hs (mem_filter.mpr ⟨mem_univ _, hends.2.2.1, by omega⟩)
    simp only [mem_insert, mem_singleton, hpx, hqx, false_or] at hpm hqm
    have hpq : p ≠ q := (G.mem_edgeSet.mp (hfq ▸ f.property)).ne
    apply Subtype.ext
    rw [← hev, ← hfq]
    rcases hpm with rfl | rfl <;> rcases hqm with rfl | rfl
    · exact (hpq rfl).elim
    · rfl
    · exact Sym2.eq_swap
    · exact (hpq rfl).elim
  have hpart : (outerEdges G Q r).card = (edgeIncidences G (outerEdges G Q r) x).card + O.card := by
    exact (card_filter_add_card_filter_not (s := outerEdges G Q r) (p := fun e => x ∈ e.val)).symm
  have hi := outer_incidence_add_type_card_le_degree G Q r x
  have hd := hΔ x
  omega

theorem clique_card_le_seventeen_of_type_four
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (conflictGraph G).degree e)
    {r : V} (hN : G.IsIndepSet (G.neighborSet r))
    (hR : (rootLabels G Q r).card = 4)
    {x : V} (hxr : x ≠ r) (hx : 4 ≤ (rootType G r x).card) : Q.card ≤ 17 := by
  have ho := outer_card_le_one_of_type_four G hΔ Q hQ h20 hN hR hxr hx
  have hm := root_incidence_eq_star_add_root G Q r hN
  have hsum := sum_le_sum (s := G.neighborFinset r)
    (fun y _ => (edgeIncidences_card_le_degree G Q y).trans (hΔ y))
  have hdr := hΔ r
  have hq := selected_card_eq_star_root_outer G Q r
  simp only [sum_const, smul_eq_mul, SimpleGraph.card_neighborFinset_eq_degree] at hsum
  omega

omit [DecidableRel (conflictGraph G).Adj] in
theorem small_type_clique_bound
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (r : V) (hR : (rootLabels G Q r).card = 4)
    (hN : G.IsIndepSet (G.neighborSet r))
    (ht : ∀ x, x ≠ r → (rootType G r x).card ≤ 2) : Q.card ≤ 18 := by
  have hs := sum_le_sum (s := multipleTips G r)
    (fun x hx => (mem_filter.mp hx).2.2)
  have hb := multiple_type_sum_le_three_neighbors G hΔ r
  have hdr := hΔ r
  simp only [sum_const, smul_eq_mul, SimpleGraph.card_neighborFinset_eq_degree] at hs hb
  have hp : (multipleTips G r).card ≤ 6 := by omega
  have htip : (rootTips G Q r).card ≤ 6 := by
    by_cases hsingle : (singleTips G Q r).Nonempty
    · obtain ⟨x, hx⟩ := hsingle
      obtain ⟨_, _, a, haN, hxT, e, heQ, he⟩ := mem_filter.mp hx
      exact rootTips_card_le_six_of_single G hΔ Q hQ hN ((G.mem_neighborFinset r a).mp haN)
        hxT e heQ he
    · exact (card_le_card (rootTips_subset_multiple_of_no_single G Q r hsingle)).trans hp
  have hfd := fullDoubleTips_card_le_four G hΔ Q hQ hN
  have hroot := rootEdges_card_le_tips_add_fullDoubleTips G Q r hN ht
  have ho := outer_subset_card_le_four G hΔ Q hQ r hR hN
    (outerEdges G Q r) (Subset.refl _) (fun e he x hx =>
      ht x (fun h => (mem_filter.mp he).2.1 (h ▸ hx)))
  have hstar : (edgeIncidences G Q r).card = 4 := by rw [← rootLabels_card G Q r, hR]
  have hc := selected_card_eq_star_root_outer G Q r
  omega

theorem proposition_4_2
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h24 : ∀ e ∈ Q, 24 ≤ (conflictGraph G).degree e) : Q.card ≤ 13 := by
  classical
  have heq : ∀ e ∈ Q, (conflictGraph G).degree e = 24 :=
    fun e he => conflict_degree_eq_24_of_ge G hΔ e (h24 e he)
  by_cases hQempty : Q = ∅
  · simp [hQempty]
  obtain ⟨e, heQ⟩ := nonempty_iff_ne_empty.mpr hQempty
  obtain ⟨u, v, he⟩ := Sym2.exists.mp (show ∃ a : Sym2 V, a = e.val from ⟨e.val, rfl⟩)
  have he' : e.val = s(u, v) := he.symm
  have huv : G.Adj u v := G.mem_edgeSet.mp (he' ▸ e.property)
  let U := branchEdges G Q v u
  let T := branchEdges G Q u v
  let A := ((G.neighborFinset u).erase v).biUnion (branchEdges G Q u)
  let B := ((G.neighborFinset v).erase u).biUnion (branchEdges G Q v)
  have hcover : Q ⊆ insert e ((U ∪ T) ∪ (A ∪ B)) := by
    intro f hf
    by_cases hfe : f = e
    · exact mem_insert.mpr (Or.inl hfe)
    apply mem_insert_of_mem
    by_cases hu : u ∈ f.val
    · have hv : v ∉ f.val := by
        intro hv
        exact hfe (Subtype.ext (((Sym2.mem_and_mem_iff huv.ne).mp ⟨hu, hv⟩).trans he'.symm))
      exact mem_union_left _ (mem_union_left _ ((mem_branchEdges G Q v u f).mpr ⟨hf, hu, hv⟩))
    by_cases hv : v ∈ f.val
    · exact mem_union_left _ (mem_union_right _ ((mem_branchEdges G Q u v f).mpr ⟨hf, hv, hu⟩))
    obtain ⟨w, hw, hwf⟩ := strongConflict_meets_cover G he' (hQ heQ hf (Ne.symm hfe))
    rcases mem_union.mp hw with hwu | hwv
    · exact mem_union_right _ (mem_union_left _
        (mem_biUnion.mpr ⟨w, hwu, (mem_branchEdges G Q u w f).mpr ⟨hf, hwf, hu⟩⟩))
    · exact mem_union_right _ (mem_union_right _
        (mem_biUnion.mpr ⟨w, hwv, (mem_branchEdges G Q v w f).mpr ⟨hf, hwf, hv⟩⟩))
  have hU : U.card ≤ 3 := branchEdges_card_le_three G hΔ Q huv.symm
  have hT : T.card ≤ 3 := branchEdges_card_le_three G hΔ Q huv
  have hA : A.card ≤ 3 := high24_side_card_le_three G hΔ Q hQ heq huv
  have hB : B.card ≤ 3 := high24_side_card_le_three G hΔ Q hQ heq huv.symm
  have hc := card_le_card hcover
  have hi := card_insert_le e ((U ∪ T) ∪ (A ∪ B))
  have hUT := card_union_le U T
  have hAB := card_union_le A B
  have hAll := card_union_le (U ∪ T) (A ∪ B)
  omega


theorem proposition_4_3
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h23 : ∀ e ∈ Q, 23 ≤ (conflictGraph G).degree e) : Q.card ≤ 16 := by
  classical
  by_cases hfour : ∃ r, (edgeIncidences G Q r).card = 4
  · obtain ⟨r, hr⟩ := hfour
    exact high23_clique_card_le_sixteen_of_root_four G hΔ Q hQ h23 r
      (by rw [rootLabels_card G Q r]; exact hr)
  have hthree : ∀ x, (edgeIncidences G Q x).card ≤ 3 := by
    intro x
    have hc := (edgeIncidences_card_le_degree G Q x).trans (hΔ x)
    have hn : (edgeIncidences G Q x).card ≠ 4 := fun h => hfour ⟨x, h⟩
    omega
  by_cases htwo : ∀ x, (edgeIncidences G Q x).card ≤ 2
  · exact (clique_card_le_thirteen_of_support_degree_le_two G hΔ Q hQ htwo).trans (by omega)
  obtain ⟨r, hr⟩ := not_forall.mp htwo
  have hR : 3 ≤ (rootLabels G Q r).card := by
    rw [rootLabels_card G Q r]
    omega
  exact (high23_clique_card_le_fourteen_of_support_degree_le_three G hΔ Q hQ h23 hthree r hR).trans
    (by omega)

theorem proposition_4_4
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h22 : ∀ e ∈ Q, 22 ≤ (conflictGraph G).degree e) : Q.card ≤ 17 := by
  by_cases hfour : ∃ r, (edgeIncidences G Q r).card = 4
  · obtain ⟨r, hr⟩ := hfour
    exact high22_clique_card_le_seventeen_of_root_four G hΔ Q hQ h22 r
      (by rw [rootLabels_card G Q r]; exact hr)
  have hthree : ∀ x, (edgeIncidences G Q x).card ≤ 3 := by
    intro x
    have hc := (edgeIncidences_card_le_degree G Q x).trans (hΔ x)
    have hn : (edgeIncidences G Q x).card ≠ 4 := fun h => hfour ⟨x, h⟩
    omega
  exact high22_clique_card_le_seventeen_of_support_degree_le_three G hΔ Q hQ h22 hthree

theorem paper_high21_root_four
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h21 : ∀ e ∈ Q, 21 ≤ (conflictGraph G).degree e)
    (r : V) (hR : (rootLabels G Q r).card = 4) : Q.card ≤ 18 := by
  by_cases htr : ∃ x, x ≠ r ∧ 3 ≤ (rootType G r x).card
  · obtain ⟨x, hxr, hx⟩ := htr
    exact high21_clique_card_le_eighteen_of_root_triple G hΔ Q hQ h21 r hR hxr hx
  have hN := high21_root_neighborhood_independent G hΔ Q h21 r (by omega)
  apply small_type_clique_bound G hΔ Q hQ r hR hN
  intro x hxr
  have hn : ¬ 3 ≤ (rootType G r x).card := fun h => htr ⟨x, hxr, h⟩
  omega

theorem proposition_4_5
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h21 : ∀ e ∈ Q, 21 ≤ (conflictGraph G).degree e) : Q.card ≤ 18 := by
  by_cases hfour : ∃ r, (edgeIncidences G Q r).card = 4
  · obtain ⟨r, hr⟩ := hfour
    exact paper_high21_root_four G hΔ Q hQ h21 r
      (by rw [rootLabels_card G Q r]; exact hr)
  have hthree : ∀ x, (edgeIncidences G Q x).card ≤ 3 := by
    intro x
    have hc := (edgeIncidences_card_le_degree G Q x).trans (hΔ x)
    have hn : (edgeIncidences G Q x).card ≠ 4 := fun h => hfour ⟨x, h⟩
    omega
  exact clique_card_le_eighteen_of_support_degree_le_three G hΔ Q hQ hthree

theorem paper_high20_root_four
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (conflictGraph G).degree e)
    (r : V) (hR : (rootLabels G Q r).card = 4) : Q.card ≤ 19 := by
  by_contra hn
  have hN := high20_large_clique_root_neighborhood_independent G hΔ Q hQ h20 (by omega) r hR
  by_cases hlarge : ∃ x, x ≠ r ∧ 3 ≤ (rootType G r x).card
  · obtain ⟨x, hxr, hx⟩ := hlarge
    by_cases hx4 : 4 ≤ (rootType G r x).card
    · have hb := clique_card_le_seventeen_of_type_four G hΔ Q hQ h20 hN hR hxr hx4
      omega
    by_cases htwo : ∃ y, y ≠ r ∧ y ≠ x ∧ 3 ≤ (rootType G r y).card
    · obtain ⟨y, hyr, hyx, hy⟩ := htwo
      have hb := high20_clique_card_le_eighteen_of_two_triples G hΔ Q hQ h20 hN hR hxr hyr hyx.symm hx hy
      omega
    have ht : ∀ y, y ≠ r → y ≠ x → (rootType G r y).card ≤ 2 := by
      intro y hyr hyx
      have hn : ¬ 3 ≤ (rootType G r y).card := fun h => htwo ⟨y, hyr, hyx, h⟩
      omega
    exact hn (clique_card_le_nineteen_of_unique_triple G hΔ Q hQ hN hR (by omega) ht)
  · have ht : ∀ x, x ≠ r → (rootType G r x).card ≤ 2 := by
      intro x hxr
      have hn : ¬ 3 ≤ (rootType G r x).card := fun h => hlarge ⟨x, hxr, h⟩
      omega
    have hb := small_type_clique_bound G hΔ Q hQ r hR hN ht
    omega

/-- Universal high20 bound in the complete original conflict graph. -/
theorem proposition_4_6
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (conflictGraph G).degree e) : Q.card ≤ 19 := by
  by_cases hfour : ∃ r, (edgeIncidences G Q r).card = 4
  · obtain ⟨r, hr⟩ := hfour
    exact paper_high20_root_four G hΔ Q hQ h20 r
      (by rw [rootLabels_card G Q r]; exact hr)
  have hthree : ∀ x, (edgeIncidences G Q x).card ≤ 3 := by
    intro x
    have hc := (edgeIncidences_card_le_degree G Q x).trans (hΔ x)
    have hn : (edgeIncidences G Q x).card ≠ 4 := fun h => hfour ⟨x, h⟩
    omega
  exact (clique_card_le_eighteen_of_support_degree_le_three G hΔ Q hQ hthree).trans (by omega)

end PaperRoute
