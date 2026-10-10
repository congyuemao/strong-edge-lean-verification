module

public import StrongEdge.Bounds.TwentyCliqueRigidity

@[expose] public section

namespace StrongEdge

open Finset

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- Full twenty-cliques contained in the candidate set, with conflicts in G. -/
noncomputable def twentyCliquesIn (F : Finset G.edgeSet) : Finset (Finset G.edgeSet) := by
  classical
  exact F.powerset.filter (fun Q => Q.card = 20 ∧ (conflictGraph G).IsClique (Q : Set G.edgeSet))

/-- Supports of whole C5[2] components whose complete edge sets lie in F.
Different presentations of the five pairs count only once. -/
noncomputable def tightComponentSupportsIn (F : Finset G.edgeSet) : Finset (Finset V) := by
  classical
  exact univ.powerset.filter (fun S => IsFiveCycleBlowupComponent G S ∧ edgesInside G univ S ⊆ F)

noncomputable def tightComponentCount (F : Finset G.edgeSet) : ℕ :=
  (tightComponentSupportsIn G F).card

omit [Fintype V] [DecidableRel G.Adj] in
theorem mem_twentyCliquesIn (F Q : Finset G.edgeSet) :
    Q ∈ twentyCliquesIn G F ↔ Q ⊆ F ∧ Q.card = 20 ∧ (conflictGraph G).IsClique (Q : Set G.edgeSet) := by
  classical
  simp only [twentyCliquesIn, mem_filter, mem_powerset]

theorem mem_tightComponentSupportsIn (F : Finset G.edgeSet) (S : Finset V) :
    S ∈ tightComponentSupportsIn G F ↔ IsFiveCycleBlowupComponent G S ∧ edgesInside G univ S ⊆ F := by
  classical
  simp only [tightComponentSupportsIn, mem_filter, mem_powerset, subset_univ, true_and]

variable [DecidableRel (conflictGraph G).Adj]

theorem twentyCliquesIn_sdiff
    (hΔ : ∀ x, G.degree x ≤ 4) (F Q : Finset G.edgeSet)
    (_hQF : Q ⊆ F) (hq : Q.card = 20)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet)) :
    twentyCliquesIn G (F \ Q) = (twentyCliquesIn G F).erase Q := by
  classical
  ext R
  rw [mem_twentyCliquesIn, mem_erase, mem_twentyCliquesIn]
  constructor
  · rintro ⟨hRF, hr, hR⟩
    refine ⟨?_, fun e he => (mem_sdiff.mp (hRF he)).1, hr, hR⟩
    intro h
    subst R
    obtain ⟨e, he⟩ := card_pos.mp (show 0 < Q.card by omega)
    exact (mem_sdiff.mp (hRF he)).2 he
  · rintro ⟨hRQ, hRF, hr, hR⟩
    have hdis : Disjoint R Q := (twenty_cliques_eq_or_disjoint G hΔ R Q hR hr hQ hq).resolve_left hRQ
    exact ⟨fun e he => mem_sdiff.mpr ⟨hRF he, fun heQ => disjoint_left.mp hdis he heQ⟩, hr, hR⟩

