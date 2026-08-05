# Design §5：Skill 包布局与构建期流水线

## Status

**Approved（2026-08-05）** — 依据 ADR-0003/0005/0007。
## 运行时交付物（用户安装）

```text
architecture-buddy/              # ADR-0014 normalized package path
  SKILL.md                 # 主持：身份、流程 A/B/C、M1–M9、Top N、圆桌主持
  references/              # 可选：从 survey 活表提炼的短参考（非全书复制）
    mechanisms.md          # M1–M9 + 关键 K*
    strategies-cheatsheet.md
    anti-patterns.md
  templates/               # 可选：架构笔记空白骨架（§3）
    architecture-note.md
```

架构师视角（构建期另产，运行时独立安装）：

```text
architecture-buddy-lens-<shortname>/
  SKILL.md                 # 透镜契约（§4 输出格式）+ 启发式正文
```

v1 **不要求**用户安装任何 Lens；仅主持即可共思。

## 构建期流水线（开发者侧，非运行时）

```text
docs/survey/living/* + 选定人物/语料
        │
        ▼
  nuwa-skill（构建期）
        │
        ├─► 蒸馏「第一性原理共抽问题」→ 合并进 architecture-buddy/SKILL.md
        └─► 蒸馏 2–3 架构师 → 各 Lens skill 包
```

规则：

- 女娲**不**出现在用户运行时依赖
- 调研全文留在 `docs/survey/`；打进 skill 的是**压缩参考**，控制体积
- 蒸馏名单与语料来源记 ADR（构建期再开），本 § 不锁人名

## SKILL.md 内容分区（主持）

1. 身份与非目标（伙伴；不替拍板）  
2. 入口 A/B/C 与主流程（§2）  
3. 第一性原理共抽（蒸馏段）  
4. 笔记锚点 M1–M9（§3）  
5. Top N 问询规则  
6. 圆桌主持 + 调用 Lens 的方式（§4）  
7. 何时提议模板沉淀  

## 与调研资产的关系

| 资产 | 用途 |
|------|------|
| `docs/survey/**` | 构建期学习与回归；可复查证据 |
| `references/*` | 运行时快速对照 |
| 活表版本 | 升版时决定是否 bump skill references |

## 验收（实现阶段用）

- 只装主持 Skill：能完成 A/B 共思并产出含 M1–M9 的笔记骨架  
- 硬分叉时会提议圆桌；无 Lens 时降级为模式词表对照  
- 包内无 nuwa 运行时调用、无密钥  

## 非目标（v1）

- 不做独立 Web 产品或向量知识库服务  
- 不自动从网上下载书单全文  

## 相关

- ADR-0003、0005、0007  
- ADR-0014（skill 包命名规范化）  
- Design §1–§4  
