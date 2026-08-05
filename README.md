# architecture-buddy-skill

让经市场验证的架构**思想与做法**成为共思伙伴，帮你做出可检验的架构设计。

## 目录怎么读

```text
skill/                      ← 唯一需要安装的东西
  architecture-buddy/       ← 主持 Skill（@architecture-buddy）
  architecture-buddy-lens-*/← 立场透镜（圆桌按需 @）
docs/                       ← 设计、ADR、调研（开发用，不装进 Cursor）
  adr/                      ← 为什么这样定
  design/                   ← 规格与 catalog
  survey/                   ← 深调研证据（构建期）
scripts/                    ← 静态校验
tools/                      ← 构建期工具说明（女娲等，gitignored 克隆）
```

## 安装（Cursor @ 调用）

把 `skill/` 下各包装到个人 skills 目录（推荐符号链接）：

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="$HOME/.cursor/skills"
mkdir -p "$DST"
for d in "$SRC"/*; do
  name=$(basename "$d")
  ln -sfn "$d" "$DST/$name"
done
```

然后 **Reload Window**，对话里输入 `@architecture-buddy`。

校验：`bash scripts/check-architecture-buddy.sh`

## 约定

- 女娲**仅构建期**蒸馏透镜；运行时不依赖。  
- 第一性原理 = 反类比、拆基本事实、再重推（见 ADR-0018），不是填三列表。  
- 透镜库动态选席（ADR-0017）；蒸馏做法不口吻（ADR-0016）。  
