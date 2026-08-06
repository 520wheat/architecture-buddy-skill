# Architecture Buddy SkillOpt 多轮训练报告

## 结论

本次训练达到“显著提升”标准：最新 v3 held-out validation 从 `0.71875` 提升到 `1.000`，绝对提升 `0.28125`，gate 为 `accept_new_best`。独立 Git 压力测试也从 `0.4375`/`0.46875` 提升到 `1.000`，未出现 test 下降。

训练使用真实 Codex backend，不是 mock；所有训练均在隔离的 `claude-home` 下运行。当前 live skill 未自动 adopt，源码和已安装版本保持不变。

## 训练轮次

| 轮次 | 任务集 | baseline | candidate | gate | 接受编辑 |
|---|---|---:|---:|---|---:|
| 1 | architecture tasks v1 | 0.400 | 1.000 | accept_new_best | memory 2 |
| 2 | architecture tasks v2 | 1.000 | 1.000 | reject | 0 |
| 3 | architecture tasks v3 | 0.71875 | 1.000 | accept_new_best | skill 2 |

第 2 轮没有提升，因此没有把重复规则作为改进；第 3 轮改用更严格的双层交付、圆桌证据链、第一性原理、组合边界和 Git 准确性任务后，取得了有效提升。

## 第 3 轮采用候选

SkillOpt 接受了两条 skill 正文候选，均只写入 staging：

1. `deliverable` 必须直接输出双层架构设计正文，按 `A1`–`A8`、`B1`–`B6` 保持完整结构，未过 S6 不得宣称完成。
2. 主策略前必须明确记录高影响互斥分叉；圆桌拒绝和无匹配透镜时使用固定的降级记录和轻量策略/反模式对照。

SkillOpt 拒绝了 3 条重复 memory 编辑。未执行 `adopt`，因此上述内容只存在于：

`/Users/apple/Desktop/skill-create/.skillopt-sleep/staging/20260805-190004/proposed_SKILL.md`

## Git 独立测试

Git test 要求输出正式双层架构，并覆盖工作树、index、对象库、refs、DAG、pack、plumbing/porcelain、离线 commit、push/fetch、失败和验收，同时加入两个负向邻近约束，防止把 Git 误写成 Kafka 核心或所有仓库共享的 Raft 系统。

- live skill target：`0.4375 -> 1.000`
- staged candidate target：`0.46875 -> 1.000`
- backend：真实 Codex
- task：`corpus/runs/2026-08-05-skillopt-git-test.json`

这两个独立 run 的 candidate 分数是 SkillOpt 在该 run 中经过 gate 的候选分数，不代表已经自动合并到 live skill；它们证明候选流程能满足 Git test judge。

## 验证

- `bash scripts/check-architecture-buddy.sh`：通过
- `bash scripts/pressure-test.sh`：通过
- 8 个 architecture lens 检查：通过
- 8 个 golden corpus 检查：通过
- 4 个任务 JSON：通过
- `git diff --check`：通过
- source 与 `/Users/apple/.codex/skills/architecture-buddy/SKILL.md`：一致
- live `skill/architecture-buddy/SKILL.md`：未被训练修改

原始 SkillOpt staging report：

`/Users/apple/Desktop/skill-create/.skillopt-sleep/staging/20260805-190004/report.md`
