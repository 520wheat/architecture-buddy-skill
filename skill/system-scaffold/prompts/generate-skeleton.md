# generate-skeleton

## 何时加载

在 SC4 加载：映射已完成，且技术栈与模块边界都已确认。

## 目标

只生成锁定技术栈所需的最小骨架，而且允许内容是闭集：types、fields、states、method signatures、minimal consumer-owned interfaces、空实现、framework registration、dependency manifest、build/test entry、以及最小目录/模块声明。

## 输入

- SC3 的映射结果
- 已确认的 stack parameters
- `templates/skeleton-manifest.md`
- `templates/unimplemented-items.md`

## 强前置条件

- 每一个待写文件必须在任何实际文件操作前完整列入 `templates/skeleton-manifest.md` 的 Generated Files 清单。
- manifest 中不存在的文件禁止写入。
- 如果 manifest 缺少任一待写文件、缺少设计追溯、或文件用途不完整，状态必须停留在 draft 或 blocked，不生成代码。

## 执行

1. 先完整填写 manifest，再开始任何文件写入。
2. 逐项核对 manifest；未列入 manifest 的文件一律不得创建、修改或补写。
3. 只生成与锁定技术栈语法相关的结构：目录/模块声明、结构体、字段、状态、接口、方法签名、注册代码、依赖配置、构建/测试入口。
4. 只保留最小的 consumer-owned 接口。
5. 允许空实现，但不得加入业务逻辑。
6. 保持依赖方向与 architecture / detailed-design 一致。
7. 每个生成文件都要能追溯到一个已确认的 design unit。

## 输出契约

必须记录：

- stack decision
- file manifest
- generated files
- dependency / build / test entry
- empty implementations
- remaining blockers

## 不得做

- 不得写入任何未列入 manifest 的文件
- 不得在 manifest 不完整时生成代码
- 不得生成逐语言 adapter package
- 不得生成 README
- 不得生成测试文件
- 不得生成过程文档
- 不得生成实施计划
- 不得生成确定性实现脚本
- 不得生成 SQL migration
- 不得生成生产数据访问实现
- 不得补写业务逻辑
- 不得补写完整算法
- 不得生成 fake success 路径
- 不得隐藏空实现
- 不得在未确认前扩展依赖
- 不得变更架构边界
