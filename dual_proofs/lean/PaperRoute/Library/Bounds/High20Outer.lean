module

public import PaperRoute.Library.Bounds.High20Local
public import PaperRoute.OuterSubsets

@[expose] public section

namespace PaperRoute.Library

open Finset
open scoped BigOperators

variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

theorem outer_avoiding_card_le_four_of_other_types_le_two
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (r : V) (hR : (rootLabels G Q r).card = 4)
    (hN : G.IsIndepSet (G.neighborSet r))
    (x : V) (ht : ∀ y, y ≠ r → y ≠ x → (rootType G r y).card ≤ 2) :
    ((outerEdges G Q r).filter (fun e => x ∉ e.val)).card ≤ 4 := by
  apply PaperRoute.outer_subset_card_le_four G hΔ Q hQ r hR hN _
    (filter_subset _ _)
  intro e he y hy
  obtain ⟨heo, hxe⟩ := mem_filter.mp he
  exact ht y (fun h => (mem_filter.mp heo).2.1 (h ▸ hy))
    (fun h => hxe (h ▸ hy))

end PaperRoute.Library
