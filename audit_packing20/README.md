# PACKING20 独立审计归档

从 [AUDIT_PACKING20_SUMMARY.md](AUDIT_PACKING20_SUMMARY.md) 开始阅读。技术核验通过；用户提供的2016年联合期刊正文已全部核查，其中没有当前任意候选集版本；全部文献中的首次性尚未确认。

- `isolated/strong_edge_lean_starter/`：从原high20 checkpoint独立解压的完整项目，既有文件未改；新增5个 `Audit*.lean` 和 `reproduce-audit.ps1`。
- `logs/`：本次实际运行的标准输出、标准错误和命令状态；失败记录也保留。
- 项目 `independent-rerun-logs/`：交付入口实际整段复跑的9项日志。Windows PowerShell重定向的输出可能为UTF-16；首轮日志为UTF-8。
- 根目录 JSON：哈希、依赖映射、静态扫描、逐项公理与命令核对。
- `research/`：指定历史commit的原说明书及出处，仅为历史对照，不作为可信证明。
- `inputs/`：用户指定审计任务的原始文件副本。
- `joos2016_review/`：用户补充论文的身份哈希、逐页证明范围复核和更新结论。

此ZIP未携带 `.lake`、依赖缓存、编译器或Git仓库。复现须安装指定Lean并按原manifest获取依赖；不要执行 `lake update`。详见 [复现报告](AUDIT_PACKING20_REPRODUCIBILITY.md)。Python脚本记录本机审计方法，部分依赖原工作区历史ZIP或工具路径；对外复现入口是项目内 `reproduce-audit.ps1`。

`ARCHIVE_CONTENTS.json` 登记除自身之外的归档成员哈希；整体ZIP的SHA-256在归档外 `checkpoint-audit.json`，避免自引用哈希。历史验收文档与新报告同时保留，若语气或范围有冲突，以新报告明示的证据层级为准。

当前更新包名为 `strong_edge_lean_packing20_joos2016_reviewed_checkpoint.zip`。首轮检查点ZIP保持不变，其中“正文未取得”是当时的历史状态；本轮更新没有重编译或修改数学定理。
