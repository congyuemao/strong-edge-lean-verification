"""Update current navigation; preserve historical handoffs and evidence."""
from pathlib import Path

project = Path(__file__).resolve().parents[1]
repo = project.parent


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


s = read(project / "README.md")
start, rest = s.split("## Verified mathematical core", 1)
start = """# Strong-edge packing: Lean formalisation

C4 and the `high24`, `high23`, `high22`, and `high21` clique bounds are complete.
In every finite simple graph of original maximum degree four, full conflict degree
is at most 24. The verified clique bounds are 13 at threshold 24, 16 at threshold 23,
17 at threshold 22, and **18 at threshold 21**.

Verified on 10 October 2026 (Australia/Sydney): the full build passed with
**1,162 jobs**, without warnings, and all **192 audited declarations** use only
`propext`, `Classical.choice`, and `Quot.sound`. The high21 stage adds 47 theorems
in nine modules. All 26 earlier mathematical modules remain byte-for-byte unchanged.

The packing theorem remains **conditional on high20**, the only remaining structural
premise. Unconditional 20-packing, the 19.5 strengthening, and integer strong-edge
20-colourability are not proved. The new threshold-free subcubic bound is 18;
the stronger bound 17 and optional high21 bound 17 have not been claimed.

See [C5_HIGH21_VERIFIED_HANDOFF.md](C5_HIGH21_VERIFIED_HANDOFF.md) for complete theorem
types, proof explanations, preservation checks and reproduction commands. Evidence:
[build](verification/high21-build.log), [audit](verification/high21-axioms.log),
[source checks](verification/high21-source-checks.json), and
[checkpoint](../strong_edge_lean_high21_checkpoint.zip).

Earlier handoffs remain intact: [high22](HIGH22_HANDOFF.md), [high23](HIGH23_HANDOFF.md),
[high24](verification/high24-handoff.md), and [C4](verification/NEXT_STAGE_REPORT.md).

"""
s = start + "## Verified mathematical core" + rest
s = s.replace("a threshold-free subcubic bound is not claimed.", "the new threshold-free bound 18 is proved separately in `SubcubicEighteen`.")
anchor = "\n`Packing.lean` extends"
new_modules = """
- `Bounds/High21Local` and `Bounds/High21Support`: local and root-label three-loss budgets.
- `Bounds/SubcubicEighteen`: threshold-free bound 18 for selected support degrees at most three.
- `Bounds/High21LargeType`: bound 18 when a four-edge root has a type of size at least three.
- `Bounds/DegreeTwoClique`: bound four with internal original degree at most two and a selected bipartition.
- `Bounds/High21Double`: at most four fully selected double tips.
- `Bounds/High21RootFour`: bound 18 for every four-edge root.
- `Bounds/High21`: universal `high21_clique_card_le_eighteen`.
- `High21Packing`: supplies high21 and exports packing with only high20 explicit.
"""
if "- `Bounds/High21Local` and" not in s:
    s = s.replace(anchor, new_modules + anchor)
s = s.replace("all eighteen earlier mathematical source modules", "all 26 earlier mathematical source modules")
s = s.replace("without the two remaining\nclique hypotheses", "without the remaining\nhigh20 hypothesis")
s = s.replace("`StrongEdge.induced_matching_packing20_of_high20_high21`", "`StrongEdge.induced_matching_packing20_of_high20`")
s = s.replace("exactly two explicit clique-bound\nparameters", "exactly one explicit clique-bound\nparameter")
s = s.replace("by supplying `high22_clique_card_le_seventeen`", "by supplying `high21_clique_card_le_eighteen`, `high22_clique_card_le_seventeen`")
s = s.replace("discharges its high22, high23,\nand high24 fields and retains high20 and high21 explicitly", "discharges its high21, high22, high23,\nand high24 fields and retains high20 explicitly")
s = s.replace("twenty-eight project Lean files", "37 project Lean files")
s = s.replace("verification/high22-source-sha256.json", "verification/high21-source-sha256.json")
s = s.replace("The last three have now been proved universally.", "The last four have now been proved universally.")
s = s.replace("| `high21` | 21 | 18 | Open |", "| `high21` | 21 | 18 | Proved |")
s = s.replace("Next, formalise `high21`, followed by `high20`.\nDischarging the two open fields", "Next, formalise `high20`.\nDischarging the last open field")
s += """
The high21 proof uses the same pinned threshold manuscript and shorter counting
arguments documented in `C5_HIGH21_VERIFIED_HANDOFF.md`. Run
`python verification/finalize-high21.py` after the Lean commands to check saved
evidence and package the source-only checkpoint. This script does not prove mathematics.
""" if "The high21 proof uses the same pinned" not in s else ""
write(project / "README.md", s)

s = read(repo / "README.md")
s = s.replace("最近一次数学验证完成于 2026-10-09", "最近一次数学验证完成于 2026-10-10")
s = s.replace("和五个历史 checkpoint", "和六个阶段 checkpoint")
s = s.replace("high24、high23、high22 三个强团界", "high24、high23、high22、high21 四个强团界")
s = s.replace("**high21 和 high20 仍未完成，无条件 20-packing 尚未证明。**", "**仅 high20 仍未完成；无条件 20-packing 尚未证明。**")
if "| high21 强团界 |" not in s:
    s = s.replace("| 条件性打包 |", "| high21 强团界 | 每条成员冲突度 ≥21 的团，边数 ≤18 | `high21_clique_card_le_eighteen` |\n| 条件性打包 |")
