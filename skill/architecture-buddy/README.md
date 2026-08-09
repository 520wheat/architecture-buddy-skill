# architecture-buddy（主持 Skill）

当前版本：`0.5.0`

安装：将本目录复制或链接到你所用 Agent 的 Skills 目录，按该 Agent 的文档重新加载并调用 `architecture-buddy`。

透镜：同级的 `../architecture-buddy-lens-*` 一并安装；圆桌时按需选用。透镜是启发式做法立场，不是名人角色。

## 模式

- **`draft`**：一起拆假设、想清楚卡点；可半成品，不做完成检查。  
- **`deliverable`**：用户要完整架构设计时默认进入；走 S0–S7，过完成门禁后才可宣称完成。

## 用户示例

开发前：

```text
使用 $architecture-buddy，先和我确认要解决的问题类和基本事实，再共同设计订单系统的架构；遇到高影响分叉时提议圆桌，最后输出正式架构设计和 ADR。
```

已有项目：

```text
使用 $architecture-buddy，以 reference/retrospective 模式分析这个仓库；把已有代码当作只读事实，判断如果从项目开始前设计，模块边界、协作机制和演进是否成立。
```

需要外部资料时：

```text
先和我确认问题类和一个具体决策问题；在我明确授权后，再使用联网调查脚本整理指定来源，最后把相关证据回写到 ADR 和正式架构设计。
```

## 成品

正式架构设计文件是必需成品，默认按 ADR-0000 的六个核心板块组织。A/B 内容仅用于内部质量映射和训练，不是用户必须看到的固定格式。失败表、领域不变量、N+1、反例和详细演进按问题风险触发；联网调查产生的 `evidence.md` 只是可追溯证据附件，不是架构设计或会议记录的替代品。
三个产物角色必须分开：正式架构设计面向陌生读者，是主要交付物；架构 ADR 记录一个具体决策的背景、选择和代价；决策过程记录保存主持人提问、圆桌观点、用户反馈和综合回写。决策过程记录不能替代正式架构设计。
旧 M1–M9 结构已降级为内部映射。

当前 skill 负责架构问题澄清、决策和正式设计产出；详细设计、系统架构落地和空骨架实现属于后续能力。

本包自包含运行时所需的行为、边界说明、模板、参考资料和脚本；维护者的 ADR、训练语料和评估记录不随发行包提供。`agents/openai.yaml` 是可选的 Agent UI 元数据，不承载 Skill 的核心行为。

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
