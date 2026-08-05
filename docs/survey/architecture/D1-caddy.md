# Caddy — Architecture
- 域: D1 Web / 边缘与接入
- 来源: https://caddyserver.com/docs/architecture
- 阶段: Phase 1 · 2026-08-05

## 问题类
提供**少活动部件、易部署、可扩展**的 Web 服务器/边缘平台：静态单二进制 + 模块化能力扩展，在线热更新配置且尽量不中断服务。

## 硬约束
- Go 静态单二进制、零外部动态依赖（愿景级）
- CLI 只做引导，不作完整配置面
- 配置变更需高并发下安全、一致

## 机制（共性）
1. **Command / Core / Modules** 三分：引导、配置生命周期、能力实现
2. **配置即 JSON 文档**；core 原生懂 admin/logging，其余经 apps 接口 `Start()/Stop()`
3. **模块生命周期**：Load → Provision(+Validate) → Use → Cleanup；host/guest 递归
4. **编译期 import 注册插件**（非动态链接）仍获扩展性
5. **配置不可变、整单替换（ACID reload）**：新配置 provision 成功才清理旧配置；短暂双配置并存
6. **Context 绑定配置状态**；确需全局状态时用类 GC 设施（如 upstream 健康）

## 策略（差异/选项）— 相对 Envoy/nginx
| 策略 | Caddy | Envoy（对照） |
|------|-------|----------------|
| 扩展模型 | Go 插件 import / 标准模块 | C++ filter / Wasm / 动态模块 |
| 配置热更新 | 整配置不可变替换 + 单锁 | xDS 动态下发 + TLS 线程本地更新 |
| 部署哲学 | 少活动部件、静态二进制 | 数据面性能与网格可编程优先 |
| 同步策略 | 拒绝热路径逐字段加锁 | shared-nothing worker |

## 显式模式名
- Microkernel / Plugin（apps + guest modules）
- Immutable configuration / Atomic swap
- Host-Guest module composition

## 决策与负面后果
- 整单替换简单正确，但短暂双配置增加内存
- 扩展需重新编译/链接进二进制，不如动态加载「即插」
- 全局状态例外路径需额外纪律

## 对写作规范的启示
- 用「愿景约束 → 机制如何满足」叙事（M3→M5）
- 明确拒绝的策略（逐参数加锁）写进文档 = 强 M6
