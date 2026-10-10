# Lean 4 形式化验证交接：最大度四图的任意候选边集二十倍诱导匹配界

> **2026-10-09 第二阶段更新（已运行 Lean）**：C4 已完成。
> `StrongEdge.conflict_degree_le_24` 仅由有限简单图的原顶点度数 ≤4 推出完整冲突度 ≤24。
> 新增八条取等结构引理：冲突度为 24 时，端点及六个其他邻点度数为四，
> 六个其他邻点构成独立集，端点不在三角形中，固定边不在四圈中。
> 新增 `MinimalCliqueBounds20`，最后一档只要求团大小 ≤15；原接口及旧核心源码不变。
> 全量构建通过（1127 jobs）；38 个定理的公理审计仅包含标准三个公理。
> 五个团界字段仍未证明，无条件 C6 未完成。当前完整记录见
> `verification/NEXT_STAGE_REPORT.md`、`verification/next-stage-build.log` 和
> `verification/next-stage-axioms.log`。下列第一阶段更新及原始正文仅作历史记录。

> **2026-10-09 本地续作更新（已运行 Lean）**：基础形式化与条件性包装定理已经编译通过，`lake build` 完成 1124 项任务。C0–C3 已完成；C4 中候选冲突度不超过完整冲突度已证明，但完整冲突度 ≤24 尚未证明；C5 和无条件 C6 仍未完成。
>
> 新增并核验：`optimal_exists`、`private_degree_mono`、`private_double_count`、`packing20_of_thresholds`、`subset_packing20_of_thresholds`、`induced_matching_packing20_of_thresholds`，以及完整原图/删边图的 P4 冲突反例。最后一个定理显式保留 `CliqueThresholds20 (conflictGraph G)` 前提，**不是无条件二十倍定理**。
>
> 13 项 `#print axioms` 检查均仅列出 `propext`、`Classical.choice`、`Quot.sound`；源码无 `sorry`、`admit`、新增 `axiom`、`unsafe` 或 `native_decide`。Lean/mathlib 版本保持原固定值，已保存 `lake-manifest.json`。详见本目录 `README.md`、`verification/build.log`、`verification/axioms.log` 和源码指纹。
>
> 下文保留原始交接正文作为历史记录；其中“未编译的起步草稿”等状态描述已由上述实际构建结果更新。最终结构性阈值证明仍须继续。

---

> **用途：** 交给下一轮 AI、Lean 工程师或数学审查者，直接接续形式化工作。本文聚焦**验证一个指定数学命题**，不承担证明原创性或解决整数强边二十色猜想的任务。
>
> **整理时间：** 2026-10-09（Australia/Melbourne）。**当前状态：未完成形式化证明。** 已有一个**尚未编译通过验证**的 Lean 起步项目，完整主定理以及高冲突强团引理均尚未由 Lean 内核检查。

## 0. 一分钟摘要

目标是验证：对于任何有限简单图 `G`，若 `Δ(G) ≤ 4`，那么对原边集的任意子集 `F`，都能从 `F` 选出一个大小至少 `|F| / 20` 的**按完整原图定义的**诱导匹配。

数学上记为

\[
\boxed{\forall G\ \bigl[\Delta(G)\le 4\bigr]\ \Longrightarrow\
\forall F\subseteq E(G),\quad |F|\le 20\nu_s^G(F).}
\tag{TARGET}
\]

其中 `ν_s^G(F)` 是 `F` 中两两**强不冲突**的最大边集大小；判定冲突时，`G` 的**全部边**都可以成为冲突见证，包含不属于 `F` 的边。二十作为统一常数是最佳的：五圈的双点吹胀图有 20 条边，任意两条互相冲突。

**严格禁止混淆：** `TARGET` **并不意味着** `χ(L(G)^2) ≤ 20`，不能将证明最后一步写成整数强边二十色。反过来，已知整数强边二十一色上界可给出较弱的 `|F| ≤ 21ν_s^G(F)`。

### 任务完成判据

