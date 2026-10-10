# Codex 任务：无条件 20-packing 定理的独立复现、语义审计与先例审查

## 角色、输入与边界

你正在维护用户本地的 `strong_edge_lean_starter` Lean 4/mathlib 项目。用户已提供一份题为 `C5 high20 and C6: verified handoff`、日期为 2026-10-10 的验收报告。**报告声称**无条件二十倍诱导匹配定理已经通过 `lake build` 和 Lean 公理审计。你的本轮任务是核查这项声称并形成面向外部研究者的可复现材料，**无需继续研究二十色猜想**。

前一个报告不是数学证明的可信输入。实际的 Lean 源码、完整定理类型、Lean 内核复现结果、锁定依赖及数学语义才是检查对象。如果完整工程不在当前工作区，明确报告缺失路径并停止验证；不得根据报告虚构构建成功。

历史数学说明书固定来源：
- `https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/packing_private_cliques.md`
- `https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/high_conflict_20_21_improved.md`
- `https://github.com/congyuemao/strong-edge-colouring-research/blob/3a95c4a9c44475196c42b6eab4749c487d15d59b/research/clique20_rigidity.md`

已有验收报告中的终点声明（必须从实际源码重新确认，不可直接信任粘贴文本）：

```lean
StrongEdge.induced_matching_packing20
  {V : Type*} [Fintype V] [DecidableEq V]
  (G : SimpleGraph V)
  [DecidableRel G.Adj]
  [DecidableRel (StrongEdge.conflictGraph G).Adj]
  (hΔ : ∀ x, G.degree x ≤ 4)
  (F : Finset G.edgeSet) :
  ∃ M ⊆ F, StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧
    F.card ≤ 20 * M.card
```

Lean 环境必须使用工作区既有锁定文件：Lean `leanprover/lean4:v4.35.0-rc4`、mathlib `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`。不要运行 `lake update`，不要修改锁定依赖，也不要使用未声明的外部公理。

## 本轮首要目标：独立复现，而非只运行原始检查脚本

1. 建立**新的、与当前目录隔离**的临时检出或解压副本，来源为用户本地最终 checkpoint ZIP `strong_edge_lean_high20_checkpoint.zip`；若无法获得完整 checkpoint 或源码，记录缺失信息。对项目 `lean-toolchain`、`lake-manifest.json` 及 Lean 源码计算 SHA-256，登记在新审计报告。
2. 在隔离副本中按锁定版本获取所需依赖（如尚未缓存），运行真实的 `lake build`、`lake env lean StrongEdge/Audit.lean` 以及 `lake env lean StrongEdge/Tests.lean`。Windows 工程允许使用已有的 `lean.ps1` 包装器，但必须同时记录其实际调用的 Lean 编译器版本。保存原始标准输出、标准错误、退出状态码、实际日期和命令。
3. 从新编译后的声明打印完整 `#check StrongEdge.induced_matching_packing20` 和 `#print axioms StrongEdge.induced_matching_packing20`；对所有五个强团字段的最终供给定理亦分别打印。确认 `high20`、`MinimalCliqueBounds20` 或任何结构记录均**不是**最终定理的显式前提，也没有隐藏在 section 变量、额外 typeclass 或局部公理中。
4. 对工程自身源文件和其真实依赖做静态审计，特别查 `sorry`、`admit`、`sorryAx`、`axiom`、`constant`、`unsafe`、`native_decide` 和不可预期的 `opaque`/`noncomputable` 包装。注意 `noncomputable` 本身不代表错误；关键是内核依赖及声明类型。不得把文本搜索代替 `#print axioms`。
5. 独立比对报告中“旧文件未修改”“225 项审计”“构建无警告”的说法与实际日志和哈希。如果无法复核某项，必须标注为“仅报告声称”。

## 第二目标：语义独立审计，排除形式化了错误命题的可能

本阶段应格外认真。最终定理经过 Lean 内核验证，只能保证**被形式化的陈述**可以从其依赖导出；它不能自动保证该陈述等价于研究者想证明的图论问题。

A. 检查 `conflictGraph G` 的顶点类型确实为**完整原图所有边**，而不是只选中的候选边形成的子图。检查两个不同原边的冲突恰包含：(i) 共同端点；(ii) 存在一条原图边连接它们的端点。应确认不允许某条边与自身形成非法冲突。

B. 在新的 `AuditSemantic.lean` 中，以**独立写出的原端点关系**定义 `directStrongConflict G e f`，优先用两条原边的端点显式存在量词完成，不直接复用现有 `StrongEdge.strongConflict` 定义。尝试证明对不同边 `e f`：`(conflictGraph G).Adj e f ↔ directStrongConflict G e f`。如果因为接口成本无法完成，把可证明的方向及卡点精确记录，不得称“已验证等价”。

C. 重新审查 `IsInducedMatching G M` 与通常图论意义的 induced matching 是否相同，即任意两条不同的已选边不共端，且两条边的任意端点之间在**完整 G** 中均不存在原边。尝试在 `AuditSemantic.lean` 中表述并证明独立等价。

D. 确认 `F : Finset G.edgeSet` 的所有元素真为 G 的边，`M ⊆ F` 在同一 edge type 中解释，返回的集合实际有限，`F.card ≤ 20*M.card` 不依赖“F 非空”等额外前提。处理空图、孤立点、空候选集、非正规图、含三角形和四圈的图。

