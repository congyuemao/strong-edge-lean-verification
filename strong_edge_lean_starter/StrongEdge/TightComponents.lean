module

public import StrongEdge.Packing195Unconditional
public import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected

@[expose] public section

namespace StrongEdge

open Finset

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

omit [DecidableEq V] in
theorem reachable_mem_of_neighbor_closed (S : Finset V)
    (hc : ∀ x ∈ S, G.neighborFinset x ⊆ S) {u v : V}
    (hu : u ∈ S) (h : G.Reachable u v) : v ∈ S := by
  obtain ⟨p⟩ := h
  induction p with
  | nil => exact hu
  | @cons u v w huv p ih => exact ih (hc u hu ((G.mem_neighborFinset u v).mpr huv))

/-- The five-pair certificate names a genuine connected component of G,
not an induced subgraph with possible connections to the rest of G. -/
theorem five_cycle_blowup_is_connected_component (S : Finset V)
    (hS : IsFiveCycleBlowupComponent G S) :
    ∃ c : G.ConnectedComponent, c.supp = (S : Set V) := by
  obtain ⟨B, A, X, Y, C, hBc, hAc, _, _, hCc, _, hS, hB, hA, hX, hY, hC⟩ := hS
  have hmem : ∀ v, v ∈ S ↔ v ∈ B ∨ v ∈ A ∨ v ∈ X ∨ v ∈ Y ∨ v ∈ C := by
    intro v
    rw [hS]
    simp only [mem_union, or_assoc]
  have hc : ∀ v ∈ S, G.neighborFinset v ⊆ S := by
    intro v hv w hw
    apply (hmem w).mpr
    rcases (hmem v).mp hv with hv | hv | hv | hv | hv
    · rw [hB v hv] at hw
      rcases mem_union.mp hw with h | h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inr (Or.inr h)))
    · rw [hA v hv] at hw
      rcases mem_union.mp hw with h | h
      · exact Or.inl h
      · exact Or.inr (Or.inr (Or.inl h))
    · rw [hX v hv] at hw
      rcases mem_union.mp hw with h | h
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inr (Or.inl h)))
    · rw [hY v hv] at hw
      rcases mem_union.mp hw with h | h
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inr (Or.inr (Or.inr (Or.inr h)))
    · rw [hC v hv] at hw
      rcases mem_union.mp hw with h | h
      · exact Or.inl h
      · exact Or.inr (Or.inr (Or.inr (Or.inl h)))
  obtain ⟨b, hb⟩ := card_pos.mp (show 0 < B.card by omega)
  obtain ⟨a, ha⟩ := card_pos.mp (show 0 < A.card by omega)
  obtain ⟨c, hcC⟩ := card_pos.mp (show 0 < C.card by omega)
  have hba : G.Adj b a := (G.mem_neighborFinset b a).mp ((hB b hb).symm ▸ mem_union_left C ha)
  have hbc : G.Adj b c := (G.mem_neighborFinset b c).mp ((hB b hb).symm ▸ mem_union_right A hcC)
  have hreach : ∀ v ∈ S, G.Reachable b v := by
    intro v hv
    rcases (hmem v).mp hv with hv | hv | hv | hv | hv
    · have hav : G.Adj a v := (G.mem_neighborFinset a v).mp ((hA a ha).symm ▸ mem_union_left X hv)
      exact hba.reachable.trans hav.reachable
    · exact ((G.mem_neighborFinset b v).mp ((hB b hb).symm ▸ mem_union_left C hv)).reachable
    · have hav : G.Adj a v := (G.mem_neighborFinset a v).mp ((hA a ha).symm ▸ mem_union_right B hv)
      exact hba.reachable.trans hav.reachable
    · have hcv : G.Adj c v := (G.mem_neighborFinset c v).mp ((hC c hcC).symm ▸ mem_union_right B hv)
      exact hbc.reachable.trans hcv.reachable
    · exact ((G.mem_neighborFinset b v).mp ((hB b hb).symm ▸ mem_union_right A hv)).reachable
  refine ⟨G.connectedComponentMk b, ?_⟩
  ext v
  rw [SimpleGraph.ConnectedComponent.mem_supp_iff, SimpleGraph.ConnectedComponent.eq]
  exact ⟨fun h => reachable_mem_of_neighbor_closed G S hc ((hmem b).mpr (Or.inl hb)) h.symm,
    fun h => (hreach v h).symm⟩

