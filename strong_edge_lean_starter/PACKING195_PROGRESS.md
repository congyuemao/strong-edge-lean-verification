# PACKING19.5 形式化进展：T1、T2、high20 与 high23

日期：2026-10-10，Australia/Sydney。

**本轮完成条件性 T1、T2，以及两个无条件局部加强：high20 ≤18、high23 ≤15。
完整的无条件 PACKING19.5 尚未完成。**

基线来自 GitHub 的 `codex/results-archive`，提交
`8de26d2d6cb17354af7fb5919fcdbbc79c8aaf6f`。本轮从远端重新克隆，并再次核对全部分支；
Lean 仓库仍只有该分支，纸面仓库仍只有 `codex/research-archive`，提交
`3a95c4a9c44475196c42b6eab4749c487d15d59b`。开发分支为 `codex/packing195`。

## 已完成的定理

| 内容 | Lean 声明 | 状态 |
|---|---|---|
| 通用条件性 19.5 打包，给出最大独立集见证 | `packing195_of_clique_bounds` | 内核检查通过 |
| 五档阈值界向诱导子图传递 | `cliqueBounds195_induce` | 内核检查通过 |
| 候选集版本，冲突保留在完整原图中 | `induced_matching_packing195_of_clique_bounds` | 内核检查通过 |
| 完整冲突度 ≥20 的强团至多 18 边 | `high20_clique_card_le_eighteen` | 无条件局部定理；内核检查通过 |
| 完整冲突度 ≥23 的强团至多 15 边 | `high23_clique_card_le_fifteen` | 无条件局部定理；内核检查通过 |
| 只剩 high21、high22 两档的阈值构造器 | `cliqueBounds195_of_two_improvements` | 条件性；内核检查通过 |
| 当前候选边集最终接口 | `induced_matching_packing195_of_two_improvements` | 条件性；内核检查通过 |

这里“无条件局部定理”仍具有其定义性的最大度、强团、完整冲突度阈值前提，
没有额外的根类型、支撑闭合或分类假设。

### 两项新阈值的完整签名

```lean
theorem StrongEdge.high20_clique_card_le_eighteen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h20 : ∀ e ∈ Q, 20 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 18

theorem StrongEdge.high23_clique_card_le_fifteen
    {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
    [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (Q : Finset G.edgeSet)
    (hQ : (StrongEdge.conflictGraph G).IsClique (Q : Set G.edgeSet))
    (h23 : ∀ e ∈ Q, 23 ≤ (StrongEdge.conflictGraph G).degree e) : Q.card ≤ 15
```

完整机器输出，包括全部隐式参数和每个新增定理，见
[packing195-axioms.log](verification/packing195-axioms.log)。

### 当前 19.5 结论的全部数学前提

对 `G` 的通常有限性、可判定性和 `∀ x, G.degree x ≤4`，还须传入：

1. 所有完整冲突度 ≥21 的强团大小 ≤17；
2. 所有完整冲突度 ≥22 的强团大小 ≤16；
3. 对当前候选集 `F`，每个 `Q⊆F` 若在完整冲突图中成团，则 `Q.card≤19`。

结论是存在 `M⊆F`，`M` 在完整原图 `G` 中为诱导匹配，且
`2 * F.card ≤ 39 * M.card`。第三项只约束当前候选集，不要求原图其他位置无二十团。
此接口尚未定义或使用 `t_G(F)`；它不是带紧分量修正项的无条件最终定理。

## 证明路线

### high20：唯一三元类型的饱和计数

复用基线中已完成的支撑最大度三、四元类型、两个三元类型和纯一/二元类型分支。
唯一三元类型点 `x` 的根部边数已经有 ≤10 的 Lean 定理，故只需将外部边数由 ≤5 改为 ≤4。

