# Corpus P3 — PoEAA 模式族对照（Phase 1：三族）
- 阶段: Phase 1 · 2026-08-04
- 来源: https://martinfowler.com/eaaCatalog/
- 状态: 领域逻辑 / 数据源 / Web 呈现 三族已建表；其余族 Phase 2+

## 覆盖范围
Fowler *Patterns of Enterprise Application Architecture* 在线目录。强调 **when to use**，同一问题类下并列策略。

## 族 1：Domain Logic（如何组织业务逻辑）

| 模式 | 问题类切片 | 适用力 | 关键后果 | 层级 |
|------|------------|--------|----------|------|
| Transaction Script | 按过程/请求组织逻辑 | 简单、少逻辑重叠 | 复杂域易重复难演化 | 企业 |
| Domain Model | 对象模型含行为与数据 | 复杂规则、丰富行为 | 建模成本高；需映射策略 | 企业 |
| Table Module | 一表一逻辑模块 | 表中心、偏记录集 | 不如富领域模型表达力 | 企业 |
| Service Layer | 应用边界上的服务操作集 | 清晰 API 边界、多入口 | 可能变成事务脚本堆 | 企业 |

**对照启示**：这是 M5「策略选项表」的教科书形态——先问题类「组织领域逻辑」，再并列模式。

## 族 2：Data Source Architectural Patterns（领域对象如何连数据）

| 模式 | 问题类切片 | 适用力 | 关键后果 | 层级 |
|------|------------|--------|----------|------|
| Table Data Gateway | 表级网关 | 简单表访问 | 与领域模型可能重复 | 企业 |
| Row Data Gateway | 行级网关 | 行对象接口 | 实例数多 | 企业 |
| Active Record | 行对象+DB+领域逻辑 | 中等复杂度 CRUD | 测试/耦合代价 | 企业 |
| Data Mapper | 映射层隔离对象与 DB | 复杂模型、持久无关 | 映射工作量大 | 企业 |

## 族 3：Web Presentation

| 模式 | 问题类切片 | 适用力 | 关键后果 | 层级 |
|------|------------|--------|----------|------|
| Model View Controller | UI 三角分工 | 多视图、可测模型 | 正确实现有成本 | 架构/企业交叉 |
| Page Controller | 一页/动作一控制器 | 简单站点结构 | 页面多时重复 | 企业 |
| Front Controller | 统一入口控制器 | 集中安全/导航/国际化 | 单点复杂 | 企业 |
| Template View / Transform View / Two Step View | 渲染策略 | 不同模板/转换需求 | 各有运维与缓存含义 | 企业 |
| Application Controller | 集中屏幕流 | 富导航/工作流 UI | 与领域逻辑边界要清 | 企业 |

## 与其他 corpus 重叠
- MVC：与 POSA MVC 同名同源气质，PoEAA 更偏企业 Web
- Gateway：与 POSA Broker/一般 Gateway 概念相邻但粒度不同

## 对 Architecture Buddy 的直接条目
- 共思「业务逻辑放哪」时，默认抛出 Transaction Script vs Domain Model vs Service Layer
- 禁止只给一个「最佳实践」而不列适用条件

## 下一步（Phase 2）
- Object-Relational 行为/结构族、Distribution、Offline Concurrency、Session State
