from pathlib import Path
P = Path(__file__).resolve().parent / 'lean' / 'PaperRoute'
B = P / 'Library' / 'Bounds'
def read(p): return p.read_text(encoding='utf-8')
def write(p,s): p.write_text(s,encoding='utf-8')
def cut(s,a,b): return s[s.index(a):s.index(b)]
def body(s,name,new):
    start=s.index('theorem '+name)
    a=s.index(':= by',start)+len(':= by')
    b=s.find('\ntheorem ',a)
    e=s.find('\nend ',a)
    if b<0 or (e>=0 and e<b): b=e
    # Preserve documentation belonging to the next theorem.
    doc=s.find('\n/--',a)
    if doc>=0 and doc<b: b=doc
    return s[:a]+'\n'+new.rstrip()+'\n'+s[b:]

f=read(P/'Foundations.lean')
f=f.replace('rcases hwe with rfl | rfl\n    · exact left_notMem_endpointNeighbourCover G u v hw\n    · exact right_notMem_endpointNeighbourCover G u v hw',
'''rcases hwe with hwu | hwv
    · exact left_notMem_endpointNeighbourCover G u v (hwu ▸ hw)
    · exact right_notMem_endpointNeighbourCover G u v (hwv ▸ hw)''')
header='''module

public import PaperRoute.Library.Bounds.EdgeCounting

@[expose] public section
namespace PaperRoute
open PaperRoute.Library Finset
open scoped BigOperators
variable {V : Type*} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

'''
cover=cut(f,'/-- Reverse implication','theorem degree_le_twenty_of_triangle')
write(P/'ExactCover.lean',header+cover+'\nend PaperRoute\n')

s23=read(B/'High23Support.lean')
defs=cut(s23,'def rootLabels','variable [DecidableRel (conflictGraph G).Adj]')
s23=s23.replace(defs,'')
write(B/'High23Support.lean',s23)
l23=read(B/'High23Local.lean')
cycles=cut(l23,'/-- A four-cycle through an oriented edge','theorem high23_at_most_one_four_cycle_on_edge')
l23=l23.replace(cycles,'').replace('public import PaperRoute.Library.Bounds.EdgeCounting','public import PaperRoute.UniformLoad')
s22=read(B/'High22Support.lean')
eqload=cut(s22,'omit [DecidableRel (conflictGraph G).Adj] in\ntheorem fourCycleOpposites_card_eq_root_load','/-- The cross-edge part')
s22=s22.replace(eqload,'')
primitive=header.replace('PaperRoute.Library.Bounds.EdgeCounting','PaperRoute.ExactCover').replace('namespace PaperRoute\n','namespace PaperRoute.Library\n').replace('open PaperRoute.Library Finset','open Finset')
eqload=eqload.replace('omit [DecidableRel (conflictGraph G).Adj] in\n','')
write(P/'RootPrimitives.lean',primitive+defs+cycles+eqload+'\nend PaperRoute.Library\n')

load=cut(f,'/-- Manuscript (3.5)','omit [DecidableRel (conflictGraph G).Adj] in\n/-- The unspecialized')
start=load.index('  obtain ⟨haN, e, heQ, he⟩')
rw=load.index('  rw [← fourCycleOpposites_card_eq_root_load]')
generic=load[:load.index('theorem root_load_budget_sub')]
generic=generic.replace('theorem root_load_budget ','theorem root_load_budget_disjoint ')
generic=generic.replace('(hN : G.IsIndepSet (G.neighborSet r))','(hdis : Disjoint ((G.neighborFinset r).erase a) ((G.neighborFinset a).erase r))')
generic=generic[:generic.index('  obtain ⟨haN, e, heQ, he⟩')]+'  obtain ⟨_, e, heQ, he⟩ := mem_filter.mp ha\n'+generic[generic.index('  rw [← fourCycleOpposites_card_eq_root_load]'):]
wrapper=load[:start]+load[start:rw]+'''  exact root_load_budget_disjoint G hΔ Q ht hdis ha

'''+load[load.index('theorem root_load_budget_sub'):]
loadheader=header.replace('PaperRoute.Library.Bounds.EdgeCounting','PaperRoute.RootPrimitives')+'variable [DecidableRel (conflictGraph G).Adj]\n\n'
write(P/'UniformLoad.lean',loadheader+generic+wrapper+'\nend PaperRoute\n')

# The specialized interfaces now instantiate the single, exact budget proof.
l23=body(l23,'high23_cover_inside_card_le_one',
'''  have := PaperRoute.inside_cover_budget G hΔ e he h23
  omega''')
write(B/'High23Local.lean',l23)
for t,name,s in [(22,'High22Support.lean',s22),(21,'High21Support.lean',read(B/'High21Support.lean'))]:
    word={22:'two',21:'three'}[t]
    s=body(s,f'high{t}_root_label_budget_{word}',f'''  obtain ⟨_, e, heQ, he⟩ := mem_filter.mp ha
  have hd := high{t}_other_neighbor_sets_disjoint G hΔ e he (h{t} e heQ)
  have hb := PaperRoute.root_load_budget_disjoint G hΔ Q h{t} hd ha
  omega''')
    write(B/name,s)
