# Architecture Buddy 验收清单

对照 spec §9。V6 由 `scripts/check-architecture-buddy.sh` 自动检查。

## V1 模式 A（只装主持）
- [ ] 识别为 A 并确认
- [ ] 共抽结果/约束/优化变量
- [ ] 问 Top N
- [ ] 产出笔记可映射 M1–M9

## V2 模式 B
- [ ] 识别为 B
- [ ] 审视假设/风险/可替换策略
- [ ] 不擅自定案

## V3 拒绝 Top N
- [ ] 用户说不做 Top N 后仍能完成笔记

## V4 圆桌 + 透镜
前置：安装 `architecture-buddy-lens-scaffold`
- [ ] 硬分叉时先提议
- [ ] 两透镜输出符合契约
- [ ] 合成表含冲突；用户选择

## V5 无透镜降级
- [ ] 未装透镜时降级到词表对照，不假装名人到场

## V6 静态
- [ ] `bash scripts/check-architecture-buddy.sh` → OK
