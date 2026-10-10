module

public import PaperRoute.ExactCover

@[expose] public section
namespace PaperRoute.Library
open Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

def rootLabels (Q : Finset G.edgeSet) (r : V) : Finset V :=
  (G.neighborFinset r).filter (fun a => ∃ e ∈ Q, e.val = s(r, a))

def rootType (r x : V) : Finset V :=
  (G.neighborFinset r).filter (G.Adj x)

omit [DecidableEq V] in
@[simp] theorem mem_rootType (r x a : V) :
    a ∈ rootType G r x ↔ G.Adj r a ∧ G.Adj x a := by
  simp [rootType]

theorem rootLabels_subset_neighbors (Q : Finset G.edgeSet) (r : V) :
    rootLabels G Q r ⊆ G.neighborFinset r := filter_subset _ _

theorem rootLabels_card (Q : Finset G.edgeSet) (r : V) :
    (rootLabels G Q r).card = (edgeIncidences G Q r).card := by
  classical
  symm
  let other := fun (e : G.edgeSet) (he : e ∈ edgeIncidences G Q r) =>
    Sym2.Mem.other ((mem_filter.mp he).2)
  have hs (e : G.edgeSet) (he : e ∈ edgeIncidences G Q r) :
      s(r, other e he) = e.val := Sym2.other_spec _
  apply card_bij other
  · intro e he
    exact mem_filter.mpr ⟨(G.mem_neighborFinset r _).mpr (G.mem_edgeSet.mp (hs e he ▸ e.property)),
      e, (mem_filter.mp he).1, (hs e he).symm⟩
  · intro e he f hf hef
    exact Subtype.ext ((hs e he).symm.trans (by rw [hef]; exact hs f hf))
  · intro a ha
    obtain ⟨_, e, heQ, hea⟩ := mem_filter.mp ha
    have he : e ∈ edgeIncidences G Q r :=
      mem_filter.mpr ⟨heQ, hea.symm ▸ Sym2.mem_mk_left r a⟩
    exact ⟨e, he, Sym2.congr_right.mp ((hs e he).trans hea)⟩

/-- A four-cycle through an oriented edge `u-v` is represented by its
ordered opposite edge `(x,y)`, with `x` on the `u` side and `y` on the `v` side. -/
def fourCycleOpposites (u v : V) : Finset (V × V) :=
  (((G.neighborFinset u).erase v) ×ˢ ((G.neighborFinset v).erase u)).filter
    (fun p => G.Adj p.1 p.2)

theorem fourCycleOpposites_card_eq_root_load (r a : V) :
    (fourCycleOpposites G r a).card =
      ∑ x ∈ (G.neighborFinset a).erase r, ((rootType G r x).erase a).card := by
  have ht (x : V) : (rootType G r x).erase a =
      ((G.neighborFinset r).erase a).filter (G.Adj x) := by
    ext b
    simp [rootType, and_assoc]
  simp only [fourCycleOpposites, ht, card_eq_sum_ones, sum_filter, sum_product]
  rw [sum_comm]
  apply sum_congr rfl
  intro x hx
  apply sum_congr rfl
  intro b hb
  simp only [G.adj_comm b x]


end PaperRoute.Library
