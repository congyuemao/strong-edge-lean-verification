module

public import PaperRoute.Library

#print axioms PaperRoute.Library.strongConflict_symm
#print axioms PaperRoute.Library.candidate_independent_iff
#print axioms PaperRoute.Library.candidate_degree_le_full
#print axioms PaperRoute.Library.private_isClique
#print axioms PaperRoute.Library.optimal_exists
#print axioms PaperRoute.Library.private_degree_mono
#print axioms PaperRoute.Library.private_double_count
#print axioms PaperRoute.Library.packing_of_local_bound
#print axioms PaperRoute.Library.packing20_of_thresholds
#print axioms PaperRoute.Library.subset_packing20_of_thresholds
#print axioms PaperRoute.Library.induced_matching_packing20_of_thresholds
#print axioms PaperRoute.Library.Tests.path_outer_edges_conflict
#print axioms PaperRoute.Library.Tests.separated_outer_edges_do_not_conflict

#print axioms PaperRoute.Library.endpointNeighbourCover_comm
#print axioms PaperRoute.Library.incident_edge_meets_cover
#print axioms PaperRoute.Library.lineGraph_adj_meets_cover
#print axioms PaperRoute.Library.left_notMem_endpointNeighbourCover
#print axioms PaperRoute.Library.right_notMem_endpointNeighbourCover
#print axioms PaperRoute.Library.strongConflict_meets_cover
#print axioms PaperRoute.Library.conflict_neighbors_subset_incidence_cover
#print axioms PaperRoute.Library.conflict_degree_le_incidence_cover_card
#print axioms PaperRoute.Library.conflict_degree_le_incidence_sum
#print axioms PaperRoute.Library.endpointNeighbourCover_card_le_six
#print axioms PaperRoute.Library.conflict_degree_le_24

#print axioms PaperRoute.Library.endpointNeighbourCover_card_eq_six_of_degree_eq_24
#print axioms PaperRoute.Library.endpoint_degrees_eq_four_of_degree_eq_24
#print axioms PaperRoute.Library.cover_degree_eq_four_of_degree_eq_24
#print axioms PaperRoute.Library.cover_independent_of_degree_eq_24
#print axioms PaperRoute.Library.other_neighbor_sets_disjoint_of_degree_eq_24
#print axioms PaperRoute.Library.endpoint_neighbor_sets_disjoint_of_degree_eq_24
#print axioms PaperRoute.Library.endpoint_neighborhood_independent_of_degree_eq_24
#print axioms PaperRoute.Library.no_cross_edge_of_degree_eq_24

#print axioms PaperRoute.Library.minimalCliqueBounds20_of_thresholds
#print axioms PaperRoute.Library.local20_of_minimal_clique_bounds
#print axioms PaperRoute.Library.packing20_of_minimal_clique_bounds
#print axioms PaperRoute.Library.minimalCliqueBounds20_induce
#print axioms PaperRoute.Library.subset_packing20_of_minimal_clique_bounds
#print axioms PaperRoute.Library.induced_matching_packing20_of_minimal_clique_bounds

#print axioms PaperRoute.Library.conflict_degree_eq_24_of_ge
#print axioms PaperRoute.Library.mem_branchEdges
#print axioms PaperRoute.Library.high24_edge_not_between_neighbors
#print axioms PaperRoute.Library.high24_external_conflict_adj
#print axioms PaperRoute.Library.high24_distinct_branches_ne
#print axioms PaperRoute.Library.high24_mixed_branches_cannot_have_fork
#print axioms PaperRoute.Library.branchEdges_card_le_three
#print axioms PaperRoute.Library.high24_branch_union_card_le_three
#print axioms PaperRoute.Library.high24_side_card_le_three
#print axioms PaperRoute.Library.high24_clique_card_le_thirteen
#print axioms PaperRoute.Library.high24_clique_card_le_fifteen
#print axioms PaperRoute.Library.minimalCliqueBounds20_of_high20_high21_high22_high23
#print axioms PaperRoute.Library.induced_matching_packing20_of_high20_high21_high22_high23

#check PaperRoute.Library.packing20_of_thresholds
#check PaperRoute.Library.induced_matching_packing20_of_thresholds
#check PaperRoute.Library.conflict_degree_le_24
#check PaperRoute.Library.induced_matching_packing20_of_minimal_clique_bounds
#check PaperRoute.Library.high24_clique_card_le_thirteen
#check PaperRoute.Library.high24_clique_card_le_fifteen
#check PaperRoute.Library.minimalCliqueBounds20_of_high20_high21_high22_high23
#check PaperRoute.Library.induced_matching_packing20_of_high20_high21_high22_high23

