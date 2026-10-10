"""Update current project documentation after the final high20 audit passes."""
from pathlib import Path
import re

project = Path(__file__).resolve().parents[1]
repo = project.parent


def read(path):
    return path.read_text(encoding="utf-8-sig")


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


assert int(read(project / "verification/high20-build-exit-code.txt")) == 0
assert int(read(project / "verification/high20-audit-exit-code.txt")) == 0
assert "Build completed successfully (1170 jobs)" in read(project / "verification/high20-build.log")
assert len(re.findall(r"'([^']+)' depends on axioms:", read(project / "verification/high20-axioms.log"))) == 225

write(project / "README.md", """# Strong-edge packing: Lean formalisation

**Unconditional induced-matching 20-packing is proved.** For every finite simple
graph G of original maximum degree at most four and every candidate edge set F,
there is an induced matching M⊆F with |F|≤20|M|. All conflicts are evaluated in
the whole original graph, retaining edges outside the candidate set as witnesses.

Verified on 10 October 2026 (Australia/Sydney): the full build passed with
**1,170 jobs**, without warnings. All **225 audited declarations** use only
`propext`, `Classical.choice` and `Quot.sound`. The high20 stage adds 33 theorems
in eight modules. All 35 previous mathematical/test modules are unchanged.

See [HIGH20_VERIFIED_HANDOFF.md](HIGH20_VERIFIED_HANDOFF.md) for exact exported
types, the proof, complete new theorem inventory and preservation checks.
Evidence: [build](verification/high20-build.log), [audit](verification/high20-axioms.log),
[source checks](verification/high20-source-checks.json),
[source hashes](verification/high20-source-sha256.json), and
[checkpoint](../strong_edge_lean_high20_checkpoint.zip).

## Checked endpoint

```lean
theorem StrongEdge.induced_matching_packing20
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧
      StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧ F.card ≤ 20 * M.card
```

The constructor `minimalCliqueBounds20_of_maxDegree_four` supplies all five
clique bounds from hΔ. There is no additional structural parameter in the final
packing theorem, and empty graphs or candidate sets need no exception.
The older conditional wrappers remain available and unchanged.

| Field | Full conflict degree threshold | Required clique bound | Verified bound |
|---|---:|---:|---:|
| high20 | ≥20 | ≤19 | ≤19 |
| high21 | ≥21 | ≤18 | ≤18 |
| high22 | ≥22 | ≤17 | ≤17 |
| high23 | ≥23 | ≤16 | ≤16 |
| high24 | ≥24 | ≤15 | ≤13 |

C4 separately proves full conflict degree at most 24. The weaker
`MinimalCliqueBounds20` interface suffices; the older `CliqueThresholds20`
record's stronger high24 ≤7 field is not asserted.

## New proof modules

- `Bounds/High20Local`: triangle-cover counting, derived root-neighbourhood
  independence, threshold-free multiple-tip counts and the four-loss label budget.
- `Bounds/High20Four`: handles a root type of size four.
- `Bounds/High20TwoTriples`: handles two distinct types of size at least three.
- `Bounds/High20Outer`: at most four outer edges avoiding a distinguished tip
  when all other types have size at most two.
- `Bounds/High20Slots`: original label slots and missing selected edges.
- `Bounds/High20UniqueTriple`: ten root edges and five outer edges in the unique
  triple case, giving 19 together with the four root-star edges.
- `Bounds/High20`: combines the cases with the previously proved threshold-free
  subcubic bound to export `high20_clique_card_le_nineteen`.
- `High20Packing`: the unconditional threshold constructor and packing theorem.

The definitions in `Basic` and `Conflict`, generic packing and exchange proofs,
and all high21–high24 modules are unchanged. The selected-bipartition and fully
selected double-tip bounds from high21 are reused under their actual hypotheses.
The proof does not require a double-C5 classification or the stronger high20 ≤18.

Earlier module inventories and stage-specific claims remain in
[high21](C5_HIGH21_VERIFIED_HANDOFF.md), [high22](HIGH22_HANDOFF.md),
[high23](HIGH23_HANDOFF.md), [high24](verification/high24-handoff.md), and
[C4](verification/NEXT_STAGE_REPORT.md). Historical conditional descriptions in
those files describe their respective stages.

## Pinned environment

- Lean: `leanprover/lean4:v4.35.0-rc4`.
- Compiler commit: `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`.
- mathlib: `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`.
- Dependency lockfile: `lake-manifest.json`.

The Windows wrapper uses `../.tools/lean-4.35.0-rc4-windows` when available,
otherwise Lake from PATH. The original compiler download has SHA-256
`549c0d70f58346be61d9353b5ff8b3d89430b49184d1833244ba2f3afca3dabd`.
Binaries, dependency checkouts and caches are excluded from the checkpoint.

## Reproduce

From this directory in Windows PowerShell:

```powershell
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
.\\lean.ps1 env lean StrongEdge/Tests.lean
```

With Lean/elan on another system:

```sh
lake exe cache get Mathlib.Combinatorics.SimpleGraph.Clique Mathlib.Combinatorics.SimpleGraph.LineGraph Mathlib.Tactic.ByContra Mathlib.Tactic.Linarith Mathlib.Tactic.Tauto Mathlib.Algebra.Order.BigOperators.Group.Finset
lake build
lake env lean StrongEdge/Audit.lean
lake env lean StrongEdge/Tests.lean
```

Keep the supplied lockfile. The first build may need network access for locked
dependencies. `Tests.lean` checks the four-vertex-path conflict regression using
kernel-checked computation. The final audit preserves all 192 previous entries
and checks all 33 new theorem signatures and dependency closures.

After saving successful logs and exit codes, run
`python verification/finalize-high20.py` to validate the evidence and package a
source-only checkpoint. From the repository root, `python scripts/verify_archive.py`
checks the inventory. These scripts inspect saved evidence and do not replace Lean.

## Scope

This completes the requested high20/C6 packing stage. Integer strong-edge
20-colourability, the 19.5 strengthening, a polynomial-time algorithm proof and
literature originality are separate questions. The optional stronger bounds
high20 ≤18, high21 ≤17, high22 ≤16, high23 ≤15 and threshold-free subcubic ≤17
are not exported. The proved threshold-free subcubic bound is 18.

The supplied brief and pinned research sources are indexed in
[the verified handoff](HIGH20_VERIFIED_HANDOFF.md). Their suggested arguments and
claims are distinguished from the actual Lean statements and proof dependencies.
""")

