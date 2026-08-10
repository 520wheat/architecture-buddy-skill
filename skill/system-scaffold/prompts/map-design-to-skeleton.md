# map-design-to-skeleton

## 何时加载

在 SC3 加载：架构与 detailed-design 已经 design-ready，且技术栈已经锁定。

## 目标

把每个设计单元映射到最小的代码模块、包或目录，同时保留模块边界、禁止边和状态约束。

## 输入

- 已确认的 language/runtime、framework、dependency manager、build/test/start 约束
- design-ready architecture
- design-ready detailed-design
- 模块边界、contracts、data shapes、state transitions、failure rules

## 执行

1. 为每个 design unit 生成一条映射。
2. 说明对应的 code module / package / folder。
3. 标出要保留的模块边界与禁止依赖。
4. 把字段、状态、输入输出形状映射到 concrete types、structures、fields。
5. 只在真实替换、隔离外部依赖、隔离测试时才提出接口。
6. 一旦出现设计与技术栈、边界或约束冲突，立即停止，不得自行修正架构。

## 输出契约

必须记录：

- design unit
- code target
- module boundary
- forbidden edges
- 字段 / 状态映射
- 接口是否有真实必要
- contradiction / blocker
- next action

## 不得做

- 不得创建文件
- 不得默认任何语言或框架
- 不得引入伪接口
- 不得扩大模块边界
- 不得掩盖冲突
