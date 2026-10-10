# Codex 任务：C5 high22 强团界的 Lean 内核验证

> 交接日期：2026-10-09。面向用户现有的 Windows / PowerShell / Lean 4 + mathlib 项目。**请直接在现有工程中实施、编译、审计并交付 checkpoint；不要只回复一个计划。** 以本地实际源代码和验证日志为准。本提示词不声称 `high22` 已获证明。

## 0. 唯一主目标与成功条件

对任意有限简单图 `G`，若原图最大顶点度数不超过四，`Q` 是**按完整原图 G 定义的冲突图**中的团，且 `Q` 中每条原边的**完整冲突度**至少为 22，则证明：

\[
\boxed{|Q|\le17.}
\]

预期新增公开定理的数学签名：

```lean
theorem StrongEdge.high22_clique_card_le_seventeen
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V)
    [DecidableRel G.Adj]
    [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4)
    (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h22 : ∀ e ∈ Q, 22 ≤ (StrongEdge.conflictGraph G).degree e) :
    Q.card ≤ 17
```

语法与 Lean 实例可按当前工程实际调整，但 **数学前提与结论不得弱化**。不得额外要求原图无三角形、无四圈、四正则、`Q` 极大、`Q` 在原图中闭合，或借用任何尚未证明的阈值界。

完成后将定理装入现有 `MinimalCliqueBounds20.high22`，另导出仅带 `high20`、`high21` 两项**显式结构参数**的条件性打包结论：

```lean
-- 名称示意，使用工程既有的真实定义和实例：
StrongEdge.minimalCliqueBounds20_of_high20_high21
StrongEdge.induced_matching_packing20_of_high20_high21
```

新包装结论仍须针对**任意 `F : Finset G.edgeSet`**，其诱导匹配按完整原图 `G` 判定，结论仍为 `F.card ≤ 20 * M.card`。`high20` 和 `high21` 尚未完成，不能伪装成无条件结论。

**可选加强：** 原始研究中的 `high_conflict_22_improved.md` 给出更强的 `|Q|≤16`，如果无需显著增加依赖且自然完成，允许额外导出；但本轮只以 `≤17` 为通过标准。

## 1. 必须继承的已核验证据

用户提供的最新 **C5 high23 verified handoff** 报告称：

- 已完成完整原图强冲突定义、诱导匹配与独立集等价、最优私有邻域交换、双重计数及条件性 `20` 打包。
- C4：`conflict_degree_le_24` 和冲突度 24 的局部取等引理已核验。
- C5 high24：`high24_clique_card_le_thirteen` 已核验，因而 `high24 ≤15` 已填入最小阈值记录。
- C5 high23：`high23_clique_card_le_sixteen` 已核验并接入最小阈值记录。**不要把原始研究中更强的 ≤15 当成已验证的 Lean 结果。**
- 最新条件包装器名称为 `induced_matching_packing20_of_high20_high21_high22`，仍显式带三个未证结构参数。
- 已有 20 个项目 Lean 源文件；报告称最终 `lake build` 共 1,136 jobs 且无警告，公理审计共 94 项，所列依赖仅 `propext`、`Classical.choice`、`Quot.sound`。
- 七个新模块分别是 `Bounds/EdgeCounting.lean`、`Bounds/High23Local.lean`、`Bounds/High23Support.lean`、`Bounds/High23Outer.lean`、`Bounds/High23Four.lean`、`Bounds/High23.lean`、`High23Packing.lean`。

**以上属于用户交接报告记录。开始前必须在本地实际运行基线构建及公理审计，不能仅凭报告文本宣称已复核。** 保留全部已有证明；优先增加新模块。若必须修改旧文件，逐项解释，保证语义与定理结论不变。

固定环境，除非遇到确切不可解的版本问题，否则不要升级：

