# Codex 继续任务：Lean 验证强边二十倍打包界的结构性前提

> **用途**：把本文直接交给本地 Codex，在现有 Lean 工作区中继续编写、编译和审核证明。本文是一份**执行提示词**，不是已经完成的数学证明。
>
> **阶段**：C4 → C5 → C6。优先完成可独立核验的 C4，随后尽可能推进 C5；只有全部结构性前提被真正证明之后，才能宣布 C6 无条件完成。
>
> **日期**：2026-10-09。**状态依据**：用户提供的当前 README 与本地运行报告。其报告称 `lake build` 已通过（1,124 jobs）、13 个导出定理已通过公理审计；本交接人未独立读取本地日志或重复执行这些测试。以你实际工作区的文件及运行结果为准。

## 你现在扮演的角色

你是一名同时熟悉 Lean 4、mathlib、有限图论和组合计数的形式化研究工程师。请**直接继续修改当前工作区的 Lean 项目**，以真实的、可通过 Lean 内核的证明为唯一验收标准。不要仅返回一份研究计划，不要把未完成的数学任务改写成隐藏假设，也不要把现有已验证代码从头重写。

## 一、项目已知状态与明确边界

用户给出的当前状态：

- `Basic.lean`：完整原图强冲突、私有团交换基础。
- `Conflict.lean`：诱导匹配与独立集等价；候选冲突度不超过完整冲突度。
- `PrivateExchange.lean`：选取最大独立集并最小化度数和；度数单调性。
- `DoubleCount.lean`：闭邻域双重计数，已证明
  
  \[
  2|W|\leq\sum_{v\in M}\bigl(d_H(v)+1+|P_v|\bigr).
  \]

- `Packing.lean`：已经验证一个**带有显式结构性前提**的条件定理：

  ```lean
  StrongEdge.induced_matching_packing20_of_thresholds
  -- 核心参数语义：
  (ht : CliqueThresholds20 (conflictGraph G))
  (F : Finset G.edgeSet) :
    ∃ M ⊆ F, IsInducedMatching G (M : Set G.edgeSet) ∧
      F.card ≤ 20 * M.card
  ```

- `Tests.lean`：四顶点路径 `0–1–2–3` 的完整原图冲突回归测试已通过。
- `StrongEdge/Audit.lean`：此前审计输出仅含 `propext`、`Classical.choice`、`Quot.sound`，见 `verification/axioms.log`。本次每新增顶层定理都应追加审计。

**仍未证明**：最大度四的原图普遍满足 `CliqueThresholds20 (conflictGraph G)`。所以目前没有无条件二十倍打包定理，也没有整数二十色定理。此前的 `LEAN_20_PACKING_HANDOFF.md` 中“起步文件尚未编译”的描述已经过时；请以实际当前 README、源码和日志为准。

**环境锁定**：

- Lean：`leanprover/lean4:v4.35.0-rc4`
- Lean compiler commit：`c29b6dda4f7c20e3eeaa717c4e565663c5cfa364`
- mathlib：`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`
- 保留 `lake-manifest.json`。不要为了修复证明而执行 `lake update`、升级版本或更换数学定义。
- Windows 优先使用仓库现有 `lean.ps1`；如有本地编译器，它可能位于 `../.tools/lean-4.35.0-rc4-windows`。不要将编译器、依赖缓存或二进制文件提交进源码包。

## 二、最终数学目标

对于任意有限无向简单图 `G`，若每个原顶点度数至多四，则对任意原边子集 `F`，存在 `M ⊆ F`，使其按**完整原图**是诱导匹配，并且

\[
\boxed{|F|\leq20|M|.}
\]

在 Lean 中最终应导出一个名称清楚的无条件定理，例如 `StrongEdge.induced_matching_packing20` 或仓库现有命名风格的 `packing20`；仅允许有关有限性、可判定性及 `∀v, G.degree v ≤ 4` 的前提。最终定理**不得仍要求** `CliqueThresholds20`、高冲突强团界、特殊围长、正则性、连通性或预先给出的图着色。

