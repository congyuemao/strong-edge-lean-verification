from pathlib import Path
P=Path(__file__).resolve().parent/'lean'/'PaperRoute'
B=P/'Library'/'Bounds'
s=(B/'High20Outer.lean').read_text(encoding='utf-8')
body=s[s.index('  let O :='):s.index('\nend PaperRoute.Library')]
body=body[body.index('  have hP :'):]
body=body.replace('    obtain ⟨heo, hxe⟩ := mem_filter.mp he','    have heo := hO he')
body=body.replace('  obtain ⟨heo, hxe⟩ := mem_filter.mp heO','  have heo := hO heO')
body='\n'.join(l for l in body.splitlines() if not l.startswith('    have hux :') and not l.startswith('    have hvx :'))
body=body.replace('have hu := ht u hends.2.1 hux','have hu := ht e he u (hev ▸ Sym2.mem_mk_left u v)')
body=body.replace('have hv := ht v hends.2.2.1 hvx','have hv := ht e he v (hev ▸ Sym2.mem_mk_right u v)')
body=body.replace('(mem_filter.mp (mem_filter.mp he).1).1','(mem_filter.mp (hO he)).1')
body=body.replace('(mem_filter.mp (mem_filter.mp hf).1).1','(mem_filter.mp (hO hf)).1')
body=body.replace('have hu := ht u (mem_filter.mp huP).2.1 (fun h => hxe (hev ▸ h ▸ Sym2.mem_mk_left u v))',
                  'have hu := ht e heO u (hev ▸ Sym2.mem_mk_left u v)')
body=body.replace('have hv := ht v (mem_filter.mp hvP).2.1 (fun h => hxe (hev ▸ h ▸ Sym2.mem_mk_right u v))',
                  'have hv := ht e heO v (hev ▸ Sym2.mem_mk_right u v)')
header='''module
public import PaperRoute.Library.Bounds.High21RootFour
@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

/-- The full arbitrary-subset statement of manuscript Lemma 3.5. -/
theorem outer_subset_card_le_four
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (conflictGraph G).IsClique (Q : Set G.edgeSet))
    (r : V) (hR : (rootLabels G Q r).card = 4)
    (hN : G.IsIndepSet (G.neighborSet r))
    (O : Finset G.edgeSet) (hO : O ⊆ outerEdges G Q r)
    (ht : ∀ e ∈ O, ∀ x ∈ e.val, (rootType G r x).card ≤ 2) :
    O.card ≤ 4 := by
'''
(P/'OuterSubsets.lean').write_text(header+body+'\n\nend PaperRoute\n',encoding='utf-8')
# Route the unique-triple case through the general manuscript lemma.
s=s[:s.index('  let O :=')]+'''  apply PaperRoute.outer_subset_card_le_four G hΔ Q hQ r hR hN _
    (filter_subset _ _)
  intro e he y hy
  obtain ⟨heo, hxe⟩ := mem_filter.mp he
  exact ht y (fun h => (mem_filter.mp heo).2.1 (h ▸ hy))
    (fun h => hxe (h ▸ hy))

end PaperRoute.Library
'''
s=s.replace('public import PaperRoute.Library.Bounds.High20Local',
            'public import PaperRoute.Library.Bounds.High20Local\npublic import PaperRoute.OuterSubsets')
(B/'High20Outer.lean').write_text(s,encoding='utf-8')
s=(P/'Thresholds.lean').read_text(encoding='utf-8')
s=s.replace('  have ho := outer_card_le_four_of_double_types G hΔ Q hQ r hR hN ht',
'''  have ho := outer_subset_card_le_four G hΔ Q hQ r hR hN
    (outerEdges G Q r) (Subset.refl _) (fun e he x hx =>
      ht x (fun h => (mem_filter.mp he).2.1 (h ▸ hx)))''')
(P/'Thresholds.lean').write_text(s,encoding='utf-8')
print('Added full arbitrary-subset Lemma 3.5 and used it in both applications.')
