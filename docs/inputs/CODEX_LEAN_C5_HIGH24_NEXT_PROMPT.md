# Codex 续研提示词：形式化证明 `high24` 强团上界

## 你的任务

你正在继续一个已经有可编译 Lean 4 项目的数学形式化研究。**直接在现有本地项目中执行工作，不要只输出建议、伪代码或证明大纲。** 先读取当前仓库和验证日志，以代码、实际编译结果和公理审计为准，完成本轮尽可能多的内核可检查证明；若遇到真实障碍，保留已有成果并留下可以继续接手的精确记录。

本轮唯一主要数学目标：在原图最大度至多四的假设下，**无任何新的结构性假设**，证明完整原图冲突图中的 `high24` 强团上界，并将其接入已经存在的 `MinimalCliqueBounds20` 接口。其他 `high20`、`high21`、`high22`、`high23` 继续保持显式待证，不得声称无条件的二十倍打包定理已经成立。

## 0. 当前核验基线，不得误改写

用户于 2026-10-09 提供的 `Next-stage Lean verification report` 记录如下，正式状态以你本地源码和日志复核为准：

- C4 已完成：`StrongEdge.conflict_degree_le_24` 在所有原顶点度数 ≤4 的条件下，证明原边完整冲突度 ≤24。
- `StrongEdge/Bounds/ConflictRigidity.lean` 中已有局部取等定理：冲突度等于24的原边两端各为四度；两端除对方外的邻点共有六个、彼此不同、每点为四度，且该六点在原图中组成独立集。
- `StrongEdge/MinimalPacking.lean` 中有 `MinimalCliqueBounds20` 及条件性打包结论，`MinimalCliqueBounds20.high24` 的义务是：一个全体顶点**完整冲突度至少24**的冲突团，大小至多15。
- 截至报告时，最终 `lake build` 1,127 jobs 成功，38 个审计定理只依赖 `propext`、`Classical.choice` 和 `Quot.sound`；但五个高冲突强团上界**一个也没有证明**。
- 未完成：`high20/high21/high22/high23/high24`、无条件20倍打包、19.5倍加强。
- 不准将有显式 `MinimalCliqueBounds20` 参数的定理冒称为无条件结论。

锁定环境，不执行随意依赖升级：

