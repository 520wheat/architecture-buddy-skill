# architecture-buddy-skill

Architecture Buddy 是一个用于架构共思的 Agent Skill：帮助开发者在编码前澄清问题类、约束、边界、机制、策略和取舍，并产出一份可检验的正式架构设计。它可以在高影响的架构分叉上提议圆桌，按问题动态加载领域透镜，再把讨论结果写回设计和 ADR。

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

## 目录怎么读

```text
skill/                      ← 唯一需要安装的东西（运行时），见 skill/README.md
  architecture-buddy/       ← 必装的主持 Skill
  architecture-buddy-lens-*/← 可选的圆桌立场透镜
  README.md                 ← 发行包索引，不是 Skill
  release-manifest.tsv      ← 包清单，不是 Skill
```

## 通用安装

先获取仓库：

```bash
git clone https://github.com/520wheat/architecture-buddy-skill.git
cd architecture-buddy-skill
```

将 `skill/` 下包含 `SKILL.md` 的直接子目录复制或链接到你的 Agent Skills 目录，然后按该 Agent 的方式重新加载 Skill。

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="/path/to/your/agent/skills"
mkdir -p "$DST"
for d in "$SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name=$(basename "$d")
  ln -sfn "$d" "$DST/$name"
done
```

只安装主 Skill 时选择 `skill/architecture-buddy`；需要圆桌领域视角时，再安装相应的 `architecture-buddy-lens-*` 子目录。生效方式和显式调用语法以所用 Agent 的 Skill 文档为准。

## 包内容

必须安装的包是 `architecture-buddy`；
`architecture-buddy-lens-*` 是可选圆桌透镜，建议在需要对应领域时一并安装。
包清单见 [`skill/release-manifest.tsv`](skill/release-manifest.tsv)，包级说明见 [`skill/README.md`](skill/README.md)。

## 能力边界

Architecture Buddy 负责架构问题澄清、架构决策协作、圆桌和正式架构设计；详细设计、系统架构落地、空骨架代码和 PR Review 属于后续能力。透镜提供经过蒸馏的实践视角，不扮演名人，也不替用户拍板。