s = s.replace("`induced_matching_packing20_of_high20_high21`", "`induced_matching_packing20_of_high20`")
s = s.replace("最后一项仍显式要求 high20（阈值 20 时团大小 ≤19）和 high21（阈值 21 时团大小 ≤18）。", "最后一项只显式要求 high20（阈值 20 时团大小 ≤19）。")
s = s.replace("最新完整定理签名见 [HIGH22_HANDOFF.md](strong_edge_lean_starter/HIGH22_HANDOFF.md)。", "最新完整定理签名见 [C5_HIGH21_VERIFIED_HANDOFF.md](strong_edge_lean_starter/C5_HIGH21_VERIFIED_HANDOFF.md)。")
s = s.replace("**28 个 Lean 源文件**", "**37 个 Lean 源文件**").replace("**1,144 jobs，无警告**", "**1,162 jobs，无警告**").replace("**145 项公理审计**", "**192 项公理审计**")
s = s.replace("本次整理核对了当前源码与 high22 散列清单，以及 high22 checkpoint 中全部文件的字节一致性。", "本次核对了当前源码与 high21 散列清单；26 个既有数学模块及全部历史 checkpoint 均保持原样。")
for suffix in ["build.log", "axioms.log", "source-sha256.json"]:
    s = s.replace("verification/high22-" + suffix, "verification/high21-" + suffix)
if "| C5 high21 |" not in s:
    s = s.replace("\n\n这些数字", "\n| C5 high21 | 强团 ≤18，剩 high20 一项结构假设 | 1,162 | 192 | [high21 checkpoint](strong_edge_lean_high21_checkpoint.zip) |\n\n这些数字")
if "- [high21 完整交接]" not in s:
    s = s.replace("- [high22 完整交接]", "- [high21 完整交接](strong_edge_lean_starter/C5_HIGH21_VERIFIED_HANDOFF.md)\n- [high22 完整交接]")
s = s.replace("先证明 high21 ≤18，再证明 high20 ≤19，并接入现有最小阈值记录。\nhigh22 的支撑度至多三分支仍使用 high22 假设；不能将其当作已证明的无阈值通用次三次图定理。", "下一步证明 high20 ≤19，并接入现有最小阈值记录。\n本次另已证明：无需冲突度阈值，选中边关联度至多三时团大小 ≤18。更强的无阈值 ≤17 尚未证明。")
write(repo / "README.md", s)

s = read(repo / "docs/RESULTS_INDEX.md")
s = s.replace("现有数学源码、历史日志、交接文件与五个 checkpoint 保持原样。", "新增 high21 证明；26 个既有数学模块、历史日志、交接与五个旧 checkpoint 保持原样。")
if "| high21 | `Bounds/High21Local`" not in s:
    s = s.replace("| 入口与审计 |", "| high21 | `Bounds/High21Local`、`Bounds/High21Support`、`Bounds/SubcubicEighteen`、`Bounds/High21LargeType`、`Bounds/DegreeTwoClique`、`Bounds/High21Double`、`Bounds/High21RootFour`、`Bounds/High21`、`High21Packing` | 三次损失预算、无阈值次三次 ≤18、high21 ≤18 及仅需 high20 的包装器 |\n| 入口与审计 |")
s = s.replace("145 项依赖审计", "192 项依赖审计")
if "| high21 | [status]" not in s:
    line = "| high21 | [status](../strong_edge_lean_starter/verification/high21-status.json) | [build](../strong_edge_lean_starter/verification/high21-build.log) | [axioms](../strong_edge_lean_starter/verification/high21-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high21-source-sha256.json) |"
    s = s.replace("\n\n历史散列", "\n" + line + "\n\n历史散列")
s = s.replace("当前工作树以 high22 清单为准", "当前工作树以 high21 清单为准").replace("两份打包脚本", "三份打包脚本")
if "- [high21 交接]" not in s:
    s = s.replace("- [high22 交接](../strong_edge_lean_starter/HIGH22_HANDOFF.md)", "- [high22 交接](../strong_edge_lean_starter/HIGH22_HANDOFF.md)\n- [high21 交接](../strong_edge_lean_starter/C5_HIGH21_VERIFIED_HANDOFF.md)")
s = s.replace("已证阈值：high24 ≤13、high23 ≤16、high22 ≤17。\n尚需证明：high21 ≤18、high20 ≤19。\n当前导出的是带这两个显式结构条件的 20-packing；", "已证阈值：high24 ≤13、high23 ≤16、high22 ≤17、high21 ≤18。\n尚需证明：high20 ≤19。\n当前导出的是仅带 high20 显式结构条件的 20-packing；")
s = s.replace("本次整理没有改动数学证明，也没有重新生成或覆盖旧 checkpoint。", "本次新增 47 项已核验定理，未改动既有数学模块，也未覆盖旧 checkpoint。")
write(repo / "docs/RESULTS_INDEX.md", s)

s = read(repo / "docs/inputs/README.md")
if "| [high21 工作说明]" not in s:
    s = s.replace("\n\n这些输入文件", "\n| [high21 工作说明](CODEX_LEAN_C5_HIGH21_NEXT_PROMPT.md) | 用户指定的 `CODEX_LEAN_C5_HIGH21_NEXT_PROMPT (8).md`；按原始字节保存 |\n\n这些输入文件")
write(repo / "docs/inputs/README.md", s)
print("Updated current documentation for high21.")
