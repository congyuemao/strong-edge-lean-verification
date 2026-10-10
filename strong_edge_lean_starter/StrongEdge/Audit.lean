module

public import StrongEdge

#print axioms StrongEdge.strongConflict_symm
#print axioms StrongEdge.candidate_independent_iff
#print axioms StrongEdge.candidate_degree_le_full
#print axioms StrongEdge.private_isClique
#print axioms StrongEdge.optimal_exists
#print axioms StrongEdge.private_degree_mono
#print axioms StrongEdge.private_double_count
#print axioms StrongEdge.packing_of_local_bound
#print axioms StrongEdge.packing20_of_thresholds
#print axioms StrongEdge.subset_packing20_of_thresholds
#print axioms StrongEdge.induced_matching_packing20_of_thresholds
#print axioms StrongEdge.Tests.path_outer_edges_conflict
#print axioms StrongEdge.Tests.separated_outer_edges_do_not_conflict

#print axioms StrongEdge.endpointNeighbourCover_comm
#print axioms StrongEdge.incident_edge_meets_cover
#print axioms StrongEdge.lineGraph_adj_meets_cover
#print axioms StrongEdge.left_notMem_endpointNeighbourCover
#print axioms StrongEdge.right_notMem_endpointNeighbourCover
#print axioms StrongEdge.strongConflict_meets_cover
#print axioms StrongEdge.conflict_neighbors_subset_incidence_cover
#print axioms StrongEdge.conflict_degree_le_incidence_cover_card
#print axioms StrongEdge.conflict_degree_le_incidence_sum
#print axioms StrongEdge.endpointNeighbourCover_card_le_six
#print axioms StrongEdge.conflict_degree_le_24

#print axioms StrongEdge.endpointNeighbourCover_card_eq_six_of_degree_eq_24
#print axioms StrongEdge.endpoint_degrees_eq_four_of_degree_eq_24
#print axioms StrongEdge.cover_degree_eq_four_of_degree_eq_24
#print axioms StrongEdge.cover_independent_of_degree_eq_24
#print axioms StrongEdge.other_neighbor_sets_disjoint_of_degree_eq_24
#print axioms StrongEdge.endpoint_neighbor_sets_disjoint_of_degree_eq_24
#print axioms StrongEdge.endpoint_neighborhood_independent_of_degree_eq_24
#print axioms StrongEdge.no_cross_edge_of_degree_eq_24

#print axioms StrongEdge.minimalCliqueBounds20_of_thresholds
#print axioms StrongEdge.local20_of_minimal_clique_bounds
#print axioms StrongEdge.packing20_of_minimal_clique_bounds
#print axioms StrongEdge.minimalCliqueBounds20_induce
#print axioms StrongEdge.subset_packing20_of_minimal_clique_bounds
#print axioms StrongEdge.induced_matching_packing20_of_minimal_clique_bounds

#print axioms StrongEdge.conflict_degree_eq_24_of_ge
#print axioms StrongEdge.mem_branchEdges
#print axioms StrongEdge.high24_edge_not_between_neighbors
#print axioms StrongEdge.high24_external_conflict_adj
#print axioms StrongEdge.high24_distinct_branches_ne
#print axioms StrongEdge.high24_mixed_branches_cannot_have_fork
#print axioms StrongEdge.branchEdges_card_le_three
#print axioms StrongEdge.high24_branch_union_card_le_three
#print axioms StrongEdge.high24_side_card_le_three
#print axioms StrongEdge.high24_clique_card_le_thirteen
#print axioms StrongEdge.high24_clique_card_le_fifteen
#print axioms StrongEdge.minimalCliqueBounds20_of_high20_high21_high22_high23
#print axioms StrongEdge.induced_matching_packing20_of_high20_high21_high22_high23