- Lean `leanprover/lean4:v4.35.0-rc4`
- Lean compiler commit `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib commit `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`
- `lake-manifest.json` 是依赖基准；常规构建不运行 `lake update`。

必要的原始数学稿，均以仓库提交 `3a95c4a9c44475196c42b6eab4749c487d15d59b` 为准：

- [critical_support.md，尤其第1–2节](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/critical_support.md)
- [packing_private_cliques.md](https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md)

原稿给出的更强结果是“完整冲突度均为24的强团至多7边”；**本轮仅须证明≤15**。下面提供的较短推导可以先获得≤13，因此足以完成当前接口；先避免形式化为获得≤7而必要的额外跨侧不等式。

## 1. 首先检查本地项目，严禁凭报告猜测 Lean API

1. 阅读 `StrongEdge/Bounds/ConflictDegree.lean`、`StrongEdge/Bounds/ConflictRigidity.lean`、`StrongEdge/MinimalPacking.lean`、`StrongEdge/Basic.lean`、`StrongEdge/Conflict.lean`、`StrongEdge/Audit.lean`、`StrongEdge.lean`。
2. 查明实际使用的 `strongConflict`、`conflictGraph`、`endpointNeighbourCover`、`MinimalCliqueBounds20`、`Finset` 强团条件的**准确 Lean 类型**。
3. 检查已有方法中如何表示原图边 `e : G.edgeSet`、两个端点、边与有限集合相交、原图邻接以及有限集合基数。
4. 阅读现有 `verification/next-stage-build.log`、`verification/next-stage-axioms.log`，基线构建一次：
   ```powershell
   .\lean.ps1 build
   .\lean.ps1 env lean StrongEdge/Audit.lean
   ```
5. 在新增任何定理前记录现有 SHA-256 与工作树状态；不覆盖用户改动或现有证书。

## 2. 精确目标及形式化边界

设 `G` 为有限简单图，`∀ x, G.degree x ≤ 4`。令 `H = conflictGraph G`，它的顶点是**原图的全部边**，任意两个不同顶点是否相邻，始终由**完整原图 G** 判定。

待证命题：对任意 `Q : Finset G.edgeSet`，若

- `Q` 在 `H` 中两两相邻（强团条件）；
- `∀ e ∈ Q, 24 ≤ H.degree e`，这里是完整 `H` 中的度数，**并非** `H.induce F` 的候选集度数；

则 `Q.card ≤ 15`。鼓励证明更强的 `Q.card ≤ 13`，但这不是必要验收条件。

可以按当前库的实际 API 定义定理名，例如：

- `StrongEdge.high24_clique_card_le_thirteen`
- `StrongEdge.high24_clique_card_le_fifteen`

下面只是数学契约，不是已验证的 Lean 签名；不要原样粘贴未经核对的语法：

```lean
-- PSEUDOSIGNATURE: adapt to actual StrongEdge definitions / instances
-- (hΔ : ∀ x, G.degree x ≤ 4)
-- (Q : Finset G.edgeSet)
-- (hQ : Q is a clique of conflictGraph G)
-- (h24 : ∀ e ∈ Q, 24 ≤ (conflictGraph G).degree e) :
-- Q.card ≤ 15
```

**验收重点：** 上述主定理除 `hΔ`、`Q`、`hQ` 和 `h24` 外，不得新增“强团规模已经≤15”“原图无三角或无四圈”“紧图分类成立”等实际等价于结论的隐含前提。尤其不能在终点回引 `MinimalCliqueBounds20`、`CliqueThresholds20` 或未证的高冲突度结构结论。

## 3. 推荐数学路径：只证明接口需要的较弱界

**原稿第2节已证明更强的7边界。本轮可直接走更短的13边界：**

### 3.1 选取基准边并使用已验证的24取等结构

若 `Q` 为空则平凡；否则取 `uv ∈ Q`。

由 C4 得 `H.degree (uv) ≤24`，结合假设 `≥24` 得 `=24`。应用 `ConflictRigidity.lean` 中现成定理，得到

\[
A=N_G(u)\setminus\{v\},\qquad
B=N_G(v)\setminus\{u\}.
\]

- `A.card = 3`，`B.card = 3`；
- `A ∩ B = ∅`；
- `S=A∪B` 为原图独立集；
- 每条 `Q` 边各自具有冲突度24，因此**每条 `Q` 边**均可使用同样的邻域独立性定理。这一点在证明分支限制时非常关键。

### 3.2 分解 `Q` 中的其他边

由 `conflict_neighbors_subset_incidence_cover`，任何 `f ∈ Q \ {uv}` 都与 `uv` 强冲突，所以至少碰到 `A∪B`。

利用 `A∪B` 在原图中的独立性，且 `u,v` 不在此集合，可把 `Q` 中的边不重不漏地分类：

1. 中心边 `uv`，恰一条。
2. 除 `uv` 外关联 `u` 或 `v` 的星边：每侧最多三条，所以总数最多六条。
3. 不关联 `u,v` 且恰有一个端点在 `A` 的 **A侧外伸边**，记数 `r`。
4. 不关联 `u,v` 且恰有一个端点在 `B` 的 **B侧外伸边**，记数 `s`。

注意没有 `A-A`、`A-B`、`B-B` 原边，因为 `A∪B` 独立。尤其不允许把一个外伸边同时计入两侧。

目标推得：

\[
|Q|\le1+6+r+s.
\]

为了完成目标，只需证明 `r≤4`、`s≤4`，此时右侧≤15。但原稿存在一个同样简洁的加强 `r≤3`、`s≤3`，若形式化方便则优先完成它，使结果≤13。

### 3.3 关键单侧引理：同分支的两条外伸边排斥其他分支

要证明 `r≤3`，将A侧外伸边按其位于 `A` 的唯一端点 `a` 分组。每个 `a ∈ A` 已邻接 `u`，且原度至多四，所以还至多有三条外伸边。

证明下列**三条边不可能同时属于 Q**的局部引理：

- `a,a' ∈ A` 且 `a ≠ a'`；
- `a x₁`, `a x₂`, `a' y` 是 `Q` 中的三条不同外伸边；
- `x₁ ≠ x₂`；三条边都在 `Q`，因而两两强冲突、完整冲突度24。

