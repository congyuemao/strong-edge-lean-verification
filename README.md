# 强边冲突与诱导匹配打包：Lean 验证成果

**无条件修正 19.5 已完成 Lean 形式化：** 对任意最大度至多四的有限简单图和任意候选边集 F，
存在原图诱导匹配 M⊆F，使 `2|F| ≤ 39|M| + t_G(F)`。
修正项严格计数原图中全部边落在 F 内的 C5[2] 连通分量；为零时得到纯 19.5 界。
五个阈值、二十团刚性、实际分量计数及最终组装均已通过内核检查。
详见[完整证明链与复验记录](strong_edge_lean_starter/PACKING195_UNCONDITIONAL.md)及[源码快照](strong_edge_lean_packing195_unconditional_checkpoint.zip)。
当前为 1,197 jobs、75 个 Lean 文件、376 项公理审计，无警告、无证明占位符。以下保留 20-packing 基线的历史说明。

英文完整证明手稿：[PDF（19 页）](output/pdf/packing195_unconditional_manuscript.pdf)、
[可编辑源稿](output/pdf/packing195_unconditional_manuscript.md)、
[自动核对记录](output/pdf/packing195_unconditional_manuscript_validation.json)及
[证明与排版复核记录](output/pdf/packing195_unconditional_manuscript_review.json)。
手稿沿用原英文 PDF 的版式，给出 37 个编号结论的完整论证，并在附录中逐项对应 Lean 模块。
手稿中的数学结论对应已验证的 Lean 定理；英文行文和排版经另外核对，不属于 Lean 内核检查的对象。

验证日期：2026-10-10（Australia/Sydney）。

## 双路线证明与独立审计

20-packing 基线交付包含两份英文手稿及各自对应的完整 Lean 工程。两条路线共享整体打包策略，
区别在局部恒等式、根部计数和阈值引理的组织方式；并非两个完全无关的证明。

| 路线 | 英文手稿 | 对应 Lean 工程 |
|---|---|---|
| A：原纸面路线的严格形式化 | [PDF](output/pdf/route_a_paper_first.pdf) | [源码 ZIP](output/dual_proofs/route_a_lean.zip) |
| B：原 Lean 路线的完整纸面证明 | [PDF](output/pdf/route_b_lean_first.pdf) | [源码 ZIP](output/dual_proofs/route_b_lean.zip) |

- [完整交付包](output/dual_proofs/packing20_two_routes_complete.zip)及[交付说明](output/dual_proofs/README.txt)
- [两条路线的详细比较](dual_proofs/ROUTE_COMPARISON.txt)及[逐项证明对应表](dual_proofs/proof_crosswalk.csv)
- [构建与审计汇总](dual_proofs/verification_summary.json)、[依赖审计](dual_proofs/dependency_audit.json)及[源码溯源](dual_proofs/final_source_provenance.json)
- [独立审计目录](audit_packing20/README.md)，含语义、复现与 Joos 2016 原创性核查材料

两份源码包各带复现脚本和哈希清单，其内容及独立审计原样保留。
主工程新增 19.5 模块，原有 44 个 Lean 模块和四个环境文件保持原样，公共入口仅追加导入；
下文的 45 个文件、1,170 jobs 和 225 项公理审计数字对应原始 high20 阶段。
编译器、依赖缓存及临时渲染文件不纳入仓库。

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
| 无条件打包 | 对任意 F，存在诱导匹配 M⊆F，且 \|F\|≤20\|M\| | `induced_matching_packing20` |

完整签名及证明说明见 [HIGH20_VERIFIED_HANDOFF.md](strong_edge_lean_starter/HIGH20_VERIFIED_HANDOFF.md)。
该历史基线不涉及整数强边二十色或算法复杂度结论；修正 19.5 加强已在本页顶部链接的最新阶段完成。

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

