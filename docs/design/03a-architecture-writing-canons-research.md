# 调研：公开公认的架构设计（写作与描述）canon

## Status

In progress（初稿地图，需加深）

## 调研边界

| 纳入 | 排除（或降级为附录） |
|------|----------------------|
| Architecture Description、决策与权衡、质量属性驱动设计 | System Design 面试题解、容量估算教程 |
| 国际标准 / SEI 方法 / 广泛采用的架构文档模板 | 某一厂商的产品参考架构照抄 |
| 「一类问题如何被架构化表达」 | 「这个系统模块怎么拆」为主线的材料 |

## 候选 canon（初选）

### 1. ISO/IEC/IEEE 42010 — Architecture Description

- **地位**：架构描述的国际标准词汇与要求
- **核心概念**：Stakeholders、Concerns、Viewpoints/Views、Architecture Decision、Rationale
- **对产物的启示**：架构写作首先回答「谁关心什么、用什么视角说清楚、做了哪些决策及理由」，而不是先画模块
- **链接**：https://www.iso-architecture.org/42010/ · IEEE 42010-2022

### 2. SEI Attribute-Driven Design (ADD)

- **地位**：CMU SEI 的架构设计方法
- **核心概念**：Architecturally Significant Requirements（功能 + 质量属性 + 约束）；用 tactics/patterns 满足驱动性质量属性；迭代分解
- **对产物的启示**：先抓住 ASR / 质量属性场景，再谈结构；结构是满足属性的手段
- **链接**：SEI ADD 2.0 等报告

### 3. SEI ATAM — Architecture Tradeoff Analysis Method

- **地位**：架构评估与权衡的经典方法
- **核心概念**：质量属性、tradeoff、sensitivity point、risk
- **对产物的启示**：笔记必须显式记录权衡与风险，而非只给「推荐方案」

### 4. Bass et al. / Richards & Ford — 质量属性与架构特征

- **地位**：教材与工业实践主流（《Software Architecture in Practice》；《Fundamentals of Software Architecture》）
- **核心概念**：Quality Attributes / Architectural Characteristics；架构是关于「重要决策」与可进化性
- **对产物的启示**：机制层应包含「必须成立的架构特征」；策略层是特征之间的取舍

### 5. Architecture Decision Records (ADR, Nygard 等)

- **地位**：业界事实标准的决策记录形式
- **核心概念**：Context / Decision / Status / Consequences（及变体）
- **对产物的启示**：取舍必须可追溯；类问题模板里的「策略选择」最终常落成一组 ADR

### 6. arc42

- **地位**：广泛使用的架构文档模板
- **核心概念**：分节文档（目标、约束、上下文、方案策略、质量、…）
- **使用注意**：其中 Building Blocks 等章节易滑向系统设计；采纳时应**抽其「目标/约束/质量/方案策略」等架构层章节**，弱化组件清单作为主线
- **链接**：https://github.com/arc42/arc42-template

### 7. 风险驱动 / Just Enough（Fairbanks 等）

- **地位**：强调架构投入与风险成正比
- **对产物的启示**：未决点与风险应是一等公民；不是每个问题类都需要同等厚度的文档

### 8. DDD Strategic Design（辅助）

- **地位**：问题空间划分的公认方法
- **核心概念**：Bounded Context、Context Map、通用语言
- **对产物的启示**：界定「问题类」与边界时很有用；不是全文主模板

## 机制骨架 v0.1（A：42010 + ADD/ATAM + ADR，辅以 arc42 裁剪）

> 状态：待你确认。确认后进入样本校准（轻量 C 后半）。

跨 canon 稳定出现、且符合「一类问题的解法抽象」的**必含机制**：

| # | 机制 | 来自 | 在共思里做什么 |
|---|------|------|----------------|
| M1 | **问题类 / 范围与边界** | 42010 Entity of Interest；arc42 Context & Scope（取其边界义，不取其部署细节） | 我们在解决哪一类问题？含什么/不含什么 |
| M2 | **干系人与关注点（Concerns）** | 42010 Stakeholders & Concerns；arc42 §1 Stakeholders | 谁在乎什么？哪些关注点是架构级的 |
| M3 | **约束** | ADD Constraints；arc42 §2 | 不可违背的技术/组织/法规边界 |
| M4 | **架构显著需求 / 质量目标（ASR）** | ADD ASR；ATAM 质量属性场景；arc42 Quality Goals（Top 3–5） | 用场景说清「够好」长什么样；明确不优化什么 |
| M5 | **解决方案策略（机制层共性 vs 策略层选项）** | arc42 Solution Strategy；ADD tactics/patterns；本项目 ADR-0001 | 先抽该类问题的共性机制，再并列可替换策略 |
| M6 | **架构决策与理由** | 42010 Decision + Rationale；Nygard ADR（Context/Decision/Status/Consequences） | 重要取舍写成可追溯决策，含后果（正/负/中性） |
| M7 | **权衡、风险与未决** | ATAM tradeoff / sensitivity / risk；arc42 Risks；Fairbanks just-enough | 显式记录冲突的质量目标、敏感点、尚不知道的事 |
| M8 | **证据与学习痕迹（可选但推荐）** | 本项目 Top N 问询；ADR「写给未来的自己」 | Top N / 圆桌 / 样本对照摘要——支撑机制为何成立 |

