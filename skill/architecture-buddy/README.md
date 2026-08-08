# architecture-buddy（主持 Skill）

安装：将本目录链到 `~/.cursor/skills/architecture-buddy`，Reload Window 后 `@architecture-buddy`。

透镜：同级的 `../architecture-buddy-lens-*` 一并安装；圆桌时按需选用。

## 模式

- **`draft`**：一起拆假设、想清楚卡点；可半成品，不做完成检查。  
- **`deliverable`**：用户要完整架构设计时默认进入；走 S0–S7，过完成门禁后才可宣称完成。

## 成品

正式架构设计文件是必需成品；可以采用自然的架构设计或 ADR 结构。`templates/architecture-deliverable.md` 的 A/B 内容用于质量映射和训练检查，不是用户可见文档唯一格式。
圆桌和主持人提问产生的决策过程记录用于整理架构 ADR，再由正式架构设计文件统合相关决策。
旧 `architecture-note.md` 已降级为内部映射。

当前 skill 负责架构问题澄清、决策和正式设计产出；详细设计、系统架构落地和空骨架实现属于后续能力。

本包自包含运行时所需的行为和边界说明；仓库中的 ADR、训练语料和校验脚本只属于维护者资料，安装后不作为运行时依赖。
