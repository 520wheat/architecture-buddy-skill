# 发布就绪清单（相对公开稳定版）

对照外部评价（约 7/10：适合内测，暂不称稳定公开发布）。本文件跟踪缺口关闭情况。

## 目标用户

不只个人自用：希望帮助需要「一起想清楚架构」的开发者。因此安装文档、触发描述、可重复测试必须对陌生人可读。

## 发布前必做（评价建议三项）

| # | 项 | 状态 |
|---|----|------|
| 1 | 全部 `description` 为触发条件 `Use when...`，不含流程摘要 | 见本轮修改 + `pressure-test.sh` |
| 2 | README 含 Cursor **与** Codex（及通用 skills 路径）安装说明 | 见根 README |
| 3 | 可执行压力测试：门禁文案 + 结构负例/正例；agent-runtime 必中主题 | `scripts/pressure-test.sh` |
| 4 | `agent-runtime` 专用复现校准 PASS | `corpus/runs/*-cal-agent-runtime.md` + COMPAT |
| 5 | 高影响互斥分叉必须触发圆桌预检；同意后可加载透镜并综合 | `architecture-buddy` 0.3.6 + `corpus/runs/2026-08-05-live-test-git-roundtable.md` |
| 6 | B6 具体证据与圆桌过程证据进入交付门禁；语义分与领域分独立 | `docs/design/architecture-quality-rubric.md` + `scripts/architecture-quality-report.sh` |

本轮补充校准已通过：主持人先提议圆桌、测试用户同意、加载 `log-stream` 与 `raft-cp` 两个透镜，并输出综合结论。

## 已吸收的思想升级（0.3.3）

- 范飞龙《别再让 AI 一直加功能》：加法陷阱 → 乘法式构架；停找分抽证；业务五问；N+1 + 反例进完成门禁与模板 B6。  
- 摘记：`docs/survey/architecture/D9-fan-multiplicative-architecture.md`。

## Phase 1B（0.3.6）

- B6 必须给出变化轴、N+1、反例、可组合能力和复杂度的具体证据。
- 圆桌触发后必须保存提议、用户选择、席位/透镜契约和主持人综合结论；正文仍保持架构设计，不变成会议记录。
- 语义质量、领域正确性、圆桌过程质量分开评分；报告工具不以关键词自动判定优秀。

## 仍属「稳定版之后」

- 对真实模型会话的 baseline pressure（多模型、多轮行为录制）——脚本只能锁住**规则写进 SKILL**与**结构门禁**，不能替代真人/模型回归。  
- 拆分「仅 skill 发布物」与「workshop 仓库」（可选）。  
- 更多领域金标与透镜。

## 成熟度声明（对外文案建议）

> Architecture Buddy 当前为 **public beta / 团队内测**：设计与金标训练基线已具备；请安装 `skill/` 目录，反馈交付物可读性与共思体验。尚未宣称语义版本稳定 API。
