# Architecture Buddy 发行包

`skill/` 是本仓库唯一的运行时发行目录。这里的每个直接子目录都是一个可安装的 Agent Skill 包；本目录中的 Markdown 和 manifest 只是发行索引，不是 Skill 包。

## 安装层级

| 包 | 类型 | 是否必装 | 当前版本 | 用途 |
|---|---|---:|---:|---|
| `architecture-buddy` | 主持 Skill | 是 | `0.3.6` | 主持架构共思、正式架构设计、ADR 和圆桌流程 |
| `architecture-buddy-lens-scaffold` | 通用透镜 | 否 | `0.1.0` | 没有领域透镜时提供通用取舍视角 |
| `architecture-buddy-lens-agent-loop` | 领域透镜 | 否 | `0.1.0` | Agent loop、工具编排、HITL 和轨迹 |
| `architecture-buddy-lens-dynamo-ap` | 领域透镜 | 否 | `0.1.0` | AP、副本、分区和冲突修复 |
| `architecture-buddy-lens-gfs-mr` | 领域透镜 | 否 | `0.2.0` | GFS/HDFS、批处理、数据局部性和 MapReduce |
| `architecture-buddy-lens-log-stream` | 领域透镜 | 否 | `0.1.0` | Kafka/Pulsar、日志流、回放和消费者进度 |
| `architecture-buddy-lens-raft-cp` | 领域透镜 | 否 | `0.1.0` | Raft、共识、控制面和防脑裂 |
| `architecture-buddy-lens-spanner-sql` | 领域透镜 | 否 | `0.1.0` | 全球 SQL、外部一致性和多区域事务 |
| `architecture-buddy-lens-zta-resource` | 安全透镜 | 否 | `0.1.0` | 零信任、资源访问、策略执行和信任边界 |

推荐安装主包和全部可选透镜；透镜默认不主动触发，只由主持 Skill 在圆桌中按问题选择。

## 安装

`SRC` 必须指向本目录。安装脚本只遍历带有 `SKILL.md` 的直接子目录，不会安装 `README.md` 或 manifest。

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="$HOME/.cursor/skills"
mkdir -p "$DST"
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  ln -sfn "$d" "$DST/$name"
done
```

安装 Codex 或其他兼容 Agent Skills 的运行时，只需将 `DST` 换成对应的用户级 skills 目录。

## 不属于发行包的内容

- `corpus/`：训练集、held-out 集、候选和评估结果。
- `docs/`：ADR、设计规范、训练计划和发布证据。
- `scripts/`：维护者校验、生成、盲评和比较工具。
- `tools/`：构建期工具说明。
- `architecture-buddy/references/` 与 `architecture-buddy/templates/`：主 Skill 包内部资源，必须随主包安装，不能单独安装。

完整机器可读清单见 [`release-manifest.tsv`](release-manifest.tsv)。
