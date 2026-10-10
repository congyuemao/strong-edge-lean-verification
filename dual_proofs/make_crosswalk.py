from pathlib import Path
import csv,json,re
D=Path(__file__).resolve().parent
P=D/'lean'
rows=[]
def add(ref,claim,a,b,note=''):
    rows.append({'paper_ref':ref,'claim':claim,'route_a':a.split(),
                 'route_b':b.split(),'difference':note})
def lib(names): return ' '.join('PaperRoute.Library.'+n for n in names.split())
def orig(names): return ' '.join('StrongEdge.'+n for n in names.split())
def common(ref,claim,names,note=''): add(ref,claim,lib(names),orig(names),note)
add('1.1','Prescribed-edge packing','PaperRoute.induced_matching_packing20','StrongEdge.induced_matching_packing20')
add('1 definitions','Independent endpoint semantics','PaperRoute.Semantics.conflict_iff_direct PaperRoute.Semantics.inducedMatching_iff_endpoints',
    'IndependentAudit.conflict_iff_direct IndependentAudit.inducedMatching_iff_endpoints')
add('2.1 / (2.1)','Cover identity / one-sided inequality',
    'PaperRoute.conflict_iff_meets_cover PaperRoute.conflict_degree_add_inside_eq_sum PaperRoute.conflict_degree_eq_sum_sub_inside',
    orig('strongConflict_meets_cover conflict_degree_add_inside_le_sum'),'A proves equality; B uses inclusion and inequality.')
common('2.1 / (2.2)','Selected clique cover','clique_card_le_one_add_incidence_sum')
common('2.2','Degree at most 24','conflict_degree_le_24')
add('2.2','Triangle and arbitrary-threshold slack','PaperRoute.degree_le_twenty_of_triangle PaperRoute.inside_cover_budget',
    orig('endpointNeighbourCover_card_le_five_of_triangle high20_triangle_cover_inside_empty high21_endpoints_degree_four high21_no_triangle_on_edge'),
    'B obtains the remaining slack cases in specialized local modules.')
common('2.3','Selected degree two bound 13','clique_card_le_thirteen_of_support_degree_le_two')
common('2.3','Selected degree three bound 18','clique_card_le_eighteen_of_support_degree_le_three')
common('2.4','Restricted degree-two clique bounds','degree_two_clique_card_le_five degree_two_clique_card_le_four_of_selected_bipartition',
       'The code uses restricted original-neighbour covers; A prose describes the equivalent vertex-induced graph.')
add('(3.1)','Star/root/outer partition',
    'PaperRoute.selected_card_eq_star_root_outer PaperRoute.root_incidence_eq_star_add_root',
    orig('clique_card_le_star_root_outer star_add_root_card_le_label_sum'),'A states two exact identities; B exposes covering inequalities.')
common('(3.2)','Meeting and outer covering','selected_edges_card_le_meeting_add_outer incidence_sum_eq_meeting_add_inside')
common('3.1 / (3.3)','Every outer edge covers all selected root labels','outer_edge_types_cover_root_labels')
common('3.1 / (3.4)','Outer incidence plus type degree','outer_incidence_add_type_card_le_degree')
add('3.1 / (3.4)','Multiple-type incidence capacity','PaperRoute.multiple_type_sum_le_three_neighbors',
    orig('multipleTips_type_sum_le_twelve multipleTips_card_le_six'),'A keeps 3|A| before specializing to 12.')
add('3.1 / (3.5)','Load budgets','PaperRoute.root_load_budget_disjoint PaperRoute.root_load_budget',
    orig('high23_at_most_one_four_cycle_on_edge fourCycleOpposites_card_eq_root_load high22_root_label_budget_two high21_root_label_budget_three high20_root_label_budget_four'),
    'A parameterizes t; B has separate thresholds and an ordered-pair uniqueness proof at 23.')
common('3.2','Independent four-element root neighbourhood','high21_root_degree_four high21_root_neighborhood_independent')
common('3.3','Singleton controls tips','rootTips_adj_of_single rootTips_card_le_six_of_single')
common('3.4','At most four fully selected doubles','fullDoubleTips_card_le_four')
add('3.5','Complementary-double outer families','PaperRoute.outer_subset_card_le_four',
    orig('outer_card_le_four_of_double_types outer_avoiding_card_le_four_of_other_types_le_two'),
    'A proves the arbitrary-subset version; B states precisely the two original special cases.')
add('3.6','Threshold-free small-type bound 18','PaperRoute.small_type_clique_bound',
    orig('clique_card_le_eighteen_of_independent_root_types_le_two'))
