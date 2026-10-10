from pathlib import Path
import json,hashlib,subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader
import pdfplumber

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/pdf'
TMP=ROOT/'tmp/pdfs/dual_review'
TMP.mkdir(parents=True,exist_ok=True)
POP=Path(r'C:\Users\21161\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
results=[]
for stem in ['route_a_paper_first','route_b_lean_first']:
    path=OUT/(stem+'.pdf')
    reader=PdfReader(path)
    texts=[p.extract_text() for p in reader.pages]
    text='\n'.join(texts)
    assert not (reader.metadata.author or '')
    assert all(t not in text for t in ['@abstract','@table','@@MATH','\ufffd'])
    assert all(t in text for t in ['Theorem 1.1','Proposition 4.2','Proposition 4.3','Proposition 4.4',
                                   'Proposition 4.5','Proposition 4.6','Lemma 5.3','Proposition 6.1','References'])
    assert sum(len(p.images) for p in reader.pages)==0
    checks=[]
    with pdfplumber.open(path) as doc:
        for i,p in enumerate(doc.pages,1):
            assert p.crop((0,p.height-50,p.width,p.height)).extract_text().strip()==str(i)
            bad=[c for c in p.chars if c['x0']<59 or c['x1']>p.width-59 or c['top']<25 or c['bottom']>p.height-25]
            assert not bad,(stem,i,bad[:3])
            checks.append({'page':i,'characters':len(p.chars),'outside_safe_area':len(bad)})
    subprocess.run([str(POP),'-scale-to','1500','-png',str(path),str(TMP/stem)],check=True,
                   capture_output=True)
    pages=sorted(TMP.glob(stem+'-*.png'))
    for start in range(0,len(pages),4):
        canvas=Image.new('RGB',(1320,1900),'#d5d5d5')
        draw=ImageDraw.Draw(canvas)
        for j,p in enumerate(pages[start:start+4]):
            im=Image.open(p).convert('RGB')
            im.thumbnail((645,912))
            x,y=8+(j%2)*660,27+(j//2)*950
            canvas.paste(im,(x,y))
            draw.text((x,y-19),f'{stem}: page {start+j+1}',fill='black')
        canvas.save(TMP/f'{stem}-contact-{start//4+1}.jpg',quality=90)
    results.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'pages':len(reader.pages),'author_empty':True,'raster_images':0,'checks':checks})
(OUT/'dual_pdf_validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k!='checks'} for r in results],indent=2))
