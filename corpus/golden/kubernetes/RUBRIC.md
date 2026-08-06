# RUBRIC — kubernetes

## 必中机制（≥5）

- 控制面与节点（数据面）分离：编排决策在控制面，容器执行在节点
- 声明式 API：用户提交期望状态对象，而非逐步命令式驱动集群内部
- Controller reconcile：watch 期望/实际差异 → 行动缩小差距（控制循环）
- etcd（或等价一致存储）为集群状态真相源；持久化对象与配置
- API Server 为无状态前门 / Gateway：唯一正规读写集群状态的入口
- 可插拔运行时与网络：CRI、CNI（及可替换调度器、CRD/聚合 API 等扩展）
- （加分）分层：API → 控制器 → 节点代理（kubelet 等）；扩展不绕过 API

## 必中策略分叉（≥3）

- 控制面部署：传统多机 / Static Pod / Self-hosted / Managed（运维复杂度与责任边界）
- 节点转发：kube-proxy vs CNI 自带转发（节点组件可裁剪）
- 云控制：cloud-controller-manager 拆分 vs 与通用控制混部
- （加分）布局：小集群混部控制面 vs 生产专用控制面节点

## 叙事完整性

- 层 A（A1–A8）与层 B（B1–B6）齐全，封面元数据完整；B6 需包含变化轴、N+1、反例及能力/复杂度边界证据
- 主路径可走通：kubectl apply → API Server → etcd → controller watch → 节点执行
- 硬约束动机（控制面容错、强一致状态、API 唯一前门、节点侧可插拔）在摘要或上下文中可见
- 取舍写清放弃了什么（如命令式直改节点、绕过 API 写 etcd、不可插拔运行时）及代价

## 幻觉黑名单（出现则 FAIL）

- 声称 **kubelet（或节点组件）绕过 API Server 直接改 etcd** 是正规扩展路径
- 把 etcd 说成可被任意节点组件随意写入的「共享文件夹」
- 声称 Kubernetes「没有声明式 / 只有命令式逐步驱动」为默认心智
- 把 API Server 说成有状态真相源本身（混淆前门与 etcd）
- 声称控制面单机无备份即可当作生产默认架构而无容错叙述
- 整段套用「SSH 进机器改容器 = 集群真相」叙事而不点出声明式 reconcile 差异
