# ADR-0015: 构建期女娲蒸馏第一性原理与透镜包

## Status

**Accepted（2026-08-05）** — 用户选定首批 6 个架构立场，使用女娲**主题 Skill**路径蒸馏（ADR-0016/0017）。

## Context

ADR-0003：女娲仅构建期。ADR-0016：蒸馏思想与做法，不口吻。ADR-0017：透镜库 >3，圆桌动态挑 ≤3。  
P0/P1 已交付主持与 scaffold。P2：用女娲主题蒸馏产出首批透镜。

## Decision

### 调用边界

- 女娲仅构建期；运行时禁止依赖 nuwa。
- 本批采用女娲 **主题 Skill** 变体（非人物角色扮演）：领域共识框架 + 流派/设计分歧；中性专业表达。
- 输出目录：`architecture-buddy-lens-<shortname>/`；须含 `disable-model-invocation: true` 与 §4 契约。

### 首批 6 席（Locked）

| shortname | 主题边界 | 主要本地语料（优先） | 公开锚点 |
|-----------|----------|----------------------|----------|
| `raft-cp` | 可理解多数派共识 / 强一致元数据 | `docs/survey/patterns/P5-*`, `D2-etcd`, `D2-kubernetes` | Raft 论文；etcd；K8s |
| `dynamo-ap` | 高可用、最终一致、去中心化副本 | living 策略表；需补 Dynamo 论文笔记 | Dynamo 论文；DynamoDB；Cassandra 谱系 |
| `log-stream` | 追加日志作集成事实来源 | `D4-kafka`, `D4-pulsar`, `P4-eip*` | Kafka；流式实践 |
| `gfs-mr` | 大规模顺序吞吐：分布式存储 + 数据局部计算 | `D3-hdfs`（GFS 思想落地） | GFS；MapReduce；Hadoop |
| `spanner-sql` | 全球外部一致 + SQL | 调研补强 Spanner 论文/官方概述 | Spanner；全球分布式 SQL |
| `zta-resource` | 零信任：资源级持续裁决 | `D7-nist-800-207`, SAMM/ASVS 笔记 | NIST SP 800-207 |

（未入首批：`bigtable-wide`、`content-dag` — 可后续增量蒸馏。）

### 蒸馏档位

- **标准档主题变体** + **本地语料优先**（survey 已有笔记）；缺口再联网补公开论文/官方架构文。
- 禁止把表达 DNA / 角色扮演写进透镜；女娲模板中的角色扮演段**删除**，改为 Architecture Buddy 透镜契约段。

### 输出与验收

同前：静态脚本通过；每透镜含 best-for / not-for / evidence-anchors 元数据；契约标题齐全；无「我就是某某」。

### 第一性原理

本批**可并行**：若时间盒紧，优先 6 透镜；主持 FP 节保持手写版，后续再女娲加厚（不阻塞本批）。

## Consequences

- Catalog 与主持选席以这 6 个为高可用底库（用户可只装子集）。
- 增量蒸馏新立场另开 shortname，更新 `lens-catalog.md`。

## Related

- ADR-0003, 0014, 0016, 0017  
- `docs/design/lens-catalog.md`  
- 女娲：主题 Skill 变体（`huashu-nuwa` SKILL.md）  
