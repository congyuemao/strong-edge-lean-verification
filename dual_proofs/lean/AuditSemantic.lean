import StrongEdge

namespace IndependentAudit

variable {V : Type*} (G : SimpleGraph V)

/-- An explicit endpoint definition, independent of line graphs and StrongConflict. -/
def directStrongConflict (e f : G.edgeSet) : Prop :=
  ∃ a b c d : V, e.val = s(a, b) ∧ f.val = s(c, d) ∧
    (a = c ∨ a = d ∨ b = c ∨ b = d ∨
      G.Adj a c ∨ G.Adj a d ∨ G.Adj b c ∨ G.Adj b d)

def endpointWitness (e f : G.edgeSet) : Prop :=
  ∃ x ∈ e.val, ∃ y ∈ f.val, x = y ∨ G.Adj x y

theorem endpointWitness_iff_direct (e f : G.edgeSet) :
    endpointWitness G e f ↔ directStrongConflict G e f := by
  obtain ⟨a, b, he⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = e.val from ⟨e.val, rfl⟩)
  obtain ⟨c, d, hf⟩ := Sym2.exists.mp (show ∃ z : Sym2 V, z = f.val from ⟨f.val, rfl⟩)
  constructor
  · intro h
    refine ⟨a, b, c, d, he.symm, hf.symm, ?_⟩
    simp only [endpointWitness, ← he, ← hf, Sym2.mem_iff] at h
    rcases h with ⟨x, hx, y, hy, hxy⟩
    rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> tauto
  · rintro ⟨a', b', c', d', he', hf', h⟩
    simp only [endpointWitness, he', hf', Sym2.mem_iff]
    rcases h with h | h | h | h | h | h | h | h
    · exact ⟨a', Or.inl rfl, c', Or.inl rfl, Or.inl h⟩
    · exact ⟨a', Or.inl rfl, d', Or.inr rfl, Or.inl h⟩
    · exact ⟨b', Or.inr rfl, c', Or.inl rfl, Or.inl h⟩
    · exact ⟨b', Or.inr rfl, d', Or.inr rfl, Or.inl h⟩
    · exact ⟨a', Or.inl rfl, c', Or.inl rfl, Or.inr h⟩
    · exact ⟨a', Or.inl rfl, d', Or.inr rfl, Or.inr h⟩
    · exact ⟨b', Or.inr rfl, c', Or.inl rfl, Or.inr h⟩
    · exact ⟨b', Or.inr rfl, d', Or.inr rfl, Or.inr h⟩

theorem conflict_iff_endpointWitness (e f : G.edgeSet) (hne : e ≠ f) :
    (StrongEdge.conflictGraph G).Adj e f ↔ endpointWitness G e f := by
  constructor
  · rintro ⟨_, h | ⟨g, heg, hgf⟩⟩
    · obtain ⟨_, x, hxe, hxf⟩ := SimpleGraph.lineGraph_adj_iff_exists.mp h
      exact ⟨x, hxe, x, hxf, Or.inl rfl⟩
    · obtain ⟨_, x, hxe, hxg⟩ := SimpleGraph.lineGraph_adj_iff_exists.mp heg
      obtain ⟨_, y, hyg, hyf⟩ := SimpleGraph.lineGraph_adj_iff_exists.mp hgf
      refine ⟨x, hxe, y, hyf, ?_⟩
      by_cases hxy : x = y
      · exact Or.inl hxy
      · right
        have hg : g.val = s(x, y) := (Sym2.mem_and_mem_iff hxy).mp ⟨hxg, hyg⟩
        have h := g.property
        rw [hg] at h
        exact h
  · rintro ⟨x, hxe, y, hyf, hxy | hxy⟩
    · subst y
      exact ⟨hne, Or.inl (SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hne, x, hxe, hyf⟩)⟩
    · let g : G.edgeSet := ⟨s(x, y), hxy⟩
      by_cases heg : e = g
      · have hye : y ∈ e.val := by rw [heg]; exact Sym2.mem_mk_right x y
        exact ⟨hne, Or.inl (SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hne, y, hye, hyf⟩)⟩
      by_cases hgf : g = f
      · have hxf : x ∈ f.val := by rw [← hgf]; exact Sym2.mem_mk_left x y
        exact ⟨hne, Or.inl (SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hne, x, hxe, hxf⟩)⟩
      exact ⟨hne, Or.inr ⟨g,
        SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨heg, x, hxe, Sym2.mem_mk_left x y⟩,
        SimpleGraph.lineGraph_adj_iff_exists.mpr ⟨hgf, y, Sym2.mem_mk_right x y, hyf⟩⟩⟩

theorem conflict_iff_direct (e f : G.edgeSet) (hne : e ≠ f) :
    (StrongEdge.conflictGraph G).Adj e f ↔ directStrongConflict G e f :=
  (conflict_iff_endpointWitness G e f hne).trans (endpointWitness_iff_direct G e f)

/-- Every endpoint pair of different selected edges is distinct and nonadjacent in G. -/
def endpointInducedMatching (M : Set G.edgeSet) : Prop :=
  ∀ e ∈ M, ∀ f ∈ M, e ≠ f →
    ∀ x ∈ e.val, ∀ y ∈ f.val, x ≠ y ∧ ¬ G.Adj x y

theorem inducedMatching_iff_endpoints (M : Set G.edgeSet) :
    StrongEdge.IsInducedMatching G M ↔ endpointInducedMatching G M := by
  constructor
  · intro h e he f hf hne x hx y hy
    have hn := h he hf hne
    constructor
    · intro hxy
      exact hn ((conflict_iff_endpointWitness G e f hne).mpr ⟨x, hx, y, hy, Or.inl hxy⟩)
    · intro hxy
      exact hn ((conflict_iff_endpointWitness G e f hne).mpr ⟨x, hx, y, hy, Or.inr hxy⟩)
  · intro h e he f hf hne hc
    obtain ⟨x, hx, y, hy, hxy⟩ := (conflict_iff_endpointWitness G e f hne).mp hc
    exact hxy.elim (h e he f hf hne x hx y hy).1 (h e he f hf hne x hx y hy).2

theorem endpoint_packing20 [Fintype V] [DecidableEq V] [DecidableRel G.Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ endpointInducedMatching G (M : Set G.edgeSet) ∧
      F.card ≤ 20 * M.card := by
  classical
  obtain ⟨M, hm, hi, hc⟩ := StrongEdge.induced_matching_packing20 G hΔ F
  exact ⟨M, hm, (inducedMatching_iff_endpoints G _).mp hi, hc⟩

theorem empty_candidates [DecidableEq G.edgeSet] :
    ∃ M : Finset G.edgeSet, M ⊆ (∅ : Finset G.edgeSet) ∧
      endpointInducedMatching G (M : Set G.edgeSet) ∧
      (∅ : Finset G.edgeSet).card ≤ 20 * M.card := by
  refine ⟨∅, Finset.Subset.refl _, ?_, by simp⟩
  intro e he
  exact False.elim (Finset.notMem_empty e he)

end IndependentAudit

#check IndependentAudit.conflict_iff_direct
#print axioms IndependentAudit.conflict_iff_direct
#check IndependentAudit.inducedMatching_iff_endpoints
#print axioms IndependentAudit.inducedMatching_iff_endpoints
#check IndependentAudit.endpoint_packing20
#print axioms IndependentAudit.endpoint_packing20
#print axioms IndependentAudit.empty_candidates
