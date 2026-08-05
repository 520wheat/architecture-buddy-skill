# Django Design Philosophies
- 域: D6 应用与平台架构
- 来源: https://docs.djangoproject.com/en/stable/misc/design-philosophies/
- 阶段: Phase 4 加深 · 2026-08-05

## 问题类
为 Web 应用框架定义**可演进的设计原则**：层间松耦合、少样板、快速开发，同时避免「魔法」侵蚀可理解性。

## 硬约束 / 原则（机制侧）
1. **Loose coupling + tight cohesion**：层互不知晓除非必要（模板不知请求；DB 层不知展示；视图不绑定特定模板引擎）
2. **Less code / DRY**：概念与数据只活一处；框架从少量声明推导更多行为
3. **Explicit > implicit**（PEP 20）：魔法仅在巨大便利且不误导学习者时使用
4. **Consistency**：从代码风格到使用体验一致
5. **Quick development**：框架存在是为消减繁琐，而非展示抽象纯度

## 策略（子系统分叉）
| 子系统 | 策略取向 | 负面/边界 |
|--------|----------|-----------|
| Models | Active Record 气质：域逻辑进模型 | 复杂域可能需另层；与 PoEAA Domain Model/Data Mapper 对照 |
| DB API | 显式 `save()`；`select_related` 可选加速；可随时降到 raw SQL | 效率靠开发者配合，非全隐式 ORM |
| URL | 与 Python 名解耦；无限灵活；鼓励漂亮 URL / APPEND_SLASH 规范化 | URL 设计成一等架构决策 |
| Templates | 表现与逻辑分离；继承消冗余；不发明完整语言；默认禁恶意代码 | 复杂表现逻辑需自定义 tag，而非模板里写业务 |
| Views | 函数即可；显式 request；区分 GET/POST | 简单优先于强制类视图 |
| Cache | 最少代码路径（尤其 get）；后端一致接口；可扩展 | 速度目标约束实现厚度 |

## 显式模式名
- Active Record（文档直接引用 Fowler）
- DRY / Loose Coupling / Explicit over Implicit
- Template Inheritance（表现层策略）

## 决策与负面后果
- 「全栈便利」与「层可替换」张力：默认一体，但设计目标是可拆
- 模板「不要编程语言」限制表达力，换来安全与角色分工（设计师可编辑）

## 对写作规范的启示
- 框架/平台架构文可用**哲学清单**承载机制，再用子系统表承载策略——对齐 M5
- 「Explicit vs Magic」应写入 M3 假设或 M7 风险（可理解性 vs 便利）
- 与 HSC/DT：同属 D6，Django 偏原则驱动，HSC/DT 偏决策链与反过度中间件
