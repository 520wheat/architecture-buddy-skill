# Architecture Quality Scorer Calibration

## Scope

本轮只校准 `scripts/architecture-quality-report.sh` 和压力测试，不修改 `SKILL.md`，不采纳 SkillOpt staging 候选。

## Implemented Changes

- A1–A8、B1–B6 支持 `##` 到 `######` 的 ATX 标题层级；正文中的 `A1`、表格文本和 `A10` 不会被当作章节。
- 章节正文按命名章节边界提取，空 B6 仍会触发 `b6-evidence-insufficient`。
- 报告保留结构、领域、圆桌和人工复核字段；语义结论固定为 `结论：_PENDING_`，不自动输出 `PASS` 或 `EXCELLENT`。
- 新增标题层级正例、空 B6 正例和圆桌综合结论正例。
- 保留并回归五类反例：模块清单、会议记录、空 B6、圆桌无综合结论、结论无证据。

## Calibration Results

| Candidate | Hard gate | Structure | Automatic signals |
|-----------|-----------|-----------|-------------------|
| Git formal design | PASS | 20/20 | none |
| Kafka golden | REJECT | 0/20 | missing B6 and all five B6 evidence markers |
| etcd golden | REJECT | 0/20 | missing B6 and all five B6 evidence markers |
| Agent Runtime golden | REJECT | 0/20 | missing B6 and all five B6 evidence markers |

所有报告的 `semantic_quality_score`、`domain_score`、`roundtable_score` 和 `human_review` 均保持人工待填写状态。自动门禁没有把旧报告中的人工高分继承进新报告。

## Regression Results

- 标题层级变体：通过；不再因为 `##` 与 `###` 混用产生结构误报。
- 空 B6：拒绝；报告包含 `b6-evidence-insufficient`。
- 模块清单：拒绝并标记 `module-list-only`。
- 会议记录：拒绝并标记 `meeting-record-only`。
- 圆桌无综合结论：保留结构信号并标记 `synthesis-missing`。
- 圆桌有综合结论：不再误报 `synthesis-missing`。
- 结论无证据：拒绝并标记 `evidence-and-cost-debt`。

## Verification

通过：

```text
bash scripts/pressure-test.sh
bash scripts/check-architecture-buddy.sh
bash -n scripts/architecture-quality-report.sh scripts/pressure-test.sh scripts/check-architecture-buddy.sh scripts/rubric-report.sh
git diff --check
```

本轮没有修改 `skill/architecture-buddy/SKILL.md`；安装目录仍应与源码保持一致。自动报告仍只是筛选和工作表，不是“优秀架构设计”的最终裁决。

## Residual Risks

- 评分器只承诺常见 ATX 标题，不覆盖所有 Markdown 方言。
- 旧 golden 文档缺 B6 是真实硬门禁缺口，不应通过放宽评分器解决；后续应补齐文档后再复评。
- 领域正确性、语义质量和圆桌过程仍需人工审阅，关键词命中不能替代这些判断。
