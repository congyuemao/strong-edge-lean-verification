import StrongEdge
import Lean

open Lean Elab Command in
run_elab do
  for name in (← getEnv).header.moduleNames do
    logInfo m!"AUDIT_IMPORT {name}"

#print StrongEdge.MinimalCliqueBounds20
#check StrongEdge.high20_clique_card_le_nineteen
#print axioms StrongEdge.high20_clique_card_le_nineteen
#check StrongEdge.high21_clique_card_le_eighteen
#print axioms StrongEdge.high21_clique_card_le_eighteen
#check StrongEdge.high22_clique_card_le_seventeen
#print axioms StrongEdge.high22_clique_card_le_seventeen
#check StrongEdge.high23_clique_card_le_sixteen
#print axioms StrongEdge.high23_clique_card_le_sixteen
#check StrongEdge.high24_clique_card_le_thirteen
#print axioms StrongEdge.high24_clique_card_le_thirteen
#check StrongEdge.minimalCliqueBounds20_of_maxDegree_four
#print axioms StrongEdge.minimalCliqueBounds20_of_maxDegree_four
#check StrongEdge.induced_matching_packing20
#print axioms StrongEdge.induced_matching_packing20
