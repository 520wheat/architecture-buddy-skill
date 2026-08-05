# 对照短记：nginx (AOSA) vs Envoy
- 域: D1
- 阶段: Phase 1 · 2026-08-05
- 关联: `03b` 种子 nginx；`D1-envoy.md`

## 同一问题类下的机制共性
- 事件驱动、非阻塞、每连接不建进程/线程
- worker 模型扛高并发
- 模块化扩展能力

## 策略差异
| 维度 | nginx | Envoy |
|------|-------|-------|
| 出身问题 | C10K / 边缘高效 Web | 服务网格可编程数据面 |
| 配置 | 文件为主，运维重载 | xDS 控制面动态配置为一等公民 |
| 扩展 | 编译期模块（传统） | Filter 链 + 威胁模型分级 + Wasm 等 |
| 治理原语 | 反向代理/缓存等经典能力 | 熔断、outlier、精细 LB、网格观测 |
| 线程叙事 | master/worker（AOSA） | main + workers + TLS/共享无所细节 |

## 对 Buddy
接入层共思时：先定问题类（静态边缘 vs mesh 数据面），再在 nginx 系哲学与 Envoy 系哲学间做策略表，勿混为一谈。
