# architecture-buddy（主持 Skill）

安装：将本目录链到 `~/.cursor/skills/architecture-buddy`，Reload Window 后 `@architecture-buddy`。

透镜：同级的 `../architecture-buddy-lens-*` 一并安装；圆桌时按需选用。透镜是启发式做法立场，不是名人角色。

## 模式

- **`draft`**：一起拆假设、想清楚卡点；可半成品，不做完成检查。  
- **`deliverable`**：用户要完整架构设计时默认进入；走 S0–S7，过完成门禁后才可宣称完成。

## 成品

正式架构设计文件是必需成品；可以采用自然的架构设计或 ADR 结构。`templates/architecture-deliverable.md` 的 A/B 内容用于质量映射和检查，不是用户可见文档唯一格式。联网调查产生的 `evidence.md` 只是可追溯证据附件，不是架构设计或会议记录的替代品。
三个产物角色必须分开：正式架构设计面向陌生读者，是主要交付物；架构 ADR 记录一个具体决策的背景、选择和代价；决策过程记录保存主持人提问、圆桌观点、用户反馈和综合回写。决策过程记录不能替代正式架构设计。
旧 M1–M9 结构已降级为内部映射。

当前 skill 负责架构问题澄清、决策和正式设计产出；详细设计、系统架构落地和空骨架实现属于后续能力。

本包自包含运行时所需的行为和边界说明；仓库中的 ADR、训练语料和校验脚本只属于维护者资料，安装后不作为运行时依赖。

## 运行时目录

- `prompts/`：五个分阶段运行提示词，分别负责问题澄清、第一性原理、圆桌、ADR 综合和正式交付审阅；由 `SKILL.md` 按阶段加载。
- `references/`：运行时架构知识和完成门禁。
- `templates/`：正式架构设计、问题类、ADR 和决策过程记录模板。
- `scripts/`：运行时确定性工具目录，提供设计工作区初始化、正式设计结构校验、圆桌过程校验和用户授权后的联网调查证据包；调查工具不执行网页指令、不判断架构、不调用训练资料或 SkillOpt。
- `agents/`：Agent UI 元数据目录。

## 脚本

在本目录中执行：

```bash
python3 scripts/init-design.py --output <输出目录> --name <设计名称>
python3 scripts/validate-deliverable.py <正式架构设计文件>
python3 scripts/validate-roundtable.py <决策过程记录文件>
python3 scripts/init-research.py --output <调查目录> --problem-class "<问题类>" --decision-question "<单一决策问题>" --authorize-online-research
python3 scripts/fetch-research.py --workspace <调查目录>
python3 scripts/build-evidence.py --workspace <调查目录>
python3 scripts/validate-evidence.py --workspace <调查目录>
```

初始化默认不覆盖已有产物；结构校验只检查必要证据是否存在，不判断架构方案是否优秀。联网调查的完整契约、来源格式、网络安全边界和字幕限制见 `references/research-evidence.md`。