- Lean：`leanprover/lean4:v4.35.0-rc4`
- 编译器 commit：`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib：`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`
- 保留 `lean-toolchain`、`lake-manifest.json` 和 `lakefile.toml`，不运行无必要的 `lake update`。

现有可复用名称（以源码中真实签名为准）：

```text
StrongEdge.conflict_degree_le_24
StrongEdge.endpointNeighbourCover
StrongEdge.conflict_degree_add_inside_le_sum
StrongEdge.incidence_sum_eq_meeting_add_inside
StrongEdge.edgeIncidences
StrongEdge.edgesMeeting
StrongEdge.edgesInside
StrongEdge.fourCycleOpposites
StrongEdge.rootLabels
StrongEdge.rootType
StrongEdge.outerEdges
StrongEdge.clique_card_le_one_add_incidence_sum
StrongEdge.clique_card_le_thirteen_of_support_degree_le_two
StrongEdge.high23_clique_card_le_sixteen
StrongEdge.high24_clique_card_le_fifteen
StrongEdge.MinimalCliqueBounds20
StrongEdge.induced_matching_packing20_of_high20_high21_high22
```

不要从这份列表推测参数顺序或适用条件；使用 `#check` 与对应源码核对，尤其注意此前的 `high23_*` 引理**依赖原冲突度至少 23**，不能直接把假设改成 22。

## 2. 固定原始数学来源

公开研究档案固定提交：

`3a95c4a9c44475196c42b6eab4749c487d15d59b`

本轮建议先阅读以下两份数学稿，并对潜在遗漏独立审查：

1. **优先路线：满足任务所需的 `high22 ≤17`**  
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_thresholds.md  
   重点是第 1 节的“四圈/重复计数预算”、第 2 节的辅助观察，以及第 4 节对 18 条边强团的排除。
2. **可选加强 `high22 ≤16`，但更复杂**  
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_22_improved.md
3. **支撑内最大度至多三的通用引理**  
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/strong_clique_subcubic.md
4. **通用 20-packing 证明的依赖清单**  
   https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md

原始稿中的“已独立复核”是旧 AI 研究流程的记录，**不等于 Lean 已经证明这些高22结论**。若找到纸面证明中的错误或隐藏前提，应先修改数学论证；不得用该前提填入 Lean 的新结构记录。

## 3. 从 23 降至 22 的决定性差别

对原边 `e={u,v}`，令

\[
S_e=(N_G(u)\setminus\{v\})\cup(N_G(v)\setminus\{u\}).
\]

当前 Lean 已建立冲突邻域到 `S_e` 的关联边覆盖，以及 incidence 的精确重复计数：

\[
c_G(e)+|E_G[S_e]|
\le\sum_{x\in S_e}d_G(x)
\le24.
\]

因此 `c_G(e)≥22` 时，期待严密推出：

1. `|S_e|=6`；`u,v` 各四度，且另外六邻点两侧不交。
2. `|E_G[S_e]|≤2`，允许**两次**重复计数；此处的 `E_G[S_e]` 是完整原图中两端都落在 `S_e` 的边集。
3. `e` 不属于任何三角形；任意经过 `e` 的四圈对应一条 `S_e` 中的跨边，因此至多有两个四圈。
4. 以上都是**某条被选 Q 边的局部结论**，绝不推出整个原图无三角形或四圈。

Lean 应优先复用 `incidence_sum_eq_meeting_add_inside`、`conflict_degree_add_inside_le_sum`、`fourCycleOpposites`，新建适当的 `high22_*` 定理。通过类型/计数证明“至多两次损失”，不要把它作为新假设加入最终签名。

高23阶段的如下结论可能仍有适用的较弱变体，但不可无证明复用：

- 原先每条 Q 边至多**一个**四圈，现在至多**两个**。
- 原先一个根 Q 标签只容许一个二元外部类型，现在可能容许两个。
- 原先不同的二元类型支持基本互斥，现在需要考虑交叠、重复与残余度数。

**新增引理中要写明实际使用的阈值 22，禁止通过 `h23`、某个隐藏的全 23 子集条件或改变冲突图定义解决主目标。**

## 4. 建议首先把主问题缩为一个 18 边反证

如果 `|Q|≥18`，可以选择子团 `Q₀ ⊆ Q`，使 `Q₀.card=18`：

- `Q₀` 中原边的完整冲突度仍然至少 22，因为它们是按**原始 G** 测量，未发生删边。
- `Q₀` 仍然是完整冲突图中的团。
- 只需排除 18 边子团，就能得到对任意规模 `Q` 的普遍上界 17。

