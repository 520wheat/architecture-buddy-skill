# Architecture corpus

金标与校准运行记录。布局见规格 §6。

- `golden/<id>/` — META、GOLDEN、RUBRIC、SOURCES（Phase 1+）
- `runs/` — 校准运行记录（不冒充金标）

## 金标 id（≥6）

| id | 阶段 | 说明 |
|----|------|------|
| `kafka` | Phase 1 | 日志/流式集成 |
| `git` | Phase 1 | 内容寻址 + 分布式协作史 |
| `kubernetes` | Phase 1 | 声明式控制面 / 协调循环 |
| `hdfs` | Phase 2 | 大规模可靠存储 + 高带宽供给计算 |
| `spark` | Phase 2 | 通用数据并行 / DAG 惰性求值 |
| `agent-runtime` | Phase 2 | LLM 工具编排循环 + 权限/人审边界 |

各目录四文件齐全。Phase 1 复现校准见 `runs/2026-08-05-cal-*.md`；Phase 2 迁移校准见 `runs/2026-08-05-mig-sre-buddy.md`（PASS，非正式 GOLDEN）。

survey 摘记在 `docs/survey/architecture/`，升格后才成为 GOLDEN。