E. 设计独立回归：四点路径的首尾两边在完整路径中冲突，只取两条候选边时仍冲突；若真正**从原图**删去中间边，才不冲突。尽可能还对十顶点、二十边的双点五圈构形写出一个可核查的小例子，验证最大原度数为四、全部二十条边两两冲突，并说明常数二十为何不能再下降。注意：这些有限测试只是测试数学语义与紧例，不能取代一般定理的 Lean 证明。

F. 可选：通过独立端点定义与 mathlib 的平方线图定义建立等价，但如果库接口复杂，不得为了此项阻塞本次审计。该部分必须清楚区分“已验证”与“待完成”。

## 第三目标：证明依赖链审计

沿终点定理的**实际引用链**追踪以下关键节点：`high20 ≤19`、`high21 ≤18`、`high22 ≤17`、`high23 ≤16`、`high24 ≤13`、`MinimalCliqueBounds20` 记录构造、私有邻域交换、双重计数、任意候选子集与诱导匹配转换。

- 对每个节点记录 Lean 文件、精确 declaration 名称、核心假设及内核公理结果。
- 不得误将 `CliqueThresholds20` 旧接口中更强的 `high24 ≤7` 当作已证；最终定理用的是较弱 `MinimalCliqueBounds20.high24 ≤15`，由已证的 13 界供给。
- 检查不存在通过导入 `High20Packing` 等包装器绕回自身的循环证明或额外结构假设；实际 Lean 内核通常会阻止递归循环，此处重点核查陈述和依赖真正符合使用意图。
- 不得改变原图的边集来简化冲突关系；原图候选集合之外的边始终允许作为冲突见证。
- 在新独立副本运行审计时，源代码尽量只读；额外验证声明放在单独文件，不修改先前225项定理。

## 第四目标：文献中是否存在更强定理隐含这一结果

证明正确性与学术新颖性分开审查。最终命题等价于对所有最大度四原图 G，平方线图的 Hall ratio 满足 `ρ(L(G)²) ≤20`。检查已有文献中是否出现了此命题的等价变体、强于它的加权/分数染色论断、或能够简单推出它的局部独立集交换引理。

必须首先核对下列文献原始定理和证明范围：

1. Felix Joos, Viet Hang Nguyen, *Induced Matchings in Graphs of Degree at Most 4*, 2016, DOI `10.1137/140986980`：`https://epubs.siam.org/doi/10.1137/140986980`。它的摘要给出完整原边集最优20倍、排除紧分量时18倍。重点检查作者的**实际证明和任何加权/任意子集版本**；不能因摘要未写便断言没有。
2. Mingfang Huang, Michael Santana, Gexin Yu, *Strong Chromatic Index of Graphs With Maximum Degree Four*, 2018, DOI `10.37236/7016`：`https://www.combinatorics.org/ojs/index.php/eljc/article/view/v25i3p31`。它给出21色，自动蕴含任意候选集的21倍保证，不能自动推出20倍。
3. Raphael Steiner, *Fractional Chromatic Number Vs. Hall Ratio*, 2025, DOI `10.1007/s00493-025-00164-0`：`https://link.springer.com/article/10.1007/s00493-025-00164-0`。区分 Hall ratio 和分数色数。若找到 `χ_f(L(G)²) ≤20` 的既有结论，应立即指出它足以覆盖本研究命题。

继续使用关键词 `Hall ratio squared line graphs maximum degree four`、`induced matching every subset of edges graph Δ 4`、`hereditary induced matching bound`、`private neighbourhood local improvements strong clique degree thresholds`。对候选先例，必须给出**确切定理编号、原文前提、蕴含推导**。如果无法读取完整论文，明确写“未核查正文”。严禁根据没有搜索到同名标题就宣称原创。不得编造 DOI、引用或定理编号。

## 必需产出

在本地项目或用户指定归档目录中创建：

- `AUDIT_PACKING20_REPRODUCIBILITY.md`：隔离环境、日志、哈希、完整 `#check` 和 `#print axioms` 记录路径。
- `AUDIT_PACKING20_SEMANTICS.md`：独立冲突定义、诱导匹配等价、空集与紧例测试，标记已证明与仅测试。
- `AUDIT_PACKING20_DEPENDENCIES.md`：从最终定理到各证明模块的真实依赖映射。
- `AUDIT_PACKING20_PRIOR_ART.md`：文献范围、确认先例、无效推导、尚不确定处。
- `AUDIT_PACKING20_SUMMARY.md`：独立验收结果及未完成事项，严格区分：(1) 文本报告声称，(2) 实际 Lean 内核重编译，(3) 语义对应核查，(4) 学术原创性。
- 单独的新审计 Lean 文件及其日志，完整 checkpoint ZIP（仅在实际核查通过后制作，保留源文件及完整锁定配置，不加入编译器二进制与依赖缓存）。

## 禁止行为与最终验收

- 不使用 `sorry`、`admit`、自定义 `axiom`、隐式新参数或未经证实的有限枚举来填补普遍定理。
- 不把期刊论文中未形式化的定理“临时假设”为已完成阶段。
- 不以“没有找到先例”证明原创，不因 Lean 编译成功宣称整数强边二十色猜想成立。
- 不执行 Git push、发布 arXiv、投稿期刊或改动用户的公开仓库，除非用户另行授权。
- 不尝试本轮继续证明19.5加强，不变更原来的数学目标。

最终答复必须给出实际完成了哪些复现检查、真实的失败或障碍、数学语义是否同构、文献结论的证据级别，以及可重复运行的命令。用户不需要乐观的阶段总结；需要准确、可审计的完成状态。
