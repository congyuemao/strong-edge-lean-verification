# PACKING20 实际证明依赖审计

日期：2026-10-10，Australia/Sydney。依赖图来自新编译环境中声明的类型与证明项，不是 import 文件名猜测或文本引用搜索。

## 1. 提取方法及结果

[AuditDependencies.lean](isolated/strong_edge_lean_starter/AuditDependencies.lean) 从 `StrongEdge.induced_matching_packing20` 出发，对每个 `ConstantInfo` 取类型的常量引用，并取 `value? (allowOpaque := true)` 的常量引用，递归到闭包。保留声明名、源模块、直接依赖、是否 axiom、是否 unsafe；`NameSet` 防止递归数据定义造成重复遍历。

原始输出：[dependencies-dev.stdout.log](logs/dependencies-dev.stdout.log)，退出状态：[dependencies-dev.json](logs/dependencies-dev.json)。此运行成功，日志名 `dev` 不代表未通过。

机器可读图：[proof-dependency-graph.json](proof-dependency-graph.json)；工程部分：[project-proof-dependencies.json](project-proof-dependencies.json)；统计：[dependency-summary.json](dependency-summary.json)。共 **8,302 个可达声明，506 个工程声明，355 个源模块**；包含自动生成的辅助证明、类型、实例和归纳类型构造器，不能将 506 当成作者手写定理数。355 个模块源码均找到并作 SHA-256 登记。

闭包中仅有 `propext`、`Classical.choice`、`Quot.sound` 三项公理，unsafe 声明为 0。与 `#print axioms` 独立核对一致。

## 2. 终点到五档阈值的实际路线

所有名称以下均位于 `StrongEdge` 命名空间。表中的 P/C/Q 表示公理结果为上述三项；完整类型及逐项公理输出在 [complete-final.stdout.log](logs/complete-final.stdout.log)。

| 节点 | 源文件 | 核心假设／作用 | 公理 |
|---|---|---|---|
| `induced_matching_packing20` | `StrongEdge/High20Packing.lean` | 有限简单 G，原度≤4，任意 F；无阈值参数 | P/C/Q |
| `minimalCliqueBounds20_of_maxDegree_four` | `StrongEdge/High20Packing.lean` | 由原度≤4供给 high20，调用下一层构造 | P/C/Q |
| `minimalCliqueBounds20_of_high20` | `StrongEdge/High21Packing.lean` | 接收 high20；供给已证 high21 | P/C/Q |
| `minimalCliqueBounds20_of_high20_high21` | `StrongEdge/High22Packing.lean` | 接收 high20、high21；供给 high22 | P/C/Q |
| `minimalCliqueBounds20_of_high20_high21_high22` | `StrongEdge/High23Packing.lean` | 实际调用记录构造器，供给 high23 和 high24≤15 | P/C/Q |
| `high20_clique_card_le_nineteen` | `StrongEdge/Bounds/High20.lean` | 原度≤4；Q 是完整冲突图团；Q 内各边完整冲突度≥20；得 Q.card≤19 | P/C/Q |
| `high21_clique_card_le_eighteen` | `StrongEdge/Bounds/High21.lean` | 同类假设，阈值21，得≤18 | P/C/Q |
| `high22_clique_card_le_seventeen` | `StrongEdge/Bounds/High22.lean` | 阈值22，得≤17 | P/C/Q |
| `high23_clique_card_le_sixteen` | `StrongEdge/Bounds/High23.lean` | 阈值23，得≤16 | P/C/Q |
| `high24_clique_card_le_thirteen` | `StrongEdge/Bounds/High24.lean` | 阈值24，得≤13 | P/C/Q |
| `high24_clique_card_le_fifteen` | `StrongEdge/Bounds/High24.lean` | 直接由≤13放宽为≤15，实际供给记录 high24 字段 | P/C/Q |

`High24Packing.lean` 虽在导入路径中，但旧的四参数构造 `minimalCliqueBounds20_of_high20_high21_high22_high23` **不在终点的实际证明依赖闭包中**；High23 构造直接构造记录。不能把“文件已导入”与“定理被引用”混为一谈。

五个最终阈值供给定理的引用闭包均未返回任何 packing 包装定理；`High20Packing` 没有被用于证明自己的 high20 供给。旧 `CliqueThresholds20` 记录也不在终点闭包中。原记录中 `high24≤7` 没有被偷偷采用：实际 `MinimalCliqueBounds20.high24` 只要求≤15，确由≤13供给。

## 3. 从抽象 packing 到任意候选集

| 节点 | 源文件 | 核心假设／作用 | 公理 |
|---|---|---|---|
| `induced_matching_packing20_of_minimal_clique_bounds` | `StrongEdge/MinimalPacking.lean` | 接收记录和原度假设；调用完整冲突度≤24、任意子集 packing，再转换成诱导匹配 | P/C/Q |
| `conflict_degree_le_24` | `StrongEdge/Bounds/ConflictDegree.lean` | 对完整 G 的全部边计数；原度≤4 | P/C/Q |
| `subset_packing20_of_minimal_clique_bounds` | `StrongEdge/MinimalPacking.lean` | 对 H.induce F 得到独立集，以 `Finset.image Subtype.val` 返回相同原顶点类型；单射保证基数不变 | P/C/Q |
| `minimalCliqueBounds20_induce` | `StrongEdge/MinimalPacking.lean` | 五档团界沿诱导子图继承 | P/C/Q |
| `clique_bound_induce` | `StrongEdge/Packing.lean` | 将子图团映入 H；子图度≤H中度，故相同阈值仍适用 | P/C/Q |
| `induced_degree_le` | `StrongEdge/Conflict.lean` | 诱导子图邻域包含于原邻域 | P/C/Q |
| `conflictGraph_independent_iff` | `StrongEdge/Conflict.lean` | 两个独立性定义的展开等价；在终点中可能经 simp 辅助证明展开，而非以独立常量出现 | 无公理（定义等价） |

