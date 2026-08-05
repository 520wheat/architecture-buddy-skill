# Corpus P3 — PoEAA 其余模式族（Phase 4）
- 阶段: Phase 4 · 2026-08-05
- 配套: `P3-poeaa-families.md`（Domain Logic / Data Source / Web Presentation）
- 来源: https://martinfowler.com/eaaCatalog/

强调：各族内模式是**并列策略**，不是进步阶梯。

## 族 4：Object-Relational Behavioral

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Unit of Work | 跟踪业务事务中的对象变更并协调写回 | 复杂对象图、一次提交 | 实现与边界要清；与会话生命周期耦合 |
| Identity Map | 每会话每实体一实例 | 避免重复加载与更新冲突幻觉 | 内存与生命周期管理 |
| Lazy Load | 按需加载关联 | 减少初始查询 | N+1；分布式时更痛 |

## 族 5：Object-Relational Structural

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Identity Field | DB 键暴露为对象标识 | 几乎总需要 | 键策略影响集成 |
| Foreign Key Mapping / Association Table Mapping | 关联如何落表 | 1-1 / 1-N / M-N | 映射复杂度 |
| Embedded Value / Serialized LOB | 值对象/大块序列化 | 简单内嵌 vs 文档块 | 查询能力与迁移代价 |
| Inheritance Mappers（单表/类表/具体表） | 继承层次如何映射 | 各有查询/演化权衡 | 选错难迁移 |

## 族 6：Object-Relational Metadata Mapping

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Metadata Mapping | 映射信息与代码分离 | 多映射/工具生成 | 间接与调试成本 |
| Query Object / Repository | 面向对象查询与集合式访问 | 复杂查询封装 | Repository 变成上帝时退化 |

## 族 7：Distribution Patterns

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Remote Facade | 粗粒度远程接口 | 聊天式细粒度远程太贵 | 门面膨胀 |
| Data Transfer Object | 跨进程传数据束 | 减少往返 | 同步与版本负担 |

**Buddy**：远程边界先问往返与一致性，再选 Facade/DTO——对齐 M3/M5。

## 族 8：Offline Concurrency

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Optimistic Offline Lock | 冲突少时提交检测 | 协作编辑/长会话 | 冲突处理 UX |
| Pessimistic Offline Lock | 先锁再改 | 高冲突关键资源 | 吞吐与死锁 |
| Coarse-Grained Lock / Implicit Lock | 锁粒度与隐式策略 | 简化加锁 | 过度锁或隐藏锁 |

## 族 9：Session State

| 模式 | 问题类切片 | 适用力 | 关键后果 |
|------|------------|--------|----------|
| Client Session State | 状态在客户端 | 无服务器亲和 | 安全/体积/篡改 |
| Server Session State | 状态在服务器 | 简化客户端 | 粘滞与扩展 |
| Database Session State | 状态落库 | 多实例共享 | 延迟与清理 |

## 与 Django / Buddy
- Django Models ≈ Active Record 策略点；复杂域可走向 Domain Model + Data Mapper（族 1–2）
- Session State 族直接支撑「无状态服务 vs 粘滞会话」架构笔记问句

## 对 Architecture Buddy 的直接条目
共思数据访问时默认序列：
1. 领域逻辑族（脚本 vs 模型 vs 服务层）
2. 数据源族（AR vs Mapper）
3. 若有远程：Distribution
4. 若有长会话编辑：Offline Concurrency + Session State
