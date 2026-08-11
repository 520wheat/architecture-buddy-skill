# Skeleton Manifest

## 写入前门禁

- 每一个待写文件必须在任何实际文件操作前完整列入下方 `Generated Files` 表。
- `Generated Files` 表之外的文件禁止写入。
- 如果 manifest 缺少任一待写文件、设计追溯、或用途说明，状态必须停留在 draft 或 blocked，不生成代码。

## Stack Decision

- 语言 / 运行时：
- 框架 / 版本：
- 依赖管理器：
- 构建命令：
- 测试命令：
- 格式化命令：
- 启动命令：
- 部署约束：

## 模块边界

| Design unit | Code target | Boundary preserved | Forbidden edges | 字段 / 状态 | 接口 |
| --- | --- | --- | --- | --- | --- |

## Generated Files

| File | Design unit | Purpose | Why it exists | Depends on | Write declared before file ops | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## 依赖 / 构建 / 测试

- 依赖：
- 构建：
- 测试：
- 启动：

## Wiring

- Framework registration:
- Minimal consumer-owned interfaces:
- Empty implementations:
- Visible unimplemented items:

## 禁止项

- 禁止业务实现
- 禁止 README
- 禁止测试文件
- 禁止过程文档
- 禁止实施计划
- 禁止确定性实现脚本
- 禁止 SQL migration
- 禁止生产数据访问实现
- 禁止伪成功
- 禁止扩大模块边界
- 禁止 manifest 外写文件
- 禁止引入多余依赖
