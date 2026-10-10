# PACKING19.5 续进：high21 完成，high22 缩到一个边界情形

日期：2026-10-10，Australia/Sydney。

**本轮完成无条件 `high21 ≤17`，并完成 `high22 ≤16` 的四边星根分支。
完整无条件 19.5 尚未完成。** 当前状态以本文件及
[续进状态](verification/packing195-continuation-status.json) 为准。
`PACKING195_PROGRESS.md`、`PACKING195_BLOCKERS.md` 和原 checkpoint 保留上一阶段原文。

## 新增的已验证结论

| 结论 | Lean 声明 | 范围 |
|---|---|---|
| 选中支撑度至多三的强团至多 17 边 | `clique_card_le_seventeen_of_support_degree_le_three` | 无冲突度阈值前提 |
| 完整冲突度至少 21 的强团至多 17 边 | `high21_clique_card_le_seventeen` | 完整的无条件局部阈值定理 |
| 完整冲突度至少 22、有四条选中关联边的强团至多 16 边 | `high22_clique_card_le_sixteen_of_root_four` | 四边星根分支 |
| 至少 17 边的次三次强团，其选中支撑在原图中闭合且四正则 | `subcubic_large_support_closed_regular` | 不删除候选集外的原边 |
| 只剩 high22 次三次 17 边排除的阈值构造器 | `cliqueBounds195_of_subcubic_high22` | 条件性接口 |
| 使用该构造器的候选集 19.5 界 | `induced_matching_packing195_of_subcubic_high22` | 还保留上述排除及 `no20` 两项前提 |

这里“无条件局部阈值”保留最大原度四、强团和阈值本身的定义性前提，
没有附加根类型、支撑闭合、分类或未证引理。它不等于无条件 19.5 总定理。

`high21` 的完整数学签名是：

```lean
theorem StrongEdge.high21_clique_card_le_seventeen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h21 : ∀ e ∈ Q, 21 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 17
```

## 次三次强团的 18 边排除：本轮使用的证明

反设强团 Q 有 18 条边，每个原顶点关联至多三条 Q 边。记这些关联度为 d(x)。
对任意 Q 边 uv，令 C(uv) 为两端除去彼此的其他原邻点之并。
已有覆盖计数给 `17 ≤ Σ_{x∈C(uv)} d(x)`，而 `|C(uv)|≤6`。
因此 C(uv) 恰有六点，每点关联至少两条 Q 边。

从任一支撑点的一条 Q 边出发，可以得到其原度为四，全部原邻点都在支撑中。
再经过一条邻点的 Q 边，可使这个支撑点进入另一个覆盖集，证明它自己的 Q 度也至少为二。
所以支撑中的 Q 度只可能是二或三。覆盖集中的二度点至多一个。

令 L 为 Q 度二的点集。对 x∈L，统计那些与 x 的原邻域相交、但不关联 x 的 Q 边。
Q 边不能位于原图三角形中，所以这项计数恰为

    c(x) = Σ_{a∈N_G(x)} d(a) − d(x)。

每条 Q 边至多计入一个 x∈L 的 c(x)，于是 `Σ_{x∈L}c(x)≤18`。
支撑闭合且原度四，邻点 Q 度至少二，先得 `c(x)≥6`，所以 `|L|≤3`。
此时 x 的四个邻点至多有两个属于 L，其余 Q 度三，进一步得 `c(x)≥8`，所以 `|L|≤2`。
握手等式是 `36+|L|=3|support(Q)|`，强迫 `|L|=0`，支撑恰有十二点且 Q 度全部为三。

固定支撑点 r。令 A=N_G(r)，R 为其三个 Q 邻点，B 为支撑中除去 r 和 A 的点。
Q 边不在三角形中，加上 r 的四个原邻点中有三个 Q 邻点，说明 A 独立。
有 `|A|=4`、`|R|=3`、`|B|=7`。对 x∈B 定义：

    s(x) = x 在 R 中的原邻点数；
    t(x) = x 在 A 中的 Q 邻点数。

