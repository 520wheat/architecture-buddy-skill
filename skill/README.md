# Architecture Buddy 发行包

`skill/` 是本仓库唯一的运行时发行目录。这里的每个直接子目录都是一个可安装的 Agent Skill 包；本目录中的 Markdown 和 manifest 只是发行索引，不是 Skill 包。

## 安装层级

| 包 | 类型 | 是否必装 | 当前版本 | 用途 |
|---|---|---:|---:|---|
| `architecture-buddy` | 主持 Skill | 是 | `0.3.6` | 主持架构共思、正式架构设计、ADR 和圆桌流程；内置透镜 |
| `detailed-design` | 后续 Skill | 否 | `0.1.0` | 承接 design-ready 架构交接并产出面向实现的详细设计 |

架构设计完成后，用户可同意将显式 handoff 交给 `detailed-design`。内置透镜默认不主动触发，只由主持 Skill 在圆桌中依据决策点选择；它们提供做法视角，不扮演真人。

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

## 包内资源

`architecture-buddy/prompts/`、`references/`、`templates/` 和 `scripts/` 是主 Skill 的运行时资源目录，必须随主包安装，不能单独拆出。它们分别承载分阶段提示词、架构知识、正式产物模板和确定性校验工具。

完整机器可读清单见 [`release-manifest.tsv`](release-manifest.tsv)。