所有多元类型的原邻接槽总数 ≤12，而 `x` 占至少三个槽，因此其余多元类型点至多四个。
若外部边至少五条，旧界迫使恰有四条避开 `x`、一条关联 `x`。四条避开 `x` 的边全在
上述至多四个二元点之间；度数求和迫每点恰有两条这类边，加上至少两条原根类型边，
使它们在原图中全部饱和。其原邻点只能在根邻域或这四点内。
第五条边的两端都在这两个集合之外，因此无法与前四条边强冲突，矛盾。

这一路线不需要把支撑最大度三的旧界从 18 加强到 17，也不需要纸面稿完整的类型分类。
最终得到 `4+10+4=18`。整个证明始终保留支撑外原邻点。

### high23：四边星根的外部边至多一条

基线已经证明三度支撑情形 ≤14，且四边星根的邻域相交边数 ≤14。
当四个根标签全部选中时，任意外部边两端类型都至多为二元，合起来必须覆盖四个根标签，
因此两端各有两个选中标签。基线的“二重根类型点关联所有外部边”引理分别作用于两端，
迫使所有外部边都有这两个端点。简单图中这样的边至多一条，故总数 ≤15。

## 实际验证记录

- 旧基线完整构建：exit 0，1,170 jobs。
- 旧基线公理审计：exit 0，225 项。
- 集成后完整构建：exit 0，1,175 jobs，无警告。
- 新公理审计：exit 0，22 个新增定理（包括三个回归定理）。
- 所有审计依赖均在 `propext`、`Classical.choice`、`Quot.sound` 范围内。
- 原四顶点路径测试：exit 0，验证候选集外连接边仍是冲突见证。
- 新测试：exit 0，验证空候选集，以及 `K20` 满足五档阈值却不满足纯 19.5 打包，
  从而核对独立的无二十团前提确实不可省略。

原有 45 个 Lean 文件中，仅公共入口 `StrongEdge.lean` 追加两个导入；其余 44 个原文件、
全部四个环境锁定/启动文件保持原始字节。新增六个 Lean 文件，共有 51 个 Lean 文件。
源文件散列、旧文件保存情况和审计解析见
[packing195-status.json](verification/packing195-status.json) 及
[packing195-source-sha256.json](verification/packing195-source-sha256.json)。

第一次基线执行因本机未安装 `lake` 失败；原重定向日志为空，工具报错的明确转录记录见
`verification/packing195-baseline-initial-error.txt`，原空日志和退出码也保留。
框架第一次编译只有一条 `unnecessarySimpa` 警告，修正后的最终构建无警告；旧日志未覆盖。

### 固定环境

- Lean `leanprover/lean4:v4.35.0-rc4`，实际编译器提交
  `c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`。
- mathlib `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`。
- 本次使用官方 Windows ZIP，SHA-256
  `fef75506e6af6c3669efc360224410865b3d292240aafc351a312435972667f3`。
  旧 README 中 `549c…` 对应同版本 `.tar.zst` 资产；已通过 GitHub 官方发布元数据核实。
  编译器版本和项目锁文件均未升级。

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Audit195.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
.\lean.ps1 env lean StrongEdge/Tests195.lean
```

本轮运行结果保存于 `verification/packing195-*.log`，对应 exit code 独立保存。
`verification/finalize-packing195.py` 检查这些记录和源码并生成源码快照；它本身不替代 Lean。

## 有限反例搜索与未完成范围

另运行了固定种子的 501 个有限图检查，对五档阈值分别求最大强团，未发现反例。
冲突图用端点定义与线图平方两种方法独立交叉核对。样本包括完整 `C5[2]` 和逐条删边，
以及 10、11、12、14、18、24 点的随机换边图。随机样本的高阈值团明显小于目标边界，
因此这项实验对临界情形的覆盖有限；不作为任何 Lean 证明的依赖。

下一步的准确数学目标见 [PACKING195_BLOCKERS.md](PACKING195_BLOCKERS.md)：
high21 ≤17、high22 ≤16、二十团刚性、真实 `C5[2]` 分量计数及最终组装均仍未完成。