设置 `d_Q(v)=|(Q.filter (fun e => v ∈ e))|` 或复用 `edgeIncidences Q v`。**切勿混淆** `d_Q(v)`、`G.degree v` 和 `(conflictGraph G).degree e`。

按照 `max_v d_Q(v)≤4`，分为：

- **情况 A：** 所有原顶点的 `Q` 支撑度至多三；
- **情况 B：** 存在一个原顶点恰关联四条 `Q` 边。

情况 A 建议独立形式化 `strongClique_card_le_seventeen_of_support_degree_le_three`，它能复用于后续 high21、高20；可以采用第 5 节的具体方法。情况 B 建议先证明下面的局部预算和三种 `h` 情形。两类都封闭才可导出最终定理。

## 5. 情况 A：支撑度至多三

对应 `strong_clique_subcubic.md`。这是通用结构引理，不依赖高22假设；如果现有 EdgeCounting 已能更短完成，优先复用。

1. 对 `Q` 中任意两条不同边的强冲突进行边对计数，证明
   \[
   \binom{|Q|}{2}\le\frac32\sum_x d_Q(x)^2,
   \]
   其中求和可以限制在 `Q` 的端点支撑上，但冲突见证仍在原图 `G` 中。
2. 若 `|Q|=18`、全部 `d_Q(x)≤3`，据此约束 `d_Q=1,2,3` 的支撑顶点数量；原始稿列出的四种度数分布必须由 Lean 中的算术或 Finset 证明覆盖。
3. 排除含 `Q` 度 1 点的两种分布；再用取等条件排除 `10` 个三度点加 `3` 个二度点的分布。
4. 唯一剩余情形：12 个支撑点的 `d_Q` 都为 3。利用每条 Q 边都与另外 17 条冲突，证明原图在该支撑上是闭合的四正则、没有三角形；**闭合必须从条件推出，不得先验删除外部顶点。**
5. 对 Q 边的四圈重复计数：原研究得至多 9 个四圈；对 12 顶点的二步路径重新计数则至少得到 15 个四圈，矛盾。

也可用更短的仅针对 `high22`、`Q.card=18` 的证明代替，但终点的声明必须真实地覆盖全部 `Q` 支撑度至多三的情况。此处可能是本轮最耗时的部分，建议先完成通用有限集合计数和易于复用的中间引理，不要把未证分支埋进主定理。

## 6. 情况 B：存在一个关联四条 Q 边的根顶点

按 `high_conflict_thresholds.md` 第 1、2、4 节；当前 `High23Support` / `High23Outer` 的根标签、类型、边分类模块可以复用定义及不依赖高23的基础引理。

令根为 `v`，`A=N_G(v)`，由四条根 Q 边与 `hΔ` 得 `|A|=4`。由原冲突度至少 22 和禁三角推出 `A` 独立。令 `B` 表示除 `v`、`A` 外关联 `Q` 的支撑点；对每个 `x∈B` 定义**完整原图邻接类型**：

\[
T_x=N_G(x)\cap A.
\]

将 `Q` 覆盖为互不混淆的根星边、`A-B` 候选边以及 `B-B` 候选边，分别计 `4`、`T`、`h`。将原图中的全部 `A-B` 边数记 `S`。在 18 边反证中期待：

\[
18=4+T+h,\qquad T\le S\le12,\qquad h\ge2.
\]

解释每一个相等或不等式来自哪个 Finset 定义；尤其 `S` 包含 `Q` 以外的原边。对于任一 `B-B` Q 边 `xy`，它的两个类型必须共同覆盖四个根标签，否则与某条根 Q 边不冲突。对 `B` 支撑点的类型非空性质也要证明，不可先验写入定义。

### B1. 两次重复计数的根预算

对根标签 `a∈A`，原文给出必要不等式：

\[
\sum_{x\in B,\ a\in T_x}(|T_x|-1)
+e_G\bigl(N_G(a)\cap B\bigr)\le2.
\]

这条预算来自高22原根边和完整原图的四圈、三角形等重复贡献。它应独立落为 Lean lemma，例如 `high22_root_label_budget_two`；不要仅通过纸面公式或普通整数 `omega` 假定计数已经正确。若用较简化的预算，只要足以严密导出所有后续类型限制即可。

