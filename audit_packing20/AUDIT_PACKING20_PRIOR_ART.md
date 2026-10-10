# PACKING20 文献先例审查

审查日期：2026-10-10（Australia/Sydney）。本文件是有范围限制的先例审查，不是原创性证明，也不是期刊论文证明的 Lean 形式化。第二轮已使用用户提供的 Joos–Nguyen 联合期刊PDF补齐正文审查。

## 结论与证据边界

已确认完整原边集的 20 倍保证存在既有先例；21 色定理、私有冲突邻域交换与双重计数也有明确先例。本轮检索没有确认一项已发表、适用于所有最大度至多四简单图的任意候选边集 20 倍定理，或足以直接覆盖它的分数强色数至多 20 定理。**不能据此宣称原创。**

上一轮“Joos–Nguyen 2016 期刊正文未取得”的缺口现已关闭：用户提供的12页联合终稿已全部核查。正文没有任意候选集／加权版本，其局部归约也不直接保证所选边属于指定 F。**相对此文，任意候选集推广有明确范围差异；全部文献中的首次性仍未确认。** 详见 [逐页原创性范围复核](joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md)。

## 1. Joos–Nguyen：联合期刊终稿已核查

Felix Joos, Viet Hang Nguyen, *Induced Matchings in Graphs of Degree at Most 4*, SIAM J. Discrete Math. 30(1), 154–165 (2016), DOI [10.1137/140986980](https://epubs.siam.org/doi/10.1137/140986980)。本轮依据用户提供的期刊PDF正文，身份与哈希见 [source.json](joos2016_review/source.json)。

**Theorem 1.1（印刷第155–156页）**：Δ(G)≤4 时，νₛ(G)≥(n(G)−i(G)−c₅(G))/9，其中 i 为孤立顶点数，c₅ 为 C₂,₅ 分量个数。第156页紧接着的**无编号推论**明确给出 m(G)/20，以及 c₅=0 时的 m(G)/18。因为 n−i≥m/2，且 c₅≤(n−i)/10，这些推导是正文内容，不再仅由摘要或预印本确认。

第155–156页还确认 C₂,₅ 的紧性及可从证明提取多项式算法。这些已有结果不可作为本项目首次提出的贡献。第156页 Conjecture 2 的无紧分量 m/17 是猜想，不能当作定理；第155页 Conjecture 1 也没有被本文证明。

原证明范围的关键证据：第156页 (2.2) 对**原图 G 的真顶点诱导子图**作归纳；第157页 k-reduction tuple 以删去顶点数及新增孤立点数计费，所选 M_X 只要求属于 G[X]。Claims 1–11 和 Subclaims 9.1/11.1 延续这一背景，没有引入指定候选 F 或权重函数。不能将它理解为对平方线图任意诱导子图的 Hall ratio 归纳。

不能直接把 G 换成只保留 F 的图：路径0–1–2–3中取 F={01,23}，删边12后诱导匹配数从原候选语义的1变为2。也不能简单把原匹配与 F 相交：同一原路径取 F={12}，论文允许的匹配 {01} 满足其保证，却与 F 无交集。

进一步，同一图的 X=N[1]、M_X={01} 是合法1-reduction tuple，但对 F={12} 候选损失为1、候选收益为0。因此不能原样搬用该局部归约来获得 F 的20倍计数。这里指出直接迁移的缺口，不声称一切可能的复杂推导均不可能。

**判定：这篇论文明确覆盖全边集20倍，未覆盖当前任意候选集版本。** 可以把当前结果称为其全边集20倍推论的候选集推广；不能笼统说完全加强了其更精细的顶点数主定理。上一轮读取的 [Joos 2014预印本](https://arxiv.org/html/1407.8336v1) 与 [Nguyen 2014预印本](https://arxiv.org/pdf/1407.7604) 仅保留为历史来源，以上编号均来自此次核查的2016年联合期刊终稿。

## 2. Huang–Santana–Yu：期刊 Theorem 2 是 21 色

Mingfang Huang, Michael Santana, Gexin Yu, *Strong Chromatic Index of Graphs With Maximum Degree Four*, EJC 25(3), P3.31 (2018), DOI [10.37236/7016](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v25i3p31)。已读取[期刊 PDF 正文](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v25i3p31/pdf)。**Theorem 2（印刷页 2）**：最大度四图的强色指数至多 21。证明在第 4 节完成，部分结构引理的证明在第 5 节；讨论的是完整图中的强边染色。

推导（本审计）：把 21 个色类与任意 F 相交，至少一个交集大小≥|F|/21，并仍为完整 G 中的诱导匹配。故该定理给出 Hall ratio≤21，不能直接给出≤20。小于四的度数可通过加入不交的度四分量再限制回原图覆盖。不能将证明中的“至多 20 个已用邻色”误读为最终总色数 20。

## 3. Steiner：Hall ratio 与分数色数必须区分

Raphael Steiner, *Fractional Chromatic Number Vs. Hall Ratio*, Combinatorica 45, article 37 (2025), DOI [10.1007/s00493-025-00164-0](https://link.springer.com/article/10.1007/s00493-025-00164-0)。已读取出版商全文的定义、Theorems 1.1、1.3、1.5 及相关证明说明。

第 1 节公式 (M) 将 χ_f 表为任意非负点权下总权重与最大独立集权重之比的上确界；限制为 0/1 权重得到 Hall ratio，因而 ρ≤χ_f≤χ。Theorem 1.5 给出对每个 δ>0、足够大的 n，存在 Hall ratio≤4+δ 而分数色数随 n 无界增长的图，并附有对子图度数权的独立集保证。该定理不限定为最大度四图的平方线图。

推导（本审计）：取 H=L(G)²。对全部 F⊆E(G) 的本项目命题恰好是 ρ(H)≤20；空 F 单独平凡处理。若已有 χ_f(H)≤20，则给每条 F 边权 1、其余权 0，即可推出本命题。反向推导对一般图不成立；本项目也未证明反向推导在这一特殊图类成立。

## 4. 私有邻域与局部交换已有方法先例

Maximilian Fürst, Marilena Leichter, Dieter Rautenbach, *Locally Searching for Large Induced Matchings*, Theoretical Computer Science 720, 64–72 (2018), DOI [10.1016/j.tcs.2018.02.006](https://www.sciencedirect.com/science/article/pii/S0304397518300835)。已读取[作者预印本 arXiv:1708.02028v1](https://arxiv.org/html/1708.02028v1) 的定义、Local Search、Lemma 1、Theorem 2、Corollary 3 及证明；以下编号属于该预印本。

该算法使用添加一条边、用两条边替换一条边的改进。其式 (2) 表明私有冲突边必须两两冲突；Theorem 2(ii) 的原文设置为最大度 d≥3、M 由 Local Search 产生，并假设每条边满足 c_G(xy)≥f、n_xy≥g，给出

`|M| ≥ m(G) / (3d² − d − f − ((d+6)/2)g)`，

其中 c_G 是含自身的冲突边数，n_xy=|N(x)∩N(y)|。证明使用私有冲突边计数和双重计数；Corollary 3 对 d-正则图给出近似算法，其证明取 f=(3d²−d)/2、g=0 并结合贪心预处理。

在该推论中代入 d=4 得 f=22，即其证明给出4-正则图完整边集 m/22，不能直接覆盖任意 F 的 20 倍结论。其无四圈等更强结果另有图类限制。**“私有团交换／双重计数”不可作为全新方法宣称。** 本次形式化的次级度数最小化及五档阈值如何与全部既有局部引理比较，仍需进一步学术审查。

## 5. 已核查的通用分数界不足以覆盖 20

Małgorzata Śleszyńska-Nowak, [*Clique number of the square of a line graph*, arXiv:1504.06585](https://arxiv.org/pdf/1504.06585)。正文 **Theorem 7** 对简单图给出分数强色指数≤1.75Δ²。其证明结合 Theorem 5 的团数界与分数版 Reed 界，还给出≤1.75Δ²−Δ+0.5；Δ=4 时分别是 28 和 24.5，均不推出 20。这里引用确已读取的预印本编号，不另行猜测期刊编号或 DOI。

另检索到二分图分数强色数与排除完全图 minor 的相关论文。它们有额外图类前提，不能直接用于本任务全部 Δ≤4 图。未将摘要检索结果升格为覆盖本结果的先例。

## 6. 检索范围、无效推导与剩余事项

使用了任务指定的 `Hall ratio squared line graphs maximum degree four`、`induced matching every subset of edges graph degree 4`、`hereditary induced matching bound`、`private neighbourhood local improvements strong clique degree thresholds`，并补充精确标题、DOI、`fractional strong chromatic index`、`Locally Searching for Large Induced Matchings` 等检索。搜索命中只是发现线索；以上数学判断仅采用出版商、作者预印本等原始来源。

以下推导均未获支持：完整边集 20 倍 ⇒ 固定原图中每个候选集 20 倍；21 色 ⇒20 倍；团数≤20 ⇒ Hall ratio≤20；Hall ratio≤20 ⇒分数强色数≤20；一次 Lean 验收 ⇒整数强边二十色猜想成立；没有搜索命中 ⇒原创。

Joos–Nguyen 2016 联合终稿的全文范围检查现已完成。仍需继续核对更广泛的局部分数染色、任意候选集／0–1权重及局部搜索改进文献，才能判断全局首次性。当前证据足以确认本项目相对此文的量词差异及若干方法先例，**不足以签署覆盖全部文献的原创性结论**。没有联系作者、购买论文、投稿或发布任何内容。
