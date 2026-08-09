# Architecture Buddy 发行包

`skill/` 是本仓库唯一的运行时发行目录。这里的每个直接子目录都是一个可安装的 Agent Skill 包；本目录中的 Markdown 和 manifest 只是发行索引，不是 Skill 包。

## 安装层级

| 包 | 类型 | 是否必装 | 当前版本 | 用途 |
|---|---|---:|---:|---|
| `architecture-buddy` | 主持 Skill | 是 | `0.5.0` | 主持架构共思、六板块正式架构设计、ADR、圆桌和授权后的调查证据包 |
| `architecture-buddy-lens-scaffold` | 通用透镜 | 否 | `0.1.0` | 没有领域透镜时提供通用取舍视角 |
| `architecture-buddy-lens-agent-loop` | 领域透镜 | 否 | `0.1.0` | Agent loop、工具编排、HITL 和轨迹 |
| `architecture-buddy-lens-dynamo-ap` | 领域透镜 | 否 | `0.1.0` | AP、副本、分区和冲突修复 |
| `architecture-buddy-lens-gfs-mr` | 领域透镜 | 否 | `0.2.0` | GFS/HDFS、批处理、数据局部性和 MapReduce |
| `architecture-buddy-lens-log-stream` | 领域透镜 | 否 | `0.1.0` | Kafka/Pulsar、日志流、回放和消费者进度 |
| `architecture-buddy-lens-raft-cp` | 领域透镜 | 否 | `0.1.0` | Raft、共识、控制面和防脑裂 |
| `architecture-buddy-lens-spanner-sql` | 领域透镜 | 否 | `0.1.0` | 全球 SQL、外部一致性和多区域事务 |
| `architecture-buddy-lens-zta-resource` | 安全透镜 | 否 | `0.1.0` | 零信任、资源访问、策略执行和信任边界 |

推荐安装主包和全部可选透镜。透镜默认不主动触发，只由主持 Skill 在圆桌中依据决策点选择；它们提供做法视角，不扮演真人。

## 通用安装

`SRC` 指向本目录，`DST` 指向你所使用 Agent 的 Skills 目录。安装时只处理带有 `SKILL.md` 的直接子目录，不会安装 `README.md` 或 manifest。

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="/path/to/your/agent/skills"
mkdir -p "$DST"
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  ln -sfn "$d" "$DST/$name"
done
```

如果运行时不支持符号链接，可以把这些 Skill 子目录复制到 `DST`；安装后按所用 Agent 的文档重新加载 Skill。

## 包内资源

`architecture-buddy/prompts/`、`references/`、`templates/` 和 `scripts/` 是主 Skill 的运行时资源目录，必须随主包安装，不能单独拆出。它们分别承载分阶段提示词、架构知识、正式产物模板和确定性校验工具。

完整机器可读清单见 [`release-manifest.tsv`](release-manifest.tsv)。
