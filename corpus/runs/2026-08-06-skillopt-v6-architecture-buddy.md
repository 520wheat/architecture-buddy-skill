# SkillOpt v6 与 Architecture Buddy 0.3.6 训练记录

## 范围

- 目标 skill：`skill/architecture-buddy/SKILL.md`，版本 `0.3.6`
- 领域：Git、Kubernetes、Minecraft、HDFS、Kafka、etcd、Agent Runtime
- 任务集：`2026-08-06-skillopt-architecture-tasks-v6.json`
- 后端：真实 Codex CLI；未使用 mock 作为质量结论
- 自动采纳：关闭

## 完整多领域 baseline

真实运行 staging：`.skillopt-sleep/staging/20260806-105004/`

- 任务集：24 个任务，`train=4`、`val=10`、`test=10`
- baseline validation hard：`0.1`
- baseline validation soft：`0.6724184149184149`
- baseline 已完成；主要失败是正式标题缺失、架构定位字段未显式写出，以及圆桌步骤和透镜契约没有稳定落盘。
- 多领域正式架构任务被保留为 held-out，未把关键词命中当作质量结论。

## 0.3.6 受控复测

受控子集包含正式交付、圆桌、Git、Kubernetes、Minecraft，`train=2`、`val=2`、`test=3`。

真实运行 staging：`.skillopt-sleep/staging/20260806-111227/`

- baseline hard：`0.0`
- baseline soft：`0.5615384615384615`
- Git 圆桌响应语义上写出了“高影响互斥分叉与提议”“提议召开圆桌”“用户同意圆桌”，但旧 judge 只接受连续字面串“提议圆桌”，暴露评分器过度依赖关键词的问题。
- 架构定位任务在事实不足时正确请求补充信息，但旧任务要求它输出完整定位字段；该 oracle 与“不凭空补事实”的 skill 规则冲突，列为评分器待修订项。

## SkillOpt candidate 结果

两次真实候选阶段均停在 Codex 子进程调用，没有产生 `candidate` 或 `gate` 证据：

- 完整 v6：staging `20260806-105004/`，阻塞在 `skillopt_sleep/backend.py` 的 `subprocess.run(...).communicate()`。
- 受控复测：staging `20260806-111227/`，同样阻塞在训练 replay 的 Codex 子进程。

因此本轮**没有 SkillOpt candidate 分数，没有显著提升结论，也没有自动采纳**。这是真实后端限制，不包装为训练成功。

## 人工受控修订

基于 baseline 的重复缺陷，`0.3.6` 增加：

1. 正式 `deliverable` 的字面 `A1–A8/B1–B6` 标题契约。
2. 圆桌固定顺序：分叉与提议、用户同意/跳过、席位理由、完整透镜契约、主持人综合、回写 A/B。
3. 圆桌固定证据标签，且未获同意时必须停止加载透镜。
4. 评分任务允许“提议召开圆桌”等自然语言变体，并允许 `##` 到 `######` 的 Lens 标题层级；不再把同义表达误判为失败。

## 质量证据

Git 正式架构设计：`corpus/runs/2026-08-06-git-architecture-design-final.md`

- hard gate：`PASS`
- structure：`20/20`
- semantic：`95/100`
- domain：`100/100`
- roundtable：`20/20`
- human review：`PASS`
- conclusion：`EXCELLENT`

该结论来自人工阅读、领域事实检查和反关键词命中复核，不是 SkillOpt candidate 分数。
