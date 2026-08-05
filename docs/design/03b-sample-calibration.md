# 样本校准：优秀架构描述 × 模式文献（路径 C）

## Status

Complete（初版校准结论）— 用于回写 §3

## 样本清单

### A. 真实项目 / 架构描述

| 样本 | 为何可学 | 链接 |
|------|----------|------|
| **AOSA · nginx** | 先讲问题类（高并发/C10K）与约束，再对比既有策略（Apache 多进程），再给出核心机制（event-driven / async / worker），并诚实写代价（磁盘阻塞、嵌入脚本风险） | https://aosabook.org/en/v2/nginx.html |
| **arc42 范例 · HTML Sanity Checker (HSC)** | 完整 arc42：目标、约束、Solution Strategy、决策含备选与标准；跨切概念里**显式使用 Template Method 等模式名** | https://hsc.aim42.org/arc42/hsc_arc42.html |

补充学习源（不逐章精读，作书库）：[Architecture of Open Source Applications](http://aosabook.org/en/index.html) —— 编辑宗旨即「像建筑师研读建筑那样研读软件」。

### B. 模式文献（写作单元）

| 样本 | 为何可学 | 链接 / 出处 |
|------|----------|-------------|
| **PoEAA 目录与领域逻辑模式族** | 同一问题类（如何组织业务逻辑）下并列 Transaction Script / Domain Model / Table Module / Service Layer，强调 **when to use**，不是唯一正确答案 | https://martinfowler.com/eaaCatalog/ |
| **POSA 模式体系** | 架构模式 → 设计模式 → 惯用法分层；模式是「可组合的已验证解法池」 | POSA Vol.1–5（Buschmann et al.） |
| **GoF 模式叙述结构** | Context / Problem / Forces / Solution / Consequences 的经典写法；**粒度细**，校准「如何写清一个解法」，默认不占架构笔记主结构 | Gamma et al., *Design Patterns* |
| **Nygard ADR** | 决策写作：Context → Decision → Consequences（含负面）；显式借鉴 Alexandrian pattern | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |

## 校准：样本如何印证 M1–M8

| 机制 | nginx (AOSA) | HSC (arc42) | PoEAA / POSA / GoF / ADR |
|------|--------------|-------------|---------------------------|
| M1 问题类与边界 | C10K、边缘卸载 vs 通用服务器 | HTML 语义检查（非语法） | 模式名本身绑定问题类 |
| M2 干系人/关注点 | 网站架构师、运维、扩展开发者 | 作者、构建集成 | Forces = 关注点张力 |
| M3 约束 | OS 事件机制、Windows 限制、许可 | 依赖少、开源许可、插件形态 | Context 中的硬边界 |
| M4 ASR/质量目标 | 高并发、低内存、可扩展 | 清晰报告、可集成构建 | 质量力驱动模式选用 |
| M5 机制 vs 策略 | **机制**：事件驱动非阻塞；相对 Apache 的策略分叉 | Solution Strategy + 可插拔 Checker | PoEAA 模式族 = 策略目录 |
| M6 决策与理由 | 为何不 per-connection 进程 | jsoup vs HTTPUnit 等，含标准 | ADR / 模式 Consequences |
| M7 权衡风险未决 | 磁盘 I/O 仍可能阻塞；脚本挂 worker | 外链检查延后 | 模式必写代价 |
| M8 证据学习痕迹 | 整章即学习叙事；对比 Apache/C10K | 文档声明自己是可学习范例 | 模式文献即公共证据 |

## 从样本学到的「写法机制」（补强骨架）

1. **先力后形**：先问题/约束/质量，后结构图（nginx、HSC 皆然；Building Blocks 在 Strategy 之后）。
2. **策略要成对出现**：至少给出被拒绝或未选的替代（Apache；HTTPUnit；Transaction Script vs Domain Model）。
3. **点名公共模式**：能对上 POSA/PoEAA/GoF/EIP 的，用公共名（HSC 的 Template Method），减少黑话。
4. **后果含负面**：nginx 的阻塞与脚本风险；ADR 要求列出负向后果。
5. **模式是响应不是起点**：PoEAA/GoF 都先问题与力，再 Solution——对齐「先 M1–M4，再 M5」。
6. **厚度可变**：HSC 承认示例文档相对代码偏厚；Fairbanks/风险驱动仍然成立——按风险裁剪节数。

## 对 §3 产物格式的直接含义

架构笔记主结构应映射 M1–M8，并内嵌：

- **策略选项表**：允许填模式名（架构/企业模式优先）
- **决策小节**：Nygard/MADR 气质（背景、选项、决定、后果）
- **模式索引（可选）**：本次用到的模式及层级（架构 / 企业 / 细粒度）
- **附录**：模块/构建块视图——需要时再写，不当第一章

## 明确不从样本学坏的东西

- 不要把 AOSA 章节写成「只有组件图没有为何」的缩写版（我们要保留为何）
- 不要把 GoF 目录整表塞进每次笔记
- 不要把容量数字与中间件品牌当架构主叙事（仍属系统设计落地）