**核心语义禁止改变**：`F` 是原边集合的子集，但判断候选边是否冲突时，作为连接见证的原边可以处在 `E(G) \ F`。绝对不能改成对删边图 `G[F]` 求诱导匹配。

## 三、启动动作：先审计现状，再写代码

在当前本地项目目录执行以下操作：

1. 阅读 `README.md`、`StrongEdge/Packing.lean`、`StrongEdge/Conflict.lean`、`StrongEdge/DoubleCount.lean`、`StrongEdge/Audit.lean`、`verification/build.log`、`verification/axioms.log` 和 `LEAN_20_PACKING_HANDOFF.md`。名称可能随实际目录有所调整，应先查找，**不要假定旧起步目录就是最新代码**。
2. 查看 `git status --short` 与 `git diff`，保留用户已有未提交改动，不能覆盖或丢弃。
3. 通过 `#check`、`#print` 或直接阅读源码确定 `CliqueThresholds20` 的**准确 Lean 定义及其字段**。尤其查清其阈值针对的是完整冲突图的度数、还是候选诱导子图的度数；不要凭这份交接文档猜测字段名称。
4. 复跑当前工程的 baseline build 和审计，确认工作区确实可用。Windows 命令：

   ```powershell
   .\lean.ps1 build
   .\lean.ps1 env lean StrongEdge/Audit.lean
   ```

   在已有 elan/Lake 的其他系统上可使用：

   ```sh
   lake build
   lake env lean StrongEdge/Audit.lean
   ```

5. 若 baseline 失败，先诊断版本、路径或已有工程错误；记录当前失败与旧报告之间的差别，不能凭旧日志宣称本次构建成功。

## 四、第一优先级：完成 `conflict_degree_le_24`

证明：若 `∀v, G.degree v ≤ 4`，则对完整原图中的每条边 `e`，有

\[
\boxed{\deg_{\operatorname{conflictGraph}(G)}(e)\leq24.}
\]

**建议的纸面计数路线**：固定原边 `e={u,v}`。与它冲突的其他原边可以由两类覆盖：

- 与 `e` 共端点的边，至多 `3+3=6` 条。
- 不共端点但有原图连接见证的边。`u,v` 合计至多六个其他邻点，每一个这样的邻点至多再发出三条与 `e` 不共端点的边，总计至多 `6×3=18` 条。

故冲突邻边总数至多 `6+18=24`。存在重叠时只会使实际数量更小。

**Lean 实现要求**：

- 优先将此命题放在独立模块，例如 `StrongEdge/Bounds/ConflictDegree.lean`；如果现有工程有既定命名规范，以原工程为准。
- 尽量重用已经验证的原边端点谓词和 `conflictGraph` 定义，不要另建一个“看起来等价”的冲突图。
- 可以先证明有限集合覆盖关系、各类边的数量上界，再使用 `Finset.card_union_le` 或相应 mathlib 引理。
- 原图是无向简单图，边以无序端点表示；必须处理 `u≠v`、端点交换、重复计数、邻点重合以及四圈等情况。不要假设原图无三角形或四圈。
- 如因 mathlib `Sym2`、`Subtype`、`Fintype` 接口困难，需要添加小型桥接引理。这些引理本身也必须有证明。
- 完成后运行全量 `lake build` 及 `Audit.lean`，确认新增定理只使用 Lean 标准逻辑基础。

**阶段 C4 的独立验收**：一个从 `Δ(G)≤4` 直接推出冲突度 `≤24` 的、量化所有有限简单图及全部原边的 Lean 顶层定理；它不依赖新的结构性假设。

## 五、第二优先级：逐项消去 `CliqueThresholds20`

仓库主证明通过私有闭邻域得到：对每个被选边 `m`，私有集 `P_m` 构成强团，且其中每条边的完整原冲突度至少为候选冲突度 `d_F(m)`。双重计数只需要

\[
\boxed{d_F(m)+1+|P_m|\leq40.}
\]

**只为最终二十倍目标服务的最低要求**：

