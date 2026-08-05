# SOURCES — minecraft

## 诚实边界（必读）

**无官方完整架构白皮书。** 本金标是基于公开 wiki、协议文档与社区/第三方服务端叙述的**合理重构**，用于问题类校准，**不是** Mojang/Microsoft 正典设计说明。版本间协议与实现细节会变；金标锁问题类机制，不锁死某一小版本包名字段。

## 公开资料（机制主依据）

1. Minecraft Wiki（社区维护百科）  
   https://minecraft.wiki/  
   游戏循环心智、区块、实体与多人游玩高层描述；非厂商架构白皮书。

2. wiki.vg Protocol（社区协议文档）  
   https://wiki.vg/Protocol  
   客户端↔服务端包类型与状态机心智：登录、游戏态、区块/实体相关同步方向。社区逆向/整理，非官方规范正典。

3. wiki.vg 相关页（按需）  
   https://wiki.vg/Protocol_FAQ · https://wiki.vg/Map_Format 等  
   兴趣同步、世界格式与协议边界的补充上下文。

## 社区 / 第三方实现叙述（策略与演进）

4. PaperMC 文档（第三方服务端）  
   https://docs.papermc.io/  
   生产向服务端、区块/实体优化与（Folia 等）区域并行叙事——作**策略选项**材料，不当作「原版唯一正典」。

5. 代理与群组服生态（公开项目文档，如 Velocity / BungeeCord 类）  
   跨逻辑服玩家路由、协议转发边界——作「单世界权威 vs 代理/群组」策略分叉依据。

6. 模组/数据驱动扩展公开叙述（Fabric / Forge / datapack 文档与 wiki）  
   内容扩展落在数据与加载器边界，而非「只教写插件 API」——支撑 B3 可模组性策略维。

## 本地 survey

7. `docs/survey/architecture/D9-minecraft-sim.md`  
   Phase 3 短摘记；本金标由其升格为完整双层 deliverable。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
- 候选若声称「摘自 Mojang 官方架构白皮书」而无公开出处 → 对照幻觉黑名单。
