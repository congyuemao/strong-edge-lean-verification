# PACKING20 数学语义独立审计

日期：2026-10-10，Australia/Sydney。结论：对不同原边的冲突关系，以及诱导匹配定义，与独立端点陈述的**双向等价均已由 Lean 验证**。这不是仅靠测试或阅读定义作出的判断。

## 1. 被审计的原定义

`StrongEdge/Basic.lean` 的 `conflictGraph G : SimpleGraph G.edgeSet` 使用完整边类型 `G.edgeSet`。`StrongConflict G e f` 要求 `e ≠ f`，并满足线图一步邻接，或存在 `g : G.edgeSet` 构成两步线图行走。中间边无候选集条件。mathlib 的 `SimpleGraph.lineGraph_adj_iff_exists` 将线图邻接解释为不同边共享某个原顶点。

`candidateConflictGraph G F` 是 `(conflictGraph G).induce F`；它限制冲突图顶点，不重新计算删边后原图的冲突。`StrongEdge/Conflict.lean` 的 `IsInducedMatching` 是集合中不同原边两两不满足 `StrongConflict`。

## 2. 新增独立定义与普遍等价证明

源文件：[AuditSemantic.lean](isolated/strong_edge_lean_starter/AuditSemantic.lean)。该文件独立定义：

```lean
def directStrongConflict (G : SimpleGraph V) (e f : G.edgeSet) : Prop :=
  ∃ a b c d : V, e.val = s(a, b) ∧ f.val = s(c, d) ∧
    (a = c ∨ a = d ∨ b = c ∨ b = d ∨
      G.Adj a c ∨ G.Adj a d ∨ G.Adj b c ∨ G.Adj b d)
```

这一定义不调用原工程的冲突定义、线图定义或候选冲突图。另定义辅助的 `endpointWitness`：存在分别属于两条边的端点 x、y，使 x=y 或 G.Adj x y。

已核验的声明（命名空间均为 `IndependentAudit`）：

| 声明 | 实际结论 |
|---|---|
| `endpointWitness_iff_direct` | 两种独立端点表述等价，无有限性或最大度要求 |
| `conflict_iff_endpointWitness` | 在 e≠f 下，原冲突图邻接等价于端点见证 |
| `conflict_iff_direct` | 在 e≠f 下，原冲突图邻接等价于显式四端点定义 |
| `inducedMatching_iff_endpoints` | 对任意集合 M，工程诱导匹配等价于不同已选边的任意端点对均不相等、在完整 G 中不邻接 |
| `endpoint_packing20` | 返回 M⊆F、独立端点意义的诱导匹配及 F.card≤20*M.card |
| `empty_candidates` | 对任何 G，空候选集可取空 M，不需要非空、有限 V 或度数限制 |

冲突等价正向：线图一步给出共享端点；两步行走给出中间边的两个端点，它们要么相同，要么由该原边连接。反向：共享端点直接给出线图一步；若端点相邻，则用真实原边 s(x,y) 作中间边。当该边等于 e 或 f 时退化为一步，其他情况得到合法两步行走。

`directStrongConflict` 本身允许 e=f 时为真；**等价定理明确要求 e≠f**。完整冲突图始终由 `SimpleGraph` 的无自环结构约束，且原定义显式排除 e=f。没有把端点重合错误地当作允许图中自环。

日志：[semantic.stdout.log](logs/semantic.stdout.log)、[semantic.stderr.log](logs/semantic.stderr.log)、[semantic.json](logs/semantic.json)。以上公开主结论的公理闭包均仅含 `propext`、`Classical.choice`、`Quot.sound`。

## 3. 量词、有限性与额外前提

`F : Finset G.edgeSet` 的每个元素都携带属于 G.edgeSet 的证明，不能夹带非原图边。返回的 M 同样是这一类型上的 Finset，故有限；`M ⊆ F` 在相同的原边类型中解释。

最终定理对所有 F 成立，没有 `F.Nonempty`、正则、无三角形、无四圈、极大候选集、支撑闭合等前提。`endpoint_packing20` 的类型甚至不要求显式提供冲突图邻接的可判定实例：通过 Lean 的经典可判定性补足，表明原接口中的该 typeclass 不是额外图论假设。保留的 `[Fintype V]`、`[DecidableEq V]`、`[DecidableRel G.Adj]` 与最大度假设均在日志中明示。

## 4. 独立回归与紧例

源文件：[AuditRegression.lean](isolated/strong_edge_lean_starter/AuditRegression.lean)，日志：[regression-dev.stdout.log](logs/regression-dev.stdout.log)、[regression-dev.json](logs/regression-dev.json)。虽然日志名带 `dev`，该次运行无错误、无警告、退出码 0，文件未再改变。

| 检查 | 实际结果与证据类别 |
|---|---|
| 路径 0–1–2–3，只选 01 和 23 | 独立端点见证为 G.Adj 1 2；经已证等价得到候选冲突图仍邻接；Lean 证明 |
| 真正删去中间原边 12 | 端点关系的有限 `decide` 与已证等价推出不冲突；Lean 内核核验的有限回归 |
| 空顶点图 Fin 0 | 对任意候选 F 实例化端点 packing；Lean 证明 |
| 五个孤立点 | 对任意候选 F 实例化 packing；Lean 证明 |
| 非正规四点路径 | 有限度数检查后，对任意 F 实例化 packing；Lean 证明 |
| 三角形 | 对任意 F 实例化 packing；Lean 证明 |
| 四圈 | 对任意 F 实例化 packing；Lean 证明 |
| 双点五圈 | 10 点、20 边、每点度恰 4、不同原边两两冲突；Lean 内核有限计算与一般等价组合 |

双点五圈的独立构造使用 `Fin 10`，点 x 的簇编号为 x.val/2；相邻簇编号在模 5 意义下差 1，各相邻簇间全连接。没有复用工程中关于极端构形的分类结论。

`doubleC5_endpoint_test` 检查所有四端点组合；使用普通 `decide`，公理输出为**不依赖任何公理**，没有使用 `native_decide`。这与 `doubleC5_degree_four`、`doubleC5_twenty_edges` 及边类型转换组合，给出 `doubleC5_all_edges_conflict`。最后 `doubleC5_matching_card_le_one` 与 `twenty_is_necessary` 证明：若自然数 c 对该图全部边给出 c 倍 packing 保证，必有 c≥20。

对任意实数常数 c<20 的数学推论也直接成立：此图最多只能选一条，故 20≤c|M| 不可能。**实数版本没有另行写成 Lean 声明**，自然数版本已形式化。有限构形只证明语义回归与下界，不能代替一般 20 倍定理。

## 5. 已完成与未做的界线

两项核心语义双向等价均完成，没有单向证明遗留。原冲突图在数学上就是平方线图：相同顶点类型、不同边之间距离一或二。未额外连接一个 mathlib 命名的图幂／平方算子接口；这是任务的可选项，不影响已证端点等价。

本审计没有证明二十色染色、任意实边权保证、19.5 加强、所有 20 强团的唯一性分类或算法复杂度。历史说明书中的更强陈述均未当作 Lean 公理或已验收结论。
