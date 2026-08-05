# Corpus P4 — Enterprise Integration Patterns 核心词汇
- 阶段: Phase 2 · 2026-08-05
- 来源: https://www.enterpriseintegrationpatterns.com/ · Hohpe/Woolf
- 说明: 65 模式目录级起步；与 D4 Kafka/Pulsar 交叉

## 元机制
- 模式是**收获的经验**不是发明；跨技术（Kafka、云队列、ESB、REST 集成）仍适用  
- 提供集成问题的**共同语言**（文档/代码/对话）  
- 本目录后续模式默认落在 **Messaging** 风格上  

## 分类骨架（七组）

| 组 | 讨论什么 | 基模式 |
|----|----------|--------|
| Integration Styles | 如何集成（历史选项）；后续以 Messaging 为主 | File Transfer / Shared DB / RPC / Messaging 等 |
| Channel Patterns | 消息如何运输 | Message Channel |
| Message Construction | 消息意图与形态 | Message |
| Routing Patterns | 如何到达正确接收方 | Message Router |
| Transformation Patterns | 如何改内容/格式 | Message Translator |
| Endpoint Patterns | 应用如何生产/消费 | Message Endpoint |
| System Management | 复杂消息系统如何运转 | — |

## 与 Buddy / D4 直接挂接的核心条目

| EIP 名 | 问题类切片 | Kafka/Pulsar 钩子 | Buddy 问句 |
|--------|------------|-------------------|-----------|
| Message Channel | 发送方与接收方经通道解耦 | Topic/Partition；Pulsar Topic | 通道语义是点对点还是发布订阅？ |
| Point-to-Point Channel | 单消费者处理 | Consumer group 内竞争 | 是否只要一人处理？ |
| Publish-Subscribe Channel | 多方独立消费 | 多 group / 多订阅 | 是否多方各自位点？ |
| Message Router | 按条件导向不同接收方 | 应用侧路由；流处理 | 路由在生产端、代理还是消费者？ |
| Message Translator | 格式/内容适配 | Schema、SMT、应用变换 | 谁拥有规范模型？ |
| Message Endpoint | 应用连接消息系统 | Producer/Consumer API | 幂等/重试在端点还是通道？ |
| Guaranteed Delivery | 持久直至妥善处理 | Kafka 持久日志；Pulsar BookKeeper | 丢失 vs 重复哪个不可接受？ |
| Competing Consumers | 扩展消费能力 | Consumer group | 分区键是否破坏并行？ |
| Event-Driven Consumer | 异步到达处理 | — | 推/拉？（Kafka 选拉） |
| Dead Letter Channel | 无法处理的消息 | DLQ 生态 | 失败消息去哪？ |

## 策略提醒（来自 D6 Dependency-Track）
EIP/Kafka **描述能力** ≠ **你的问题类需要公司级总线**。先 M1/M3（运维边界），再选通道技术。

## 下一步
Phase 3：补 System Management 组；选 5 个路由模式深挖（Content-Based Router、Splitter、Aggregator 等）
