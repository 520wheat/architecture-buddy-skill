# SQLite Architecture
- 域: D3 数据存储与查询
- 来源: https://www.sqlite.org/arch.html
- 阶段: Phase 4 加深 · 2026-08-05（书单可换项；对照嵌入式 vs 服务型存储）

## 问题类
在**进程内、单文件、可嵌入**约束下，提供可靠 SQL 存储：编译 SQL → 字节码 → VM 执行，并对磁盘 B-tree 做事务安全访问。

## 硬约束
- 库形态（非独立服务进程为主叙事）
- 跨 OS：经 VFS 抽象
- 文件格式稳定向前兼容
- 线程安全/可重入解析器（Lemon；tokenizer 调用 parser）

## 机制（共性）
1. **SQL 编译为字节码**，由 **VDBE** 虚拟机执行（prepare / step）
2. **分层后端**：B-Tree ↔ Page Cache（含回滚/原子提交/锁）↔ OS VFS
3. **查询规划**在代码生成（尤其 where*/select）中选择算法
4. **表/索引各一棵 B-tree**，同文件共存
5. 扩展与内建函数多为 **C 回调**挂到 VM

## 策略（差异/选项）
| 选项 | 含义 | 与 BDB/HDFS 对照 |
|------|------|------------------|
| 嵌入式单文件 | 零运维服务 | vs BDB 嵌入式库；vs HDFS 分布式服务 |
| page_size / WAL | 缓存与提交策略 | 局部调优，非问题类变更 |
| 手写 tokenizer + Lemon | 解析策略 | 可理解性/可移植性优先 |

## 显式模式名 / 相邻
- Layers（Interface → Compiler → VM → B-Tree → Pager → VFS）
- Virtual Machine / Bytecode IR（与 LLVM「一等 IR」气质相邻，域不同）
- Pager = 事务与持久化抽象边界

## 决策与负面后果
- 单写者/文件锁模型适合嵌入与中小并发，不替代分布式 DB
- 「查询规划是 AI」叙事：规划错误代价由语句路径承担——需可解释与可调

## 对写作规范的启示
- 组件图可作附录；正文应先写「编译→VM→页缓存→VFS」数据路径 = M5 机制
- 与 HDFS：同为 D3，**嵌入式本地可靠** vs **分布式海量**——问题类边界示范（M1）
