# 成果与证据索引

整理日期：2026-10-10。现有数学源码、历史日志、交接文件与五个 checkpoint 保持原样。

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
| 入口与审计 | `../StrongEdge.lean`、`Audit` | 公开导入、145 项依赖审计和完整签名输出 |

[浏览全部源码](../strong_edge_lean_starter/StrongEdge/)。

## 各阶段的最终验证记录

| 阶段 | 状态 | 构建日志 | 公理审计 | 源码散列 |
|---|---|---|---|---|
| 初始核验 | [status](../strong_edge_lean_starter/verification/status.json) | [build](../strong_edge_lean_starter/verification/build.log) | [axioms](../strong_edge_lean_starter/verification/axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/source-sha256.json) |
| C4 | [status](../strong_edge_lean_starter/verification/next-stage-status.json) | [build](../strong_edge_lean_starter/verification/next-stage-build.log) | [axioms](../strong_edge_lean_starter/verification/next-stage-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/next-stage-source-sha256.json) |
| high24 | [status](../strong_edge_lean_starter/verification/high24-status.json) | [build](../strong_edge_lean_starter/verification/high24-build.log) | [axioms](../strong_edge_lean_starter/verification/high24-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high24-source-sha256.json) |
| high23 | [status](../strong_edge_lean_starter/verification/high23-status.json) | [build](../strong_edge_lean_starter/verification/high23-build.log) | [axioms](../strong_edge_lean_starter/verification/high23-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high23-source-sha256.json) |
| high22 | [status](../strong_edge_lean_starter/verification/high22-status.json) | [build](../strong_edge_lean_starter/verification/high22-build.log) | [axioms](../strong_edge_lean_starter/verification/high22-axioms.log) | [SHA-256](../strong_edge_lean_starter/verification/high22-source-sha256.json) |

历史散列应与相应阶段 ZIP 比较；当前工作树以 high22 清单为准。
`verification/` 还保留各阶段基线日志、真实源码 diff、文件变动摘要、开发中间日志和两份打包脚本。
中间日志中的历史错误或警告不代表最终构建状态；上表链接的是最终验证记录。

## 交接和原始来源

- [最初项目交接](../strong_edge_lean_starter/LEAN_20_PACKING_HANDOFF.md)
- [C4 报告](../strong_edge_lean_starter/verification/NEXT_STAGE_REPORT.md)
- [high24 交接](../strong_edge_lean_starter/verification/high24-handoff.md)
- [high23 交接](../strong_edge_lean_starter/HIGH23_HANDOFF.md)
- [high22 交接](../strong_edge_lean_starter/HIGH22_HANDOFF.md)
- [用户提供的原始输入](inputs/README.md)

研究来源固定在公开仓库提交
[`3a95c4a9c44475196c42b6eab4749c487d15d59b`](https://github.com/congyuemao/strong-edge-colouring-research/tree/3a95c4a9c44475196c42b6eab4749c487d15d59b)。
三份 high22 阶段参考稿的本地副本保存在 `verification/high22-research-*.md`。
研究稿或提示词中的建议、声称和未完成目标不等同于已核验成果。

## 当前边界

已证阈值：high24 ≤13、high23 ≤16、high22 ≤17。
尚需证明：high21 ≤18、high20 ≤19。
当前导出的是带这两个显式结构条件的 20-packing；无条件 20-packing、19.5 加强和整数强边二十色均未完成。

本次整理没有改动数学证明，也没有重新生成或覆盖旧 checkpoint。
归档核验结果与全量文件散列见 [ARCHIVE_MANIFEST.json](ARCHIVE_MANIFEST.json)。