### 与「做架构即学习」（ADR-0008）对齐

- 上表不是讲义目录，而是共思时 naturally 会碰到的锚点。
- 伙伴按对话推进；关键分叉用一两句点明「我们刚在澄清的是 M4/M6」。
- 笔记是学习痕迹的沉淀，不是填空考试。

## 策略候选（写法差异，按问题选用）

| 策略 | 何时偏向 |
|------|----------|
| 轻量：一页架构笔记 + 少量 ADR | 早期探索、风险尚不清晰 |
| 中量：笔记 + 质量场景表 + 决策日志 | 默认软件产品共思 |
| 重量：向 arc42 多节展开 + 多 viewpoint | 强合规、多干系人、或要对外评审 |
| Top N 深挖 vs 跳过 | 用户同意调研时做；否则用已知模式轻量对照 |
| 圆桌视角 | 取舍尖锐或用户要求多视角时 |

## 明确降级 / 排除出主结构

| 降级项 | 原因 |
|--------|------|
| Building Blocks / 模块分解作第一章 | 易滑成系统设计；可作附录或下游输入 |
| Runtime/Deployment 细图作主叙事 | 偏系统与运维设计；除非某 Concern 强制要求该 viewpoint |
| QPS/容量/具体中间件选型作主线 | 系统设计落地，不是问题类架构抽象 |
| 无理由的「最佳实践」清单 | 违背 ADR/42010 的 rationale 要求 |

## Nygard ADR 要点摘录（写作机制）

- 只记 **architecturally significant** 决策（影响结构、非功能特征、依赖、接口或构建方式）
- 短文：Context（价值中立的力）→ Decision（We will…）→ Status → Consequences（含负面）
- 写给未来的开发者；决策被推翻时保留并标记 superseded

## Patterns canon（ADR-0009，与样本调研并行）

模式是「对一类反复出现问题的命名解法」，天然贴合本项目的机制/策略抽象。  
层次不分清时，容易把架构笔记写成模式背诵表——故分层使用：

| 层次 | 代表文献 | 在 Buddy 中的位置 |
|------|----------|-------------------|
| **架构模式** | POSA（Buschmann et al.）；Layered / Pipes-Filters / Broker / Microkernel 等 | **优先**进入 M5：问题类级的机制或主策略候选 |
| **企业应用 / 集成模式** | Fowler *PoEAA*；Hohpe *Enterprise Integration Patterns* | M5 策略目录；选用写入 M6 |
| **架构风格与模式对照** | Richards & Ford 等对 Architecture Patterns 的讨论 | 帮助区分「脚手架级」与「类内部结构级」 |
| **细粒度设计模式** | GoF *Design Patterns* | 机制/边界清晰后的**局部策略或附录**；不默认占笔记主结构 |
| **模式作为决策单元** | Nygard ADR 显式借鉴 Alexandrian pattern 写法（forces → decision） | M6 的写作气质：力、响应、后果 |

### 使用原则（共思时）

1. 先 M1–M4（问题类、关注点、约束、ASR），再谈「有哪些模式候选」——模式是响应，不是起点。  
2. 每个候选模式至少说清：**解决哪类力 / 适用条件 / 代价与后果**（模式文献的 Context–Forces–Solution–Consequences）。  
3. Top N 样本里若反复出现同一结构，优先用**已有模式名**命名机制，避免私有黑话。  
4. 细粒度 GoF 模式：仅当某决策落在组件内部协作、且影响架构特征时才升格进笔记；否则留给实现设计。

### 与机制骨架的挂接

- **M5**：模式库 = 策略选项的公共词汇表  
- **M6**：选用/排除模式必须有理由与后果  
- **M8**：模式文献 + Top N 实例互相印证「这不是我们发明的」

## 下一步

1. ~~你确认机制骨架 v0.1~~ → **已确认**  
2. ~~纳入 Patterns~~ → **已确认（ADR-0009）**  
3. ~~样本校准（路径 C）~~ → 见 `03b-sample-calibration.md`  
4. **待你批准**：`03-notes-and-templates.md`（Proposed）→ Approved  