#print axioms PaperRoute.Library.card_le_via_relation
#print axioms PaperRoute.Library.edgeIncidences_univ_card
#print axioms PaperRoute.Library.edgeIncidences_card_le_degree
#print axioms PaperRoute.Library.edge_endpoint_count
#print axioms PaperRoute.Library.incidence_sum_eq_meeting_add_inside
#print axioms PaperRoute.Library.conflict_degree_add_inside_le_sum
#print axioms PaperRoute.Library.clique_card_le_one_add_incidence_sum
#print axioms PaperRoute.Library.clique_card_le_thirteen_of_support_degree_le_two

#print axioms PaperRoute.Library.high23_cover_card_eq_six
#print axioms PaperRoute.Library.high23_endpoints_degree_four
#print axioms PaperRoute.Library.high23_other_neighbor_sets_disjoint
#print axioms PaperRoute.Library.high23_no_triangle_on_edge
#print axioms PaperRoute.Library.high23_cover_inside_card_le_one
#print axioms PaperRoute.Library.high23_cross_edges_unique
#print axioms PaperRoute.Library.high23_at_most_one_four_cycle_on_edge

#print axioms PaperRoute.Library.mem_rootType
#print axioms PaperRoute.Library.rootLabels_subset_neighbors
#print axioms PaperRoute.Library.rootLabels_card
#print axioms PaperRoute.Library.high23_root_degree_four
#print axioms PaperRoute.Library.high23_root_neighborhood_independent
#print axioms PaperRoute.Library.high23_root_cross_unique
#print axioms PaperRoute.Library.high23_type_meets_root_labels
#print axioms PaperRoute.Library.high23_root_type_card_le_two
#print axioms PaperRoute.Library.high23_double_type_unique
#print axioms PaperRoute.Library.high23_type_singleton_of_sharing_double

#print axioms PaperRoute.Library.outerEdges_endpoints
#print axioms PaperRoute.Library.outer_edge_types_cover_root_labels
#print axioms PaperRoute.Library.high23_outer_edges_incident_double_root
#print axioms PaperRoute.Library.high23_outer_card_le_two_of_double_root_type
#print axioms PaperRoute.Library.high23_outer_edges_card_le_two
#print axioms PaperRoute.Library.selected_edges_card_le_meeting_add_outer
#print axioms PaperRoute.Library.high23_clique_card_le_fourteen_of_support_degree_le_three

#print axioms PaperRoute.Library.root_edge_tip_not_neighbor
#print axioms PaperRoute.Library.root_single_edges_outer_adj
#print axioms PaperRoute.Library.high23_singleTips_card_le_six
#print axioms PaperRoute.Library.singleRootEdges_card_le_singleTips
#print axioms PaperRoute.Library.high23_doubleRootEdges_card_le_four

#print axioms PaperRoute.Library.meeting_edges_subset_root_single_double
#print axioms PaperRoute.Library.high23_meeting_card_le_fourteen_of_root_four
#print axioms PaperRoute.Library.high23_clique_card_le_sixteen_of_root_four
#print axioms PaperRoute.Library.high23_clique_card_le_sixteen

#print axioms PaperRoute.Library.minimalCliqueBounds20_of_high20_high21_high22
#print axioms PaperRoute.Library.induced_matching_packing20_of_high20_high21_high22
#check PaperRoute.Library.high23_cover_inside_card_le_one
#check PaperRoute.Library.high23_at_most_one_four_cycle_on_edge
#check PaperRoute.Library.high23_clique_card_le_sixteen
#check PaperRoute.Library.minimalCliqueBounds20_of_high20_high21_high22
#check PaperRoute.Library.induced_matching_packing20_of_high20_high21_high22

#print axioms PaperRoute.Library.high22_cover_card_eq_six
#print axioms PaperRoute.Library.high22_endpoints_degree_four
#print axioms PaperRoute.Library.high22_other_neighbor_sets_disjoint
#print axioms PaperRoute.Library.high22_no_triangle_on_edge
#print axioms PaperRoute.Library.high22_cover_inside_card_le_two
#print axioms PaperRoute.Library.high22_at_most_two_four_cycles_on_edge