证明思路（必须在 Lean 中把端点相等、原边见证等情况展开，不能引用未经证明的“显然”）：

- `xᵢ=y` 会形成 `u-a-xᵢ-a'-u` 四圈，违背 Q 边 `a xᵢ` 的24取等邻域独立性；
- `a` 与 `a'` 不相邻，由基准边 `uv` 的独立六邻域得到；
- `xᵢ` 与 `a'` 相邻也会产生上面的四圈；`a` 与 `y` 相邻同样会产生 `u-a-y-a'-u` 四圈。这些都可优先用已验证的 `no_cross_edge_of_degree_eq_24` 或 `cover_independent_of_degree_eq_24` 排除，避免另建一整套四圈 API；
- 由于 `a xᵢ` 与 `a' y` 强冲突，在共享端点和其他连接见证都被排除后，只能有 `G.Adj xᵢ y`；
- 因此 `y` 同时邻接 `x₁` 和 `x₂`，而 `a` 邻接 `x₁,x₂`。这构成 `a-x₁-y-x₂-a` 四圈，违背 `a x₁` 的24取等条件。

由此，每当至少两个不同A分支有外伸边，任何已被使用的分支都不能包含两条以上外伸边。由于 `|A|=3`，可得 `r≤3`。如果只有一个分支有外伸边，原度≤4使其最多三条。因此统一 `r≤3`。交换 `u,v` 得 `s≤3`。

得到：

\[
|Q|\le1+6+3+3=13\le15.
\]

**重要提醒：** 原始 `critical_support.md` 在继续分析跨侧星边后能加强到 `|Q|≤7`；这不是本阶段必要条件。形式化13边界后即可停止该分支，以免为了更强但暂时无用的结果耗费时间。

### 3.4 建议拆出的 Lean 引理

文件建议 `StrongEdge/Bounds/High24.lean`。实际命名遵循项目既有风格，不强制以下命名：

1. 给冲突度≥24的边推出=24；
2. 给基准边推导 `A,B` 的三个元素、互不相交和独立性；
3. 每条和基准边强冲突的不同边，都落入中心星边/一侧外伸边；
4. 对一条24度边，精确排除其两侧邻点间额外原边；优先重用现有 rigidity 引理；
5. `mixed_branches_cannot_have_fork`：不同A分支存在外伸边时，同分支不允许两个Q外伸边；
6. `u_side_external_card_le_three`；
7. `v_side_external_card_le_three`（能复用端点交换对称性）；
8. `high24_clique_card_le_thirteen`；
9. `high24_clique_card_le_fifteen`；
10. 在 `MinimalCliqueBounds20` 的实际结构/构造 API 中接入 `high24` 的无条件证明，保留其他四个未证字段为**显式参数**。

可用 `Finset` 的过滤、分割、注入与映射基数证明，优先利用 mathlib 已有定理，避免对图的整个邻接矩阵做穷举。

## 4. 数学审计中的易错点

