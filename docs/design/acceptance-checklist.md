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
