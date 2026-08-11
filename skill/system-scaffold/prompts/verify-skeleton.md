# SC6 骨架验证 Prompt

## 何时加载

在 SC6 加载。必须在 SC5 记录未实现项之后运行；任何 `skeleton-ready` 结论都只能在这里给出。

## 目标

检查项目骨架是否遵守已确认技术栈、完整覆盖已确认模块边界，并把未完成业务项显式保留在 unimplemented 列表中。`skeleton-ready` 只表示骨架可继续进入实现阶段，不代表业务功能已经完成。

## 输入

- 已确认的 architecture handoff；
- 已确认的 detailed-design handoff；
- 已确认的 technology-stack decision（包含 language/runtime + version、framework + version、core_dependencies、dependency_manager、build_command、test_command、format_command、start_command、deployment constraint）；
- skeleton manifest；
- 生成的骨架文件列表；
- unimplemented-items 列表；
- build / compile / test / format / start 相关命令及其最新输出；
- `references/verification-gate.md`；
- `references/skeleton-rules.md`；
- 只使用显式输入。

## 执行

1. 先说明为什么现在需要验证，以及本次验证会决定 `draft`、`blocked` 或 `skeleton-ready` 哪个状态。
2. 检查技术栈合规性：language/runtime + version、framework + version、core_dependencies、dependency_manager、build_command、test_command、format_command、start_command、deployment constraint 是否与已确认 decision 一致。
3. 检查模块覆盖：每个已确认模块边界都要映射到最小可见的 package、module 或 folder。
4. 检查依赖方向：生成骨架不得违背 architecture 与 detailed-design 里确认的依赖方向、边界和 ownership。
5. 检查 required fields and interfaces：必须字段、必要入口、必需接口或 concrete symbol 是否齐全；不得凭空扩展业务契约。
6. 检查 framework wiring：仅注册已确认技术栈要求的最小框架接线，不得引入未确认扩展点。
7. 检查 compile / build、test、format、start entry：能运行的构建或编译命令必须成功；若技术栈支持测试、格式化或启动入口，则这些入口都必须可达并被明确记录。
8. 检查 deployment constraint：生成骨架不得违反已确认的部署约束、运行边界或打包前提。
9. 检查 unimplemented-items 与 skeleton manifest：所有未完成业务行为都要可见，且生成文件清单必须完整列出每个文件及其用途。
10. 如果缺少确认栈字段、manifest 不完整、或验证证据不足，保持 `draft`；如果出现架构/设计/栈冲突，输出 `blocked` 并说明回退去向；只有全部必需检查通过时才输出 `skeleton-ready`。

## 输出契约

输出一个验证框架，必须包含以下字段：

```text
状态：draft / blocked / skeleton-ready
技术栈结论：
模块覆盖结论：
依赖方向结论：
接口与必填项结论：
框架接线结论：
构建/编译结论：
测试入口结论：
格式入口结论：
启动入口结论：
部署约束结论：
未实现项结论：
生成文件清单结论：
当前问题：<一个问题或“无”>
后续动作：继续确认 / 返回 architecture-buddy / 返回 detailed-design / 进入实现
```

## 不得做

- 不得把 `skeleton-ready` 解释为业务完成；
- 不得绕过 SC6 直接输出 `skeleton-ready`；
- 不得因为 build 通过就忽略模块覆盖、依赖方向或 unimplemented 清单；
- 不得跳过技术栈确认门禁；
- 不得依赖隐藏上下文或未执行的命令；
- 不得在冲突仍存在时宣称骨架可交付。
