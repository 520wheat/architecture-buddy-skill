# generate-skeleton

## 何时加载

在 SC4 加载：映射已完成，且技术栈与模块边界都已确认。

## 目标

只生成锁定技术栈所需的最小骨架：types、fields、method signatures、minimal consumer-owned interfaces、空实现、framework registration、dependency manifest、build/test entry。

## 输入

- SC3 的映射结果
- 已确认的 stack parameters
- `templates/skeleton-manifest.md`
- `templates/unimplemented-items.md`

## 执行

1. 在写入前先列出所有将生成的文件。
2. 只生成与锁定技术栈语法相关的结构：结构体、字段、接口、方法签名、注册代码、依赖配置、构建/测试入口。
3. 只保留最小的 consumer-owned 接口。
4. 允许空实现，但不得加入业务逻辑。
5. 保持依赖方向与 architecture / detailed-design 一致。
6. 每个生成文件都要能追溯到一个已确认的 design unit。

## 输出契约

必须记录：

- stack decision
- file manifest
- generated files
- dependency / build / test entry
- empty implementations
- remaining blockers

## 不得做

- 不得遗漏任何将写入的文件
- 不得生成逐语言 adapter package
- 不得补写业务行为
- 不得隐藏空实现
- 不得在未确认前扩展依赖
