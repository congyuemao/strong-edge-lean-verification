# Codex 任务：形式化验证 C5 的 high23 强团界

> 交接日期：2026-10-09。此文件是交给**已有本地 Lean 4 项目**继续执行的工作指令。请直接实施、编译、核查并保存结果，不要只回复数学构想。当前项目已有 C4 与 high24 证明。保持现有项目、依赖版本和已验证成果。

## 0. 唯一主目标与当前可信状态

**本轮主目标**：对于任意有限简单图 `G`，若所有原图顶点度数至多四，`Q` 是按照**完整原图**定义的强边冲突团，且 `Q` 中每条原边在完整冲突图中的度数都至少为 23，则证明

\[
|Q|\le16.
\]

要求导出内核验证的 Lean 声明（具体实例参数、命名空间按现有项目调整，数学前提与结论不得削弱）：

```lean
theorem StrongEdge.high23_clique_card_le_sixteen
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V)
    [DecidableRel G.Adj]
    [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h23 : ∀ e ∈ Q, 23 ≤ (StrongEdge.conflictGraph G).degree e) :
    Q.card ≤ 16
```

请将它接入原来的 `MinimalCliqueBounds20.high23` 字段，并另外导出**只保留 `high20`、`high21`、`high22` 三个结构前提**的条件性二十倍诱导匹配定理。不得把这三个剩余条件隐藏为局部实例、公理、定义或未声明的假设。

**可选强化**：如果短证明自然得到 `Q.card ≤ 15`，可以同时导出 `high23_clique_card_le_fifteen`，然后用它推出所需 `≤16`。但不得为了更强常数阻滞本轮的基本目标。

### 已完成、必须保留的结果

根据用户贴出的 **C5 high24 verified handoff**：

- `StrongEdge/Bounds/ConflictDegree.lean`：完整冲突度 `≤24` 已内核验证。
- `StrongEdge/Bounds/ConflictRigidity.lean`：冲突度恰 24 的局部取等结构已验证。
- `StrongEdge/Bounds/High24.lean`：`high24_clique_card_le_thirteen`、`high24_clique_card_le_fifteen` 已验证。
- `StrongEdge/High24Packing.lean`：把 high24 连接至 `MinimalCliqueBounds20`，剩余 high20–high23 是显式参数。
- 私有邻域、交换引理、双重计数、任意候选边集的条件性打包结论已经完成；不得重写这些模块或放宽原图冲突定义。
- 上阶段报告称完整构建通过（1,129 jobs），`StrongEdge/Audit.lean` 中有 51 项公理审计记录，每项仅依赖 `propext`、`Classical.choice`、`Quot.sound`。这些是交接报告声称的状态；请从本地源代码和日志核实，不要根据文本直接假设下一阶段环境正常。

**尚未完成**：high20–high23 普遍强团界、无条件 20-packing，以及后续 19.5 加强。不要声称本轮证明了这些更大目标。

## 1. 固定数学来源和项目版本

研究仓库的固定提交：

`3a95c4a9c44475196c42b6eab4749c487d15d59b`

重点阅读：

1. **本轮推荐路线（短证明，目标上界 15）**：
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_23_improved.md
2. **备选路线（旧版上界 16，含较长缺额计数）**：
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_subcubic.md
3. 原通用双重计数证明：
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md
4. high24 局部结构作为参考：
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/critical_support.md

**本轮推荐先核查 `high_conflict_23_improved.md` 的短证明，再开始翻译为 Lean。** 不要因为纸面文档声称已审核就跳过数学审计。发现原文有隐含假设或错误时，先明确写出问题、尝试修复；修复失败则保留可证明的引理并诚实报告阻塞。

固定工具链（以现有 `lake-manifest.json` 和 `lean-toolchain` 为准）：

