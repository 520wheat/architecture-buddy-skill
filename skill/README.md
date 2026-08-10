# Architecture Buddy 发行包

`skill/` 是本仓库唯一的运行时发行目录。这里的每个直接子目录都是一个可安装的 Agent Skill 包；本目录中的 Markdown 和 manifest 只是发行索引，不是 Skill 包。

## 安装层级

| 包 | 类型 | 是否必装 | 当前版本 | 用途 |
|---|---|---:|---:|---|
| `architecture-buddy` | 主持 Skill | 是 | `0.5.0` | 主持架构共思、六板块正式架构设计、ADR、圆桌和授权后的调查证据包；内置透镜 |
| `detailed-design` | 后续 Skill | 否 | `0.1.0` | 承接 design-ready 架构交接并产出面向实现的详细设计 |

架构设计完成后，用户可同意将显式 handoff 交给 `detailed-design`。内置透镜默认不主动触发，只由主持 Skill 在圆桌中依据决策点选择；它们提供做法视角，不扮演真人。

## 通用安装

`SRC` 指向本目录，`DST` 指向所使用 Agent 的 Skills 目录。安装时只处理带有 `SKILL.md` 的直接子目录，不会安装 `README.md` 或 manifest。

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

`architecture-buddy/prompts/`、`references/`、`templates/` 和 `scripts/` 是主 Skill 的运行时资源目录，必须随主包安装，不能单独拆出。它们承载分阶段提示词、架构知识、正式产物模板、调查证据工具和确定性校验工具。透镜位于 `architecture-buddy/lenses/*.md`，作为主包内部资源按需加载。

完整机器可读清单见 [`release-manifest.tsv`](release-manifest.tsv)。
