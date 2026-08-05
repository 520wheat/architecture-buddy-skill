# Architecture Buddy 验收清单

V6 由 `scripts/check-architecture-buddy.sh` 自动检查。

## V1 draft 共思（不交完整设计）
- [ ] 识别为 draft（或未要求完整设计）
- [ ] 真第一性原理：假设 → 事实 → 重推（非结果/约束/优化三表）
- [ ] 不逼用户填不会的分类
- [ ] 不跑 S6，不宣称「架构设计已完成」

## V2 已有方案审阅
- [ ] 审视假设/风险/可替换策略
- [ ] 不擅自定案

## V3 拒绝 Top N
- [ ] 用户拒绝对照后仍能完成 deliverable（B5 写「未对照」）

## V4 圆桌 + 透镜
前置：安装任一 `architecture-buddy-lens-*`
- [ ] 硬分叉时先提议
- [ ] 透镜输出符合契约
- [ ] 用户选择；合成说明冲突

## V5 无透镜降级
- [ ] 未装透镜时词表对照，不假装名人到场

## V6 静态
- [ ] `bash scripts/check-architecture-buddy.sh` → OK

## V7 deliverable 完整交卷（人工）
- [ ] 用户说「做一份架构设计」→ 进入 deliverable
- [ ] 产出单一文件，含层 A（A1–A8）与层 B（B1–B5）
- [ ] 交卷前显式过完成门禁（或列出阻塞/待验证）
- [ ] 正文无 M1–M9 问卷结构；陌生人能讲清解决什么与主路径
- [ ] 全程无「开考/打分/及格」话术

## V8 Phase 1 金标与校准（维护者）
- [ ] corpus/golden/{kafka,git,kubernetes} 四文件齐全
- [ ] 三份 cal runs 判定均为 PASS
- [ ] 用户侧 SKILL 仍无开考/打分话术

## V9 Phase 2 扩库与迁移（维护者）
- [ ] 金标目录 ≥6（原 3 + hdfs/spark/agent-runtime）
- [ ] 迁移校准 mig-sre-buddy 判定 PASS
- [ ] 至少 1 个透镜新建或金标加厚升级
- [ ] 用户侧 SKILL 仍无开考话术

## V10 Phase 3 工具与盲区（维护者）
- [ ] `scripts/rubric-report.sh` 可对 cal 候选生成勾选报告
- [ ] `corpus/COMPAT.md` 记录 skill 0.3.0 与已知 PASS
- [ ] 金标含 etcd、minecraft
- [ ] etcd 复现校准 PASS

## V11 公开内测就绪（评价缺口关闭）
- [ ] 全部 skill `description` 以 `Use when...` 开头（流程细节只在正文）
- [ ] README 含 Cursor 与 Codex 安装路径
- [ ] `bash scripts/pressure-test.sh` → OK（门禁结构负例/正例 + agent-runtime 主题）
- [ ] `agent-runtime` 专用复现校准 PASS（COMPAT 有行）
- [ ] `docs/build/release-readiness.md` 与对外「public beta」定位一致