- Lean `leanprover/lean4:v4.35.0-rc4`
- Lean 编译器提交 `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib 提交 `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`

不要无必要运行 `lake update`；不要删除 `.lake`、改动缓存布局、重置用户现有工程或覆盖旧 checkpoint。

## 2. 核心差异：23 不能当作 24

现有 `high24` 证明依赖冲突度 **恰好 24** 时全部局部计数取等。本轮假设 `c_G(e) ≥ 23`，每条边允许至多一次计数损失。禁止直接把 `high24` 的无三角、无四圈或分支禁叉引理在弱化前提下套用。

首先构建下面的 `high23` 基础结构（若已有可用定理则复用）：

1. `high23_endpoints_degree_four`：原冲突度至少 23 的边，其两个原端点都为四度。
2. `high23_no_triangle_on_edge`：这样的边不属于任何原图三角形。
3. `high23_at_most_one_four_cycle_on_edge`：这样的边至多属于一个原图四圈。这里需要给出“两个不同四圈”的**精确定义**，并保证四圈对应不同的计数重复边。
4. `high23_root_neighborhood_independent`：若原图顶点 `v` 关联 `Q` 中至少三条边、这些边冲突度均至少 23，则 `N_G(v)` 独立；特别不要假定整个 `G` 无三角形。

一种可行的证明方式：对于 `e={u,v}`，已有六邻点覆盖

\[
S_e=(N(u)\setminus\{v\})\cup(N(v)\setminus\{u\}).
\]

所有与 `e` 冲突的原边都与 `S_e` 相交，且

\[
c_G(e)\le \Bigl|\bigcup_{x\in S_e}\operatorname{Inc}_G(x)\Bigr|
\le\sum_{x\in S_e}d_G(x)\le4|S_e|\le24.
\]

- 若某端点度数小于四，或 `u,v` 有公共邻点，则 `|S_e|≤5`，得 `c_G(e)≤20`。
- 当 `c_G(e)≥23` 时，`|S_e|=6`，全部六点的度数几乎饱和，而且 `S_e` 内部至多存在一条原边，否则在并集中出现至少两个重复计数，推出 `c_G(e)≤22`。
- 每条经过 `e` 的四圈都对应一条连接两侧邻点的 `S_e` 内部边；两个不同四圈对应不同内部边。

这是建议的计数路线，**不得仅凭这段解释把未证的“至多一条内边”当作形式化前提**。该桥梁必须进入 Lean 证明链，能由内核独立验证。

## 3. 推荐主证明：用强团支撑内部的最大原顶点度分类

定义候选边集 `Q` 在原图顶点 `v` 处的内部度：

\[
d_Q(v)=|\{e\in Q:v\in e\}|.
\]

保持其与 `G.degree v` 严格区分。`d_Q(v)≤4` 来自 `Q⊆E(G)` 与原最大度四。

建议先把更大强团缩为一个固定大小的 `Q'`（例如 `|Q'|=17`）以便排反证；亦可直接证明上界。有限子集缩小必须保留全部原图中的冲突度，因为这些度数按照 `G` 定义，与 `Q'` 无关。不要在缩小过程中把冲突图变成由 `Q'` 边生成的新原图。

### A. 内部度最多二：目标 `|Q|≤13`

这部分可以尝试比原始论文更短的局部覆盖证明：

- 若 `Q` 非空，任取 `e={u,v}∈Q`。
- 除 `e` 外，每条 `Q` 边都与 `e` 冲突，因此必须碰到 `S_e` 中至少一个顶点。
- `S_e` 最多六个顶点，每点最多关联 **两条 Q 边**；所以 \(|Q|-1≤6·2=12\)。
- 因而 \(|Q|≤13\)。

这是一条有用的通用有限集合覆盖引理。注意 `e` 自身不碰到 `S_e`，而 `Q` 中其余边可以重复碰到多个覆盖顶点；用并集基数上界即可，不要求不相交。

### B. 内部度恰有三：目标 `|Q|≤14`

按照 `high_conflict_23_improved.md` 第 2 节：

- 固定 `v`，它恰有三条属于 `Q` 的星边 `va,vb,vc`；原图还有第四邻点 `d`，记 `A={a,b,c,d}`。
- 令 `B` 为 `Q` 中所有原边端点中，除 `v` 与 `A` 之外的点；对 `x∈B` 定义类型 `T_x=N_G(x)∩A`。仍然保留 `G` 的全部顶点和原边。
- 从 high23 每条根星边至多一个四圈，证明 `|T_x|≤2`，且对每个根 Q 标签 `a,b,c`，至多有一个二元类型包含该标签。
- 证明每个 `B` 中的 Q 支撑点的类型非空；这个步骤需要真正展开它与三条根星边的冲突见证，不能仅凭“显然”。
- `A–B` 的 Q 边数 `T` 至多 `2+2+2+3=9`，因为三个根 Q 邻点剩余 Q 度最多 2，第四点最多 3。
- 若 Q 中某条 `B–B` 边 `xy` 存在，`T_x∪T_y` 必须覆盖三个根 Q 标签 `{a,b,c}`。在类型最大大小 2、二元类型支持容量的限制下，全部 B–B 的 Q 边数 `h≤2`。
- 因而 `Q.card=3+T+h≤3+9+2=14`。

建议先把 `A–B`、`B–B`、根星三类明确写成 **Finset 计数上的覆盖或划分**，再证明每类界，避免无根据地使用计数等式。

### C. 内部度有四：目标 `|Q|≤15`

按照 `high_conflict_23_improved.md` 第 3 节：

- 固定 `v`，它关联四条 Q 边，`A=N_G(v)` 恰有四点且独立。
- 外部 Q 支撑点的 `A`-邻接类型非空、大小至多二。每个根星边最多出现于一个原图四圈，因此每个 `A` 标签至多属于一个二元类型；故二元类型点数量 `c₂≤2`。
- 任何 B–B Q 边 `xy` 必须满足 `T_x∪T_y=A`，因此只能连接互补的两个二元类型点；其总数 `h≤1`。
- 设 `p` 为 A–B 中属于 Q 的**一元类型**边数，按标签 `a∈A` 分组为 `p_a`。每个 `p_a≤3`。
- 来自不同标签的两条一元类型 Q 边 `ax`、`by` 要互相冲突，由独立性与类型精确性迫使 `G.Adj x y`；于是当 `p_a>0` 时 `p-p_a≤3`。结合 `p_a≤3`，得到 `p≤6`。
- 二元类型贡献的 A–B Q 边数至多 `2c₂≤4`，故 `T≤p+4≤10`。
- 整体 `Q.card=4+T+h≤4+10+1=15`。

**这一短证明如果 Lean 全部通过，则比本轮需求 `≤16` 更强，而且可能比旧版 `≤16` 的支撑闭合、缺额恒等式证明更省工作。** 但必须先确认每个“类型”结论在 Lean 的完整原图冲突定义下无隐藏前提。

## 4. 实现建议与文件组织

不要求完全使用下面的模块名称，但每个导出定理应有单独可审计的声明：

```text
StrongEdge/
  Bounds/
    ConflictDegree.lean       -- 已有；保持
    ConflictRigidity.lean     -- 已有；保持
    High24.lean               -- 已有；保持
    High23Local.lean          -- 新：23度局部缺额/三角/四圈
    High23Support.lean        -- 新：Q支撑度、类型、有限集合计数
    High23.lean               -- 新：≤16（可选≤15）
  MinimalPacking.lean         -- 已有；保持
  High24Packing.lean          -- 已有；保持
  High23Packing.lean          -- 新：只留下 high20–high22 条件
  Audit.lean                  -- 增加 #print axioms 与全类型输出