old_readme = read(repo / "README.md")
history = old_readme.split("| 阶段 |", 1)[1].split("\n\n这些数字", 1)[0]
history = "| 阶段 |" + history
if "| C5 high20 / C6 |" not in history:
    history += "\n| C5 high20 / C6 | 强团 ≤19，无条件任意候选集 20-packing | 1,170 | 225 | [high20 checkpoint](strong_edge_lean_high20_checkpoint.zip) |"
write(repo / "README.md", """# 强边冲突与诱导匹配打包：Lean 验证成果

验证日期：2026-10-10（Australia/Sydney）。

**无条件诱导匹配 20-packing 已完成 Lean 验证。** 对任意有限简单图 G，
若每个原顶点度数至多四，则对任意候选边集 F，存在诱导匹配 M⊆F，使 |F|≤20|M|。
冲突始终在完整原图中定义，候选边集外的原边仍可作为冲突见证。

C4 和 C5 的五个阈值界均已完成。最终定理只需原图最大度数条件及普通有限性、
可判定性实例，不再要求任何额外的 high20 假设。

## 当前已验证结论

| 内容 | 已验证结论 | 主声明 |
|---|---|---|
| C4 | 完整冲突度 ≤24 | `conflict_degree_le_24` |
| high24 | 成员完整冲突度 ≥24 的团大小 ≤13，满足所需 ≤15 | `high24_clique_card_le_thirteen` |
| high23 | 成员完整冲突度 ≥23 的团大小 ≤16 | `high23_clique_card_le_sixteen` |
| high22 | 成员完整冲突度 ≥22 的团大小 ≤17 | `high22_clique_card_le_seventeen` |
| high21 | 成员完整冲突度 ≥21 的团大小 ≤18 | `high21_clique_card_le_eighteen` |
| high20 | 成员完整冲突度 ≥20 的团大小 ≤19 | `high20_clique_card_le_nineteen` |
| 无条件打包 | 对任意 F，存在诱导匹配 M⊆F，且 \\|F\\|≤20\\|M\\| | `induced_matching_packing20` |

完整签名及证明说明见 [HIGH20_VERIFIED_HANDOFF.md](strong_edge_lean_starter/HIGH20_VERIFIED_HANDOFF.md)。
本结果不宣称整数强边二十色、19.5 加强或算法复杂度结论。

## 验证证据

- **45 个 Lean 源文件**，49 项源码及配置 SHA-256。
- 完整构建通过：**1,170 jobs，无警告**。
- **225 项公理审计**均仅使用 `propext`、`Classical.choice`、`Quot.sound`。
- 新增八个模块、33 个定理，旧有 192 项审计全部保留。
- 35 个既有数学及测试模块、全部版本锁定文件和六个历史 checkpoint 原样保留。
- 四顶点路径回归通过；源码扫描未发现证明缺口标记。

原始证据：[构建](strong_edge_lean_starter/verification/high20-build.log)、
[公理审计](strong_edge_lean_starter/verification/high20-axioms.log)、
[源码 SHA-256](strong_edge_lean_starter/verification/high20-source-sha256.json)、
[状态](strong_edge_lean_starter/verification/high20-status.json)。
仓库归档清单：[ARCHIVE_MANIFEST.json](docs/ARCHIVE_MANIFEST.json)。

## 阶段与交付物

""" + history + """

这些数字来自各阶段实际日志。历史 ZIP、交接和验证日志均未覆盖；当前仓库共保留七个阶段快照。

## 导航

- [Lean 项目说明](strong_edge_lean_starter/README.md)
- [成果与证据索引](docs/RESULTS_INDEX.md)
- [high20 / C6 完整交接](strong_edge_lean_starter/HIGH20_VERIFIED_HANDOFF.md)
- [high21 交接](strong_edge_lean_starter/C5_HIGH21_VERIFIED_HANDOFF.md)
- [high22 交接](strong_edge_lean_starter/HIGH22_HANDOFF.md)
- [原始输入说明](docs/inputs/README.md)

## 复现

固定 Lean `v4.35.0-rc4`，编译器提交
`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`，mathlib 提交
`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`。保留现有 lockfile。

```powershell
cd strong_edge_lean_starter
.\\lean.ps1 build
.\\lean.ps1 env lean StrongEdge/Audit.lean
.\\lean.ps1 env lean StrongEdge/Tests.lean
```

其他系统使用 `lake build` 和 `lake env lean`；依赖缓存命令见
[项目 README](strong_edge_lean_starter/README.md#reproduce)。编译器、依赖树和缓存不包含在源码快照中。

在仓库根目录运行 `python scripts/verify_archive.py` 核对文件清单与历史证据。
该脚本不能替代 Lean 内核检查。`.gitattributes` 保留原始换行字节，以维护历史散列。

## 当前边界

本次要求的 high20 和无条件 20-packing 阶段已完成，无剩余结构假设。
整数强边二十色、19.5 加强、完整极值图分类和更强阈值界留作独立项目。
历史交接中“尚需 high20”的表述对应各自阶段，不代表当前结果。
""")