预计的结构结论：

- 四元类型会给任何相关根 Q 边至少 3 次四圈损失，因而不存在。
- 三元类型至多一个；存在三元类型时，不能有二元类型，且 `B-B` 中 Q 边最多一条，与 `h≥2` 矛盾。
- 因此所有 B 支撑点的类型大小为 1 或 2。
- 记 `k` 为二元类型点数。根预算给 `k≤4`。两点类型互补时才可能存在 `B-B` Q 边，这些边构成最大度至多二的二部图，且 `h≤k≤4`。

这些结论都要求完整证明，不能从 high23 的较强类型唯一性直接复制。

### B2. 剩余三种 `h` 值，逐个排除

在 18 边反证中 `h∈{2,3,4}`。

**`h=4`：** 二元类型恰有四点、其 `B-B` Q 边构成四圈。每个二元类型点已由两条 `A-B` 原边及两条 `B-B` Q 边达到原度四。又 `T=10`，二元类型最多贡献八条 `A-B` Q 边，必存在一个一元类型 Q 边 `ax`。类型不含 `a` 的两个饱和二元点若仍各保留某条 `A-B` Q 边，则要有新的 `x-y` 冲突见证，违反饱和。这迫使至少四条 `A-B` 原边不属于 `Q`，与 `S-T≤2` 矛盾。

**`h=3`：** 四个二元类型点之间的 Q 子图必须是四点路径 `P₄`。中间两点分别属于互补类型，且已达到原度四。又 `T=11`，必有一条一元类型 Q 边 `ax`；选一个类型不含 `a` 的饱和中间点，至少两条 `A-B` 原边不能进入 `Q`，却有 `S-T≤1`，矛盾。

**`h=2`：** `T=12`，故 `T=S=12`，所有 `A-B` 原边都被 `Q` 选中。令 `a_i` 为四种标签的一元类型点数，`c₁=∑a_i`，`k=c₂`。因每个标签二元支持至多二，而每个标签在 B 中原有三个邻点，得 `a_i≥1` 和 `c₁=12-2k≥4`。不同标签的一元类型 Q 边的外端必须相邻，度数约束给 `c₁-a_i≤3`。对四个标签求和，推出 `c₁≤4`，因此 `c₁=4`、`a_i=1`、`k=4`。这四个一元类型点构成 `K₄`，每个点再有一条 A 邻边，全部原度饱和。最后与一条标签不相容的二元类型 `A-B` Q 边的冲突要求新增邻边，矛盾。

完成 B1+B2 后，18 边子团的四星根情形被排除。**禁止将“度数饱和”理解为 Q 度饱和，须始终证明该原顶点已拥有四条不同的原图边。**

## 7. 工程实施和建议文件布局

允许按实际源文件选择更合理的 Lean 组织；尽量沿用既有 Finset / SimpleGraph 结构。建议：

```text
StrongEdge/
  Bounds/
    EdgeCounting.lean         # 已有：保留
    High23Local.lean          # 已有：保留
    High23Support.lean        # 已有：保留
    High23Outer.lean          # 已有：保留
    High23Four.lean           # 已有：保留
    High23.lean               # 已有：保留
    High24.lean               # 已有：保留
    High22Local.lean          # 新：22 度、双重复预算
    High22Subcubic.lean      # 新：Q 支撑度≤3
    High22RootFour.lean      # 新：根四星类型与 18 边排除
    High22.lean              # 新：通用上界 ≤17
  High23Packing.lean          # 已有：保留
  High22Packing.lean          # 新：只留下 high20/high21
  Audit.lean                  # 追加新定理的公理审计
```

开发顺序建议：

1. 复跑基线测试，检查所有真实签名和现存文件版本。
2. 实施 high22 的局部结构与两次损失计数，完成并审核 `High22Local.lean`。
3. 选择情况 A 或 B 中依赖较短的一支先证明；每一支单独可编译。
4. 完成另一支、合并 `high22_clique_card_le_seventeen`。
5. 追加条件性打包 wrapper，`high20`、`high21` 原样保留显式假设。
6. 运行完整构建、公理审计、源代码比较、checkpoint 归档。

