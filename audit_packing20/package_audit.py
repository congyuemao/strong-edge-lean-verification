"""Build a source-and-evidence checkpoint after successful technical verification."""
import argparse, datetime, hashlib, json, os, pathlib, re, zipfile

ROOT = pathlib.Path(__file__).resolve().parent
P = ROOT / 'isolated' / 'strong_edge_lean_starter'
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='strong_edge_lean_packing20_independent_kernel_verified_checkpoint.zip')
args = parser.parse_args()
assert pathlib.Path(args.output).name == args.output and args.output.endswith('.zip')
OUT = ROOT / args.output
assert not OUT.exists(), 'Refusing to replace an existing checkpoint; choose a new output name.'
verification = json.loads((ROOT / 'verification-results.json').read_text(encoding='utf-8'))
assert verification['technical_pass'] and verification['entrypoint_successful_commands'] == 9
source_hashes = json.loads((ROOT / 'source-sha256-after.json').read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

for name, expected in source_hashes.items():
    assert sha((P / name).read_bytes()) == expected, name

for record in json.loads((ROOT / 'research' / 'sources.json').read_text(encoding='utf-8')):
    content = (ROOT / 'research' / record['file']).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(content)).encode() + bytes([0]) + content).hexdigest() == record['git_blob_sha']

excluded_dirs = {'.lake', '.git', '.cache', '__pycache__', 'dependency-cache', '.tools'}
excluded_names = {OUT.name, 'ARCHIVE_CONTENTS.json', 'checkpoint-audit.json'}
binary_extensions = {'.exe', '.dll', '.olean', '.ilean', '.pyc', '.pyo', '.so', '.a', '.o'}
members = {}
for directory, dirs, files in os.walk(ROOT):
    dirs[:] = sorted(d for d in dirs if d not in excluded_dirs)
    for name in sorted(files):
        path = pathlib.Path(directory) / name
        if name in excluded_names or path.suffix.lower() == '.zip':
            continue
        assert path.suffix.lower() not in binary_extensions, path
        assert not path.is_symlink(), path
        rel = path.relative_to(ROOT).as_posix()
        members[rel] = {'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())}

required = ['AUDIT_PACKING20_' + s + '.md' for s in ['SUMMARY', 'REPRODUCIBILITY', 'SEMANTICS', 'DEPENDENCIES', 'PRIOR_ART']]
assert all(n in members for n in required)

# Catch broken relative file links and malformed Markdown tables in the new reports.
for name in required + ['README.md', 'joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md']:
    source = (ROOT / name).read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', source):
        if '://' in target or target.startswith('#'):
            continue
        assert (ROOT / name).parent.joinpath(target.split('#')[0]).exists(), (name, target)
    previous = None
    for line in source.splitlines():
        if line.startswith('|'):
            count = len(re.findall(r'(?<!\\)\|', line))
            if previous is not None:
                assert count == previous, ('table', name, line)
            previous = count
        else:
            previous = None

manifest = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'note': 'Paths relative to audit_packing20/. Manifest excludes itself and external ZIP verification.',
            'technical_verification': verification, 'files': members}
(ROOT / 'ARCHIVE_CONTENTS.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for rel in sorted([*members, 'ARCHIVE_CONTENTS.json']):
        z.write(ROOT / rel, 'audit_packing20/' + rel)

with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(members) + 1
    for rel, data in members.items():
        assert sha(z.read('audit_packing20/' + rel)) == data['sha256'], rel
    for name, expected in source_hashes.items():
        assert sha(z.read('audit_packing20/isolated/strong_edge_lean_starter/' + name)) == expected, name
    assert not any(set(pathlib.PurePosixPath(n).parts) & excluded_dirs for n in z.namelist())

result = {'archive': OUT.name, 'sha256': sha(OUT.read_bytes()), 'bytes': OUT.stat().st_size,
          'member_count': len(members) + 1, 'uncompressed_bytes': sum(x['bytes'] for x in members.values()) + (ROOT / 'ARCHIVE_CONTENTS.json').stat().st_size,
          'zip_crc_pass': True, 'all_member_sha256_pass': True, 'source_and_config_hashes_checked': len(source_hashes),
          'excluded': sorted(excluded_dirs),
          'literature_full_2016_joint_paper_verified': verification['literature_full_2016_joint_paper_verified'],
          'originality_established': False,
          'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROOT / 'checkpoint-audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
