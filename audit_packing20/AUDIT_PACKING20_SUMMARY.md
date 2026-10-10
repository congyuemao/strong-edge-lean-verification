# PACKING20 独立审计总报告

日期：2026-10-10，Australia/Sydney。审计依据用户提供的 `CODEX_LEAN_PACKING20_INDEPENDENT_AUDIT_PROMPT (1).md`；被审材料为本地最终 high20 checkpoint，而非把原验收报告当作证明。

**验收结论：Lean 工程独立复现、一般数学语义对应、实际证明依赖和紧例核查通过。用户补充的 Joos–Nguyen 2016 联合期刊全文现已核查；其中没有当前“固定完整原图、任意候选集 F”的20倍版本。相对此文有明确范围差异，但全部文献中的首次性仍未确认。** 本轮文献更新未修改 Lean 源码。

## 1. 四类证据分别验收

| 证据类别 | 本轮实际完成 | 判定与边界 |
|---|---|---|
| 原文本报告声称 | 对比 ZIP、原工作项目、新副本、上一 high21 checkpoint 和旧日志 | “225项公理审计”成立；并非原文件已有225个 #check。35个旧数学／测试文件和4个配置未改，两个入口文件只追加；不能概括为所有旧文件都未改。历史更强数学／复杂度结论仍只是文本声称。 |
| 实际 Lean 检查 | 从新解压源码 build；原 Audit／Tests；新增225项完整类型和公理打印；检查5个阈值及最终定理；实际证明项闭包 | 1170 jobs完成，44个工程模块新编译，Audit另行检查。目标及225项公理输出只含标准三公理的子集，无 sorryAx。复用锁定依赖缓存，未做编译器自举或 mathlib 全量冷编译。 |
| 数学语义对应 | 独立四端点冲突定义与原冲突图在不同边上双向等价；诱导匹配与任意端点不重合、不在完整 G 中相邻双向等价；边界和紧例 | 两项普遍等价均由 Lean 证明；候选外原边继续充当冲突见证。有限回归补充而不替代普遍证明。 |
| 学术原创性 | 已核查2016联合期刊全文及其他可访问的原始论文、精确定理编号和蕴含范围 | 完整边集20倍、21色、私有邻域局部交换均有先例。2016全文没有任意候选集版本，其归约不能直接搬用；全局原创性仍未确认。 |

机器可核对的结论：[verification-results.json](verification-results.json)。源文件、锁定配置、原始命令、日期、退出码、哈希和失败记录均在本归档中。

## 2. 最终数学结论确实核验了什么

对任意有限简单图 G，若每个原顶点度数≤4，那么对任意原边有限集合 F，存在有限 M⊆F，使 M 为**完整 G 中**的诱导匹配，且 F.card≤20*M.card。没有 F 非空、正则、无三角形、无四圈、候选集闭合或未证阈值记录作为额外前提。

完整最终声明与公理输出在 [environment.stdout.log](logs/environment.stdout.log) 末尾。全225项完整打印在 [complete-final.stdout.log](logs/complete-final.stdout.log)。标准三公理是 `propext`、`Classical.choice`、`Quot.sound`。

实际供给链是 high20≤19、high21≤18、high22≤17、high23≤16、high24≤13；最后一项放宽为 `MinimalCliqueBounds20.high24` 所需的≤15。旧接口的 high24≤7 没有进入最终依赖闭包。8,302个可达声明（含506个工程声明）的实际证明闭包无 unsafe 或额外公理；五个阈值供给不反向引用 packing 包装器。

新紧例为10顶点双点五圈：20条边、每点度4、不同边两两冲突；任何诱导匹配至多一条。Lean 已证明自然数统一常数不能小于20；实数常数的小于20不可能性是同一有限构形的直接数学推论，未额外形式化实数版本。没有证明整数强边20色、任意权重20倍或19.5加强。

## 3. 新增检查和回归