#check StrongEdge.packing20_of_thresholds
#check StrongEdge.induced_matching_packing20_of_thresholds
#check StrongEdge.conflict_degree_le_24
#check StrongEdge.induced_matching_packing20_of_minimal_clique_bounds
#check StrongEdge.high24_clique_card_le_thirteen
#check StrongEdge.high24_clique_card_le_fifteen
#check StrongEdge.minimalCliqueBounds20_of_high20_high21_high22_high23
#check StrongEdge.induced_matching_packing20_of_high20_high21_high22_high23

#print axioms StrongEdge.card_le_via_relation
#print axioms StrongEdge.edgeIncidences_univ_card
#print axioms StrongEdge.edgeIncidences_card_le_degree
#print axioms StrongEdge.edge_endpoint_count
#print axioms StrongEdge.incidence_sum_eq_meeting_add_inside
#print axioms StrongEdge.conflict_degree_add_inside_le_sum
#print axioms StrongEdge.clique_card_le_one_add_incidence_sum
#print axioms StrongEdge.clique_card_le_thirteen_of_support_degree_le_two

#print axioms StrongEdge.high23_cover_card_eq_six
#print axioms StrongEdge.high23_endpoints_degree_four
#print axioms StrongEdge.high23_other_neighbor_sets_disjoint
#print axioms StrongEdge.high23_no_triangle_on_edge
#print axioms StrongEdge.high23_cover_inside_card_le_one
#print axioms StrongEdge.high23_cross_edges_unique
#print axioms StrongEdge.high23_at_most_one_four_cycle_on_edge

#print axioms StrongEdge.mem_rootType
#print axioms StrongEdge.rootLabels_subset_neighbors
#print axioms StrongEdge.rootLabels_card
#print axioms StrongEdge.high23_root_degree_four
#print axioms StrongEdge.high23_root_neighborhood_independent
#print axioms StrongEdge.high23_root_cross_unique
#print axioms StrongEdge.high23_type_meets_root_labels
#print axioms StrongEdge.high23_root_type_card_le_two
#print axioms StrongEdge.high23_double_type_unique
#print axioms StrongEdge.high23_type_singleton_of_sharing_double

#print axioms StrongEdge.outerEdges_endpoints
#print axioms StrongEdge.outer_edge_types_cover_root_labels
#print axioms StrongEdge.high23_outer_edges_incident_double_root
#print axioms StrongEdge.high23_outer_card_le_two_of_double_root_type
#print axioms StrongEdge.high23_outer_edges_card_le_two
#print axioms StrongEdge.selected_edges_card_le_meeting_add_outer
#print axioms StrongEdge.high23_clique_card_le_fourteen_of_support_degree_le_three

#print axioms StrongEdge.root_edge_tip_not_neighbor
#print axioms StrongEdge.root_single_edges_outer_adj
#print axioms StrongEdge.high23_singleTips_card_le_six
#print axioms StrongEdge.singleRootEdges_card_le_singleTips
#print axioms StrongEdge.high23_doubleRootEdges_card_le_four

#print axioms StrongEdge.meeting_edges_subset_root_single_double
#print axioms StrongEdge.high23_meeting_card_le_fourteen_of_root_four
#print axioms StrongEdge.high23_clique_card_le_sixteen_of_root_four
#print axioms StrongEdge.high23_clique_card_le_sixteen

#print axioms StrongEdge.minimalCliqueBounds20_of_high20_high21_high22
#print axioms StrongEdge.induced_matching_packing20_of_high20_high21_high22
#check StrongEdge.high23_cover_inside_card_le_one
#check StrongEdge.high23_at_most_one_four_cycle_on_edge
#check StrongEdge.high23_clique_card_le_sixteen
#check StrongEdge.minimalCliqueBounds20_of_high20_high21_high22
#check StrongEdge.induced_matching_packing20_of_high20_high21_high22

#print axioms StrongEdge.high22_cover_card_eq_six
#print axioms StrongEdge.high22_endpoints_degree_four
#print axioms StrongEdge.high22_other_neighbor_sets_disjoint
#print axioms StrongEdge.high22_no_triangle_on_edge
#print axioms StrongEdge.high22_cover_inside_card_le_two
#print axioms StrongEdge.high22_at_most_two_four_cycles_on_edge

