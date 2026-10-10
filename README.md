# 强边冲突与诱导匹配打包：Lean 验证成果

整理日期：2026-10-10（Australia/Sydney）。最近一次数学验证完成于 2026-10-09。

本仓库汇总目前全部本地 Lean 证明、阶段交接、构建日志、公理审计、源码散列和五个历史 checkpoint。
证明始终采用**完整原图**的强边冲突，候选边集外的原边仍可作为冲突见证。

目前已完成 C4，以及 C5 的 high24、high23、high22 三个强团界。
**high21 和 high20 仍未完成，无条件 20-packing 尚未证明。**

## 当前已验证结论

以下结论针对任意有限简单图 `G`，假设每个原顶点度数至多四。
表中的阈值均指每条候选边在完整冲突图中的度数。

| 内容 | 已验证结论 | 主声明 |
|---|---|---|
| 完整冲突度上界 C4 | 每条原边的完整冲突度 ≤24 | `conflict_degree_le_24` |
| high24 强团界 | 每条成员冲突度 ≥24 的团，边数 ≤13；满足所需 ≤15 | `high24_clique_card_le_thirteen` |
| high23 强团界 | 每条成员冲突度 ≥23 的团，边数 ≤16 | `high23_clique_card_le_sixteen` |
| high22 强团界 | 每条成员冲突度 ≥22 的团，边数 ≤17 | `high22_clique_card_le_seventeen` |
| 条件性打包 | 对任意候选边集 F，存在诱导匹配 M⊆F，且 \|F\|≤20\|M\| | `induced_matching_packing20_of_high20_high21` |

最后一项仍显式要求 high20（阈值 20 时团大小 ≤19）和 high21（阈值 21 时团大小 ≤18）。
最新完整定理签名见 [HIGH22_HANDOFF.md](strong_edge_lean_starter/HIGH22_HANDOFF.md)。

已完成的通用基础包括完整冲突与候选限制、独立集与诱导匹配等价、最优私有邻域交换、度数单调性、双重计数，以及任意候选边集上的条件性打包。
本仓库没有宣称整数强边二十色、19.5 加强、high23 ≤15 或 high22 ≤16 已获 Lean 验证。

## 验证证据

- 当前项目含 **28 个 Lean 源文件**。
- 最近一次完整构建通过：**1,144 jobs，无警告**。
- **145 项公理审计**均仅列出 `propext`、`Classical.choice`、`Quot.sound`。
- 项目 Lean 源码没有 `sorry`、`admit`、`sorryAx`、自定义 `axiom`、`constant`、`unsafe` 或 `native_decide`。
- 本次整理核对了当前源码与 high22 散列清单，以及 high22 checkpoint 中全部文件的字节一致性。

原始依据：[最终构建日志](strong_edge_lean_starter/verification/high22-build.log)、
[最终公理审计](strong_edge_lean_starter/verification/high22-axioms.log)、
[源码 SHA-256](strong_edge_lean_starter/verification/high22-source-sha256.json)。
本次归档清单为 [ARCHIVE_MANIFEST.json](docs/ARCHIVE_MANIFEST.json)。

## 阶段与交付物

| 阶段 | 主要成果 | 构建 jobs | 审计项数 | 源码与证据快照 |
|---|---|---:|---:|---|
| 初始核验 | 通用交换、双重计数、条件性打包 | 1,124 | 13 | [verified checkpoint](strong_edge_lean_verified_checkpoint.zip) |
| C4 | 完整冲突度 ≤24、取等结构、最小阈值接口 | 1,127 | 38 | [C4 checkpoint](strong_edge_lean_c4_checkpoint.zip) |
| C5 high24 | 强团 ≤13，接入所需 ≤15 | 1,129 | 51 | [high24 checkpoint](strong_edge_lean_high24_checkpoint.zip) |
| C5 high23 | 强团 ≤16，剩三项结构假设 | 1,136 | 94 | [high23 checkpoint](strong_edge_lean_high23_checkpoint.zip) |
| C5 high22 | 强团 ≤17，剩两项结构假设 | 1,144 | 145 | [high22 checkpoint](strong_edge_lean_high22_checkpoint.zip) |

这些数字是各阶段实际日志中的构建任务数与审计声明数，不表示 Lean 定理总数。
历史 ZIP 原样保留；源码和交接材料仍使用原有相对路径，便于后续继续证明。

## 导航

- [Lean 项目说明与模块清单](strong_edge_lean_starter/README.md)
- [全部成果与证据索引](docs/RESULTS_INDEX.md)
- [high22 完整交接](strong_edge_lean_starter/HIGH22_HANDOFF.md)
- [high23 完整交接](strong_edge_lean_starter/HIGH23_HANDOFF.md)
- [high24 完整交接](strong_edge_lean_starter/verification/high24-handoff.md)
- [C4 阶段报告](strong_edge_lean_starter/verification/NEXT_STAGE_REPORT.md)
- [原始输入与交接说明](docs/inputs/README.md)

## 复现

固定版本：

- Lean：`leanprover/lean4:v4.35.0-rc4`
- Lean 编译器提交：`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib：`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`

安装 Lean/elan 后，在项目子目录执行；保留现有 lockfile：

```powershell
cd strong_edge_lean_starter
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

在其他系统上可直接执行 `lake build` 和 `lake env lean StrongEdge/Audit.lean`。
首次构建需要获取锁定的依赖；mathlib 缓存命令见 [项目 README](strong_edge_lean_starter/README.md#reproduce)。
编译器二进制、`.lake` 和 `.cache` 不上传，均可按固定版本重新获取。

在仓库根目录核对归档完整性：

```powershell
python scripts/verify_archive.py
```

该脚本检查文件与历史证据，不能替代 Lean 内核构建与公理审计。
`.gitattributes` 禁用自动换行转换，以保持已验证散列和日志的原始字节。

## 接下来

先证明 high21 ≤18，再证明 high20 ≤19，并接入现有最小阈值记录。
high22 的支撑度至多三分支仍使用 high22 假设；不能将其当作已证明的无阈值通用次三次图定理。
各阶段更具体的复用条件与未完成目标均记录于相应 handoff。
