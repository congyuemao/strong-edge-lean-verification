# PACKING20 独立复现记录

审计日期：2026-10-10；时区 Australia/Sydney（UTC+11）。结果：从最终 checkpoint 的新解压副本重建工程，原审计、原测试、完整类型／公理审计、新语义证明及回归均通过。不是只复读旧验收日志。

## 1. 输入、隔离与版本

输入归档为工作区的 `strong_edge_lean_high20_checkpoint.zip`，SHA-256：

```text
7dd2a102dda783f1ade4ec53096928bc52dcc246a6432c9221c9fe3ac4a41818
```

原工作项目：`C:\Users\21161\Documents\ChatGPT\math\strong_edge_lean_starter`。

本轮独立项目：`C:\Users\21161\Documents\ChatGPT\math\audit_packing20\isolated\strong_edge_lean_starter`。先检查 ZIP 路径不越过目标目录，再解压。原工程和新副本的45个既有 Lean 文件及4个配置文件均保持字节不变；新增检查全部置于项目根目录的独立 `Audit*.lean` 文件。

依赖版本由归档配置固定：

- `lean-toolchain`：`leanprover/lean4:v4.35.0-rc4`。
- mathlib：`49fd9dee36e7bbf345fe7981d2de6aeeb591f75b`。
- 其余8个包：见完整 [lake-manifest.json](isolated/strong_edge_lean_starter/lake-manifest.json)。9个包的 Git HEAD 与锁定值逐一一致，受跟踪文件状态干净；复制前后记录见 [dependency-states.json](dependency-states.json)、[dependency-states-after.json](dependency-states-after.json)。未运行 `lake update`。

实际直接调用 `.tools\lean-4.35.0-rc4-windows\bin\lake.exe`，将同目录放在 PATH 首位；未依赖 `lean.ps1` 隐式选择版本。实际 `lean --version` 输出：

```text
Lean (version 4.35.0-rc4, x86_64-w64-windows-gnu, commit c29b6dda4f7c20e3eeaa717c4e565663c5cfa364, Release)
```

证据：[compiler-version.stdout.log](logs/compiler-version.stdout.log)、[compiler-version.json](logs/compiler-version.json)、[compiler-sha256.json](compiler-sha256.json)。最后一项只登记执行文件哈希，不表示已自举验证编译器。

## 2. SHA-256 与文件保留核验

初始49项完整哈希：[source-sha256-before.json](source-sha256-before.json)；结束时含5个新审计源文件及复现脚本的哈希：[source-sha256-after.json](source-sha256-after.json)。关键配置如下：

| 文件 | SHA-256 |
|---|---|
| lean-toolchain | `8f89aa44fccdb1a0b6cc768c7c9f54b94cd40e47a08d582f82d1235f13075cf7` |
| lake-manifest.json | `8514da62e26146984cfb3eff374af2f90f2404fbd7e2c4ff5965b9cf9bb0a9bf` |
| lakefile.toml | `4f9ceaec88afaeaf4c9aa398cb37eb93a14d8b19967740cc6a43016568007147` |
| lean.ps1 | `dde5022f61ef2df720b823d8eed89cd762a07876a36cad25c40448a375412186` |

不仅检查源码：输入 ZIP 的全部205个文件在原工作项目和隔离副本均逐字节一致，见 [checkpoint-member-preservation.json](checkpoint-member-preservation.json)。工作区7个历史 checkpoint 的哈希重新核对，见 [historical-checkpoint-verification.json](historical-checkpoint-verification.json)。这核验了所提供字节的一致性，不证明更早外部发布的真实性。

对上一 high21 checkpoint 逐成员比对：[high21-checkpoint-comparison.json](high21-checkpoint-comparison.json)。35个旧数学／测试 Lean 文件和4个配置文件未修改；`StrongEdge.lean` 与 `StrongEdge/Audit.lean` 只追加；README 改动；新增8个 high20 Lean 文件。故不能笼统说“所有旧文件未修改”，但旧数学／测试内容未改的限定说法成立。

指定历史 commit 的3份说明书由 GitHub 连接器取得；本地最初写入时多出的末尾换行已去除，当前字节重新计算的 Git blob SHA 与连接器提供值完全一致，见 [research/verification.json](research/verification.json)。这确认历史文本身份，不验收其中额外数学声称。

## 3. 实际运行和原始日志