#print axioms StrongEdge.root_single_edge_outer_adj
#print axioms StrongEdge.rootTips_adj_of_single
#print axioms StrongEdge.rootTips_card_le_six_of_single
#print axioms StrongEdge.rootEdges_card_le_tip_weight
#print axioms StrongEdge.clique_card_le_star_root_outer
#print axioms StrongEdge.outer_incidence_add_type_card_le_degree

#print axioms StrongEdge.high22_root_degree_four
#print axioms StrongEdge.high22_root_neighborhood_independent
#print axioms StrongEdge.fourCycleOpposites_card_eq_root_load
#print axioms StrongEdge.high22_root_label_budget_two
#print axioms StrongEdge.high22_root_type_erase_card_le_two
#print axioms StrongEdge.high22_root_type_card_le_three
#print axioms StrongEdge.high22_root_label_multiple_card_le_two
#print axioms StrongEdge.high22_shared_root_types_card_le_four
#print axioms StrongEdge.root_type_card_sum_eq_label_sum
#print axioms StrongEdge.high22_multipleTips_card_le_four
#print axioms StrongEdge.high22_multipleTips_eq_of_triple

#print axioms StrongEdge.high22_clique_card_le_seventeen_of_root_triple
#print axioms StrongEdge.outer_endpoints_multiple_of_root_four
#print axioms StrongEdge.outer_incidence_sum_eq_twice
#print axioms StrongEdge.high22_outer_card_le_four_of_root_types_le_two
#print axioms StrongEdge.rootEdges_card_le_tips_add_multiple
#print axioms StrongEdge.rootEdges_card_le_twice_multiple_of_no_single
#print axioms StrongEdge.high22_outer_degree_eq_two_of_four
#print axioms StrongEdge.outer_saturated_neighbors
#print axioms StrongEdge.high22_active_multiple_card_le_two_of_outer_four
#print axioms StrongEdge.high22_clique_card_le_seventeen_of_root_four

#print axioms StrongEdge.labelHeavyTips_subset_multiple
#print axioms StrongEdge.root_type_inter_card_sum
#print axioms StrongEdge.outerEdges_meet_labelHeavyTips
#print axioms StrongEdge.high22_heavy_label_card_le_two
#print axioms StrongEdge.high22_labelHeavyTips_card_le_three
#print axioms StrongEdge.high22_outer_incidence_le_two_at_heavy
#print axioms StrongEdge.high22_outer_card_le_six_of_root_three
#print axioms StrongEdge.high22_heavy_card_and_degree_of_outer_six
#print axioms StrongEdge.high22_heavy_label_card_eq_two_of_three
#print axioms StrongEdge.high22_multiple_subset_heavy_of_three

#print axioms StrongEdge.root_outer_incidence_add_le
#print axioms StrongEdge.root_incidence_at_tip_le_type
#print axioms StrongEdge.rootEdges_card_le_tips_of_incidence_le_one
#print axioms StrongEdge.rootTips_subset_multiple_of_no_single
#print axioms StrongEdge.high22_clique_card_le_seventeen_of_support_degree_le_three

#print axioms StrongEdge.high22_clique_card_le_seventeen

#print axioms StrongEdge.minimalCliqueBounds20_of_high20_high21
#print axioms StrongEdge.induced_matching_packing20_of_high20_high21
#check StrongEdge.high22_cover_inside_card_le_two
#check StrongEdge.high22_at_most_two_four_cycles_on_edge
#check StrongEdge.high22_root_label_budget_two
#check StrongEdge.high22_clique_card_le_seventeen_of_root_four
#check StrongEdge.high22_clique_card_le_seventeen_of_support_degree_le_three
#check StrongEdge.high22_clique_card_le_seventeen
#check StrongEdge.minimalCliqueBounds20_of_high20_high21
#check StrongEdge.induced_matching_packing20_of_high20_high21
