# PACKING19.5 剩余证明目标

更新：2026-10-10。这里登记尚未形式化的依赖，不表示已找到数学反例。
编译环境已恢复，T1/T2 与 high20 ≤18、high23 ≤15 已通过内核检查。

## 1. high21 ≤17

需要证明的声明如下；尚未作为 Lean 声明导入工程：

```lean
theorem high21_clique_card_le_seventeen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 17
```

现有 `High21.lean` 将问题分成选中支撑最大度 ≤3 和具有四边星根两个分支；二者目前只得 ≤18。
`SubcubicEighteen.lean` 排除了 19 边，不能排除 18 边。固定纸面版本的
`research/strong_clique_subcubic.md` 第 1—4 节给出了进一步所需的全局边对计数、
12 点闭合支撑与四圈计数路线；这些还没有对应的完整 Lean 引理。

四边星根分支见 `research/high_conflict_20_21_improved.md` 第 4 节。
可复用本轮的根部槽计数和饱和工具，但仍需补上全选四个二元点的饱和分类及其余排除。
不得把本轮已证 high20 ≤18 当成 high21 ≤17。

## 2. high22 ≤16

需要与上一个签名相同的图与团前提，将阈值改为 22、结论改为 `Q.card ≤16`。
现有 `high22_clique_card_le_seventeen` 还差一个单位。

固定纸面版本 `research/high_conflict_22_improved.md`：

- 第 1 节是支撑最大度 ≤3 的 17 边排除，需要缺额度数总和与二步邻域计数，现有模块未形式化。
- 第 2—5 节是四边星根分支，需要对外部边数 1—4 的遗漏边与饱和情形逐一处理。

这两个尚未证明的全局阈值，以 `h21`、`h22` 的名称完整暴露在
`induced_matching_packing195_of_two_improvements` 的签名中。

## 3. 二十边强团刚性及紧分量计数

还需要将任意 20 边强团分类为孤立的完整 `C5[2]` 分量，或者先证明其在完整冲突图中隔离。
二者都未由本轮证明。`no20` 仍然是独立的候选集假设。

最终 `t_G(F)` 必须准确统计原图中被 `F` 完整包含的 `C5[2]` 分量。
尚未定义此计数，也尚未证明剔除这些分量后候选边数、最大诱导匹配数分别减少 `20t`、`t`。
部分选取紧分量边、多个紧分量和空候选集都必须纳入最终组装。

无条件最终目标仍为：仅由原图最大度 ≤4，推出
`∃ M ⊆ F, IsInducedMatching G ↑M ∧ 2 * F.card ≤39 * M.card + t_G(F)`。

## 4. 下一轮入口

先保留并复核 [PACKING195_PROGRESS.md](PACKING195_PROGRESS.md) 的新定理和审计。
随后优先补 high21 的支撑最大度三边界及四边星根分支；high22 和刚性分类独立推进。
所有未完成命题仅登记于本文件，已验证模块没有引入占位证明或自定义领域公理。
