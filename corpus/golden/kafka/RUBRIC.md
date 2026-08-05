# RUBRIC — kafka

## 必中机制（≥5）

- 持久化追加日志（commit / write-ahead log 心智），而非「内存队列 + 消费即删」
- 拥抱文件系统与 OS pagecache；顺序写为主路径
- 消息按 topic 分区；分区是并行与有序的边界
- Producer 直连分区 leader；按键语义分区（或显式指定）
- Consumer **pull**（可含长轮询）；消费位点是分区上的 offset 整数
- Consumer group：组内同一分区至多一个活跃消费者；可 rewind / 重放
- 长时间保留策略支撑 backlog 与重放（非消费即从日志删除）

## 必中策略分叉（≥3）

- 存储：pagecache 中心日志 vs 堆内大缓存（GC / 双缓存）
- 消费模型：pull vs broker push
- 消费位点：客户端侧 offset vs broker 逐条 ack 状态机
- （加分）分区：键哈希语义局部性 vs 纯随机；压缩：批次端到端 vs 逐条

## 叙事完整性

- 层 A（A1–A8）与层 B（B1–B5）齐全，封面元数据完整
- 主路径可走通：生产者 → 分区 leader → 追加日志 → consumer pull / group 位点推进
- 硬约束动机（吞吐、积压、低延迟、分区并行、容错）在摘要或上下文中可见
- 取舍写清放弃了什么（如 push、消费即删、堆内大缓存）及代价

## 幻觉黑名单（出现则 FAIL）

- 把 Kafka 写成「必须 broker push」或默认 push 投递
- 声称消息消费后必须从日志删除、无法重放
- 把位点说成「只能由 broker 逐条 ack 状态机保管、客户端不可 rewind」
- 声称 Kafka「不能落盘 / 必须纯内存才能高吞吐」
- 把分区有序说成「全 topic 全局总序」且无分区限定
- 整段套用传统 JMS/AMQP「队列 + 消费确认即消失」叙事而不点出日志差异