| 候选冲突度 `d_F(m)` | 需要的 `|P_m|` 上界 | 可用的结构结论 |
|---|---:|---|
| `0…19` | `d_F(m)+1` | 闭邻域包含关系，已属通用证明 |
| `20` | `19` | 不存在 20 点、且全体完整冲突度至少 20 的强团 |
| `21` | `18` | 完整冲突度均 ≥21 的强团至多 18 点 |
| `22` | `17` | 完整冲突度均 ≥22 的强团至多 17 点 |
| `23` | `16` | 完整冲突度均 ≥23 的强团至多 16 点 |
| `24` | `15` | 完整冲突度均 ≥24 的强团至多 15 点即可 |

**重要优化**：原证明对最后一档使用了更强的“完整冲突度 24 的强团至多 7 条边”。为了证明二十倍打包，`≤15` 已足够。也可以使用原稿的增强结论“完整冲突度均 ≥23 的强团至多 15 条边”同时处理 `d=23,24`。不要因追求最强版本而延迟最小必要目标。

请先检查目前的 `CliqueThresholds20` 具体字段：

- 若已要求较强的 `≤7` 等条件，可以选择证明原接口；或在**保留原条件定理与已有通过证明不变**的前提下，新增一个仅要求上表弱界的 `MinimalCliqueThresholds20` 或同等局部接口，再证明它足以导出二十倍结论。
- 不得悄悄削弱原字段的定义却仍使用原名称和旧验证结论。
- 先从最容易形式化的一项结构引理入手，完整通过 Lean 后再推进下一项。证明 C5 的一个节点已经是有效进度；不要求在一次工作中完成所有结构分类。

### 具体原始证明文件与建议次序

研究仓库固定版本：
`https://github.com/congyuemao/strong-edge-colouring-research/tree/3a95c4a9c44475196c42b6eab4749c487d15d59b`

建议按逻辑依赖阅读：

1. `research/packing_private_cliques.md`：最终归约，尤其第 1—3 节。
2. `research/strong_clique_subcubic.md`：当强团内部原顶点关联度 ≤3 时，团至多 17 条边。可优先尝试这个相对独立的计数引理。
3. `research/clique20_rigidity.md`：20 条两两冲突边的取等分类。若完整分类形式化过重，优先尝试其**恰好足够的推论**：不存在一个大小 20、其中每条边完整冲突度都 ≥20 的强团。
4. `research/high_conflict_thresholds.md`：`≥21 ⇒ ≤18`、`≥22 ⇒ ≤17`。
5. `research/high_conflict_subcubic.md`：`≥23 ⇒ ≤16`。
6. `research/critical_support.md`：完整冲突度 24 的强团 `≤7`。
7. 可选替代：`research/high_conflict_23_improved.md` 的 `≥23 ⇒ ≤15`；亦可查阅 `research/high_conflict_20_21_improved.md`、`research/high_conflict_22_improved.md`，但第一轮无需证明 19.5 加强版。

### 图论结构证明的约束

- **完整原图与强团支撑严格分离**：为对强团中的边分类，可以只记录被强团使用的端点；但在证明完整冲突度、三角形损失、四圈损失时，仍须计算原图中可能存在的所有外部边。
- 区分“强团的诱导冲突度”和“其每条原边在整个 `conflictGraph G` 中的度数”。不能用小子图中的度数代替完整冲突度。
- 如果某个纸面分支在 Lean 中无法完成，先判断是 API 问题、缺少组合引理，还是原有数学推理存在漏洞。发现数学错误要提供准确反例或明确的失败步骤，不得加入新公理掩盖。
- 可以用 Python/JSON 为局部有限分类发现模式，但程序输出不能直接当作普遍 Lean 证明。若要调用有限穷举，必须**先形式化证明归约的完备性与可靠性**，并由 Lean 内核核验最终有限检查。不得拿既有搜索结果、外部 SAT 求解结果或 `native_decide` 直接冒充数学证明。

## 六、如果 C5 规模过大：采用可检验的中间目标

在不牺牲已有成果的前提下，允许采用以下分层交付：