- 形式化源代码能在记录的 Lean/mathlib 版本上 `lake build` 成功。
- 顶层定理对**所有有限简单图、所有候选边集**量化；没有偷偷假设围长、正则性、连通性或具体图规模。
- 从冲突定义到最后推论的**所有被调用引理**都有经过内核核验的证明；不得以未经证明的局部上界作为隐藏假设。
- 无 `sorry`、`admit`、非必要 `axiom`、`unsafe` 的证明替代品；`#print axioms` 的输出要附审查说明（Lean 的标准逻辑公理应与人为增添的公理区分）。
- 有测试证明：删去不属于 `F` 的原边**会改变**候选边的冲突关系，因此代码确实保留完整原图。
- 在完成这些条件前，只能称为 *formalisation in progress*，不能称为 Lean 已证明二十倍定理。

## 1. 唯一权威输入与版本

**公开研究仓库：** <https://github.com/congyuemao/strong-edge-colouring-research>

**研究分支：** `codex/research-archive`  
**审查时仓库提交：** `3a95c4a9c44475196c42b6eab4749c487d15d59b`

**首先阅读：**

1. [`research/packing_private_cliques.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/packing_private_cliques.md)：最终数学证明、双重计数、20/19.5 两个结论和局部改进算法。
2. [`research/clique20_rigidity.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/clique20_rigidity.md)：20 条强团边的唯一紧例及孤立分量分类。
3. [`research/high_conflict_thresholds.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/high_conflict_thresholds.md)：较早的 21、22 阈值强团界。
4. [`research/high_conflict_subcubic.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/high_conflict_subcubic.md) 与 [`research/strong_clique_subcubic.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/strong_clique_subcubic.md)：无四边星时的团界及关联引理。
5. [`research/critical_support.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/critical_support.md)：完整冲突度 24 的强团至多 7 边。
6. [`research/high_conflict_20_21_improved.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/high_conflict_20_21_improved.md)、[`research/high_conflict_22_improved.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/high_conflict_22_improved.md)、[`research/high_conflict_23_improved.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/research/high_conflict_23_improved.md)：19.5 加强版使用的更严阈值。
7. [`docs/AUDIT_AND_CORRECTIONS.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/docs/AUDIT_AND_CORRECTIONS.md) 与 [`docs/REPRODUCIBILITY.md`](https://github.com/congyuemao/strong-edge-colouring-research/blob/codex/research-archive/docs/REPRODUCIBILITY.md)：证据边界和既往错误。

**辅助 Python：** `research/packing_local_algorithm.py`、`research/packing_verify.py`、`research/packing_certificates.json`。程序样例与有限证书可用于回归测试，但**不能替代普遍证明**。

**已准备的独立 Lean 起步目录**（来自此前对话，可与本 MD 放在同一工程目录）：

```text
strong_edge_lean_starter/
  lean-toolchain
  lakefile.toml
  StrongEdge.lean
  StrongEdge/Basic.lean
  README.md
```

在 2026-10-09 创建时，起步项目把 mathlib 固定在提交 `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`，工具链声明 `leanprover/lean4:v4.35.0-rc4`。**注意：旧 `Basic.lean` 未经 `lean` / `lake` 编译！** 其标识符或 tactic 使用可能无法类型检查；它是一个待调试的草稿，不是可信的证明前置条件。若更新版本，记录 `lean-toolchain`、`lake-manifest.json` 和新提交 SHA。

## 2. 必须固定的定义与等价关系

### 2.1 原图边、候选边、冲突关系

- `G`：有限、无向、无自环的 `SimpleGraph V`。
- `E(G)`：原图全部边；可以使用 `G.edgeSet` 的子类型。
- `F : Finset G.edgeSet` 或 `F : Set G.edgeSet` 且 `[Fintype F]`。推荐第一种以便计数。
- 对 `e ≠ f`，若它们共用原顶点，或存在 `G` 的某条边连接 `e` 的某端点与 `f` 的某端点，就称 `StrongConflict G e f`。
- 等价实现：`G.lineGraph` 中 `e,f` 距离为一或二；**中间边必须允许从整个 `G.edgeSet` 选择**。
- `H_F`：把完整冲突图 `H_G = L(G)^2` 限制到顶点集 `F` 所得的**诱导子图**。先建立 `H_G` 再取 `induce F`；不要先删原图边。
- `ν_s^G(F) = α(H_F)`：`H_F` 的独立数。

要在 Lean 中证明并留下两项规格检查：

1. `H_F.Adj e f ↔ StrongConflict G e f`，其中 `e,f ∈ F`。
2. `H_F` 中的独立顶点集与原图 `G` 中候选边的诱导匹配**精确等价**。

**关键反例测试**：四点路径 `0—1—2—3`，`F = {01,23}`。在完整图中这两条候选边冲突，`ν_s^G(F)=1`；仅保留 `F` 得到的两条不连通原边则不冲突，诱导匹配数为 2。任何把它们误认为相同的定义必须退回修正。

### 2.2 完整冲突度与候选冲突度

对 `e ∈ E(G)` 记

\[
c_G(e)=\deg_{H_G}(e).
\]

对 `e ∈ F` 记

\[
d_F(e)=\deg_{H_F}(e).
\]

必须始终区分：

\[
0\le d_F(e)\le c_G(e)\le24\quad(\Delta(G)\le4).
\]

**局部阈值定理的前提是完整原图冲突度 `c_G(e)`，而私有集的交换证明最先得到的是 `d_F(e)`。** 连接两者的单调关系是主证明不可省略的接口。

## 3. 纸面证明的主干（先形式化这一层）

接下来暂将 `H` 看作任意有限简单图，顶点集 `U`，以便把一般组合论证从 `G` 的特殊结构中分离。

### 3.1 选择最优独立集

选择最大独立集 `M`，在全部最大独立集中使

\[
\Phi(M)=\sum_{m\in M} d_H(m)
\]

最小。有限性确保该选择存在。`M=∅` / `U=∅` 等边界须明确处理。

对 `m ∈ M`，设

\[
P_m=\{x\in U:N_H[x]\cap M=\{m\}\}.
\]

这是 `m` 的**私有闭邻域**，包含 `m` 本身。

### 3.2 两个交换引理

- **私有团**：`P_m` 在 `H` 中是团。若不同的 `x,y ∈ P_m` 不相邻，则 `(M \ {m}) ∪ {x,y}` 是更大的独立集，矛盾。
- **度数单调**：对每个 `x ∈ P_m`，有 `d_H(x) ≥ d_H(m)`。否则 `(M \ {m}) ∪ {x}` 仍是同样大小的独立集，但其度数和更小，矛盾。

这里的 `d_H` 必须是**当前整个 `H` 的度数**，不可替换为 `H[P_m]` 的内部度数。

### 3.3 私有集与双重计数

定义覆盖次数

\[
r(x)=\left|N_H[x]\cap M\right|.
\]

由于 `M` 是极大独立集，`r(x)≥1`。`r(x)=1` 的顶点分别且仅分别落在某个 `P_m`，这些 `P_m` 彼此不交；其余点有 `r(x)≥2`。双计数给

\[
\sum_{m\in M}\bigl(d_H(m)+1\bigr)
=\sum_{x\in U}r(x)
\ge 2|U|-\sum_{m\in M}|P_m|.
\]

从而得到通用引理：

\[
\boxed{2|U|\le\sum_{m\in M}\left(d_H(m)+1+|P_m|\right).}
\tag{COUNT}
\]

**Lean 形式化推荐证明顺序**：有限和交换、唯一归属、覆盖次数的逐点下界、`COUNT`。不要把 `COUNT` 当作外部假设导入最终定理。

### 3.4 将具体强团界接到抽象引理

对于 `H=H_F`，每个 `P_m` 在 `H_F` 中为团，即原图 `G` 的**强团**。由交换引理：

\[
\forall x\in P_m:\quad c_G(x)\ge d_F(x)\ge d_F(m).
\]

因此，只要有一组“所有团成员的完整冲突度至少 `d` 时，该团至多 `b(d)` 点”的界，便可限制 `P_m`。

### 3.5 二十倍主定理真正需要的局部表

| `d = d_F(m)` | `|P_m|` 上界 | `d+1+|P_m|` 上界 | 来源 |
|---:|---:|---:|---|
| `0…19` | `d+1` | `≤40` | `P_m ⊆ N_H[m]` |
| `20` | `19` | `40` | 20 团等号刚性 |
| `21` | `18` | `40` | 完整冲突度 ≥21 的团界 |
| `22` | `17` | `40` | 完整冲突度 ≥22 的团界 |
| `23` | `16` | `40` | 完整冲突度 ≥23 的团界 |
| `24` | `7` | `32` | 完整冲突度 24 的团界 |

所有情况满足

\[
d_F(m)+1+|P_m|\le40.
\tag{LOCAL}
\]

将 `LOCAL` 代入 `COUNT`，得到

\[
2|F|\le40|M|\quad\Longrightarrow\quad |F|\le20|M|\le20\nu_s^G(F).
\]

为了简化 Lean 工程，建议先实现**抽象定理**：有限图满足上面局部团界配置，则其 Hall ratio 至多 20；随后把 `H_F` 作为实例，并形式化验证团界。注意这个抽象定理可以使用**有名的、明确的局部前提**，但最终对 `G,F` 的定理不允许保留这些尚未证实的前提。

## 4. 最难的证明依赖与独立验收

严格区分三类：

- **定义、组合推导**：Lean 应首先完成。没有充分理由跳过它们。
- **结构性图论分类**：可能需要大量形式化，最好逐档攻克。
- **Python 检查及已有 JSON 证书**：只用于提出反例、交叉测试或者在经过证明的有限归约后作内核可检查的计算；不能直接替代结构定理。

### 必需的局部证明节点

| 节点名（建议） | 目标命题 | 前置材料 | 验收条件 |
|---|---|---|---|
| `conflict_degree_le_24` | 若 `Δ(G)≤4`，则 `c_G(e)≤24` | 端点及邻边计数 | 任意 `G,e` 的 Lean 定理 |
| `clique20_rigidity` | 20 条两两冲突原边必恰为一个孤立的双点五圈完整分量 | `clique20_rigidity.md` | 任意 `G,Q`，包含完整等号结论 |
| `high_conflict_21_le_18` | 团中每条边 `c_G≥21` ⇒ `|Q|≤18` | `high_conflict_thresholds.md` | 完整原图原度数，不是假设候选图度数 |
| `high_conflict_22_le_17` | `c_G≥22` ⇒ `|Q|≤17` | 同上 | 全部结构分支结束 |
| `high_conflict_23_le_16` | `c_G≥23` ⇒ `|Q|≤16` | `high_conflict_subcubic.md` | 团支撑外的原边仍参与冲突 |
| `high_conflict_24_le_7` | `c_G≥24` ⇒ `|Q|≤7` | `critical_support.md` | 只由 `Δ(G)≤4` 推出，无附加正则性 |
| `packing20` | 最终 `|F|≤20ν_s^G(F)` | 全部上述结论、`COUNT`、`LOCAL` | 顶层定理无未证前提 |

若先对后五项建“证明规格接口”，可以在独立文件中临时作**条件性定理**，例如 `packing20_of_thresholds`；条件必须在最终的 theorem 参数中明确出现。绝对不要用隐藏的 `axiom high_conflict_...` 伪装为已完成的结果。

### 需要重点防范的证明漏洞

1. **把完整冲突度与候选冲突度混为一谈。** `c_G` 和 `d_F` 只能经证明了的 `d_F≤c_G` 连接。
2. **在抽取候选边后删除冲突见证。** `F` 是冲突图的顶点子集，不是重新定义原图。
3. **把 20 强团大小上界当作其等号分类。** `d_F=20` 档需要团的刚性，不能仅引用 `ω≤20` 就得到 `|P_m|≤19`。
4. **给局部支撑点错误补满原度数。** 一些结构证明只能给出不等式，不能默许未知外部邻边不存在。
5. **误用有限样本计算。** 1362 份实验不涵盖任意规模、任意 `F`，也不能代替含全量词的结构证明。
6. **把 19.5 加强版的强团表与 20 版混写。** 先单独完成 `packing20`，再做加强版。
7. **把 `packing20` 当成二十色染色。** Hall ratio 上界没有自动给出整数染色。

## 5. 第二目标：排除紧分量后的 19.5 倍加强（可后置）

原稿另有

\[
2|F|\le 39\nu_s^G(F)+t,
\tag{BONUS}
\]

其中 `t` 是**原图中的孤立紧二十边分量、并且其全部 20 条边均包含于 `F`** 的分量数量。若 `t=0`，得 `|F| ≤ (39/2)ν_s^G(F)`。

去掉这些完整紧分量后，局部表加强为：

| 候选度 `d` | 私有团规模上界 |
|---:|---:|
| `0…18` | `d+1` |
| `19` | `19`（20 点强团被孤立紧例分类排除） |
| `20` | `18` |
| `21` | `17` |
| `22` | `16` |
| `23` | `15` |
| `24` | `7` |

从而每项 `d+1+|P_m|≤39`。原文 `research/high_conflict_*_improved.md` 给出加强阈值。对于 `BONUS`，还必须形式化证明图按孤立紧分量分解时，`|F|` 的变化及最大诱导匹配数的可加性。**这部分不属于第一轮成功标准。**

## 6. Lean 工程分层与建议文件

建议先保留起步项目，再逐步拆分成：

```text
StrongEdge/
  Basic.lean                 # 旧起步草稿；先编译/修正，再逐步迁移
  Conflict.lean              # 完整原图冲突定义、对称、无环、诱导子图
  FiniteIndependent.lean     # Finset/Set 独立性、选最优 M、私有集
  PrivateExchange.lean      # 私有团、度数交换、覆盖次数
  DoubleCount.lean          # COUNT 及抽象图的 packing 定理
  Bounds/
    Degree24.lean           # c_G(e) ≤ 24
    Clique20.lean           # 紧二十团结构
    High21.lean             # 21 阈值
    High22.lean             # 22 阈值
    High23.lean             # 23 阈值
    High24.lean             # 24 阈值
  Packing20.lean            # 完整主定理（不得留结构性假设）
  Packing195.lean           # 后续可选
  Tests.lean                # P4 反例及小图回归测试
```

### 类型接口示意（*伪签名，未经编译*）

以下仅展示数学语义与模块边界；mathlib 具体名称、型别转换、`Fintype` 实例和 `Finset`/`Set` 接口应以实际 `#check` 与编译结果为准。

```lean
-- SPECIFICATION ONLY: do not assume these signatures compile verbatim.
namespace StrongEdge

-- All witnesses live in G.edgeSet, independently of F.
def StrongConflict (G : SimpleGraph V)
    (e f : G.edgeSet) : Prop := ...

-- Vertices are selected original edges, while conflicts come from G.
def CandidateConflictGraph (G : SimpleGraph V)
    (F : Set G.edgeSet) : SimpleGraph F := ...

-- For an independent M, define private vertices for each m ∈ M.
def PrivateSet (H : SimpleGraph U) (M : Finset U) (m : U) := ...

-- Generic graph theory: private clique, swap monotonicity, COUNT.
-- Then export a conditional packing theorem with visible hypotheses.

-- FINAL GOAL (pseudo-interface):
-- theorem packing20 {V : Type*} [Fintype V] [DecidableEq V]
--     (G : SimpleGraph V) (hΔ : ∀ v, G.degree v ≤ 4)
--     (F : Finset G.edgeSet) :
--     F.card ≤ 20 * maxInducedMatchingSize G F := by ...

end StrongEdge
```

可避免一开始就绑定 mathlib 尚不熟悉的 `indepNum` 接口：先用 `∃ M : Finset F, M.card * 20 ≥ F.card ∧ IsIndep M` 形式给出**存在性目标**。随后再定义或引用最大独立数并证明等价；这也自然覆盖 `F=∅` 的情况。

## 7. 具体执行顺序与停止条件

建议不要一次性让一个代理生成数千行 Lean 代码，而是按以下检查点逐步完成：

- [ ] **C0 环境复现。** 解压并构建旧起步工程；记录 Lean / mathlib 版本及每一个编译错误。当前没有任何“已编译通过”的记录。
- [ ] **C1 冲突定义。** 完成 `StrongConflict`、`CandidateConflictGraph`、定义等价及 P4 小例子。
- [ ] **C2 纯图论私有邻域。** 最大独立集存在性、私有集是团、次级最小度数和选择、度数单调性。
- [ ] **C3 双重计数。** 推出 `COUNT`，并证明抽象 `LOCAL ⇒ packing20` 版本。这是第一个有实质意义且不依赖复杂结构分类的内核检查里程碑。
- [ ] **C4 原图度数。** 证明 `Δ(G)≤4 ⇒ c_G(e)≤24`、`d_F(e)≤c_G(e)`。
- [ ] **C5 强团阈值。** 逐一完成 20 团刚性、21/22/23/24 阈值证明；每完成一档都保留独立顶层 `theorem` 及审查记录。
- [ ] **C6 最终无条件主定理。** 组合 C1–C5，检验 `∀ F` 与 `∃ M⊆F`；运行 `#print axioms`。
- [ ] **C7 可选加强。** 证明 `BONUS` 与局部算法终止/复杂度；第一轮不必做。

**如果卡在 C5**：保留 C1–C4 已证明的模块，明确写出卡住的阈值，不得通过添加未经证实的假设来声称 C6 成功。这本身也能显著定位原纸面证明需要人工审查的部分。

## 8. 构建与审计命令

在已安装 Lean 4 / elan 且能取得 mathlib 的环境中：

```bash
cd strong_edge_lean_starter
lake update
lake exe cache get
lake env lean StrongEdge/Basic.lean
lake build
```

注意：`lake update` 可能重写依赖锁定信息，严格复现时应保存原版并检查变更。首次构建通过之后，将 `lake-manifest.json` 纳入版本控制，再开展增量形式化。

对最终完成的主定理额外运行（示意，具体名称按代码调整）：

```lean
#print StrongEdge.packing20
#print axioms StrongEdge.packing20
```

还需要审查 `import` 引入的定义是否真的表示欲证明的对象、主定理是否偷偷添加了过强的 `[Decidable]` 之外的数学假设。`Classical.choice`、`propext` 等 Lean 标准逻辑基础须与人为新增公理区别对待。

## 9. 交接者应持续填写的进度日志

请每次实际运行 Lean 后维护这一小表，而不是更新无证据的“已完成”描述：

| 日期 | 文件 / 定理 | 状态 | 运行命令与结果 | 剩余问题 |
|---|---|---|---|---|
| 2026-10-09 | `StrongEdge/Basic.lean` 起步草稿 | **未编译，未认证** | 原环境无 `lean` / `lake` | API 与证明脚本都可能有错误 |
| 2026-10-09 | `TARGET` | **尚未形式化** | 无 | `COUNT`、阈值分类、最终组合均待完成 |
| 2026-10-09 | `BONUS` | **尚未形式化** | 无 | 加强阈值及紧分量计数 |

## 10. 给下一轮执行者的直接工作指令

> 先阅读本文，以及 `research/packing_private_cliques.md`、`research/clique20_rigidity.md` 和此前 Lean 起步项目。当前没有任何经过 Lean 核验的二十倍主定理。先在实际 Lean/mathlib 环境中编译旧 `Basic.lean`，修复 API 与类型问题；随后优先完成私有团、度数交换和双重计数，建立含**显式局部界前提**的通用定理，再逐个形式化强团阈值。每次只报告确实通过内核检查的 theorem 名称和构建日志。保留完整原图中的所有边作为冲突见证；不要把候选集外的边删掉。不得使用 `sorry`、新增 `axiom` 或把样本验证伪装成全量词证明。若纸面引理被 Lean 揭示为错误，应给出最小反例或准确指出失败的数学假设，并更新研究状态。

---

**最终成功标志：** Lean 内核确实接受一个无需未证数学前提、对所有有限简单 `G` 和所有 `F⊆E(G)` 成立的二十倍诱导匹配定理。它只认证数学正确性；不能认证新颖性，也不能自动解决整数二十色猜想。