| 阶段 | 主要成果 | 构建 jobs | 审计项数 | 源码与证据快照 |
|---|---|---:|---:|---|
| 初始核验 | 通用交换、双重计数、条件性打包 | 1,124 | 13 | [verified checkpoint](strong_edge_lean_verified_checkpoint.zip) |
| C4 | 完整冲突度 ≤24、取等结构、最小阈值接口 | 1,127 | 38 | [C4 checkpoint](strong_edge_lean_c4_checkpoint.zip) |
| C5 high24 | 强团 ≤13，接入所需 ≤15 | 1,129 | 51 | [high24 checkpoint](strong_edge_lean_high24_checkpoint.zip) |
| C5 high23 | 强团 ≤16，剩三项结构假设 | 1,136 | 94 | [high23 checkpoint](strong_edge_lean_high23_checkpoint.zip) |
| C5 high22 | 强团 ≤17，剩两项结构假设 | 1,144 | 145 | [high22 checkpoint](strong_edge_lean_high22_checkpoint.zip) |
| C5 high21 | 强团 ≤18，剩 high20 一项结构假设 | 1,162 | 192 | [high21 checkpoint](strong_edge_lean_high21_checkpoint.zip) |
| C5 high20 / C6 | 强团 ≤19，无条件任意候选集 20-packing | 1,170 | 225 | [high20 checkpoint](strong_edge_lean_high20_checkpoint.zip) |
| PACKING19.5 续进 | 条件性 T1/T2、high20 ≤18、high23 ≤15；完整无条件 19.5 待完成 | 1,175 | 原有 225 + 新增 22 | [packing195 checkpoint](strong_edge_lean_packing195_checkpoint.zip) |
| PACKING19.5 第二阶段 | high21 ≤17、次三次强团 ≤17、high22 四边星根 ≤16；剩余接口缩减 | 1,181 | 225 + 22 + 31（含三个新定义） | [续进 checkpoint](strong_edge_lean_packing195_continuation_checkpoint.zip) |
| PACKING19.5 完成 | 五阈值、C5[2] 刚性、实际连通分量计数与无条件修正界 | 1,197 | 376 项 | [无条件 checkpoint](strong_edge_lean_packing195_unconditional_checkpoint.zip) |

这些数字来自各阶段实际日志。历史 ZIP、交接和验证日志均未覆盖；当前仓库共保留十个阶段快照。

## 导航

- [Lean 项目说明](strong_edge_lean_starter/README.md)
- [成果与证据索引](docs/RESULTS_INDEX.md)
- [手稿与两边 Lean 证明的合并保留核验](docs/MERGE_VERIFICATION.json)
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
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Audit195.lean
.\lean.ps1 env lean StrongEdge/Audit195Continuation.lean
.\lean.ps1 env lean StrongEdge/Audit195Thresholds.lean
.\lean.ps1 env lean StrongEdge/Audit195Unconditional.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
.\lean.ps1 env lean StrongEdge/Tests195.lean
.\lean.ps1 env lean StrongEdge/Tests195Unconditional.lean
```

其他系统使用 `lake build` 和 `lake env lean`；依赖缓存命令见
[项目 README](strong_edge_lean_starter/README.md#reproduce)。编译器、依赖树和缓存不包含在源码快照中。

在仓库根目录运行 `python scripts/verify_archive.py` 核对文件清单与历史证据。
该脚本不能替代 Lean 内核检查。`.gitattributes` 保留原始换行字节，以维护历史散列。

## 当前边界

无条件 20-packing 和带紧分量修正项的无条件 19.5-packing 均已完成，无剩余结构假设。
19.5 的五个阈值、二十团刚性和实际原图连通分量计数均已完成；修正项为零时得到纯 19.5 界。
C5[2] 回归验证了修正项不可直接省略。
两份手稿与 A/B 证明对应此前的无条件 20-packing；本次结果不宣称解决整数强边二十色。
历史交接中的“尚需 high20”或“完整无条件 19.5 待完成”对应各自阶段，最新状态见本页顶部的完成记录。