如果先完成情况 B，但情况 A 未完成，应保留 B 的证明作为独立模块，不要用 `by_cases` 空分支、临时常量或显式类型字段掩盖余项。

## 8. 绝对禁止的捷径

- **不允许** `sorry`、`admit`、`sorryAx`、自定义 `axiom`、任意外加的 `constant`、`unsafe`、`native_decide` 作为数学正确性的替代。
- **不允许**把 `high20`、`high21`、`high22` 本身作为某个未说明的结构实例填给最后的 record；本轮要从 `hΔ`、`hQ`、`h22` 证明 high22。
- **不允许**在条件性推论中隐藏额外的 `NoTriangle`、`Girth`、`SupportClosed`、`AllDegrees23` 等前提。
- **不允许**把 `Q` 限制诱导的原图当作完整原图来重新计算强冲突，或让 `Q` 外的连接见证边消失。
- **不允许**把 `c_G(e)≥22` 擅自增强为 `c_G(e)≥23`，也不能把每条边“最多两个四圈”偷换成“全图无四圈”。
- **不允许**将有限规模原图枚举、Python 样本、外部 JSON 证书直接当成无限规模的普遍证明；只有 Lean 内核能检查的完整归约与有限验证才可能构成形式化证明。
- **不允许**编造编译、审计、散列值或已生成的文件；任何证明进度都以实际运行命令的日志为准。
- **不允许**更改已经定义的原强冲突、诱导匹配、计数对象，使较弱问题取代当前任务。

## 9. 验证与最终交接

在本地项目根目录运行基线：

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

按原样保存：

```text
verification/high22-baseline-build.log
verification/high22-baseline-axioms.log
```

中间可以单独构建新模块；最终**必须**运行完整命令：

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

将输出保存为 `verification/high22-build.log`、`verification/high22-axioms.log`。在 `StrongEdge/Audit.lean` 中为所有新公开定理追加独立 `#print axioms`；保存最终 `#check` 给出的**完整定理签名**。期望除 Lean/mathlib 常规逻辑公理 `propext`、`Classical.choice`、`Quot.sound` 外，没有其他公理依赖；若有额外依赖必须明确列出并说明来源。

补充完成以下可复核交付物：

```text
HIGH22_HANDOFF.md                         # 实际结果、数学结论、未证目标、完整签名
verification/high22-source-sha256.json    # 新旧源文件与配置的 SHA-256
verification/high22-source.diff           # 与上个 high23 checkpoint 比较
verification/high22-change-summary.json   # 增删改文件清单
verification/high22-source-checks.json    # 禁止项扫描，不能替代公理审计
../strong_edge_lean_high22_checkpoint.zip # 源码+锁文件+文档+日志，排除编译器、.lake、cache
```

核对 checkpoint 中源文件与本地工作区逐字节一致；保留旧 checkpoint、旧验证日志和已有变更。若本项目仍是外层 Git 仓库的 **untracked** 目录，`git diff --stat` 为空并不表示源码没有变化；须对照前一个 checkpoint 的内容与 SHA-256 清单。**不擅自提交或推送到公开 GitHub。**

### 最终验收分类

- **完整成功：** `high22_clique_card_le_seventeen` 仅在 `hΔ`、`hQ`、`h22` 等正当假设下通过 Lean；最小 record `high22` 完成；条件打包器只剩 `high20`、`high21` 显式前提；完整构建和公理审计真实通过。
- **部分成功：** 只有新局部引理、情况 A 或情况 B 被内核验证；列出尚未证明的**具体 Lean 声明**、失败的逻辑步骤及其实际条件，保持其余成果可复现。
- **发现反例或漏洞：** 提供确切的有限原图边集、候选强团 Q、原图最大度、所有 Q 边的完整冲突度、冲突表及独立核查方法；区分数学错误与 Lean 语法/类型阻塞。不要把一次编译失败断言成反例。

**无论本轮结果如何，不得报告“二十倍无条件打包完成”或“强边二十色已证明”，除非所有相应证明义务真的在 Lean 内核中被逐项解除。**