```

开始时先仔细阅读项目中真实的 `conflictGraph`、`strongConflict`、`endpointNeighbourCover` 与 Finset edgeSet 的定义。优先复用已验证的 C4 覆盖引理；新添加局部定义不得改变强冲突数学语义。

可以将 `Q` 内部度、支撑点、类型及其分类封装为小型结构或 `Finset`，但每个辅助定理都必须能展开回完整 `G`、完整 `Q` 的前提。避免通过新结构的字段默默假设要证明的性质。

若初步代码更适合按“≥17 即矛盾”的反证构造，允许使用这一接口；但最终应输出对**任意 Q** 的普遍上界。不得只验证某个固定顶点数的原图。

### 与打包定理连接

接入 `MinimalCliqueBounds20` 时，只构造下面这个**条件性**新接口：

```lean
-- 示意名称，具体语法需与真实定义统一。
minimalCliqueBounds20_of_high20_high21_high22
induced_matching_packing20_of_high20_high21_high22
```

- `high23` 由本轮定理提供。
- `high24` 继续由已验证的 `high24_clique_card_le_fifteen` 提供。
- `high20`、`high21`、`high22` 仍是显式的三项参数。
- 原图最大度四是假设；完整冲突度≤24由 C4 现有定理提供。
- 输出应继续适用于**任意**候选边集 `F`，并沿用完整原图的 `IsInducedMatching G` 定义。
- 禁止将 `high23` 错接到 23 条 Q 边、或者将“Q 内部冲突度”误认为完整原图的冲突度。

## 5. 验证、审计与质量控制

首先保存现有工作区状态；不删除、重置或覆盖此前 checkpoint。Windows PowerShell 预计执行：

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

中途可以用具体的 `lake build StrongEdge.Bounds.High23Local` 等方式只检查新增模块，最终必须进行完整构建与全量审计。

**完成条件**：

1. 导出目标 `high23_clique_card_le_sixteen`，其完整类型中只有 `hΔ`、`hQ`、`h23` 等必需的正常类型/可判定性前提，不夹带其余强团界或未验证结构前提。
2. 给出 `#print`/`#check` 后的完整 theorem signature，而不只展示简称。
3. 对每一个新增正式定理执行 `#print axioms`，其依赖闭包不得引入 `sorryAx`、自定义公理、`native_decide` 或未经信任的计算。
4. 扫描所有项目 Lean 源文件是否有 `sorry`、`admit`、`axiom`、`constant`、`unsafe`、`native_decide`；审计证明依赖比纯文本扫描更重要。
5. 编译器、mathlib、lockfile 版本保持固定；保留基线及最终构建日志。
6. 新建 `verification/high23-*.log`、源文件 hash 清单、摘要报告及与上一 checkpoint 的真实文件差异。若项目未被 Git 跟踪，不要用空白 `git diff` 冒充无变更。
7. 如果有新定理的数学条件被无意增强，必须在总结中突出该增强，不能把它记作无条件结果。
8. 不将有限样本通过、Python 整数表或 `decide` 针对固定大小的验证冒充所有有限简单图的普遍证明。
9. 不声称得到整数强边二十色；本轮也不处理后续 19.5 目标。

