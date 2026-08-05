# Anti-patterns & Writing Rules (runtime cheat sheet)
Source: docs/survey/living/anti-patterns-and-writing-rules.md — compressed for skill runtime.

## 内容反模式
| 反模式 | 证据 |
|--------|------|
| 为 Agent 而 Agent | Anthropic |
| 协调库当业务主键库 | etcd |
| Lease/Lock 当外部资源银弹互斥 | etcd |
| 无威胁模型的数据面扩展 | Envoy |
| 单点元数据无备份纪律 | HDFS/K8s |
| 只讲边界防火墙 | NIST ZTA |
| 热路径逐字段加锁 | Caddy |
| 客户端强制访问控制 | ASVS |
| 多套强弱不一认证入口 | ASVS |
| DAG 编排需要循环的 agent | LangGraph |
| 为中间件而中间件 | Dependency-Track |
| 单体编译器全局状态/层泄漏却当库 | LLVM |
| GoF 词汇通胀 | P1 |
| 用 Raft/Paxos 却不接受 CP 语义 | Raft/etcd |

## 写作禁忌 → 改为
| 禁忌 | 改为 |
|------|------|
| 模块图第一章 | 问题类→假设→质量→机制/策略 |
| 单一最佳实践 | 并列策略+条件+代价 |
| 不写负面后果 | Consequences 必含负向 |
| 私有黑话 | 公共模式名优先 |
| 隐藏信任/一致性假设 | 写入 M3 |
| 容量数字当主叙事 | 仅作 M4 场景 |

## Buddy 运行时红线
- 不替用户拍板  
- Top N / 深调研先问再做  
- 提出 agent / 消息总线 / 共识组件前先问「更简单方案是否足够」  
