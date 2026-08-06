# Architecture Quality Scorer Calibration Design

## Goal

校准 `architecture-quality-report.sh`，使它回答两个不同问题：

1. 交付物是否具备可检查的结构和最低证据；
2. 交付物是否可能是一份优秀架构设计。

自动工具只负责结构门禁和可解释的缺陷信号，不把关键词命中当成语义质量或“优秀”。本轮不修改 `SKILL.md`，不采纳 SkillOpt staging 候选，不引入外部依赖或 LLM judge。

## Scope and Non-goals

范围包括：

- Markdown 标题识别和章节正文提取；
- A1–A8、B1–B6 和 B6 证据门禁；
- 五类语义反例的自动分类；
- 评分报告字段与人工复核工作表；
- pressure tests、Git 正例和 held-out 回归记录。

不包括：

- 修改 Architecture Buddy 的行为规则；
- 自动生成或自动填写五维语义分；
- 用 LLM 替代人工架构评审；
- 将领域正确性分、圆桌过程分合并为正文质量分；
- 删除或重写用户已有的 golden corpus。

## Design

### 1. Section Parser

评分器按标题标识识别章节，而不是固定要求 `###`。接受 `## A1`、`### A1` 等合法 Markdown 标题；只把标题行开头的完整标识当作章节，不把正文中的 `A1` 或表格单元格误认为章节。

章节正文从目标标题之后开始，到下一个同级或更高层级标题结束。没有正文的标题仍被识别为存在，但会产生空章节信号；这保证“有 B6 标题但没有证据”不会被结构门禁误判为完整。

### 2. Automated Gates and Signals

自动结果分为 hard gate 和 diagnostic flags。

hard gate 在下列情况拒绝：

- A1–A8 或 B1–B6 缺失；
- B6 缺少具体的变化轴、N+1、反例、可组合能力或复杂度证据；
- 文档只有会议记录或只有模块清单，无法作为陌生读者可用的架构设计；
- 主结论存在，但没有任何事实、依据、代价、风险、质量属性或验收连接。

diagnostic flags 使用稳定 ID：

- `structure-incomplete`
- `b6-evidence-insufficient`
- `module-list-only`
- `meeting-record-only`
- `roundtable-synthesis-missing`
- `evidence-and-cost-debt`

关键词只能触发待审信号，不能单独使候选通过，也不能单独赋予语义分。

### 3. Independent Score Fields

报告固定输出并分开维护：

- `structure_score`：自动结构和最低证据结果；
- `semantic_quality_score`：人工填写，五维 `0–4` 换算为 `0–100`；
- `domain_score`：依据领域 golden rubric 单独填写；
- `roundtable_score`：圆桌过程单独填写，或标记 `not-needed`；
- `human_review`：`PENDING`、`PASS` 或 `FAIL`。

五个语义维度保持现有 rubric：问题类与边界、机制与策略分离、失败/安全/恢复、演进/N+1/反例、证据/决策理由/质量属性。

结论规则：

- hard gate 失败：`REJECT`；
- hard gate 通过但总分低于 80 或任一维度低于 2：`RETRY`；
- 总分 80–89 且人工复核通过：`PASS`；
- 总分至少 90、五维均至少 3、领域与反关键词复核通过：`EXCELLENT`。

自动脚本不得输出 `PASS` 或 `EXCELLENT` 作为语义结论，只能生成待填写工作表。

### 4. Calibration Corpus

回归夹具保留并明确期望分类：

- 模块清单：`REJECT` / `module-list-only`；
- 会议记录：`REJECT` / `meeting-record-only`；
- 空 B6：`REJECT` / `b6-evidence-insufficient`；
- 有圆桌无综合结论：保留结构，标记 `roundtable-synthesis-missing`；
- 有结论无证据：`REJECT` / `evidence-and-cost-debt`；
- Git 双层架构正例：通过自动门禁，但语义与领域分数必须人工填写；
- Kafka、etcd、Agent Runtime：用于跨领域回归，禁止仅按篇幅或关键词判优。

正例和反例都要测试“同义表达”和“标题层级变化”，避免评分器只适配某一份 fixture 的原文。

### 5. Verification

实现前先为标题层级兼容、空 B6、五类反例和报告字段增加失败测试。实现后依次运行：

```text
bash scripts/pressure-test.sh
bash scripts/check-architecture-buddy.sh
bash -n scripts/architecture-quality-report.sh scripts/pressure-test.sh scripts/check-architecture-buddy.sh scripts/rubric-report.sh
git diff --check
```

再对 Git、Kafka、etcd、Agent Runtime 的现有记录生成质量工作表，检查自动信号是否与人工 rubric 的缺陷一致。校准成功的标准是：反例均不被判为优秀，合法标题层级不再造成误报，且自动报告不输出未经人工审阅的语义满分。

## Error Handling and Compatibility

- 输入不存在或无法读取时保持当前非零退出行为；
- 章节解析失败时宁可报告缺失，不猜测正文结构；
- 保留现有报告字段，新增字段不得破坏已有 pressure tests；
- 不修改现有 golden corpus 内容，只增加必要的期望分类或测试夹具；
- Bash 版本保持项目当前兼容范围，优先使用标准工具。

## Open Risks

- 纯 shell 的 Markdown 解析无法覆盖所有 Markdown 方言；本轮只承诺常见 ATX 标题格式。
- “只有会议记录”和“附带圆桌过程的正式设计”存在边界，需要用结构和正文判断组合，而不能只查 `圆桌` 关键词。
- 自动缺陷检测只能发现可解释的表面缺口，不能证明技术方案正确；领域和语义分仍需人工复核。
