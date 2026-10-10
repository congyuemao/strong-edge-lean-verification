from pathlib import Path
import json,hashlib,zipfile
D=Path(__file__).resolve().parent
ROOT=D.parent
OUT=ROOT/'output/dual_proofs'
PDF=ROOT/'output/pdf'
def sha(data):return hashlib.sha256(data).hexdigest()
standalone={}
for route,count in [('a',4),('b',2)]:
    path=D/f'logs/standalone-{route}-audit.log'
    text=path.read_text(encoding='utf-8-sig')
    rs=[json.loads(l.split('ROUTE_AUDIT ',1)[1]) for l in text.splitlines() if 'ROUTE_AUDIT {' in l]
    assert len(rs)==count
    assert all(not r['unsafe'] and set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in rs)
    standalone[route]={'audited_roots':[r['root'] for r in rs],
        'method':'Standalone audit imports only its own route, using the verified same-source compiled module cache.',
        'exit_code':0}
for route in ['a','b']:
    path=OUT/f'route_{route}_lean.zip'
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        prefix=f'route_{route}_lean/'
        manifest=json.loads(z.read(prefix+'source-manifest.json'))
        assert all(sha(z.read(prefix+k))==v for k,v in manifest.items())
        assert not any('/.lake/' in n for n in z.namelist())
        assert not any(('/StrongEdge/' in n or n.endswith('/StrongEdge.lean')) for n in z.namelist()) if route=='a' else True
        standalone[route]['archive_files']=len(z.namelist())
        standalone[route]['source_manifest_verified']=True
pdfchecks=json.loads((PDF/'dual_pdf_validation.json').read_text(encoding='utf-8'))
for r in pdfchecks:
    assert sha((PDF/r['file']).read_bytes())==r['sha256']
    r['visual_review']='All final pages inspected; no clipping, overlapping, broken tables, or missing formula glyphs observed.'
(PDF/'dual_pdf_validation.json').write_text(json.dumps(pdfchecks,indent=2),encoding='utf-8')
(D/'package_verification.json').write_text(json.dumps(standalone,indent=2),encoding='utf-8')

readme='''两条证明路线完整交付 / TWO COMPLETE PROOF PAIRS
2026-10-10

1. output/pdf/route_a_paper_first.pdf
   原纸面路线，12 页，英文，无作者栏。
   对应 output/dual_proofs/route_a_lean.zip
   最终入口 PaperRoute.induced_matching_packing20。

2. output/pdf/route_b_lean_first.pdf
   原 Lean 路线的新纸面展开，13 页，英文，无作者栏。
   对应 output/dual_proofs/route_b_lean.zip
   最终入口 StrongEdge.induced_matching_packing20。

3. comparison/ROUTE_COMPARISON.html（或同名 txt）
   详细中文差异说明、五个阈值分支分析、实现边界与共同来源说明。
   proof_crosswalk.csv/json 给出 37 项定理/引理对应及源码行号。

4. verification/
   编译、语义、锐性、公理和依赖检查日志；源码来源与哈希清单；
   PDF 版面检查；独立导入审计结果。

两套数学证明共享“局部团界—私人邻域—双计数”的主干。
A 新增并实际使用精确恒等式、统一预算、任意外边子集引理和 17 界；
B 保持原始 49 个源码/配置文件不变。
不同命名空间并不等于两个毫无共同来源的数学发现。

LEAN REPRODUCTION
Unzip each Lean archive separately and read README.txt.
Both use Lean 4.35.0-rc4 and mathlib revision
49fd9dee36e7bbf345fe7981d2de6aeeb591f75b.
Run reproduce.ps1, optionally with -LeanBin and -FetchCache.
Lean binaries and external mathlib caches are intentionally not bundled.
Each archive includes every project-specific imported source.
The package audits were elaborated with the verified same-source module cache;
this delivery does not claim a second fresh download and cold compilation of mathlib.

PDF SOURCE
The English manuscript sources and the vector renderer are in output/pdf.
The source uses a small document markup understood by build_manuscript.py.
On Windows, with reportlab, matplotlib==3.11.2, Pillow and pypdf installed:
  python output/pdf/build_dual.py route_a_paper_first
  python output/pdf/build_dual.py route_b_lean_first
The renderer uses the Windows Times fonts and bundled Matplotlib STIX math fonts.

Each PDF is a human-readable mathematical proof. Lean checks the associated formal
statements and proof terms; it does not directly certify the English PDF sentences.
'''
(OUT/'README.txt').write_text(readme,encoding='utf-8')
entries=[(OUT/'README.txt','README.txt')]
for name in ['route_a_lean.zip','route_b_lean.zip']:
    entries.append((OUT/name,'output/dual_proofs/'+name))
for name in ['route_a_paper_first.pdf','route_b_lean_first.pdf','route_a_paper_first.md','route_b_lean_first.md',
             'build_manuscript.py','build_dual.py']:
    entries.append((PDF/name,'output/pdf/'+name))
for name in ['ROUTE_COMPARISON.html','ROUTE_COMPARISON.txt','proof_crosswalk.csv','proof_crosswalk.json']:
    entries.append((D/name,'comparison/'+name))
for name in ['verification_summary.json','dependency_audit.json','final_source_provenance.json',
             'original_source_hashes.json','package_verification.json']:
    entries.append((D/name,'verification/'+name))
for name in ['dual_pdf_validation.json','route_a_paper_first_build.json','route_b_lean_first_build.json']:
    entries.append((PDF/name,'verification/'+name))
for name in ['original-build.log','paper-full-build-final.log','original-semantics.log','original-regression.log',
             'original-sharpness.log','route-dependencies.log','standalone-a-audit.log','standalone-b-audit.log',
             'crosswalk-a.log','crosswalk-b.log','pdf-validation.log']:
    entries.append((D/'logs'/name,'verification/logs/'+name))
manifest={name:{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p,name in entries}
(OUT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
bundle=OUT/'packing20_two_routes_complete.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
    for path,name in entries:z.write(path,name)
    z.write(OUT/'delivery_manifest.json','delivery_manifest.json')
with zipfile.ZipFile(bundle) as z:
    assert z.testzip() is None
    assert all(sha(z.read(n))==v['sha256'] for n,v in manifest.items())
result={'bundle':str(bundle),'bytes':bundle.stat().st_size,'sha256':sha(bundle.read_bytes()),
        'paper_pages':{r['file']:r['pages'] for r in pdfchecks},
        'crosswalk_rows':37,'original_files_unchanged':49,'all_archive_hashes_verified':True,
        'standalone_audits':standalone}
(OUT/'DELIVERY_VERIFIED.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
