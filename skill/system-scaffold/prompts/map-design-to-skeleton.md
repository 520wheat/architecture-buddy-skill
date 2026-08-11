# map-design-to-skeleton

## 何时加载

在 SC3 加载：架构与 detailed-design 已经 design-ready，且技术栈已经锁定。

## 目标

把每个设计单元映射到最小的代码模块、包或目录，同时保留模块边界、禁止边和状态约束。

## 输入

- 已确认的 language/runtime + version、framework + version、core_dependencies、dependency_manager、build_command、test_command、format_command、start_command、deployment constraint
- design-ready architecture
- design-ready detailed-design
- 模块边界、contracts、data shapes、state transitions、failure rules

## 执行

1. 为每个 design unit 生成一条映射。
2. 说明对应的 code module / package / folder。
3. 标出要保留的模块边界与禁止依赖。
4. 把字段、状态、输入输出形状映射到 concrete types、structures、fields。
5. 只在真实替换、隔离外部依赖、策略变化、隔离测试时才提出最小接口；若都不满足，则默认不建伪接口。
6. 一旦出现架构边界、数据归属、trust boundary、一致性或质量属性冲突，立即停止并返回 `architecture-buddy`；不得自行修正。
7. 一旦出现 detailed-design 契约、字段、状态或失败行为歧义，立即停止并返回 `detailed-design`；不得自行补全或改写。
8. 一旦出现设计与技术栈、边界或约束冲突，立即停止，不得自行修复或改写架构/设计。

## 输出契约

必须记录：

- design unit
- code target
- module boundary
- forbidden edges
- 字段 / 状态映射
- 接口是否有真实必要
- contradiction / blocker
- next action（continue mapping / return to architecture-buddy / return to detailed-design）

## 不得做

- 不得创建文件
- 不得默认任何语言或框架
- 不得引入伪接口
- 不得扩大模块边界
- 不得掩盖冲突
- 不得自行修复 architecture 或 detailed-design 冲突
