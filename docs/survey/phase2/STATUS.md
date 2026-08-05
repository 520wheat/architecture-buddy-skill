# Phase 2 状态

**更新日期**: 2026-08-05（第二波）  
**状态**: D1–D8 架构样本下限 **全部达标**；模式 P1/P4 已起步；活表 **v0.4**

## 本波新增
| 项 | 文件 |
|----|------|
| D5 LLVM | `architecture/D5-llvm.md` |
| P1 GoF 三族索引 | `patterns/P1-gof-index.md` |
| P4 EIP 核心词汇 | `patterns/P4-eip-core.md` |

## 域进度（退出标准 E1）
| 域 | 要求 | 状态 |
|----|------|------|
| D1–D4 | ≥2 | ✓ |
| D5 | ≥2 | ✓ Git + LLVM |
| D6 | ≥2 | ✓ HSC + Dependency-Track ADR |
| D7 | ≥3 | ✓ |
| D8 | ≥3 | ✓ |

## 模式进度（退出标准 E2）
| Corpus | 状态 |
|--------|------|
| P1 GoF | **索引起步** ✓（深挖可选） |
| P2 POSA | 索引 + 三模式深挖 |
| P3 PoEAA | 三族 |
| P4 EIP | **核心词汇起步** ✓ |
| P5 并发/分布式 | **未开始** ← Phase 3 重点 |
| P9 Agent | ✓ 种子+三家对照 |

## 活表
`living/*` → **v0.4**（机制 K1–K19）

## 距冻结 §3
- E1 架构样本：**已满足书单下限**  
- E2 模式：差 **P5**；建议补一轮 POSA/PoEAA/EIP/GoF 的「够用深挖」后开 Phase 3  
- E3 活表：已有，需 Phase 3 整理定稿  
- E4 回写 §3：待 Phase 3  

## 下一波建议（Phase 3 序章）
1. **P5**：Raft/共识 + POSA Vol.2 或并发模式综述要点  
2. 整理活表 v1.0（去重、定 M1–M8 修订建议）  
3. 回写 `docs/design/03-notes-and-templates.md` 为 Proposed→准备批准  