- **完整原图原则：** `Q` 的强团与每条边的24度都在 `conflictGraph G` 中判断。筛选 `Q`、候选集 `F`、删去中心边等操作，不能改变原图冲突的见证。
- **边的无序性：** `G.edgeSet` 是无序端点边；把每条边写成 `a-x` 时，需要保持证明与端点顺序无关。必要时先建立端点选择和两端互换引理。
- **避免重复分类：** `uv` 先从 `Q` 去掉，`u` 星边与 `v` 星边除 `uv` 外不重合。外伸边没有同时位于 `A,B` 的可能性，理由是24度基准边的六邻域独立。
- **仅用原有的局部24取等条件：** 不得额外假设整个 `G` 无三角形或四圈。只使用选定24度Q边各自已证的局部禁形性质。
- **完整冲突度与候选冲突度分开：** 已有 `Conflict.lean` 包含“候选冲突度≤完整冲突度”，不要反过来使用。
- **组合数字**：`1+6+3+3=13`，故足以推出所需 `≤15`；既不证明 `≤7`，也不直接解决其余四档 `high20–high23`。
- **证明参数**：严禁使用一个名称模糊的 `hStructural`、`hCliqueBound` 等来暗中承载待证数学结论。

## 5. 验证、审核与验收

每完成一个可编译的引理就先做模块构建。完成后必须执行：

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
```

同时做到：

1. 新增的最终 `high24` 定理进入 `StrongEdge/Audit.lean`，显示实际 Lean 命题及 `#print axioms` 依赖闭包。
2. 没有 `sorry`、`admit`、自定义 `axiom`、`unsafe`、`native_decide` 或同效的未证实现；不得仅依赖文本扫描，必须核查审计中的依赖。
3. `#print axioms` 仅出现 Lean/mathlib 常规逻辑公理：`propext`、`Classical.choice`、`Quot.sound`。若有差异，逐项说明，不擅自隐去。
4. 检查 `MinimalCliqueBounds20` 中新接入的 `high24` 的调用方向，确保已经不需要来自任何未证强团上界的假设。
5. 原先已经通过的38个审计定理继续有效；不能通过删除原有审计项来制造“全部通过”。
6. 日志放入 `verification/high24-build.log`、`verification/high24-axioms.log`；记录项目源码/锁文件哈希，例如 `verification/high24-source-sha256.json`。
7. 更新项目 `README.md` 状态表与 `verification/high24-handoff.md`。明确本轮新增哪些 kernel-checked 定理、哪些仍未证明、是否有反例/错误假设、下一步应去哪一档。
8. 在不影响原项目的前提下生成源代码与必要验证日志的检查点归档，避免放入 Lean 编译器、`.lake/packages`、缓存等大型依赖文件。

**本轮达到目标的唯一判据：** `high24` 的原图结构界不带隐含前提、Lean 内核检查通过、确实用于填补接口中的 `high24` 项；其他字段保留显式待证，且旧定理和测试没有退步。

## 6. 如果遇到困难

优先在数学层面确认局部三边禁形引理是否正确，然后把 Lean 遇到的证明问题具体定位在：端点选择、邻点计数、冲突见证的分类、四圈排除、分支外伸边基数，或接口接入。

若本轮无法完整证明 `high24`：

- 保留所有已验证的新局部引理；
- 不要把含有待证明命题作为参数的 lemma 误报成无条件强团上界；
- 交接文档逐条列出已完成的 Lean 定理名、剩余精确数学命题、相应文件位置和编译状态；
- 区分数学反例、真正的理论证明缺口、Lean 实现困难；
- 不得报告虚构的 `lake build`、公理审计或文件产物。

若 `high24` 成功，下一阶段建议分别处理 `high23`、`high22`、`high21`、`high20`。本轮优先不要同时展开其余四条长证明，以保证已经完成的24取等成果能够形成可复用的模块。

## 7. 期望最终汇报

最终回应使用简洁的 Markdown 报告，至少包括：

- **证明结论**：`high24` 是否已经由最大原度≤4无条件推出；具体得到了≤15、≤13还是更强值。
- **可核验证据**：确切 Lean 定理名、文件路径、构建和公理审计命令及退出结果。
- **接口影响**：`MinimalCliqueBounds20` 还剩哪些字段未证明。
- **数学风险**：是否发现反例、需要补证的命题或仅仅存在实现阻碍。
- **保存状态**：新增源码、日志、哈希清单、检查点归档的位置。

以源码、锁定依赖、Lean 内核核验和真实日志为最终证据。禁止将当前阶段称为“无条件二十倍打包定理已证明”。
