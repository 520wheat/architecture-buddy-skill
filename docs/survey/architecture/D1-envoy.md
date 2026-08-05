# Envoy Proxy — Architecture Overview / Threading Model
- 域: D1 Web / 边缘与接入
- 来源: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/
- 阶段: Phase 1 · 2026-08-04

## 问题类
在服务网格/边缘为大量并发连接提供**可编程的 L3/L7 代理与流量治理**（路由、发现、健康检查、熔断、可观测、安全），并支持动态配置（xDS）。

## 硬约束
- 热路径必须高度并发且尽量非阻塞
- 配置可从控制面动态下发，不能靠重启凑合
- 扩展（filter）要能在不信任下游/上游场景下声明威胁模型等级

## 机制（共性）
1. **Listener → Filter Chain → Upstream Cluster** 的分层处理管道
2. **控制面/数据面分离**：xDS 动态配置；main 线程协调，worker 处理流量
3. **共享无所（shared-nothing）热路径**：连接绑定单 worker，TLS/本地缓存减锁
4. **韧性原语内建**：health check、outlier detection、circuit breaking、rate limit
5. **可观测一等公民**：stats、access log、tracing

## 策略（差异/选项）
| 策略 | 适用 | 代价 |
|------|------|------|
| 单进程多线程（main + N workers） | 通用数据面 | 需严格线程模型；扩展作者易犯错 |
| 连接绑死单 worker | 避免热路径锁 | 长连接不均时需显式 connection balancing |
| Filter 扩展（含 Wasm/动态模块） | 可编程性 | 安全等级不一；威胁模型要标注 |
| 内核负载均衡 vs Envoy 强制 balancing | 默认靠内核；mesh 长连接场景可强制 | Windows 强制 balancing 有性能代价 |

## 显式模式名
- Pipes and Filters（HTTP/网络 filter 链）
- Broker / Sidecar 数据面（相对应用进程）
- Circuit Breaker、Outlier Detection（稳定性格局）

## 决策与负面后果
- 热路径 lock-free 换来的是复杂的 TLS 更新与「必须按 Dispatcher/post 编程」
- Watchdog 监控卡死——承认扩展可能堵死 worker
- 异步文件/DNS 等必须甩到专用线程，否则破坏非阻塞假设

## 对写作规范的启示
- 先讲线程/事件模型（约束下的机制），再列功能清单
- 安全单独成章并给扩展**威胁模型分级**——值得进 M2/M7