#print axioms PaperRoute.Library.root_single_edge_outer_adj
#print axioms PaperRoute.Library.rootTips_adj_of_single
#print axioms PaperRoute.Library.rootTips_card_le_six_of_single
#print axioms PaperRoute.Library.rootEdges_card_le_tip_weight
#print axioms PaperRoute.Library.clique_card_le_star_root_outer
#print axioms PaperRoute.Library.outer_incidence_add_type_card_le_degree

#print axioms PaperRoute.Library.high22_root_degree_four
#print axioms PaperRoute.Library.high22_root_neighborhood_independent
#print axioms PaperRoute.Library.fourCycleOpposites_card_eq_root_load
#print axioms PaperRoute.Library.high22_root_label_budget_two
#print axioms PaperRoute.Library.high22_root_type_erase_card_le_two
#print axioms PaperRoute.Library.high22_root_type_card_le_three
#print axioms PaperRoute.Library.high22_root_label_multiple_card_le_two
#print axioms PaperRoute.Library.high22_shared_root_types_card_le_four
#print axioms PaperRoute.Library.root_type_card_sum_eq_label_sum
#print axioms PaperRoute.Library.high22_multipleTips_card_le_four
#print axioms PaperRoute.Library.high22_multipleTips_eq_of_triple

#print axioms PaperRoute.Library.high22_clique_card_le_seventeen_of_root_triple
#print axioms PaperRoute.Library.outer_endpoints_multiple_of_root_four
#print axioms PaperRoute.Library.outer_incidence_sum_eq_twice
#print axioms PaperRoute.Library.high22_outer_card_le_four_of_root_types_le_two
#print axioms PaperRoute.Library.rootEdges_card_le_tips_add_multiple
#print axioms PaperRoute.Library.rootEdges_card_le_twice_multiple_of_no_single
#print axioms PaperRoute.Library.high22_outer_degree_eq_two_of_four
#print axioms PaperRoute.Library.outer_saturated_neighbors
#print axioms PaperRoute.Library.high22_active_multiple_card_le_two_of_outer_four
#print axioms PaperRoute.Library.high22_clique_card_le_seventeen_of_root_four

#print axioms PaperRoute.Library.labelHeavyTips_subset_multiple
#print axioms PaperRoute.Library.root_type_inter_card_sum
#print axioms PaperRoute.Library.outerEdges_meet_labelHeavyTips
#print axioms PaperRoute.Library.high22_heavy_label_card_le_two
#print axioms PaperRoute.Library.high22_labelHeavyTips_card_le_three
#print axioms PaperRoute.Library.high22_outer_incidence_le_two_at_heavy
#print axioms PaperRoute.Library.high22_outer_card_le_six_of_root_three
#print axioms PaperRoute.Library.high22_heavy_card_and_degree_of_outer_six
#print axioms PaperRoute.Library.high22_heavy_label_card_eq_two_of_three
#print axioms PaperRoute.Library.high22_multiple_subset_heavy_of_three

#print axioms PaperRoute.Library.root_outer_incidence_add_le
#print axioms PaperRoute.Library.root_incidence_at_tip_le_type
#print axioms PaperRoute.Library.rootEdges_card_le_tips_of_incidence_le_one
#print axioms PaperRoute.Library.rootTips_subset_multiple_of_no_single
#print axioms PaperRoute.Library.high22_clique_card_le_seventeen_of_support_degree_le_three

#print axioms PaperRoute.Library.high22_clique_card_le_seventeen

#print axioms PaperRoute.Library.minimalCliqueBounds20_of_high20_high21
#print axioms PaperRoute.Library.induced_matching_packing20_of_high20_high21
#check PaperRoute.Library.high22_cover_inside_card_le_two
#check PaperRoute.Library.high22_at_most_two_four_cycles_on_edge
#check PaperRoute.Library.high22_root_label_budget_two
#check PaperRoute.Library.high22_clique_card_le_seventeen_of_root_four
#check PaperRoute.Library.high22_clique_card_le_seventeen_of_support_degree_le_three
#check PaperRoute.Library.high22_clique_card_le_seventeen
#check PaperRoute.Library.minimalCliqueBounds20_of_high20_high21
#check PaperRoute.Library.induced_matching_packing20_of_high20_high21

