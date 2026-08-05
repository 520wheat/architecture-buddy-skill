# OWASP SAMM — Secure Architecture Practice
- 域: D7 安全架构
- 来源: https://owaspsamm.org/model/design/secure-architecture/
- 阶段: Phase 1 · 2026-08-04

## 问题类
如何在组织的软件设计过程中**系统性地纳入安全架构能力**（不仅是单个系统的一次设计）。

## 硬约束
- 面向成熟度阶梯（M1→M3），可评估可改进
- 同时覆盖「架构设计」与「技术栈治理」两条流

## 机制（共性）
1. **安全原则进入设计过程**（培训 → 模式库 → 参考架构管控）
2. **技术与组件的风险管理**（识别 → 标准化 → 强制）
3. 安全解法沉淀为**可复用模式与参考架构**（与本项目「类问题模板」同构）

## 策略（差异/选项）— 成熟度即策略厚度
| 级 | Architecture Design | Technology Management |
|----|---------------------|------------------------|
| M1 | 培训基本安全原则 | 梳理技术识别风险 |
| M2 | 建立通用安全设计模式/解法 | 标准化技术与框架 |
| M3 | 参考架构采用并持续评估 | 强制标准技术 |

## 显式模式名
- Secure design patterns / Reference architectures（SAMM 用语）
- Secure-by-default

## 对写作规范的启示
- 「组织如何保证架构含安全」本身是一类问题——Buddy 面对企业场景时应问 SAMM 式问题
- 参考架构的治理 = 类问题模板的组织版