for i,t,bound in [(2,24,'thirteen'),(3,23,'sixteen'),(4,22,'seventeen'),(5,21,'eighteen'),(6,20,'nineteen')]:
    add('4.'+str(i),f'Universal threshold {t} clique bound',f'PaperRoute.proposition_4_{i}',
        f'StrongEdge.high{t}_clique_card_le_{bound}')
common('4.4, three selected labels','Heavy-vertex equality exclusion',
       'high22_labelHeavyTips_card_le_three high22_heavy_card_and_degree_of_outer_six high22_multiple_subset_heavy_of_three')
add('4.5, small types','Small-type branch at threshold 21','PaperRoute.small_type_clique_bound',
    orig('high21_multipleTips_card_le_six high21_clique_card_le_eighteen_of_root_types_le_two'),
    'A reuses the threshold-free lemma; B counts multiple vertices from the high21 loads.')
add('4.6, type four','Four-element-type branch',
    'PaperRoute.outer_card_le_one_of_type_four PaperRoute.clique_card_le_seventeen_of_type_four',
    orig('high20_outer_card_le_two_of_root_type_four high20_clique_card_le_eighteen_of_root_type_four'),
    'A exposes o<=1 and q<=17; B exposes o<=2 and q<=18, although its proof internally bounds the avoiding family by one.')
common('4.6, two triples','Two-triple branch','high20_clique_card_le_eighteen_of_two_triples')
common('4.6, unique triple','Unique-triple branch','clique_card_le_nineteen_of_unique_triple')
common('5.1','Optimal independent set and exchanges','optimal_exists private_isClique private_degree_mono private_centre')
add('5.1 definition','Private-set semantics','PaperRoute.private_iff_closed_intersection',
    orig('private_iff_covering_singleton'),'The original covering predicate is the same closed-neighbourhood relation.')
common('5.2','Private double count','private_double_count')
add('5.3','Twenty-packing criterion','PaperRoute.local20_of_minimal_clique_bounds PaperRoute.packing20_of_minimal_clique_bounds',
    orig('local20_of_minimal_clique_bounds packing20_of_minimal_clique_bounds'))
add('Proof of 1.1','Induced-subgraph transfer','PaperRoute.minimalCliqueBounds20_induce PaperRoute.subset_packing20_of_minimal_clique_bounds',
    orig('minimalCliqueBounds20_induce subset_packing20_of_minimal_clique_bounds'))
add('6.1','Doubled-cycle witness','PaperRoute.Sharpness.doubleC5_degree_four PaperRoute.Sharpness.doubleC5_twenty_edges PaperRoute.Sharpness.doubleC5_matching_card_le_one',
    'IndependentAudit.Regression.doubleC5_degree_four IndependentAudit.Regression.doubleC5_twenty_edges IndependentAudit.Regression.doubleC5_matching_card_le_one')
add('6.1','Optimality against any real constant','PaperRoute.Sharpness.twenty_is_necessary_real',
    'OriginalSharpness.twenty_is_necessary_real','Both sharpness endpoints are supplemental; original 49 source/config files remain unchanged.')

files=list(P.rglob('*.lean'))
files=[p for p in files if '.lake' not in p.parts]
declmap={}
for p in files:
    text=p.read_text(encoding='utf-8')
    namespaces=[]
    for i,line in enumerate(text.splitlines(),1):
        m=re.match(r'namespace\s+([\w.]+)',line)
        if m:namespaces.append(m[1])
        m=re.match(r'(?:@\[[^\]]+\]\s*)?(?:theorem|def|structure)\s+(\w+)',line)
        if m:declmap['.'.join(namespaces+[m[1]])]={'file':str(p.relative_to(P)).replace('\\','/'),'line':i}
        if line.startswith('end ') and namespaces:namespaces.pop()
for r in rows:
    for key in ['route_a','route_b']:
        r[key+'_locations']=[declmap[n] for n in r[key]]
(D/'proof_crosswalk.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (D/'proof_crosswalk.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['paper_ref','claim','route_a_declarations','route_a_locations','route_b_declarations','route_b_locations','difference'])
    for r in rows:
        writer.writerow([r['paper_ref'],r['claim'],'; '.join(r['route_a']),
            '; '.join(f"{x['file']}:{x['line']}" for x in r['route_a_locations']),
            '; '.join(r['route_b']),'; '.join(f"{x['file']}:{x['line']}" for x in r['route_b_locations']),r['difference']])
for route in ['a','b']:
    decls=sorted({n for r in rows for n in r['route_'+route]})
    imports='import PaperRoute\n' if route=='a' else 'import OriginalSharpness\n'
    (P/f'Crosswalk{route.upper()}.lean').write_text(imports+'\n'+'\n'.join('#check '+n for n in decls)+'\n',encoding='utf-8')
print(f'{len(rows)} crosswalk rows; all declaration source locations resolved.')
