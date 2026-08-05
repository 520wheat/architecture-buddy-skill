# architecture-buddy（主持 Skill）

安装：将本目录链到 `~/.cursor/skills/architecture-buddy`，Reload Window 后 `@architecture-buddy`。

透镜：同级的 `../architecture-buddy-lens-*` 一并安装；圆桌时按需选用。

## 模式

- **`draft`**：一起拆假设、想清楚卡点；可半成品，不做完成检查。  
- **`deliverable`**：用户要完整架构设计时默认进入；走 S0–S7，过完成门禁后才可宣称完成。

## 成品

权威成品是双层模板 `templates/architecture-deliverable.md`（叙事层 A + 机制/策略层 B）。  
旧 `architecture-note.md` 已降级为内部映射。

行为与边界见仓库 `docs/adr/0018-collaboration-ux-and-real-first-principles.md`、`docs/adr/0019-deliverable-workflow-and-calibration-boundary.md`。