建议输出到本地：

```text
StrongEdge/Bounds/High23Local.lean
StrongEdge/Bounds/High23Support.lean
StrongEdge/Bounds/High23.lean
StrongEdge/High23Packing.lean
verification/high23-baseline-build.log
verification/high23-baseline-axioms.log
verification/high23-build.log
verification/high23-axioms.log
verification/high23-source-sha256.json
verification/high23-source.diff
HIGH23_HANDOFF.md
```

上述文件名只是建议，实际审计记录必须和真正生成的文件一一对应。另保存可在另一台机器上重现的源代码与验证日志 ZIP，排除编译器二进制、`.lake`、缓存及不必要的大型依赖。不要擅自推送或更改公开 GitHub 仓库。

## 6. 遇到卡点时的处理规则

优先完成经过内核证明的局部结构引理，并将其提交到现有项目文件。若本轮完整 high23 仍不能完成：

- 明确指出最小的未解决 Lean 声明名称和**完整数学前提**。
- 标记它属于 Lean API/类型问题、有限集合计数问题，还是**真实数学证明缺口**。
- 给出已通过的 `lake build` 和 `#print axioms` 结果，不虚报剩余目标。
- 若发现原研究证明存在可复现反例，给出原图边集、候选强团边集、最大度、所有相关冲突度及验证代码/证书；不要在没有充分验证时宣称原命题被推翻。
- 保留可验证的部分成果与明确交接点；不要把最终失败解释成整项定理为假。

## 7. 最终回报格式

在本地项目中生成 `HIGH23_HANDOFF.md`，至少包括：

1. 结论：high23 `≤16` 是否已完成；是否顺带达到 `≤15`。
2. 精确 Lean 导出签名，完整说明剩余假设。
3. 新增定义、引理与证明思路，尤其是“至多一个四圈”、三度根和四度根的分类。
4. 编译、审计、源码扫描的真实命令及退出状态。
5. 与 high24 checkpoint 相比的修改文件及 hashes。
6. 新的 packing wrapper 状态：理想情况下还剩 high20、high21、high22 三项显式未证条件。
7. 未完成部分和下阶段最短依赖路线。建议下一关优先 `high22 ≤17`，之后 `high21 ≤18`、`high20 ≤19`，但只在实际完成 high23 后才按结果重新安排。

**终止标准**：本阶段的目标是“带最大原度数四假设的普遍 high23 强团界，Lean 内核认可，并接入现有条件性打包证明”。除此之外的所有成果均为附加工作。不要因为一般高冲突问题艰难，就退回到固定小图搜索来代替全称证明。
