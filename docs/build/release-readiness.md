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

## 仍属「稳定版之后」

- 对真实模型会话的 baseline pressure（多模型、多轮行为录制）——脚本只能锁住**规则写进 SKILL**与**结构门禁**，不能替代真人/模型回归。  
- 拆分「仅 skill 发布物」与「workshop 仓库」（可选）。  
- 更多领域金标与透镜。

## 成熟度声明（对外文案建议）

> Architecture Buddy 当前为 **public beta / 团队内测**：设计与金标训练基线已具备；请安装 `skill/` 目录，反馈交付物可读性与共思体验。尚未宣称语义版本稳定 API。
