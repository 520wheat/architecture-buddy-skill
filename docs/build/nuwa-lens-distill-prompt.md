# 女娲主题蒸馏 → Architecture Buddy 透镜（构建说明）

## 方法

遵循 `tools/nuwa-skill/SKILL.md` 的 **主题 Skill** 变体 + `references/extraction-framework.md` 三重验证。  
**不**使用人物角色扮演模板；输出适配 Architecture Buddy（ADR-0016）。

## 每个透镜必须产出

路径：`architecture-buddy-lens-<shortname>/SKILL.md`

```yaml
---
name: architecture-buddy-lens-<shortname>
description: <≤1024 chars; stance + when to use; say Architecture Buddy roundtable>
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (<Title>)
  version: "0.1.0"
  stance: <一句话>
  best-for: <逗号分隔或短句>
  not-for: <短句>
  evidence-anchors: <系统/论文>
---
```

正文结构：

1. 标题与立场声明（启发式透镜，非真人）  
2. 选席元数据复述（best-for / not-for / evidence）  
3. **框架概览**：3–7 个心智模型（各含：一句话、证据≥2、应用、局限）——须过三重验证  
4. **决策启发式** 5–10 条（做法级）  
5. **流派/设计分歧**（主题内张力，非人物八卦）  
6. **Would not do / 反模式**  
7. **诚实边界**  
8. **圆桌输出契约**（fenced ```text 含 On the decision point 等）  
9. **附录：调研来源**（本地 survey 路径 + URL）  

禁止：表达 DNA、角色扮演、「我就是某某」、运行时女娲。

可选：`references/research-notes.md` 短调研笔记。
