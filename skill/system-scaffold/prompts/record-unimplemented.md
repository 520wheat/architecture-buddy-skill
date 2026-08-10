# record-unimplemented

## 何时加载

在 SC5 加载：骨架已经生成，需要把所有未实现点显式记录下来。

## 目标

记录每一个空方法和 `not implemented` path，避免 fake success response。

## 输入

- skeleton manifest
- generated files
- empty implementations
- confirmed stack decision

## 执行

1. 找出所有空实现、占位返回、未完成分支。
2. 为每个条目记录 module、contract、reason、expected later implementation、acceptance condition。
3. 如果某个路径只能靠 fake success 维持表面通过，必须明确标记禁止。
4. 不得把未实现状态写成已完成。

## 输出契约

必须记录：

- module
- contract
- empty method / not implemented path
- reason
- expected later implementation
- acceptance condition
- status

## 不得做

- 不得伪造成功响应
- 不得隐藏未实现路径
- 不得删除空实现记录
- 不得把风险改写成已完成