/-- The literal family of connected components counted by the correction. -/
noncomputable def componentVertices (c : G.ConnectedComponent) : Finset V := by
  classical
  exact c.supp.toFinset

omit [DecidableEq V] [DecidableRel G.Adj] in
theorem coe_componentVertices (c : G.ConnectedComponent) :
    (componentVertices G c : Set V) = c.supp := by
  classical
  simp only [componentVertices, Set.coe_toFinset]

noncomputable def tightComponentsIn (F : Finset G.edgeSet) : Finset G.ConnectedComponent := by
  classical
  letI : Fintype G.ConnectedComponent := Fintype.ofFinite _
  exact univ.filter (fun c => IsFiveCycleBlowupComponent G (componentVertices G c) ∧
    edgesInside G univ (componentVertices G c) ⊆ F)

theorem mem_tightComponentsIn (F : Finset G.edgeSet) (c : G.ConnectedComponent) :
    c ∈ tightComponentsIn G F ↔ IsFiveCycleBlowupComponent G (componentVertices G c) ∧
      edgesInside G univ (componentVertices G c) ⊆ F := by
  classical
  simp only [tightComponentsIn, mem_filter, mem_univ, true_and]

/-- The support count used in the main theorem equals the number of actual
original connected components with the specified shape and all edges in F. -/
theorem tightComponentCount_eq_connected_component_count (F : Finset G.edgeSet) :
    tightComponentCount G F = (tightComponentsIn G F).card := by
  classical
  apply Nat.le_antisymm
  · change (tightComponentSupportsIn G F).card ≤ (tightComponentsIn G F).card
    apply card_le_via_relation (tightComponentSupportsIn G F) (tightComponentsIn G F)
      (fun S c => c.supp = (S : Set V))
    · intro S hS
      obtain ⟨hshape, hSF⟩ := (mem_tightComponentSupportsIn G F S).mp hS
      obtain ⟨c, hc⟩ := five_cycle_blowup_is_connected_component G S hshape
      refine ⟨c, (mem_tightComponentsIn G F c).mpr ?_, hc⟩
      have hv : componentVertices G c = S := Finset.coe_injective ((coe_componentVertices G c).trans hc)
      simpa only [hv] using And.intro hshape hSF
    · intro S _ T _ c hS hT
      exact Finset.coe_injective (hS.symm.trans hT)
  · change (tightComponentsIn G F).card ≤ (tightComponentSupportsIn G F).card
    apply card_le_via_relation (tightComponentsIn G F) (tightComponentSupportsIn G F)
      (fun c S => componentVertices G c = S)
    · intro c hc
      exact ⟨componentVertices G c, (mem_tightComponentSupportsIn G F _).mpr
        ((mem_tightComponentsIn G F c).mp hc), rfl⟩
    · intro c _ d _ S hc hd
      apply SimpleGraph.ConnectedComponent.supp_injective
      have he := congrArg (fun T : Finset V => (T : Set V)) (hc.trans hd.symm)
      simpa only [coe_componentVertices] using he

variable [DecidableRel (conflictGraph G).Adj]

theorem induced_matching_packing195_with_connected_component_count
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ IsInducedMatching G (M : Set G.edgeSet) ∧
      2 * F.card ≤ 39 * M.card + (tightComponentsIn G F).card := by
  rw [← tightComponentCount_eq_connected_component_count G F]
  exact induced_matching_packing195_unconditional G hΔ F

end StrongEdge
