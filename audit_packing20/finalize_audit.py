"""Check recorded process results and preservation; does not replace Lean checks."""
import collections, datetime, hashlib, json, pathlib, re, subprocess, zipfile

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT.parent
P = ROOT / 'isolated' / 'strong_edge_lean_starter'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def read_log(path):
    b = path.read_bytes()
    return b.decode('utf-16') if b.startswith(b'\xff\xfe') else b.decode('utf-8-sig')

def parse_axioms(s):
    results = {}
    for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", s):
        axioms = sorted(re.sub(r'\.\{[^}]*\}', '', x.strip()) for x in (match[2] or '').split(',') if x.strip())
        assert set(axioms) <= ALLOWED, (match[1], axioms)
        assert match[1] not in results, match[1]
        results[match[1]] = axioms
    return results

labels = ['compiler-version', 'build', 'audit', 'tests', 'build-confirm', 'complete-final',
          'semantic', 'regression-dev', 'environment', 'dependencies-dev', 'rerun-entrypoint']
commands = {}
axiom_outputs = {}
for label in labels:
    meta = json.loads((ROOT / 'logs' / (label + '.json')).read_text(encoding='utf-8-sig'))
    assert meta['exit_code'] == 0, (label, meta)
    output = read_log(ROOT / 'logs' / (label + '.stdout.log'))
    error = read_log(ROOT / 'logs' / (label + '.stderr.log'))
    assert not re.search(r'\b(?:warning|error):', output + error, re.I), label
    assert not error.strip(), (label, error)
    commands[label] = meta
    if label not in ['dependencies-dev', 'compiler-version', 'build', 'build-confirm', 'tests', 'rerun-entrypoint']:
        ax = parse_axioms(output)
        axiom_outputs[label] = ax
        if label in ['audit', 'complete-final']:
            assert len(ax) == 225, (label, len(ax))

assert set(axiom_outputs['audit']) == set(axiom_outputs['complete-final'])
assert axiom_outputs['audit'] == axiom_outputs['complete-final']
build = read_log(ROOT / 'logs' / 'build.stdout.log')
assert 'Build completed successfully (1170 jobs).' in build
assert len(re.findall(r'Built StrongEdge(?:\.| \()', build)) == 44

reruns = {}
for name in ['version', 'build', 'audit', 'tests', 'complete', 'semantic', 'regression', 'environment', 'dependencies']:
    folder = P / 'independent-rerun-logs'
    meta = json.loads((folder / (name + '.json')).read_text(encoding='utf-8-sig'))
    assert meta['exit_code'] == 0, (name, meta)
    output = read_log(folder / (name + '.stdout.log'))
    error = read_log(folder / (name + '.stderr.log'))
    assert not error.strip() and not re.search(r'\b(?:warning|error):', output + error, re.I), name
    if name in ['audit', 'complete']:
        assert parse_axioms(output) == axiom_outputs['audit']
    reruns[name] = meta

before = json.loads((ROOT / 'source-sha256-before.json').read_text())
after = {n: sha(P / n) for n in before}
assert before == after
assert before == {n: sha(BASE / 'strong_edge_lean_starter' / n) for n in before}
for path in sorted(P.glob('Audit*.lean')):
    after[path.name] = sha(path)
after['reproduce-audit.ps1'] = sha(P / 'reproduce-audit.ps1')
save('source-sha256-after.json', after)

preservation = []
with zipfile.ZipFile(BASE / 'strong_edge_lean_high20_checkpoint.zip') as z:
    for name in z.namelist():
        if name.endswith('/'):
            continue
        rel = name.removeprefix('strong_edge_lean_starter/')
        content = z.read(name)
        assert (P / rel).read_bytes() == content, ('isolated', rel)
        assert (BASE / 'strong_edge_lean_starter' / rel).read_bytes() == content, ('original', rel)
        preservation.append(dict(path=rel, sha256=hashlib.sha256(content).hexdigest()))
save('checkpoint-member-preservation.json', preservation)

historical = json.loads((BASE / 'docs' / 'ARCHIVE_MANIFEST.json').read_text(encoding='utf-8-sig'))['verification']['preserved_checkpoints']
historical['strong_edge_lean_high20_checkpoint.zip'] = json.loads((ROOT / 'checkpoint-sha256.json').read_text())['strong_edge_lean_high20_checkpoint.zip']
assert historical == {n: sha(BASE / n) for n in historical}
save('historical-checkpoint-verification.json', historical)

states = []
pins = json.loads((P / 'lake-manifest.json').read_text())['packages']
for pin in pins:
    repo = P / '.lake' / 'packages' / pin['name']
    head = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    status = subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--untracked-files=no'], text=True)
    assert head == pin['rev'] and not status, (pin['name'], head, status)
    states.append(dict(name=pin['name'], expected=pin['rev'], actual=head, tracked_status=status))
save('dependency-states-after.json', states)

bins = BASE / '.tools' / 'lean-4.35.0-rc4-windows' / 'bin'
save('compiler-sha256.json', {n: sha(bins / n) for n in ['lean.exe', 'lake.exe']})
save('axiom-verification.json', axiom_outputs)
save('command-verification.json', dict(individual=commands, entrypoint=reruns))

# Additional audit files undergo the same lexical scan as original project files.
# This scan deliberately supplements, rather than substitutes for, kernel output.
from static_audit import strip_comments, tokens
new_findings = []
for path in sorted(P.glob('Audit*.lean')):
    raw = path.read_text(encoding='utf-8-sig')
    for line, text in enumerate(strip_comments(raw).splitlines(), 1):
        for match in tokens.finditer(text):
            new_findings.append(dict(file=path.name, line=line, token=match.group()))
assert not new_findings, new_findings
save('new-audit-static-findings.json', new_findings)

review_path = ROOT / 'joos2016_review' / 'review-result.json'
review = json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
result = dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    technical_pass=True, original_source_and_configs_unchanged=len(before),
    original_zip_files_unchanged_in_both_copies=len(preservation),
    original_project_lean_files=45, new_audit_lean_files=5,
    original_axiom_declarations=225, complete_type_and_axiom_checks=225,
    allowed_axioms=sorted(ALLOWED), build_jobs=1170, freshly_built_project_modules=44,
    individual_successful_commands=len(commands), entrypoint_successful_commands=len(reruns),
    locked_dependencies_verified=len(states), preserved_historical_zip_count=len(historical),
    literature_full_2016_joint_paper_verified=bool(review.get('full_text_review_completed')),
    literature_review_record='joos2016_review/review-result.json' if review else None,
    originality_established=False,
    optional_named_mathlib_square_interface_verified=False,
    cache_boundary='Locked dependency .olean cache reused; project modules rebuilt from extracted sources.')
save('verification-results.json', result)
print(json.dumps(result, indent=2))