原度四、Q 度三以及 A\R 只有一个点给出 `s(x)≤t(x)+1` 和 `t(x)≤s(x)+1`，
从而对所有这些自然数有 `s(x)+t(x)≤1+s(x)t(x)`。

双计数给 `Σ_B s=9`、`Σ_B t=9`。对每个 a∈R，边 ra 的六点覆盖集内部至多有一条 Q 边；
把这条边和 a 的另外两条 Q 边相加，得到 `Σ_{x∈B∩N(a)}t(x)≤3`。
再对三个 a 求和，得到 `Σ_B st≤9`。于是

    18 = Σ_B(s+t) ≤ |B|+Σ_B st ≤7+9=16，

矛盾。结合原来已验证的 ≤18，得到无阈值的 ≤17。
这条形式化路线不需要先补齐纸面稿的全局边对计数和四圈总数分类。

## 四边星根分支

四个全选二元点会耗尽各自除根邻域之外的全部原邻接位置。
进一步证明，若所有类型至多为二元，就不能再有其他选中的根部端点。
这个饱和引理甚至不需要 high21 阈值。

在 high21 分支，四个全选二元点给根部边数至多八；少于四个时至多九，
外部边数至多四。三元类型分支复用之前的十槽上界和至多两条外部边，得到更强的总数至多十六。
因此全部四边星根分支至多十七。

在 high22 分支，若有单元类型且外部边数为四，原有饱和引理把活跃二元点压到两个，
根部边数至多八；若外部边数至多三，新全选计数给根部边数至多九。
没有单元类型时，至多四个二元点直接给根部边数至多八。
结合三元类型分支，得到全部四边星根分支至多十六。

## 仍须完成的内容

1. **high22 的次三次 17 边边界。**
   `High22SubcubicSeventeenExcluded G` 明确定义为：不存在 17 条两两冲突的边，
   同时每个原顶点至多关联三条、每条边的完整冲突度至少 22。
   这是尚未证明的前提，不是公理或已断言的定理。
   新的闭合四正则支撑引理已经可用；纸面入口是
   [high_conflict_22_improved.md 第 1 节](../../../research/high_conflict_22_improved.md)。
2. **二十边强团刚性。** 仍须证明其对应原图的孤立完整 C5[2] 分量。
3. **真实紧分量计数与最终组装。** 定义 t_G(F)，处理完整、部分选取及多个紧分量，
   完成 `2|F|≤39|M|+t_G(F)`。当前接口没有引入该计数，`no20` 仍须显式提供。

high21 已从剩余前提中移除；high22 的四边星根分支也已移除。
整数强边二十色、算法复杂度及 19.5 常数的最优性不在本轮已证范围内。

## 验证与复现

- 完整构建：1,181 jobs，退出码 0，无警告。
- 新增 28 个定理及 3 个定义，31 项公理审计全部通过。
- 原 225 项和上一阶段 22 项公理审计重新运行通过；合计 278 项。
- 全部依赖只含 `propext`、`Classical.choice`、`Quot.sound`。
- 原四顶点路径测试和上一阶段 19.5 回归测试通过，分别覆盖候选集外冲突见证、空集和 K20 例外。
- 原 51 个 Lean 文件中仅入口 `StrongEdge.lean` 追加导入，其余 50 个及四个环境文件保持原始字节。
- 新增七个 Lean 文件，共 58 个；源码及环境散列共 62 项。
- 没有以随机或有限搜索代替任一新增普遍定理的证明，也没有加入未经内核检查的求值依赖。

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Audit195.lean
.\lean.ps1 env lean StrongEdge/Audit195Continuation.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
.\lean.ps1 env lean StrongEdge/Tests195.lean
python verification/finalize-packing195-continuation.py
```

全部实际日志以 `verification/packing195-continuation-` 为前缀。
[新源码快照](../strong_edge_lean_packing195_continuation_checkpoint.zip) 与旧快照并存。
第一次集成构建因引用未导入的旧 high22 全局声明失败；最终改用已经证明的无阈值次三次上界，
保留失败日志和退出码，最终构建及审计均通过。
