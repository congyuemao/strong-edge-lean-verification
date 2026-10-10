"""Preserve the prior checkpoint and record the completed human-readable scope review."""
import datetime, hashlib, itertools, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
source = json.loads((HERE / 'source.json').read_text(encoding='utf-8'))
assert hashlib.sha256(pathlib.Path(source['source']).read_bytes()).hexdigest() == source['sha256']
assert source['pages'] == 12
before = json.loads((ROOT / 'source-sha256-after.json').read_text(encoding='utf-8'))
project = ROOT / 'isolated' / 'strong_edge_lean_starter'
assert all(hashlib.sha256((project / n).read_bytes()).hexdigest() == h for n,h in before.items())

old_zip = ROOT / 'strong_edge_lean_packing20_independent_kernel_verified_checkpoint.zip'
old_sha = hashlib.sha256(old_zip.read_bytes()).hexdigest()
assert old_sha == '689349eff54d63cc9ed00d64e4a5953f3db1713c8f64b435755e77ba53e520d0'
previous = HERE / 'previous-checkpoint-audit.json'
if not previous.exists():
    previous.write_bytes((ROOT / 'checkpoint-audit.json').read_bytes())
assert json.loads(previous.read_text())['sha256'] == old_sha

# Independently check the two elementary P4 obstructions used in the prose.
V = {0, 1, 2, 3}
E = {frozenset(e) for e in [(0,1), (1,2), (2,3)]}
outer = {frozenset((0,1)), frozenset((2,3))}
middle = {frozenset((1,2))}
def induced(edges, selected):
    return all(not (e & f) and not any(frozenset((x,y)) in edges for x in e for y in f)
               for e,f in itertools.combinations(selected, 2))
def alpha(edges, candidates):
    ordered = sorted(candidates, key=lambda e: sorted(e))
    return max(len(s) for k in range(len(ordered)+1) for s in itertools.combinations(ordered,k)
               if induced(edges, s))
assert alpha(E, outer) == 1 and alpha(outer, outer) == 2
X = {0, 1, 2}
MX = {frozenset((0,1))}
remaining = {e for e in E if not (e & X)}
Fprime = middle & remaining
isolated = {v for v in V-X if not any(v in e for e in remaining)}
closed_neighbors = set().union(*MX)
for v in list(closed_neighbors):
    closed_neighbors |= {u for e in E if v in e for u in e}
assert induced(E, MX) and closed_neighbors <= X and len(X)+len(isolated) <= 9*len(MX)
assert len(middle)-len(Fprime) == 1 and len(MX & middle) == 0
examples = dict(path_edges=[[0,1],[1,2],[2,3]],
    outer_candidate_example=dict(candidates=[[0,1],[2,3]],alpha_in_full_graph=1,alpha_after_deleting_middle_edge=2),
    reduction_example=dict(candidates=[[1,2]],X=sorted(X),local_matching=[[0,1]],
        isolated_after_deletion=sorted(isolated),vertex_cost=4,k=1,
        paper_reduction_inequality='4 <= 9',candidate_loss=1,candidate_gain=0),
    proof_status='Elementary finite check in Python plus explicit mathematical argument; not a new Lean theorem.')
(HERE / 'comparison-examples.json').write_text(json.dumps(examples,indent=2),encoding='utf-8')

result = dict(updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source_sha256=source['sha256'],full_text_review_completed=True,
    pages_read=list(range(1,13)),printed_pages='154-165',
    theorem='Theorem 1.1, printed pp.155-156',
    proof_scope='Section 2; Claims 1-11; Subclaims 9.1 and 11.1; Cases 1, 2.1, 2.2',
    contains_full_edge_set_20_bound=True,contains_tight_double_C5_example=True,
    contains_arbitrary_candidate_set_statement=False,contains_weighted_or_fractional_20_statement=False,
    direct_extension_of_its_reductions_to_candidates_verified=False,
    relative_assessment='Candidate-set guarantee is a distinct extension of the paper\'s full-edge-set corollary; direct deletion/intersection/reduction transfers fail.',
    global_originality_established=False,
    paper_proof_formalized_in_lean=False,lean_sources_changed=False,lean_recompiled_this_review=False,
    unchanged_source_and_config_files=len(before),previous_checkpoint_sha256=old_sha,
    report='JOOS2016_ORIGINALITY_REVIEW.md')
(HERE / 'review-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
verification = json.loads((ROOT / 'verification-results.json').read_text(encoding='utf-8'))
verification.update(literature_full_2016_joint_paper_verified=True,
                    literature_review_record='joos2016_review/review-result.json',
                    originality_established=False,literature_review_updated_utc=result['updated_utc'])
(ROOT / 'verification-results.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