1. 完成 C4 冲突度 ≤24 的普遍定理。
2. 形式化强团内部原顶点最大关联度 ≤3 时 `|Q|≤17` 的结构结果。
3. 建立一个统一的“固定强团、完整原冲突度下界、团大小上界”API，并证明候选私有集可调用该接口。
4. 对 `d=20` 先尝试只排除“20 点强团且全部成员完整冲突度 ≥20”的情形，无须立即完成整个五圈双点吹胀的同构分类。
5. 每完成一条，更新一个**仍保留其余显式假设**的中间推论，让 `Audit.lean` 审核它。

优先保证一个真正通过内核检查的中间定理。不要把由于时间或工具限制尚未完成的部分描述为已验证。

## 七、验收与安全规则

**严禁**：`sorry`、`admit`、自定义 `axiom`、隐含的 `constant` 数学断言、绕过内核的 `unsafe` 证明替代、`native_decide`、在结果文件中使用尚未证明的定理名、把强团界当作不加说明的 `variable` / `instance`、删去冲突见证以弱化目标。

`propext`、`Classical.choice`、`Quot.sound` 是此前报告中使用的 Lean 标准逻辑基础，不能把它们误报成新增数学公理。请审计实际新增证明依赖；若出现其他公理，逐一解释并确认其正当性，否则不要宣称审计通过。

对于任何有限计算证书，核验它证明的精确范围。旧研究中的 1,362 份诱导匹配证书只能验证样本，无法认证“任意有限图”的普遍结论。

**不得修改**现有已经通过的核心结论的数学含义，不得为了编译通过而增添更强数学假设，不得改变 `lean-toolchain` 或 `lake-manifest.json` 的依赖版本。确有必要的重构须保持旧导出定理并运行回归测试。

## 八、工作结束前必须执行的检查与报告

1. `lake build` 或 `.\lean.ps1 build` 完成，并将本次输出存入 `verification/` 下新的有辨识度的日志，保留旧日志作为历史记录。
2. `lake env lean StrongEdge/Audit.lean` 或 PowerShell 对应命令通过；`Audit.lean` 中包含所有本次新增顶层定理的 `#print axioms`。
3. 对项目自有 Lean 文件执行占位符及风险关键词扫描；扫描只作为辅助，必须结合公理审计。
4. 更新 `verification/source-sha256.json` 或新增带版本标识的源文件校验清单；不要伪造 SHA 值。
5. 保存 `git status --short`、相关 `git diff --stat` 的结果，列明改动的 Lean 文件与新增声明。
6. 在 `verification/NEXT_STAGE_REPORT.md` 中记录：**已内核验证 / 显式条件性 / 未完成 / 已发现反例**四类状态，并把每项声明与编译日志对应起来。

### 最终回复格式

完成实际代码修改和检查以后，输出：

- **本轮真实新增的 Lean 定理**：准确名称、文件、最关键的数学假设。
- **通过的检查**：运行的确切命令、结果、日志路径、`#print axioms` 输出摘要。
- **尚未消去的假设**：逐字段列明 `CliqueThresholds20` 或新最小接口中的残余内容。
- **下一步最短路径**：一到两个具体待证明引理及依赖关系。
- **数学风险**：如存在不能形式化的纸面推理，明确指出并给出证据。

**不要只输出“下一步建议”而没有执行任何可行的代码工作。不要声称已经证明无条件 20-packing，除非最终导出 theorem 在未要求 `CliqueThresholds20` 等数学前提的情况下通过 Lean 内核和公理审计。**

---

## 附：无条件完成的唯一验收标志

在实际源代码里看到一个已构建成功的定理，其数学意义确为

\[
\forall G\; [\Delta(G)\leq4]\;\forall F\subseteq E(G),\quad
\exists M\subseteq F:\;M\text{ 在完整 }G\text{ 中为诱导匹配}\land|F|\leq20|M|,
\]

并且全部调用的结构定理均已证明，审计中没有自定义数学公理。这个完成标志也**不**等同于整数强边二十色、原创性确认或论文同行评审。
