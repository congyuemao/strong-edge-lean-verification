# 成果与证据索引

## 合并后的最新内容

- 双路线手稿与配套证明：[A 手稿](../output/pdf/route_a_paper_first.pdf)、[A Lean](../output/dual_proofs/route_a_lean.zip)、[B 手稿](../output/pdf/route_b_lean_first.pdf)、[B Lean](../output/dual_proofs/route_b_lean.zip)，以及[独立审计](../audit_packing20/README.md)。
- PACKING19.5：[进展](../strong_edge_lean_starter/PACKING195_PROGRESS.md)、[剩余目标](../strong_edge_lean_starter/PACKING195_BLOCKERS.md)、[源码快照](../strong_edge_lean_packing195_checkpoint.zip)。
- 主工程共有 51 个 Lean 文件；1,175 jobs 构建通过，原有 225 项和新增 22 项审计均保留。
- 当前工作树散列以 [packing195-source-sha256.json](../strong_edge_lean_starter/verification/packing195-source-sha256.json) 为准；完整无条件 19.5 尚未完成。

以下记录保留 high20 阶段的原始成果与证据。

整理日期：2026-10-10。新增 high20 及无条件 20-packing 证明；35 个既有数学及测试模块、历史日志、交接与六个旧 checkpoint 保持原样。

## 数学模块

所有路径均相对于 `strong_edge_lean_starter/StrongEdge/`。

| 组别 | 模块 | 作用 |
|---|---|---|
| 通用基础 | `Basic`、`Conflict`、`PrivateExchange`、`DoubleCount`、`Packing`、`Tests` | 完整冲突、候选限制、交换、计数、条件性打包及基本例子 |
| C4 | `Bounds/ConflictDegree`、`Bounds/ConflictRigidity` | 完整冲突度上界和 24 度取等结构 |
| 最小接口 | `MinimalPacking` | 只需 high24 ≤15 的五阈值打包接口 |
| high24 | `Bounds/High24`、`High24Packing` | high24 ≤13，以及保留四项结构参数的包装器 |
| high23 | `Bounds/EdgeCounting`、`Bounds/High23Local`、`Bounds/High23Support`、`Bounds/High23Outer`、`Bounds/High23Four`、`Bounds/High23`、`High23Packing` | 精确关联计数、一次损失预算、high23 ≤16 及三参数包装器 |
| high22 | `Bounds/High22Local`、`Bounds/RootCounting`、`Bounds/High22Support`、`Bounds/High22RootFour`、`Bounds/High22Heavy`、`Bounds/High22Subcubic`、`Bounds/High22`、`High22Packing` | 两次损失预算、根类型计数、high22 ≤17 及两参数包装器 |
| high21 | `Bounds/High21Local`、`Bounds/High21Support`、`Bounds/SubcubicEighteen`、`Bounds/High21LargeType`、`Bounds/DegreeTwoClique`、`Bounds/High21Double`、`Bounds/High21RootFour`、`Bounds/High21`、`High21Packing` | 三次损失预算、无阈值次三次 ≤18、high21 ≤18 及仅需 high20 的包装器 |
| high20 / C6 | `Bounds/High20Local`、`Bounds/High20Four`、`Bounds/High20TwoTriples`、`Bounds/High20Outer`、`Bounds/High20Slots`、`Bounds/High20UniqueTriple`、`Bounds/High20`、`High20Packing` | 四次损失预算、三点类型计数、high20 ≤19 及无条件任意候选集 20-packing |
| 入口与审计 | `../StrongEdge.lean`、`Audit` | 公开导入、225 项依赖审计和完整签名输出 |

[浏览全部源码](../strong_edge_lean_starter/StrongEdge/)。

## 各阶段的最终验证记录

| 阶段 | 状态 | 构建日志 | 公理审计 | 源码散列 |
|---|---|---|---|---|
| 初始核验 | [status](../strong_edge_lean_starter/verification/status.json) | [build](../strong_edge_lean_starter/verification/build.log) | [axioms](../strong_edge_lean_starter/verification/axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/source-sha256.json) |
| C4 | [status](../strong_edge_lean_starter/verification/next-stage-status.json) | [build](../strong_edge_lean_starter/verification/next-stage-build.log) | [axioms](../strong_edge_lean_starter/verification/next-stage-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/next-stage-source-sha256.json) |
| high24 | [status](../strong_edge_lean_starter/verification/high24-status.json) | [build](../strong_edge_lean_starter/verification/high24-build.log) | [axioms](../strong_edge_lean_starter/verification/high24-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high24-source-sha256.json) |
| high23 | [status](../strong_edge_lean_starter/verification/high23-status.json) | [build](../strong_edge_lean_starter/verification/high23-build.log) | [axioms](../strong_edge_lean_starter/verification/high23-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high23-source-sha256.json) |
| high22 | [status](../strong_edge_lean_starter/verification/high22-status.json) | [build](../strong_edge_lean_starter/verification/high22-build.log) | [axioms](../strong_edge_lean_starter/verification/high22-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high22-source-sha256.json) |
| high21 | [status](../strong_edge_lean_starter/verification/high21-status.json) | [build](../strong_edge_lean_starter/verification/high21-build.log) | [axioms](../strong_edge_lean_starter/verification/high21-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high21-source-sha256.json) |
| high20 | [status](../strong_edge_lean_starter/verification/high20-status.json) | [build](../strong_edge_lean_starter/verification/high20-build.log) | [axioms](../strong_edge_lean_starter/verification/high20-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high20-source-sha256.json) |

历史散列应与相应阶段 ZIP 比较；high20 清单对应 high20 快照。
`verification/` 还保留各阶段基线日志、真实源码 diff、文件变动摘要、开发中间日志和各阶段打包脚本。
中间日志中的历史错误或警告不代表最终构建状态；上表链接的是最终验证记录。

## 交接和原始来源

- [最初项目交接](../strong_edge_lean_starter/LEAN_20_PACKING_HANDOFF.md)
- [C4 报告](../strong_edge_lean_starter/verification/NEXT_STAGE_REPORT.md)
- [high24 交接](../strong_edge_lean_starter/verification/high24-handoff.md)
- [high23 交接](../strong_edge_lean_starter/HIGH23_HANDOFF.md)
- [high22 交接](../strong_edge_lean_starter/HIGH22_HANDOFF.md)
- [high21 交接](../strong_edge_lean_starter/C5_HIGH21_VERIFIED_HANDOFF.md)
- [high20 / C6 交接](../strong_edge_lean_starter/HIGH20_VERIFIED_HANDOFF.md)
- [用户提供的原始输入](inputs/README.md)

研究来源固定在公开仓库提交
[`3a95c4a9c44475196c42b6eab4749c487d15d59b`](https://github.com/congyuemao/strong-edge-colouring-research/tree/3a95c4a9c44475196c42b6eab4749c487d15d59b)。
high22 参考稿保存在 `verification/high22-research-*.md`；本次两份 high20 参考稿保存在 `verification/high20-research-*.md`。
研究稿或提示词中的建议、声称和未完成目标不等同于已核验成果。

## 当前边界

已证阈值：high24 ≤13、high23 ≤16、high22 ≤17、high21 ≤18、high20 ≤19。
`induced_matching_packing20` 对每个候选边集 F 给出无条件 20-packing；仅需原图最大度数 ≤4。
整数强边二十色、19.5 加强和算法复杂度结论不在本次结果内。

本次新增 33 项已核验定理，未改动既有数学模块，也未覆盖旧 checkpoint。
完整源码散列与归档核验结果见 [ARCHIVE_MANIFEST.json](ARCHIVE_MANIFEST.json)。
