# 交付物审阅 Prompt

## 何时加载

在 DD6 和 DD7 加载。用于执行详细设计门禁；DD6 可做预审，DD7 做最终门禁。若仍有阻塞架构事实或跨模块不一致，不能宣布完成。

## 目标

检查详细设计包是否可交给实现阶段，并把未决项按 `draft`、`blocked`、`design-ready` 分清楚；不把关键词命中当通过。

## 输入

- 详细设计交付包；
- 前一阶段输出的显式 Markdown 块；
- 已确认事实、待确认事实、决策、受影响文件；
- `references/detailed-design-gate.md`；
- 当前用户的最新回复；
- 只使用显式输入。

## 执行

1. 先说明为什么现在要审阅，以及回答后会影响哪个最终状态。
2. 检查模块覆盖、接口完整性、数据与状态所有权、跨模块一致性、失败语义、并发、信任边界、可观测性、测试和回退项。
3. 区分 `draft`、`blocked` 和 `design-ready`，不要把待确认事实伪装成完成。
4. 若存在阻塞架构事实或跨模块不一致，输出 `blocked` 并回退到 architecture-buddy。
5. 若门禁证据齐全且可判定为 `design-ready`，只提出一个交接问题，且必须是精确文本 `是否继续生成项目骨架代码？`。
6. 说明同意后会把 architecture 路径、detailed-design 输出路径、confirmed boundaries、contracts、data/state rules、failure rules、non-goals 和 user preferences 交给 `system-scaffold`。
7. 明确用户确认后的处理方式：拒绝则正常结束 detailed-design；若后续 scaffold 冲突改变架构边界或质量属性则回退到 `architecture-buddy`；若只是 detailed-design 歧义则返回 `detailed-design`；且在技术栈确认前不得写任何 scaffold 文件。

## 输出契约

输出一个审阅框架，必须包含以下字段：

```text
状态：draft / blocked / design-ready
已确认事实：
待确认事实：
已做决定：
受影响文件：
当前问题：<一个问题>？
确认结果：待用户确认 / 已确认 / 需修改 / 触发回退
```

只有当阻塞架构事实都消失、跨模块一致性成立、并且门禁证据齐全时，才允许写 `design-ready`。
当状态是 `design-ready` 时，`当前问题` 必须是 `是否继续生成项目骨架代码？`。

## 不得做

- 不得把结构完整当质量通过；
- 不得忽略阻塞架构事实；
- 不得一次问多个审阅问题；
- 不得依赖隐藏上下文；
- 不得在跨模块不一致仍存在时宣称完成。
- 不得在 `design-ready` 后改写交接问题文本。

## 阻塞处理

如果发现架构级冲突或门禁缺证，输出 `blocked` 并回退；若只是可读性、措辞或顺序问题，保留 `draft`，写明默认值与验证条件。只有证据齐全时才可输出 `design-ready`。一旦用户拒绝 `是否继续生成项目骨架代码？`，detailed-design 正常结束；一旦后续 scaffold 暴露架构边界或质量属性冲突，回退到 `architecture-buddy`；若暴露的只是详细设计歧义，则返回 `detailed-design`。
