# 透镜目录（运行时）

这是 Architecture Buddy 主持 Skill 的运行时选席目录。透镜以 `architecture-buddy/lenses/*.md` 形式随主包内置，由主持 Skill 按需加载，不单独安装。完整研究目录由维护者在发行包外保存。
动态选席：根据 `best-for` / `not-for` 为当前决策点选择不超过 3 个内置透镜（ADR-0017）。透镜提炼做法，不模仿名人声音（ADR-0016）。

| shortname | resource path | 适合（摘要） | 不适合（摘要） | 主要冲突 |
|-----------|-------------|--------------------|-------------------|---------------|
| raft-cp | architecture-buddy/lenses/raft-cp.md | CP metadata、membership、fencing、control plane | 大业务数据、AP 写路径 | dynamo-ap、spanner-sql（强一致范围） |
| dynamo-ap | architecture-buddy/lenses/dynamo-ap.md | 高可用 KV、全球写入、冲突容忍数据 | linearizable ledger、lock | raft-cp、spanner-sql |
| log-stream | architecture-buddy/lenses/log-stream.md | 事件集成、审计、replay、多消费者 | 把 log 当跨服务 XA 银弹 | 常与 CP 或 AP 存储配合 |
| gfs-mr | architecture-buddy/lenses/gfs-mr.md | 批处理/扫描分析、move compute to data | 低延迟 OLTP、小文件 | spanner-sql（OLTP 与 batch） |
| spanner-sql | architecture-buddy/lenses/spanner-sql.md | 全球 external consistency 与 SQL | AP-first、offline merge | dynamo-ap |
| zta-resource | architecture-buddy/lenses/zta-resource.md | Zero Trust resource access、PEP placement | 只依赖 perimeter 的安全模型 | 正交；信任边界是分叉时选席 |
| agent-loop | architecture-buddy/lenses/agent-loop.md | LLM tool loop、permission/HITL、session 边界、trace、agent runtime | 把产品模块图当架构、无护栏自治、没有 observe loop | 常与 zta-resource 配合；不替代 log-stream/CP/AP 存储透镜 |

`architecture-buddy/lenses/scaffold.md` 仅用于契约测试；存在匹配的真实做法透镜时，优先使用真实透镜。