-- PaperRoute.Library/Bounds/DegreeTwoClique.lean
#check PaperRoute.Library.restricted_incidence_card_le
#print axioms PaperRoute.Library.restricted_incidence_card_le
#check PaperRoute.Library.restricted_cover_card_le_two
#print axioms PaperRoute.Library.restricted_cover_card_le_two
#check PaperRoute.Library.clique_card_le_one_add_restricted_incidence_sum
#print axioms PaperRoute.Library.clique_card_le_one_add_restricted_incidence_sum
#check PaperRoute.Library.degree_two_clique_card_le_five
#print axioms PaperRoute.Library.degree_two_clique_card_le_five
#check PaperRoute.Library.degree_two_five_cover_saturated
#print axioms PaperRoute.Library.degree_two_five_cover_saturated
#check PaperRoute.Library.degree_two_five_supported_degree_two
#print axioms PaperRoute.Library.degree_two_five_supported_degree_two
#check PaperRoute.Library.degree_two_clique_card_le_four_of_selected_bipartition
#print axioms PaperRoute.Library.degree_two_clique_card_le_four_of_selected_bipartition

-- PaperRoute.Library/Bounds/High21.lean
#check PaperRoute.Library.high21_clique_card_le_eighteen
#print axioms PaperRoute.Library.high21_clique_card_le_eighteen

-- PaperRoute.Library/Bounds/High21Double.lean
#check PaperRoute.Library.rootType_eq_neighbor_inter
#print axioms PaperRoute.Library.rootType_eq_neighbor_inter
#check PaperRoute.Library.multipleTips_not_neighbor
#print axioms PaperRoute.Library.multipleTips_not_neighbor
#check PaperRoute.Library.residual_neighbors_add_type_card
#print axioms PaperRoute.Library.residual_neighbors_add_type_card
#check PaperRoute.Library.root_selected_edges_force_adj
#print axioms PaperRoute.Library.root_selected_edges_force_adj
#check PaperRoute.Library.fullDoubleTips_adj_of_types_ne
#print axioms PaperRoute.Library.fullDoubleTips_adj_of_types_ne
#check PaperRoute.Library.high21_full_double_types_equal_or_disjoint
#print axioms PaperRoute.Library.high21_full_double_types_equal_or_disjoint
#check PaperRoute.Library.fullDoubleTips_card_le_four
#print axioms PaperRoute.Library.fullDoubleTips_card_le_four

-- PaperRoute.Library/Bounds/High21LargeType.lean
#check PaperRoute.Library.high21_large_types_share_label
#print axioms PaperRoute.Library.high21_large_types_share_label
#check PaperRoute.Library.high21_multipleTips_eq_of_type_four
#print axioms PaperRoute.Library.high21_multipleTips_eq_of_type_four
#check PaperRoute.Library.high21_other_type_le_two_of_triple
#print axioms PaperRoute.Library.high21_other_type_le_two_of_triple
#check PaperRoute.Library.high21_multiple_unique_at_triple_label
#print axioms PaperRoute.Library.high21_multiple_unique_at_triple_label
#check PaperRoute.Library.high21_multipleTips_subset_triple_outer_endpoints
#print axioms PaperRoute.Library.high21_multipleTips_subset_triple_outer_endpoints
#check PaperRoute.Library.high21_outer_card_le_two_of_root_triple
#print axioms PaperRoute.Library.high21_outer_card_le_two_of_root_triple
#check PaperRoute.Library.high21_clique_card_le_eighteen_of_root_triple
#print axioms PaperRoute.Library.high21_clique_card_le_eighteen_of_root_triple

-- PaperRoute.Library/Bounds/High21Local.lean
#check PaperRoute.Library.high21_cover_card_eq_six
#print axioms PaperRoute.Library.high21_cover_card_eq_six
#check PaperRoute.Library.high21_endpoints_degree_four
#print axioms PaperRoute.Library.high21_endpoints_degree_four
#check PaperRoute.Library.high21_other_neighbor_sets_disjoint
#print axioms PaperRoute.Library.high21_other_neighbor_sets_disjoint
#check PaperRoute.Library.high21_no_triangle_on_edge
#print axioms PaperRoute.Library.high21_no_triangle_on_edge
#check PaperRoute.Library.high21_cover_inside_card_le_three
#print axioms PaperRoute.Library.high21_cover_inside_card_le_three
#check PaperRoute.Library.high21_at_most_three_four_cycles_on_edge
#print axioms PaperRoute.Library.high21_at_most_three_four_cycles_on_edge