每个日志前缀有三个文件：`.stdout.log`、`.stderr.log`、`.json`。JSON 保存实际完整命令数组、绝对工作目录、编译器路径、UTC起止时间、悉尼开始时间、耗时和**子进程**退出码。下表时间均为2026-10-10悉尼时间；详尽记录以 JSON 为准。

| 检查 | 开始时间 | 退出码 | 日志与结果 |
|---|---|---|---|
| `lake build` | 16:11:31 | 0 | [build.json](logs/build.json)、[stdout](logs/build.stdout.log)；327秒；1170 jobs；44个工程模块新编译；无 warning/error；stderr为空 |
| `lake env lean StrongEdge/Audit.lean` | 16:17:14 | 0 | [audit.json](logs/audit.json)、[stdout](logs/audit.stdout.log)；225项公理输出 |
| `lake env lean StrongEdge/Tests.lean` | 16:18:05 | 0 | [tests.json](logs/tests.json)、[stdout](logs/tests.stdout.log)；无诊断 |
| `lake build` 日志包装器修正后复核 | 16:19:48 | 0 | [build-confirm.json](logs/build-confirm.json)；缓存构建再次成功 |
| `AuditComplete.lean` | 16:19:48 | 0 | [complete-final.json](logs/complete-final.json)、[stdout](logs/complete-final.stdout.log)；同225声明逐一完整 #check 和 #print axioms |
| `AuditSemantic.lean`，并输出 olean | 16:19:26 | 0 | [semantic.json](logs/semantic.json)、[stdout](logs/semantic.stdout.log)；独立端点等价 |
| `AuditRegression.lean` | 16:20:16 | 0 | [regression-dev.json](logs/regression-dev.json)、[stdout](logs/regression-dev.stdout.log)；有限构形及紧例 |
| `AuditDependencies.lean` | 16:17:14 | 0 | [dependencies-dev.json](logs/dependencies-dev.json)、[stdout](logs/dependencies-dev.stdout.log)；真实证明闭包 |
| `AuditEnvironment.lean` | 16:21:15 | 0 | [environment.json](logs/environment.json)、[stdout](logs/environment.stdout.log)；导入清单、记录与5档供给完整类型 |

日志名带 `dev` 的两项是成功的最终文件运行，不能由文件名判断失败。原 `StrongEdge/Audit.lean` 的文本包含101个 `#check` 和225个不同声明的 `#print axioms`；**“225项审计”不是225次完整类型打印**。新增 `AuditComplete.lean` 对相同225项全部补做完整类型与公理打印。两份公理清单完全一致，逐项只有标准三公理的子集，见 [axiom-verification.json](axiom-verification.json)。

所有以上成功执行的原始日志均无警告／错误；旧报告过去那一次的“无警告”仍由旧日志描述，本轮独立确认的是本轮执行。记录和日志结果汇总见 [command-verification.json](command-verification.json)、[verification-results.json](verification-results.json)。

## 4. 最终类型、公理和五档供给

新编译声明的输出（从 [environment.stdout.log](logs/environment.stdout.log) 末尾原样摘录）：

```lean
StrongEdge.induced_matching_packing20.{u_1} {V : Type u_1} [Fintype V] [DecidableEq V] (G : SimpleGraph V)
  [DecidableRel G.Adj] [DecidableRel (StrongEdge.conflictGraph G).Adj] (hΔ : ∀ (x : V), G.degree x ≤ 4)
  (F : Finset ↑G.edgeSet) : ∃ M ⊆ F, StrongEdge.IsInducedMatching G ↑M ∧ F.card ≤ 20 * M.card
```

```text
'StrongEdge.induced_matching_packing20' depends on axioms: [propext, Classical.choice, Quot.sound]
```

没有 `high20`、`MinimalCliqueBounds20`、任何额外记录、非空性或其他图类假设作为隐藏参数。所有 typeclass 也在完整输出中显式出现。五档供给的完整类型和公理就在同一日志末尾：`high20_clique_card_le_nineteen`、`high21_clique_card_le_eighteen`、`high22_clique_card_le_seventeen`、`high23_clique_card_le_sixteen`、`high24_clique_card_le_thirteen`，各自仅依赖上述三项。实际记录使用的 high24≤15 放宽定理也在225项完整日志中。

## 5. 可信缓存范围与实际遇到的失败