| 文件 | 内容 |
|---|---|
| [AuditSemantic.lean](isolated/strong_edge_lean_starter/AuditSemantic.lean) | 独立端点定义；冲突与匹配的普遍双向等价；以新语义重述最终 packing；空候选集 |
| [AuditRegression.lean](isolated/strong_edge_lean_starter/AuditRegression.lean) | 四点路径候选外连接边；删中间边；空图、孤立点、非正规路径、三角形、四圈；双点五圈及常数必要性 |
| [AuditComplete.lean](isolated/strong_edge_lean_starter/AuditComplete.lean) | 原225项声明逐一完整类型与公理打印 |
| [AuditDependencies.lean](isolated/strong_edge_lean_starter/AuditDependencies.lean) | 从最终声明类型及证明项提取递归依赖 |
| [AuditEnvironment.lean](isolated/strong_edge_lean_starter/AuditEnvironment.lean) | 全部3648个传递导入模块登记、记录字段和终点／阈值完整输出 |

普通 `decide` 完成有限回归，没有 `native_decide`。原205个 checkpoint 文件在原项目和隔离副本中均保持原字节，修改仅发生于新增审计材料。

## 4. 障碍、修正与尚未完成事项

首次审计辅助运行遇到未完成构建导致缺 olean、错误打印选项 `pp.width`、Windows `-o` 根路径盘符大小写，以及 Python 控制台 GBK 输出失败。均已修正，成功和失败日志都保留。首次 build／audit 的子进程已成功；GBK错误发生在包装器重印输出阶段。之后整段复现脚本9项全部退出0，悉尼时间16:30:16–16:32:11，约115秒。

**已关闭的文献缺口：** 用户提供的 [Joos–Nguyen 2016 期刊](https://epubs.siam.org/doi/10.1137/140986980) 12页PDF已全部核查。Theorem 1.1 在第155–156页，给出 νₛ(G)≥(n−i−c₅)/9；第156页明确推出全边集20倍和无紧分量时18倍。第156–163页的归约不要求局部所选边属于指定 F，没有加权／任意候选集版本。路径实例明确说明删去候选外原边或将既有匹配与 F 相交的直接套用均失败。详见 [全文原创性范围复核](joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md)。

**剩余学术问题：** 当前候选集推广相对此文有区别；但排查一篇论文不能排除其他先例。可确认的新增范围是任意 F 量词，而非完整边集20倍、常数20最优或双点五圈紧例；后几项均已见于2016论文。它也不自动完全加强该文的顶点数主定理。具体阈值、其他方法文献及形式化的首次性仍须进一步核对。

**可选项未做：** 未额外桥接 mathlib 命名的平方／图幂接口。已经证明的独立端点等价给出了所需数学语义，不留单向等价缺口。

**不属于已验收结果：** 固定历史 commit 的3篇数学说明书中还声称完整20强团分类、更强阈值、19.5推论及算法复杂度；本次只将它们作为历史说明对照，未替代 Lean 证明。快照与出处在 [research/sources.json](research/sources.json)，任何文本中的“已证”“代理核验”措辞均不自动得到本审计认可。

没有修改公开仓库、push、投稿、联系作者或购买论文。原工程及既有 checkpoint 未改。

## 5. 报告索引、复现与归档

- [复现、版本、哈希、命令与失败记录](AUDIT_PACKING20_REPRODUCIBILITY.md)
- [一般语义等价与回归](AUDIT_PACKING20_SEMANTICS.md)
- [实际证明依赖链与公理边界](AUDIT_PACKING20_DEPENDENCIES.md)
- [文献定理、先例、无效推导与缺口](AUDIT_PACKING20_PRIOR_ART.md)
- [Joos–Nguyen 2016 全文原创性范围复核](joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md)

在工作区根目录运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\audit_packing20\isolated\strong_edge_lean_starter\reproduce-audit.ps1 -LeanBin .\.tools\lean-4.35.0-rc4-windows\bin
```

新机器需要相同 Lean 版本和锁定依赖；详细命令见复现报告。该入口已真实执行，所有原始输出可检查。

更新归档为 `strong_edge_lean_packing20_joos2016_reviewed_checkpoint.zip`，内部保持 `audit_packing20/isolated/strong_edge_lean_starter` 路径，收录完整源码、锁定配置、更新报告和全文审查证据，排除编译器、依赖缓存与 `.lake`。名称表示该文已经审阅，不承诺全局原创性。ZIP整体哈希和成员检查见归档旁的 `checkpoint-audit.json`。此前 `strong_edge_lean_packing20_independent_kernel_verified_checkpoint.zip` 保持原字节，记录的是尚未取得期刊正文时的历史状态。
