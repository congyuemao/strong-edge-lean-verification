"""Verify immutable GitHub source text and save byte-identical historical snapshots."""
import hashlib, json, pathlib

P = pathlib.Path(__file__).resolve().parent / 'research'
records = json.loads((P / 'connector-content.json').read_text(encoding='utf-8'))
results = []
for record in records:
    data = record['content'].encode('utf-8')
    header = b'blob ' + str(len(data)).encode() + bytes([0])
    blob = hashlib.sha1(header + data).hexdigest()
    assert blob == record['sha'], (record['file'], blob, record['sha'])
    target = P / record['file']
    before = target.read_bytes()
    difference = 'identical' if before == data else ('trailing_newline_only' if before.rstrip(b'\r\n') == data.rstrip(b'\r\n') else 'other')
    assert difference != 'other', record['file']
    target.write_bytes(data)
    results.append(dict(file=record['file'], original_copy_difference=difference,
                        git_blob_sha=blob, git_blob_matches=True,
                        sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
(P / 'verification.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