这里诱导的是**冲突图**，没有删去原图候选集合之外的边。子图度只能变小，正是 `clique_bound_induce` 提升阈值假设的方向；没有反向使用度数不等式。

## 4. 私有邻域交换及双重计数

| 节点 | 源文件 | 核心假设／作用 | 公理 |
|---|---|---|---|
| `packing20_of_minimal_clique_bounds` | `StrongEdge/MinimalPacking.lean` | H 最大度≤24，五档记录；选最优独立集并调用局部计数 | P/C/Q |
| `optimal_exists` | `StrongEdge/PrivateExchange.lean` | 有限 H；先最大化独立集大小，再最小化其 H 度数和 | P/C/Q |
| `private_isClique` | `StrongEdge/Basic.lean` | 最大独立集 M；若私有点有不相邻两点，则以二换一增大 M，矛盾 | P/C/Q |
| `private_degree_mono` | `StrongEdge/PrivateExchange.lean` | `IsOptimal`；以一个私有点替换中心，保持大小，由次级最小化推出度数不降 | P/C/Q |
| `local20_of_minimal_clique_bounds` | `StrongEdge/MinimalPacking.lean` | 得每个 v∈M 的 `degree v+1+privateCard v≤40` | P/C/Q |
| `coverage_pointwise` | `StrongEdge/DoubleCount.lean` | 最大独立集覆盖全部顶点；私有点计一次，其他点至少两次 | P/C/Q |
| `sum_covering`、`sum_privateOwners` | `StrongEdge/DoubleCount.lean` | 有限双重求和换序，不假设一般闭邻域互不相交 | P/C/Q |
| `private_double_count` | `StrongEdge/DoubleCount.lean` | 两倍顶点数≤各 v∈M 的 degree v+1+私有集合大小之和 | P/C/Q |
| `packing_of_local_bound` | `StrongEdge/DoubleCount.lean` | 显式局部上界≤2k推出顶点数≤k*M.card；终点用k=20 | P/C/Q |

低度 d≤19 时用 |P_v|≤d+1；d=20、21、22、23 分别代入19、18、17、16；d=24 用15即可得到40。已证13提供富余，但没有使用未证7。

## 5. high20 关键分支的类型检查

`Bounds/High20.lean` 的一般定理先区分 Q 支撑最大度≤3（调用已有≤18界），或选到四条 Q 星边的根。四根情形先由 `high20_large_clique_root_neighborhood_independent` 导出原邻域独立，再区分四元类型、两个至少三元类型、唯一三元类型、全部类型≤2。对应供给来自 `High20Four`、`High20TwoTriples`、`High20UniqueTriple`、`High20Outer`、`High20Slots` 以及已有低度结构引理。

四元／两三元分支导出≤18，唯一三元分支导出≤19，全≤2分支导出≤18；均足以排除 |Q|≥20。`rootType`、原邻域及完整冲突度始终从 G 计算，不把支撑外顶点当成不存在。无需历史文稿所声称的完整20强团分类或 high20≤18 加强。

## 6. 静态扫描与可信边界

工程原45个 Lean 文件去除注释／字符串后，仅命中两个 `noncomputable`：`privateFinset`、`privateOwners`，都用于经典有限集合筛选。无 `sorry`、`admit`、`sorryAx`、自定义 `axiom`、`constant`、`unsafe`、`native_decide`、`opaque` 声明。见 [own-static-findings.json](own-static-findings.json)。

355个实际证明涉及的模块源码也扫描并哈希登记，见 [dependency-static-findings.json](dependency-static-findings.json)、[dependency-source-sha256.json](dependency-source-sha256.json)。这些**整文件**包含 Lean 的 `sorryAx` 定义、sorry/admit tactic 宏、运行时 unsafe/extern、与目标无关的 opaque 等；扫描命中不等于目标定理引用它们。实际8,302声明闭包没有 `sorryAx`、unsafe 或额外公理。

另外扫描并登记审计环境的全部 3,648 个传递导入模块（包括审计工具用到的 Lean 元编程模块），源码全部找到，见 [import-summary.json](import-summary.json)、[import-static-findings.json](import-static-findings.json)、[import-source-sha256.json](import-source-sha256.json)。它比最终定理证明闭包更宽；不能用这里存在 native_decide 实现代码来断言本证明使用 native_decide。

审计依赖正常 Lean 内核、指定编译器和本地锁定依赖缓存。没有对编译器二进制进行从源码自举验证，也没有把全部 mathlib 缓存重新从零编译；缓存复用范围在复现报告中披露。哈希和静态扫描补充而不替代内核公理输出。
