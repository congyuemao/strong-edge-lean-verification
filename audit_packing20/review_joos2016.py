"""Read-only PDF extraction for the user-supplied final journal article."""
import datetime, hashlib, json, pathlib
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = pathlib.Path(r'C:\Users\21161\Downloads\joos2016.pdf')
OUT = ROOT / 'joos2016_review'
TMP = ROOT.parent / 'tmp' / 'pdfs' / 'joos2016'
OUT.mkdir(exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
reader = PdfReader(SOURCE)
pages = []
for i, page in enumerate(reader.pages, 1):
    content = page.extract_text() or ''
    (TMP / f'page-{i:02}.txt').write_text(content, encoding='utf-8')
    pages.append(f'\n========== PDF PAGE {i} ==========\n{content}')
(TMP / 'full-text.txt').write_text('\n'.join(pages), encoding='utf-8')
record = dict(source=str(SOURCE), sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              bytes=SOURCE.stat().st_size, pages=len(reader.pages),
              metadata={str(k): str(v) for k,v in (reader.metadata or {}).items()},
              read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              note='User-supplied PDF read locally; no changes to original PDF or Lean sources.')
(OUT / 'source.json').write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(record, indent=2, ensure_ascii=True))
