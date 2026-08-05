# ADR-0014: 安装目录名 architecture-buddy

## Status
Accepted

## Context
Agent Skills 要求 frontmatter `name` 为小写字母/数字/连字符，且与父目录名一致。
ADR-0005 使用显示名「Architecture Buddy」与空格目录，与协议冲突。

## Decision
- 安装路径与 `name`：`architecture-buddy`
- 显示名（SKILL.md 标题与文档）：Architecture Buddy
- 透镜包：`architecture-buddy-lens-<shortname>/`，`name: architecture-buddy-lens-<shortname>`

## Consequences
- 更新 ADR-0005 目录表；旧空目录 `Architecture Buddy/` 若存在则删除或改为 README 指针。
