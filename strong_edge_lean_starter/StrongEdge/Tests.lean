module

public import StrongEdge.Basic

/-! The connecting edge 12 must remain a conflict witness even when only 01 and 23
are candidates. All computations below use kernel-checked `decide`. -/

@[expose] public section

namespace StrongEdge.Tests

def path4 : SimpleGraph (Fin 4) where
  Adj x y := x.val + 1 = y.val ∨ y.val + 1 = x.val
  symm := ⟨fun _ _ h => h.symm⟩
  loopless := ⟨by intro x; omega⟩

instance : DecidableRel path4.Adj := fun _ _ => inferInstanceAs (Decidable (_ ∨ _))

def separated : SimpleGraph (Fin 4) where
  Adj x y := (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 0) ∨
    (x = 2 ∧ y = 3) ∨ (x = 3 ∧ y = 2)
  symm := ⟨by intro x y h; tauto⟩
  loopless := ⟨by intro x; omega⟩

instance : DecidableRel separated.Adj := fun _ _ => inferInstanceAs (Decidable (_ ∨ _))

def path01 : path4.edgeSet := ⟨s(0, 1), by decide⟩
def path23 : path4.edgeSet := ⟨s(2, 3), by decide⟩
def sep01 : separated.edgeSet := ⟨s(0, 1), by decide⟩
def sep23 : separated.edgeSet := ⟨s(2, 3), by decide⟩

theorem path_outer_edges_conflict : StrongConflict path4 path01 path23 := by
  simp only [StrongConflict, SimpleGraph.lineGraph_adj_iff_exists]
  decide

theorem separated_outer_edges_do_not_conflict : ¬ StrongConflict separated sep01 sep23 := by
  simp only [StrongConflict, SimpleGraph.lineGraph_adj_iff_exists]
  decide

def candidates : Set path4.edgeSet := {path01, path23}

theorem candidate_outer_edges_adjacent :
    (candidateConflictGraph path4 candidates).Adj
      ⟨path01, by simp [candidates]⟩ ⟨path23, by simp [candidates]⟩ :=
  path_outer_edges_conflict

end StrongEdge.Tests