-- PaperRoute.Library/Bounds/High21RootFour.lean
#check PaperRoute.Library.outer_card_le_four_of_double_types
#print axioms PaperRoute.Library.outer_card_le_four_of_double_types
#check PaperRoute.Library.rootLabels_rootEdges_at_tip_subset_type
#print axioms PaperRoute.Library.rootLabels_rootEdges_at_tip_subset_type
#check PaperRoute.Library.root_incidence_two_mem_fullDoubleTips
#print axioms PaperRoute.Library.root_incidence_two_mem_fullDoubleTips
#check PaperRoute.Library.rootEdges_card_le_tips_add_fullDoubleTips
#print axioms PaperRoute.Library.rootEdges_card_le_tips_add_fullDoubleTips
#check PaperRoute.Library.high21_clique_card_le_eighteen_of_root_types_le_two
#print axioms PaperRoute.Library.high21_clique_card_le_eighteen_of_root_types_le_two
#check PaperRoute.Library.high21_clique_card_le_eighteen_of_root_four
#print axioms PaperRoute.Library.high21_clique_card_le_eighteen_of_root_four

-- PaperRoute.Library/Bounds/High21Support.lean
#check PaperRoute.Library.high21_root_degree_four
#print axioms PaperRoute.Library.high21_root_degree_four
#check PaperRoute.Library.high21_root_neighborhood_independent
#print axioms PaperRoute.Library.high21_root_neighborhood_independent
#check PaperRoute.Library.high21_root_label_budget_three
#print axioms PaperRoute.Library.high21_root_label_budget_three
#check PaperRoute.Library.high21_root_type_erase_card_le_three
#print axioms PaperRoute.Library.high21_root_type_erase_card_le_three
#check PaperRoute.Library.high21_root_label_multiple_card_le_three
#print axioms PaperRoute.Library.high21_root_label_multiple_card_le_three
#check PaperRoute.Library.high21_shared_root_types_card_le_five
#print axioms PaperRoute.Library.high21_shared_root_types_card_le_five
#check PaperRoute.Library.high21_multipleTips_card_le_six
#print axioms PaperRoute.Library.high21_multipleTips_card_le_six

-- PaperRoute.Library/Bounds/SubcubicEighteen.lean
#check PaperRoute.Library.clique_card_le_nineteen_of_support_degree_le_three
#print axioms PaperRoute.Library.clique_card_le_nineteen_of_support_degree_le_three
#check PaperRoute.Library.subcubic_nineteen_cover_saturated
#print axioms PaperRoute.Library.subcubic_nineteen_cover_saturated
#check PaperRoute.Library.subcubic_nineteen_supported_degree_three
#print axioms PaperRoute.Library.subcubic_nineteen_supported_degree_three
#check PaperRoute.Library.clique_card_le_eighteen_of_support_degree_le_three
#print axioms PaperRoute.Library.clique_card_le_eighteen_of_support_degree_le_three

-- PaperRoute.Library/High21Packing.lean
#check PaperRoute.Library.minimalCliqueBounds20_of_high20
#print axioms PaperRoute.Library.minimalCliqueBounds20_of_high20
#check PaperRoute.Library.induced_matching_packing20_of_high20
#print axioms PaperRoute.Library.induced_matching_packing20_of_high20

-- PaperRoute.Library/Bounds/High20.lean
#check PaperRoute.Library.clique_card_le_eighteen_of_independent_root_types_le_two
#print axioms PaperRoute.Library.clique_card_le_eighteen_of_independent_root_types_le_two
#check PaperRoute.Library.high20_clique_card_le_nineteen_of_root_four
#print axioms PaperRoute.Library.high20_clique_card_le_nineteen_of_root_four
#check PaperRoute.Library.high20_clique_card_le_nineteen
#print axioms PaperRoute.Library.high20_clique_card_le_nineteen

-- PaperRoute.Library/Bounds/High20Four.lean
#check PaperRoute.Library.high20_other_type_le_two_of_four
#print axioms PaperRoute.Library.high20_other_type_le_two_of_four
#check PaperRoute.Library.high20_multiple_unique_at_four_label
#print axioms PaperRoute.Library.high20_multiple_unique_at_four_label
#check PaperRoute.Library.high20_multipleTips_subset_four_outer_endpoints
#print axioms PaperRoute.Library.high20_multipleTips_subset_four_outer_endpoints
#check PaperRoute.Library.high20_outer_card_le_two_of_root_type_four
#print axioms PaperRoute.Library.high20_outer_card_le_two_of_root_type_four
#check PaperRoute.Library.high20_clique_card_le_eighteen_of_root_type_four
#print axioms PaperRoute.Library.high20_clique_card_le_eighteen_of_root_type_four