隔离项目的 `.lake/build` 未从原项目复制；45个原源文件中44个模块由 build 新编译，审计文件另行重新 elaboration。复用的是锁定的 `.lake/packages` 源码和已有依赖 olean 缓存，约3.09 GB。新副本通过实际文件复制获得这些依赖，项目源码不是共享链接。不能把1170 jobs理解成1170个模块全部从零重编译。未验证缓存二进制可从干净机器逐一复现，未验证编译器自举；通常的 Lean 内核／工具链及锁定依赖缓存是本轮可信基础。

真实失败均保留或明确记录：

1. 创建依赖目录 junction 被本机文件系统拒绝；改为复制缓存，不改变证明或锁定文件。
2. 首次新语义检查在工程 build 完成前启动，缺 `StrongEdge.olean`，见 [semantic-dev.stdout.log](logs/semantic-dev.stdout.log)。等待构建后解决。
3. 首版完整审计使用不存在的 `pp.width`，见 [complete.stdout.log](logs/complete.stdout.log)；改为 `format.width` 后完整检查成功。未忽略失败退出码。
4. Windows 上 Lean `-o` 的根路径与盘符大小写检查导致 `semantic-dev2/3/5` 失败；显式使用小写盘符的绝对 `-R` 和输入路径后成功。复现脚本已包含该处理。
5. 最初 Python 日志包装器在子进程成功、日志和 JSON 已写入后，向 GBK 控制台重印 Unicode 时失败。build 和 audit 的 Lean **子进程均为0**，不能与包装器状态混淆。之后修正为 UTF-8，并再次执行 build 和完整复现入口；全部成功。

这些是构建时序、输出选项与Windows工具包装问题，没有发现原225项证明的数学／类型错误。保留失败日志是为了完整追溯，不将它们藏在成功汇总后。

## 6. 可重复执行的入口

本工作区 PowerShell 命令（从工作区根目录执行）：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\audit_packing20\isolated\strong_edge_lean_starter\reproduce-audit.ps1 -LeanBin .\.tools\lean-4.35.0-rc4-windows\bin
```

`ExecutionPolicy Bypass` 仅适用于这一脚本进程，不修改系统执行策略。脚本 [reproduce-audit.ps1](isolated/strong_edge_lean_starter/reproduce-audit.ps1) 按顺序执行版本、build、原 Audit、原 Tests、完整类型审计、语义编译、回归、环境和依赖闭包，共9项，每项保存标准输出、标准错误与 JSON，失败立即退出。新日志写到项目的 `independent-rerun-logs`。

该入口已实际整段执行；包装命令及结果见 [rerun-entrypoint.json](logs/rerun-entrypoint.json)、[rerun-entrypoint.stdout.log](logs/rerun-entrypoint.stdout.log)，逐命令日志位于 [independent-rerun-logs](isolated/strong_edge_lean_starter/independent-rerun-logs)。首次逐项核查与整段复跑的时间、路径分别记录，不混用。

在新机器上解压归档，先安装指定 Lean 版本，并在项目目录使用同一锁定 manifest 获取依赖。可运行下列命令获取 mathlib 缓存（网络与平台可用性由复现者环境决定；本轮不宣称已完成断网／冷缓存复现）：

```powershell
lake exe cache get
```

随后执行 `reproduce-audit.ps1`，给 `-LeanBin` 指定本机相同版本的 bin 目录。不要运行 `lake update`。历史准备／分析 Python 脚本保留用于追溯，本地绝对路径仅属原审计出处；独立复现以项目内 PowerShell 入口为准。

## 7. 交付归档范围

首轮 ZIP `strong_edge_lean_packing20_independent_kernel_verified_checkpoint.zip` 仅在上述技术核验通过后生成，保持原字节。用户提供2016年联合期刊PDF后，另生成 `strong_edge_lean_packing20_joos2016_reviewed_checkpoint.zip`，包含完整项目源码、锁定配置、旧材料、新审计文件、更新报告、原始成功／失败日志和全文范围复核。新包未修改数学源文件或重新宣称一次 Lean 编译；只是更新文献证据。排除 `.lake`、编译器二进制、Git目录、依赖缓存、Python缓存；不收录论文全文。新归档成员哈希、CRC及源码一致性由当前 `checkpoint-audit.json` 登记，首轮归档外记录保留在 `joos2016_review/previous-checkpoint-audit.json`。

首轮“kernel_verified”限定为本报告披露的技术验证。2016终稿的全文范围核查现已完成，但全部文献中的原创性仍未确认，见 [文献报告](AUDIT_PACKING20_PRIOR_ART.md) 和 [逐页复核](joos2016_review/JOOS2016_ORIGINALITY_REVIEW.md)。