/-- Removing an isolated twenty-clique costs one matching edge and exactly
one unit of correction. The recursion keeps the original conflict graph. -/
theorem induced_matching_packing195_with_twenty_clique_count
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ IsInducedMatching G (M : Set G.edgeSet) ∧
      2 * F.card ≤ 39 * M.card + (twentyCliquesIn G F).card := by
  classical
  refine Finset.strongInductionOn F fun F ih => ?_
  ·
    by_cases hex : ∃ Q : Finset G.edgeSet, Q ⊆ F ∧ Q.card = 20 ∧
        (conflictGraph G).IsClique (Q : Set G.edgeSet)
    · obtain ⟨Q, hQF, hq, hQ⟩ := hex
      have hQne : Q.Nonempty := card_pos.mp (by omega)
      obtain ⟨M, hMF, hM, hbound⟩ := ih (F \ Q) (sdiff_ssubset hQF hQne)
      obtain ⟨e, heQ⟩ := hQne
      have heM : e ∉ M := fun h => (mem_sdiff.mp (hMF h)).2 heQ
      have hcross : ∀ f ∈ M, ¬ StrongConflict G e f := by
        intro f hf hconf
        exact (mem_sdiff.mp (hMF hf)).2 (twenty_clique_conflict_closed G hΔ Q hQ hq heQ hconf)
      refine ⟨insert e M, ?_, ?_, ?_⟩
      · intro f hf
        rcases mem_insert.mp hf with h | h
        · exact h ▸ hQF heQ
        · exact (mem_sdiff.mp (hMF h)).1
      · intro a ha b hb hab
        rcases mem_insert.mp ha with ha | ha
        · subst a
          rcases mem_insert.mp hb with hb | hb
          · exact (hab hb.symm).elim
          · exact hcross b hb
        · rcases mem_insert.mp hb with hb | hb
          · subst b
            exact fun h => hcross a ha (strongConflict_symm G h)
          · exact hM ha hb hab
      · have hFcard := card_sdiff_add_card_eq_card hQF
        have hcount := card_erase_add_one ((mem_twentyCliquesIn G F Q).mpr ⟨hQF, hq, hQ⟩)
        rw [← twentyCliquesIn_sdiff G hΔ F Q hQF hq hQ] at hcount
        rw [card_insert_of_notMem heM]
        omega
    · have hno : ∀ Q : Finset G.edgeSet, Q ⊆ F →
          (conflictGraph G).IsClique (Q : Set G.edgeSet) → Q.card ≤ 19 := by
        intro Q hQF hQ
        have hc := clique_card_le_twenty G hΔ Q hQ
        have hn : Q.card ≠ 20 := fun h => hex ⟨Q, hQF, h, hQ⟩
        omega
      obtain ⟨M, hMF, hM, hb⟩ := induced_matching_packing195_of_no_twenty_clique G hΔ F hno
      exact ⟨M, hMF, hM, by omega⟩

theorem twenty_clique_eq_edgesInside_support
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet)) (hq : Q.card = 20) :
    Q = edgesInside G univ (selectedSupport G Q) := by
  have hd := twenty_clique_support_selected_degree_four G hΔ Q hQ hq
  ext e
  constructor
  · intro he
    refine mem_filter.mpr ⟨mem_univ _, ?_⟩
    intro x hx
    exact mem_filter.mpr ⟨mem_univ _, card_pos.mpr ⟨e, mem_filter.mpr ⟨he, hx⟩⟩⟩
  · intro he
    obtain ⟨u, v, hev⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = e.val from ⟨e.val, rfl⟩)
    have hu := (mem_filter.mp he).2 u (hev ▸ Sym2.mem_mk_left u v)
    exact incident_edge_mem_of_selected_degree_four G hΔ Q (hd u hu) e (hev ▸ Sym2.mem_mk_left u v)

theorem twenty_clique_count_le_tight_component_count
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    (twentyCliquesIn G F).card ≤ tightComponentCount G F := by
  classical
  apply card_le_via_relation _ _ (fun Q S => selectedSupport G Q = S)
  · intro Q hQmem
    obtain ⟨hQF, hq, hQ⟩ := (mem_twentyCliquesIn G F Q).mp hQmem
    refine ⟨selectedSupport G Q, (mem_tightComponentSupportsIn G F _).mpr ⟨?_, ?_⟩, rfl⟩
    · exact twenty_clique_support_is_five_cycle_blowup G hΔ Q hQ hq
    · rw [← twenty_clique_eq_edgesInside_support G hΔ Q hQ hq]
      exact hQF
  · intro Q hQmem R hRmem S hQS hRS
    obtain ⟨_, hq, hQ⟩ := (mem_twentyCliquesIn G F Q).mp hQmem
    obtain ⟨_, hr, hR⟩ := (mem_twentyCliquesIn G F R).mp hRmem
    rw [twenty_clique_eq_edgesInside_support G hΔ Q hQ hq,
      twenty_clique_eq_edgesInside_support G hΔ R hR hr, hQS, hRS]

/-- Unconditional corrected 19.5 packing for every candidate set. The only
graph hypothesis is maximum original degree four. -/
theorem induced_matching_packing195_unconditional
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ IsInducedMatching G (M : Set G.edgeSet) ∧
      2 * F.card ≤ 39 * M.card + tightComponentCount G F := by
  obtain ⟨M, hMF, hM, hb⟩ := induced_matching_packing195_with_twenty_clique_count G hΔ F
  have hc := twenty_clique_count_le_tight_component_count G hΔ F
  exact ⟨M, hMF, hM, by omega⟩

theorem induced_matching_packing195_of_no_full_tight_component
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet)
    (hzero : tightComponentCount G F = 0) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ IsInducedMatching G (M : Set G.edgeSet) ∧
      2 * F.card ≤ 39 * M.card := by
  simpa only [hzero, Nat.add_zero] using induced_matching_packing195_unconditional G hΔ F

end StrongEdge
