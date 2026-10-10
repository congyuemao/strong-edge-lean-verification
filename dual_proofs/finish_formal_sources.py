from pathlib import Path
P=Path(__file__).resolve().parent/'lean'
A=P/'PaperRoute'
s=(P/'StrongEdge'/'MinimalPacking.lean').read_text(encoding='utf-8')
s=s.replace('StrongEdge','PaperRoute')
s=s.replace('public import PaperRoute.Packing\npublic import PaperRoute.Bounds.ConflictDegree','public import PaperRoute.Thresholds\npublic import PaperRoute.Library.Packing')
s=s.replace('open Finset','open PaperRoute.Library Finset')
a=s.index('omit [DecidableEq W] in\ntheorem minimalCliqueBounds20_of_thresholds')
b=s.index('theorem local20_of_minimal_clique_bounds',a)
s=s[:a]+s[b:]
s=s.replace('MinimalCliqueBounds20','CliqueProfile20')
s=s.replace('induced_matching_packing20_of_minimal_clique_bounds','packing_from_profile')
s=s[:s.index('\nend PaperRoute')]+'''

/-- Theorem 4.1, assembled from the manuscript's five propositions. -/
theorem manuscript_profile
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) : CliqueProfile20 (conflictGraph G) where
  high20 := proposition_4_6 G hΔ
  high21 := proposition_4_5 G hΔ
  high22 := proposition_4_4 G hΔ
  high23 := proposition_4_3 G hΔ
  high24 Q hQ ht := (proposition_4_2 G hΔ Q hQ ht).trans (by omega)

/-- Manuscript Theorem 1.1. No StrongEdge declaration is imported here. -/
theorem induced_matching_packing20
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧ IsInducedMatching G (M : Set G.edgeSet) ∧
      F.card ≤ 20 * M.card :=
  packing_from_profile G hΔ (manuscript_profile G hΔ) F

end PaperRoute
'''
(A/'Packing.lean').write_text(s,encoding='utf-8')

s=(P/'AuditSemantic.lean').read_text(encoding='utf-8')
s=s.replace('import StrongEdge','module\npublic import PaperRoute.Packing\n\n@[expose] public section',1)
s=s.replace('StrongEdge','PaperRoute.Library').replace('IndependentAudit','PaperRoute.Semantics')
s=s.replace('PaperRoute.Library.induced_matching_packing20','PaperRoute.induced_matching_packing20')
s=s[:s.index('\n#check')]
(A/'Semantics.lean').write_text(s,encoding='utf-8')

s=(P/'AuditRegression.lean').read_text(encoding='utf-8')
s=s[s.index('def doubleC5'):s.index('theorem empty_graph_packing')]
s=s.replace('StrongEdge','PaperRoute.Library').replace('IndependentAudit','PaperRoute.Semantics')
s='''module
public import PaperRoute.Semantics
public import Mathlib.Data.Real.Basic
@[expose] public section
namespace PaperRoute.Sharpness

'''+s+'''
/-- The manuscript claims sharpness against arbitrary real constants. -/
theorem twenty_is_necessary_real (c : ℝ)
    (h : ∃ M : Finset doubleC5.edgeSet,
      PaperRoute.Library.IsInducedMatching doubleC5 (M : Set doubleC5.edgeSet) ∧
      (Fintype.card doubleC5.edgeSet : ℝ) ≤ c * (M.card : ℝ)) : 20 ≤ c := by
  obtain ⟨M, hm, hc⟩ := h
  have hn := doubleC5_matching_card_le_one M hm
  rw [doubleC5_twenty_edges] at hc
  have hp : M.card ≠ 0 := by
    intro hz
    simp only [hz, Nat.cast_zero, mul_zero] at hc
    norm_num at hc
  have he : M.card = 1 := by omega
  simpa only [he, Nat.cast_one, mul_one] using hc

end PaperRoute.Sharpness
'''
(A/'Sharpness.lean').write_text(s,encoding='utf-8')

(A/'PrivateSemantics.lean').write_text('''module
public import PaperRoute.Packing
@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
variable {W : Type*} [Fintype W] [DecidableEq W]
variable (H : SimpleGraph W) [DecidableRel H.Adj]

/-- Exact translation of the manuscript's closed-neighbourhood definition. -/
theorem private_iff_closed_intersection (I : Finset W) {v x : W} (hv : v ∈ I) :
    IsPrivate H I v x ↔ I.filter (fun w => x = w ∨ H.Adj x w) = {v} := by
  constructor
  · intro h
    ext w
    simp only [mem_filter, mem_singleton]
    constructor
    · rintro ⟨hw, hc⟩
      by_contra hwv
      exact hc.elim (h.2 w hw hwv).1 (h.2 w hw hwv).2
    · intro hwv
      subst w
      exact ⟨hv, h.1⟩
  · intro h
    have hh : v ∈ I.filter (fun w => x = w ∨ H.Adj x w) := by rw [h]; simp
    refine ⟨(mem_filter.mp hh).2, ?_⟩
    intro w hw hwv
    have hn : ¬ (x = w ∨ H.Adj x w) := by
      intro hc
      have hh := mem_filter.mpr ⟨hw, hc⟩
      rw [h] at hh
      exact hwv (mem_singleton.mp hh)
    exact ⟨fun hx => hn (Or.inl hx), fun hx => hn (Or.inr hx)⟩

end PaperRoute
''',encoding='utf-8')
(P/'PaperRoute.lean').write_text('''module
public import PaperRoute.Packing
public import PaperRoute.PrivateSemantics
public import PaperRoute.Sharpness
''',encoding='utf-8')
print('Created packing, semantic, and real-sharpness endpoints.')
