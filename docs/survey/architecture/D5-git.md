# AOSA — Git
- 域: D5 语言运行时 / VCS / 工具链
- 来源: https://aosabook.org/en/v2/git.html
- 阶段: Phase 2 · 2026-08-05

## 问题类
在高方差贡献者群体中，维护可分布式协作的数字工作体（常为代码）：支持发散/收敛工作流、防内容损坏、高性能——**反 CVS** 哲学。

## 硬约束（Torvalds 目标）
- 分布式工作流（类 BitKeeper）
- 内容完整性防护
- 高性能

## 机制（共性）
1. **内容寻址对象库**（blob/tree/commit/tag）形成 DAG 快照
2. **历史亦为 DAG**（多父合并）
3. **引用（refs）** 指向提交；分支轻量
4. **本地提交与推送分享解耦**
5. **Plumbing / Porcelain 分层工具箱**
6. 相同 SHA ⇒ 相同内容，可短路比较与高效合并祖先查找

## 策略（差异/选项）
| 维度 | Git | 对照 |
|------|-----|------|
| 内容存储 | DAG 快照 | 基于 delta changeset（多数传统 VCS） |
| 历史 | DAG | 线性历史（SVN 等） |
| 分发 | 分布式多仓库 | 中央服务器必经 |
| 工作流复杂度 | 高灵活换心智成本 | 中央模型「忘记 push」更简单 |

## 显式模式名
- Content-Addressable Storage
- DAG
- Command layered architecture (plumbing/porcelain)
- Snapshot vs Delta

## 决策与负面后果
- 灵活工作流 ↔ 用户概念负担（commit vs push）
- 完整快照对象在大文件小改时曾低效，后续有优化路径（章内讨论）

## 对写作规范的启示
- 用「功能需求三问」（存内容/追历史/分发）组织策略空间——可复用到其他工具链问题类