s = read(repo / "docs/RESULTS_INDEX.md")
s = s.replace("新增 high21 证明；26 个既有数学模块、历史日志、交接与五个旧 checkpoint 保持原样。",
              "新增 high20 及无条件 20-packing 证明；35 个既有数学及测试模块、历史日志、交接与六个旧 checkpoint 保持原样。")
if "| high20 / C6 |" not in s:
    s = s.replace("| 入口与审计 |", "| high20 / C6 | `Bounds/High20Local`、`Bounds/High20Four`、`Bounds/High20TwoTriples`、`Bounds/High20Outer`、`Bounds/High20Slots`、`Bounds/High20UniqueTriple`、`Bounds/High20`、`High20Packing` | 四次损失预算、三点类型计数、high20 ≤19 及无条件任意候选集 20-packing |\n| 入口与审计 |")
s = s.replace("192 项依赖审计", "225 项依赖审计")
if "| high20 | [status]" not in s:
    s = s.replace("\n\n历史散列", "\n| high20 | [status](../strong_edge_lean_starter/verification/high20-status.json) | [build](../strong_edge_lean_starter/verification/high20-build.log) | [axioms](../strong_edge_lean_starter/verification/high20-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high20-source-sha256.json) |\n\n历史散列")
s = s.replace("当前工作树以 high21 清单为准", "当前工作树以 high20 清单为准").replace("三份打包脚本", "各阶段打包脚本")
if "- [high20 / C6 交接]" not in s:
    s = s.replace("- [用户提供的原始输入]", "- [high20 / C6 交接](../strong_edge_lean_starter/HIGH20_VERIFIED_HANDOFF.md)\n- [用户提供的原始输入]")
s = s.replace("三份 high22 阶段参考稿的本地副本保存在 `verification/high22-research-*.md`。",
              "high22 参考稿保存在 `verification/high22-research-*.md`；本次两份 high20 参考稿保存在 `verification/high20-research-*.md`。")
s = s[:s.index("## 当前边界")] + """## 当前边界

已证阈值：high24 ≤13、high23 ≤16、high22 ≤17、high21 ≤18、high20 ≤19。
`induced_matching_packing20` 对每个候选边集 F 给出无条件 20-packing；仅需原图最大度数 ≤4。
整数强边二十色、19.5 加强和算法复杂度结论不在本次结果内。

本次新增 33 项已核验定理，未改动既有数学模块，也未覆盖旧 checkpoint。
完整源码散列与归档核验结果见 [ARCHIVE_MANIFEST.json](ARCHIVE_MANIFEST.json)。
"""
write(repo / "docs/RESULTS_INDEX.md", s)

s = read(repo / "docs/inputs/README.md")
if "| [high20 最终工作说明]" not in s:
    s = s.replace("\n\n这些输入文件", "\n| [high20 最终工作说明](CODEX_LEAN_C5_HIGH20_FINAL_PROMPT.md) | 用户指定的 `CODEX_LEAN_C5_HIGH20_FINAL_PROMPT.md`；按原始字节保存 |\n\n这些输入文件")
write(repo / "docs/inputs/README.md", s)
print("Updated current documentation for high20 and unconditional 20-packing.")
