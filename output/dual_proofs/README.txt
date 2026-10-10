两条证明路线完整交付 / TWO COMPLETE PROOF PAIRS
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
