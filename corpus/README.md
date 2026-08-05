# Architecture corpus

金标与校准运行记录。布局见规格 §6。

- `golden/<id>/` — META、GOLDEN、RUBRIC、SOURCES（Phase 1+）
- `runs/` — 校准运行记录（不冒充金标）

种子（Phase 1，已填充）：`kafka`、`git`、`kubernetes` — 各目录四文件齐全；对应校准见 `runs/2026-08-05-cal-*.md`。

survey 摘记在 `docs/survey/architecture/`，升格后才成为 GOLDEN。