-- PaperRoute.Library/Bounds/High20Local.lean
#check PaperRoute.Library.endpointNeighbourCover_card_le_five_of_triangle
#print axioms PaperRoute.Library.endpointNeighbourCover_card_le_five_of_triangle
#check PaperRoute.Library.root_label_multiple_card_le_three
#print axioms PaperRoute.Library.root_label_multiple_card_le_three
#check PaperRoute.Library.multipleTips_type_sum_le_twelve
#print axioms PaperRoute.Library.multipleTips_type_sum_le_twelve
#check PaperRoute.Library.multipleTips_card_le_six
#print axioms PaperRoute.Library.multipleTips_card_le_six
#check PaperRoute.Library.high20_cover_inside_card_le_four
#print axioms PaperRoute.Library.high20_cover_inside_card_le_four
#check PaperRoute.Library.high20_triangle_cover_inside_empty
#print axioms PaperRoute.Library.high20_triangle_cover_inside_empty
#check PaperRoute.Library.high20_triangle_root_type_singleton
#print axioms PaperRoute.Library.high20_triangle_root_type_singleton
#check PaperRoute.Library.high20_root_triangle_outer_empty
#print axioms PaperRoute.Library.high20_root_triangle_outer_empty
#check PaperRoute.Library.high20_large_clique_root_neighborhood_independent
#print axioms PaperRoute.Library.high20_large_clique_root_neighborhood_independent
#check PaperRoute.Library.high20_root_label_budget_four
#print axioms PaperRoute.Library.high20_root_label_budget_four
#check PaperRoute.Library.high20_shared_root_types_card_le_six
#print axioms PaperRoute.Library.high20_shared_root_types_card_le_six

-- PaperRoute.Library/Bounds/High20Outer.lean
#check PaperRoute.Library.outer_avoiding_card_le_four_of_other_types_le_two
#print axioms PaperRoute.Library.outer_avoiding_card_le_four_of_other_types_le_two

-- PaperRoute.Library/Bounds/High20Slots.lean
#check PaperRoute.Library.star_add_root_card_le_label_sum
#print axioms PaperRoute.Library.star_add_root_card_le_label_sum
#check PaperRoute.Library.selected_degree_add_one_le_of_missing_label
#print axioms PaperRoute.Library.selected_degree_add_one_le_of_missing_label
#check PaperRoute.Library.root_label_mem_symm
#print axioms PaperRoute.Library.root_label_mem_symm
#check PaperRoute.Library.root_card_add_missing_type_le_twelve
#print axioms PaperRoute.Library.root_card_add_missing_type_le_twelve
#check PaperRoute.Library.root_card_le_ten_of_label_selected_degree_le_two
#print axioms PaperRoute.Library.root_card_le_ten_of_label_selected_degree_le_two

-- PaperRoute.Library/Bounds/High20TwoTriples.lean
#check PaperRoute.Library.high20_other_type_single_at_shared_triple_label
#print axioms PaperRoute.Library.high20_other_type_single_at_shared_triple_label
#check PaperRoute.Library.high20_outer_meets_two_triples
#print axioms PaperRoute.Library.high20_outer_meets_two_triples
#check PaperRoute.Library.high20_clique_card_le_eighteen_of_two_triples
#print axioms PaperRoute.Library.high20_clique_card_le_eighteen_of_two_triples

-- PaperRoute.Library/Bounds/High20UniqueTriple.lean
#check PaperRoute.Library.root_missing_label_selected_degree_le_two_of_unique_triple
#print axioms PaperRoute.Library.root_missing_label_selected_degree_le_two_of_unique_triple
#check PaperRoute.Library.root_card_le_ten_of_unique_triple
#print axioms PaperRoute.Library.root_card_le_ten_of_unique_triple
#check PaperRoute.Library.clique_card_le_nineteen_of_unique_triple
#print axioms PaperRoute.Library.clique_card_le_nineteen_of_unique_triple

-- PaperRoute.Library/High20Packing.lean
#check PaperRoute.Library.minimalCliqueBounds20_of_maxDegree_four
#print axioms PaperRoute.Library.minimalCliqueBounds20_of_maxDegree_four
#check PaperRoute.Library.induced_matching_packing20
#print axioms PaperRoute.Library.induced_matching_packing20