s=read(B/'High20Local.lean')
s=body(s,'high20_root_label_budget_four',
'''  have := PaperRoute.root_load_budget G hΔ Q h20 hN ha
  omega''')
write(B/'High20Local.lean',s)

# Keep the exact root-partition and triangle statements in the later module.
f=f[:f.index('/-- Reverse implication')]+f[f.index('theorem degree_le_twenty_of_triangle'):]
a=f.index('/-- Manuscript (3.5)')
b=f.index('omit [DecidableRel (conflictGraph G).Adj] in\n/-- The unspecialized')
f=f[:a]+f[b:]
f=f.replace('theorem degree_le_twenty_of_triangle','variable [DecidableRel (conflictGraph G).Adj]\n\ntheorem degree_le_twenty_of_triangle',1)
write(P/'Foundations.lean',f)

# Assemble fresh manuscript-level propositions; copy only their explicit bodies.
imports=['Foundations','Library.Bounds.High24','Library.Bounds.High23','Library.Bounds.High22']
th=header[:header.index('public import')]+''.join('public import PaperRoute.'+x+'\n' for x in imports)+header[header.index('@[expose]'):]
th+='variable [DecidableRel (conflictGraph G).Adj]\n\n'
s=read(B/'High20Four.lean')
four=cut(s,'theorem high20_outer_card_le_two_of_root_type_four','\nend PaperRoute.Library')
four=four.replace('high20_outer_card_le_two_of_root_type_four','outer_card_le_one_of_type_four').replace('(outerEdges G Q r).card ≤ 2','(outerEdges G Q r).card ≤ 1')
four=four.replace('high20_clique_card_le_eighteen_of_root_type_four','clique_card_le_seventeen_of_type_four').replace('Q.card ≤ 18','Q.card ≤ 17')
th+=four+'\n'
# Generic small-type argument is genuinely shared by the paper's t=20 and t=21 cases.
s=read(B/'High20.lean')
small=cut(s,'theorem clique_card_le_eighteen_of_independent_root_types_le_two','variable [DecidableRel (conflictGraph G).Adj]')
small=small.replace('clique_card_le_eighteen_of_independent_root_types_le_two','small_type_clique_bound')
small=small.replace('have hc := clique_card_le_star_root_outer G Q r','have hc := selected_card_eq_star_root_outer G Q r')
th+='omit [DecidableRel (conflictGraph G).Adj] in\n'+small
for file,start,end,rename in [
('High24.lean','theorem high24_clique_card_le_thirteen','theorem high24_clique_card_le_fifteen','proposition_4_2'),
('High23.lean','theorem high23_clique_card_le_sixteen\n','\nend PaperRoute.Library','proposition_4_3'),
('High22.lean','theorem high22_clique_card_le_seventeen\n','\nend PaperRoute.Library','proposition_4_4')]:
    ss=read(B/file); block=cut(ss,start,end); old=block.split()[1]
    th+=block.replace('theorem '+old,'theorem '+rename,1)+'\n'
# t=21: use the paper's threshold-free small-type lemma.
ss=read(B/'High21RootFour.lean')
block=cut(ss,'theorem high21_clique_card_le_eighteen_of_root_four','\nend PaperRoute.Library')
block=block.replace('theorem high21_clique_card_le_eighteen_of_root_four','theorem paper_high21_root_four',1)
block=block.replace('  apply high21_clique_card_le_eighteen_of_root_types_le_two G hΔ Q hQ h21 r hR',
'''  have hN := high21_root_neighborhood_independent G hΔ Q h21 r (by omega)
  apply small_type_clique_bound G hΔ Q hQ r hR hN''')
th+=block+'\n'
ss=read(B/'High21.lean')
block=cut(ss,'theorem high21_clique_card_le_eighteen\n','\nend PaperRoute.Library')
th+=block.replace('theorem high21_clique_card_le_eighteen','theorem proposition_4_5',1).replace('high21_clique_card_le_eighteen_of_root_four','paper_high21_root_four')+'\n'
ss=read(B/'High20.lean')
block=cut(ss,'theorem high20_clique_card_le_nineteen_of_root_four','\nend PaperRoute.Library')
block=block.replace('high20_clique_card_le_nineteen_of_root_four','paper_high20_root_four').replace('theorem high20_clique_card_le_nineteen\n','theorem proposition_4_6\n')
block=block.replace('high20_clique_card_le_eighteen_of_root_type_four','clique_card_le_seventeen_of_type_four')
block=block.replace('clique_card_le_eighteen_of_independent_root_types_le_two','small_type_clique_bound')
th+=block+'\nend PaperRoute\n'
write(P/'Thresholds.lean',th)
print('Refactored exact cover, uniform load, and manuscript propositions.')
