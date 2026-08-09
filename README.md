# architecture-buddy-skill

Architecture Buddy 是一个用于架构共思的 Agent Skill：帮助开发者在编码前澄清问题类、约束、边界、机制、策略和取舍，并产出一份可检验的正式架构设计。它可以在高影响的架构分叉上提议圆桌，按问题动态加载领域透镜，再把讨论结果写回设计和 ADR。

当前发行版本：`0.4.1`。当前定位：**public beta / 团队内测**。它已经具备可安装的运行时包，但尚未宣称稳定版 API。

本仓库只包含运行时发行包和必要的安装说明。安装时直接使用 `skill/`。

## 快速示例

### 开发前设计

```text
使用 $architecture-buddy，在开发前和我共同设计一个文件同步系统。先确认问题类、基本事实和约束；如果出现会改变一致性或失败语义的分叉，提议圆桌；最后输出正式架构设计、ADR 和简短决策过程记录。
```

### 已有项目分析

```text
使用 $architecture-buddy，以 reference/retrospective 模式分析这个仓库。已有代码只作为只读事实，输出一份面向“项目开始前”的架构设计评估，不把目录清单或当前实现直接冒充架构设计。
```

### 授权后联网调查

```text
先和我确认问题类和需要验证的单一架构决策问题；不要默认联网。得到我的明确授权后，再用指定的官方文档或论文生成可追溯证据包，并将已确认的机制、适用条件、代价和反例回写到 ADR 与正式架构设计。
```

示例中的 `$architecture-buddy` 是显式调用方式；也可以直接描述架构设计场景，让兼容 Agent 根据 Skill 描述自动发现它。

## 发行说明

### 0.4.1

- 补齐 Agent UI 元数据和默认调用提示词。
- 增加开发前设计、已有项目分析和授权后联网调查示例。
- 统一发行版本、包清单和用户可见说明。

### 0.4.0

- 增加用户授权后的联网调查与证据包能力。
- 增加来源 provenance、原始/清洗材料、失败记录和证据完整性校验。
- 支持 HTML、纯文本、Markdown、JSON、SRT/VTT 来源。

## 目录怎么读

```text
skill/                      ← 唯一需要安装的东西（运行时），见 skill/README.md
  architecture-buddy/       ← 必装的主持 Skill
  architecture-buddy-lens-*/← 可选的圆桌立场透镜
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

生效方式：新开会话后，用自然语言说明场景（例如「一起做一份架构设计」），或按产品文档用 skill 调用语法点名 `architecture-buddy`。透镜默认 `disable-model-invocation: true`，由主持 Skill 在圆桌时按需加载。

## 发行内容

必须安装的包是 `architecture-buddy`；`architecture-buddy-lens-*` 是可选圆桌透镜，建议在需要对应领域时一并安装。机器可读清单见 [`skill/release-manifest.tsv`](skill/release-manifest.tsv)，包级说明见 [`skill/README.md`](skill/README.md)。

## 能力边界

Architecture Buddy 负责架构问题澄清、架构决策协作、圆桌和正式架构设计；详细设计、系统架构落地、空骨架代码和 PR Review 属于后续能力。透镜提供经过蒸馏的实践视角，不扮演名人，也不替用户拍板。
