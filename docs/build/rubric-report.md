# RUBRIC 对照报告工具（维护者）

**受众：维护者与构建流程。不对用户暴露。**

半自动生成候选 deliverable 对照金标 RUBRIC 的勾选骨架。脚本只做结构门禁与清单导出，**不自动判定 PASS**；维护者勾选后结论写入 `corpus/runs/`。

校准边界见 ADR-0019；流程见 [`skill-calibration.md`](skill-calibration.md)。

## 用法

```bash
bash scripts/rubric-report.sh <golden_id> <candidate.md> [out.md]
```

| 参数 | 说明 |
|------|------|
| `golden_id` | `corpus/golden/<id>/` 目录名（如 `kafka`） |
| `candidate.md` | 候选交付正文（含 `### A1`…`### A8`、`### B1`…`### B6`） |
| `out.md` | 可选；省略则打印到 stdout |

```bash
bash scripts/rubric-report.sh --help
```

## 行为

1. 校验 `corpus/golden/<id>/{GOLDEN,RUBRIC}.md` 与候选文件存在
2. 结构门禁：候选必须含层 A（A1–A8）与层 B（B1–B6）标题，并通过 B6 最低证据检查；缺则 **FAIL**（非 0）
3. 从 RUBRIC 中标题含「必中」的章节提取 `- ` 列表项 → 报告 `- [ ] …`
4. 从「幻觉黑名单」章节提取列表项 → 报告 `- [ ] 未出现：…`
5. 报告头部声明：**本报告不自动判定 PASS；维护者勾选后写入 corpus/runs**

「叙事完整性」等非「必中」标题章节不进入勾选表（仍由维护者人工阅读）。语义质量请使用 `docs/design/architecture-quality-rubric.md` 与 `scripts/architecture-quality-report.sh`，本脚本不以关键词自动判定优秀。

## 冒烟

```bash
bash scripts/rubric-report.sh kafka corpus/runs/2026-08-05-cal-kafka.md /tmp/rubric-kafka.md
head -40 /tmp/rubric-kafka.md
```

期望：exit 0；报告含必中与黑名单勾选骨架。

## 与静态检查的关系

`scripts/check-architecture-buddy.sh` 可轻量校验本脚本存在且 `--help` 退出 0。金标四文件与 GOLDEN 结构仍由该检查脚本负责。
