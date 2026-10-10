# 无条件修正 19.5 打包界：Lean 完成记录

对任意有限简单图 G，若原图每个顶点度数至多四，则对任意候选边集 F，存在原图中的诱导匹配 M⊆F，使

\[
2|F|\le 39|M|+t_G(F).
\]

这里 t_G(F) 是原图中同构于 C5[2]、且全部二十条边均属于 F 的连通分量数。C5[2] 将五圈的每个顶点替换为一个独立的二元组，相邻组间加入全部四条边。若 t_G(F)=0，就得到纯 19.5 界。所有冲突都在完整原图中计算，候选集外的边仍可作为冲突见证。

## 最终接口

```lean
theorem StrongEdge.induced_matching_packing195_with_connected_component_count
    {V : Type*} [Fintype V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj]
    [DecidableRel (StrongEdge.conflictGraph G).Adj]
    (hΔ : ∀ x, G.degree x ≤ 4) (F : Finset G.edgeSet) :
    ∃ M : Finset G.edgeSet, M ⊆ F ∧
      StrongEdge.IsInducedMatching G (M : Set G.edgeSet) ∧
      2 * F.card ≤ 39 * M.card + (StrongEdge.tightComponentsIn G F).card
```

最终签名没有 high20–high24 的额外假设，也没有二十团排除假设。

- [主打包证明](StrongEdge/Packing195Unconditional.lean)：`induced_matching_packing195_unconditional`。
- [实际连通分量版本](StrongEdge/TightComponents.lean)：`induced_matching_packing195_with_connected_component_count`。
- `induced_matching_packing195_of_no_full_tight_component` 给出修正项为零时的纯 19.5 推论。

## 证明链

1. 五个较强阈值界全部由原图最大度四推出：high20≤18、high21≤17、high22≤16、high23≤15、high24≤13。最后的 high22 次三次边界通过缺额度量、加权双重计数和十三点支撑分析排除，见 `SubcubicDefect`、`High22SupportSize`、`LowSupportGeometry`、`High22Improved`。
2. 二十团必有选中度四的根；所有这样的根的原图邻域均独立。三邻接型和全部至多二邻接型排除后，必须存在第二个连接全部四个根邻点的顶点。
3. 等号迫使四个完全选中的二邻接点、四条外层边，以及十个四度支撑顶点。`TwentyCliqueComponent` 证明全部原图关联边均在团内，且无团外边与其冲突。
4. `TwentyCliqueParts` 和 `TwentyCliqueRigidity` 把支撑拆成五个不交二元组，并验证每组顶点在完整 G 中的精确邻点集合。这是 C5[2] 的直接结构定义，不是额外假设。`five_cycle_blowup_is_connected_component` 进一步证明它就是 G 的一个完整连通分量。
5. 逐个移除候选集内的完整二十团，每团加入一条匹配边。因为这些团在完整冲突图中封闭，合并后仍是原图诱导匹配。每移除二十条候选边，计数两边分别增加四十和三十九，差的一单位由分量修正项承担。剩余候选集应用已验证的无二十团 19.5 定理。
6. 团支撑映射保持不同分量可区分，`tightComponentCount_eq_connected_component_count` 将支撑计数严格等同于实际 `G.ConnectedComponent` 的计数。

## 验证

2026-10-10（Australia/Sydney），Lean v4.35.0-rc4，mathlib 提交 `49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`。

- 全量构建：1,197 jobs，无警告。
- 公理审计：225 + 22 + 31 + 34 + 64 = 376 项，依赖仅为 `propext`、`Classical.choice`、`Quot.sound`。
- 75 个 Lean 文件及四个环境配置文件，共 79 项 SHA-256。
- 上一阶段的 57 个 Lean 文件和四个环境配置原样保留；公共入口只追加导入。
- 四顶点路径回归保留集外冲突见证；旧 19.5 回归通过。
- 新增十顶点 C5[2] 回归通过：每点度四、二十条边、五对结构、实际连通分量、全边强团，以及省略修正项时纯 19.5 确实失败。有限例子的计算使用内核检查的 `decide`，不使用 `native_decide`。
- 未发现数学证明错误；主源码无 `sorry`、`admit`、自设领域公理或不可信计算依赖。

证据：[构建日志](verification/packing195-unconditional-build.log)、[最终签名与公理](verification/packing195-unconditional-Audit195Unconditional.log)、[审计汇总](verification/packing195-unconditional-audit-checks.json)、[状态](verification/packing195-unconditional-status.json)、[源码 SHA-256](verification/packing195-unconditional-source-sha256.json)、[源码与证据快照](../strong_edge_lean_packing195_unconditional_checkpoint.zip)。

## 复验

在本目录运行：

```powershell
.\lean.ps1 build
.\lean.ps1 env lean StrongEdge/Audit.lean
.\lean.ps1 env lean StrongEdge/Audit195.lean
.\lean.ps1 env lean StrongEdge/Audit195Continuation.lean
.\lean.ps1 env lean StrongEdge/Audit195Thresholds.lean
.\lean.ps1 env lean StrongEdge/Audit195Unconditional.lean
.\lean.ps1 env lean StrongEdge/Tests.lean
.\lean.ps1 env lean StrongEdge/Tests195.lean
.\lean.ps1 env lean StrongEdge/Tests195Unconditional.lean
```

`verification/finalize-packing195-unconditional.py` 校验保存的退出码、日志、公理清单和源码溯源，再生成源码包；它不代替 Lean 编译。仓库级 `scripts/verify_archive.py` 校验全部归档。

以上完成的是带紧分量修正项的无条件 19.5 诱导匹配打包形式化，不涉及整数强边二十色猜想或 19.5 的最优性主张。历史阶段文档中的“待完成”保留为当时记录，当前状态以本文件为准。
