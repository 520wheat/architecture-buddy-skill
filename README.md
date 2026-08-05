# architecture-buddy-skill

让经市场验证的架构**思想与做法**成为共思伙伴，帮你做出可检验的架构设计。

**定位：** 开源/共享向的开发仓库（运行时包 + 训练素材）。可安装物只在 `skill/`；`corpus/` 与 `docs/` 是维护者训练与设计证据，不是 Cursor/Codex 运行时依赖。

当前成熟度：适合个人与团队内测；公开稳定版发布前见 `docs/build/release-readiness.md`。

## 目录怎么读

```text
skill/                      ← 唯一需要安装的东西（运行时）
  architecture-buddy/       ← 主持 Skill
  architecture-buddy-lens-*/← 立场透镜（圆桌按需）
corpus/                     ← 金标与校准（训练用，勿装进 skills）
docs/                       ← 设计、ADR、调研、发布就绪清单
scripts/                    ← 静态校验与压力测试
tools/                      ← 构建期工具说明（女娲等）
```

## 安装

把 `skill/` 下各包装到对应 Agent 的 skills 目录（推荐符号链接），**不要**链接整个仓库或 `corpus/`。

### Cursor

```bash
SRC="/path/to/architecture-buddy-skill/skill"
DST="$HOME/.cursor/skills"
mkdir -p "$DST"
for d in "$SRC"/*; do
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
for d in "$SRC"/*; do
  name=$(basename "$d")
  ln -sfn "$d" "$DST/$name"
done
```

若你的 Codex / Cursor 已统一读 `~/.agents/skills` 或其它目录，把 `DST` 改成该路径即可；**原则不变：只链 `skill/*`**。

生效方式：新开会话后，用自然语言说明场景（例如「一起做一份架构设计」），或按产品文档用 skill 调用语法点名 `architecture-buddy`。透镜默认 `disable-model-invocation: true`，由主持 Skill 在圆桌时按需加载。

## 校验

```bash
bash scripts/check-architecture-buddy.sh
bash scripts/pressure-test.sh
```

维护者校准流程见 `docs/build/skill-calibration.md`。

## 约定

- 女娲**仅构建期**蒸馏透镜；运行时不依赖。  
- 第一性原理 = 反类比、拆基本事实、再重推（ADR-0018），不是填三列表。  
- 透镜库动态选席（ADR-0017）；蒸馏做法不口吻（ADR-0016）。  
- 用户对话禁止开考/打分；复现校准只给维护者（ADR-0019）。  
