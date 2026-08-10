# architecture-buddy-skill

Architecture Buddy 是一个用于架构共思的 Agent Skill：帮助开发者在编码前澄清问题类、约束、边界、机制、策略和取舍，并产出一份可检验的正式架构设计。它可以在高影响的架构分叉上提议圆桌，按问题动态加载领域透镜，再把讨论结果写回设计和 ADR。

当前发行版本：`0.3.6`。当前定位：**public beta / 团队内测**。它已经具备可安装的运行时包，但尚未宣称稳定版 API。

本仓库只包含运行时发行包和必要的安装说明。安装时直接使用 `skill/`。

## 目录怎么读

```text
skill/                      ← 唯一需要安装的东西（运行时），见 skill/README.md
  architecture-buddy/       ← 必装的架构主持 Skill，内置圆桌透镜
  detailed-design/           ← 可选的详细设计 Skill
  README.md                 ← 发行说明，不是 Skill
  release-manifest.tsv      ← 发行清单，不是 Skill
```

## 安装

先获取仓库：

```bash
git clone https://github.com/520wheat/architecture-buddy-skill.git
cd architecture-buddy-skill
```

把 `skill/` 下各包装到对应 Agent 的 skills 目录（推荐符号链接）。

### Cursor

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="$HOME/.cursor/skills"
mkdir -p "$DST"
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name=$(basename "$d")
  ln -sfn "$d" "$DST/$name"
done
```

然后 **Reload Window**，对话里 `@architecture-buddy`（或自然语言触发）。

### Codex（及兼容 Agent Skills 的 CLI）

Codex 通常从用户级 skills 目录发现 Skill（常见路径之一）：

```bash
SRC="/path/to/architecture-buddy-skill/skill"
# 优先使用你本机 Codex 文档中的 skills 目录；若已有 ~/.codex/skills，可装到此处：
DST="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$DST"
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name=$(basename "$d")
  ln -sfn "$d" "$DST/$name"
done
```

若你的 Codex / Cursor 已统一读 `~/.agents/skills` 或其它目录，把 `DST` 改成该路径即可；**原则不变：只链 `skill/*`**。

生效方式：新开会话后，用自然语言说明场景（例如「一起做一份架构设计」），或按产品文档用 skill 调用语法点名 `architecture-buddy` / `detailed-design`。内置透镜由主持 Skill 在圆桌时按需加载，不单独安装。

## 发行内容

必须安装的包是 `architecture-buddy`；`detailed-design` 在架构交接后按需安装或调用。机器可读清单见 [`skill/release-manifest.tsv`](skill/release-manifest.tsv)，包级说明见 [`skill/README.md`](skill/README.md)。

## 能力边界

Architecture Buddy 负责架构问题澄清、架构决策协作、圆桌和正式架构设计；详细设计、系统架构落地、空骨架代码和 PR Review 属于后续能力。透镜提供经过蒸馏的实践视角，不扮演名人，也不替用户拍板。
