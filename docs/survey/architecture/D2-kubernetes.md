# Kubernetes — Cluster Architecture
- 域: D2 分布式协调与集群
- 来源: https://kubernetes.io/docs/concepts/architecture/
- 阶段: Phase 1 · 2026-08-04

## 问题类
在集群上运行容器化工作负载：声明期望状态，由控制面持续调和（reconcile）到实际状态。

## 硬约束
- 控制面需可容错（生产多机）；状态需强一致存储（etcd）
- 节点侧提供运行时、网络、代理等可插拔实现
- API 是唯一前门；扩展不能绕过

## 机制（共性）
1. **控制面 / 数据面（节点）分离**
2. **声明式 API + Controller 调和循环**（watch → diff → act）
3. **集中式一致状态存储（etcd）** 作为真相源
4. **水平扩展的 API Server** 作为无状态前门
5. **可插拔运行时/网络/调度**（CRI、CNI、自定义调度器、CRD/聚合 API）

## 策略（差异/选项）
| 策略 | 说明 |
|------|------|
| 控制面部署：传统 / Static Pod / Self-hosted / Managed | 运维复杂度与责任边界不同 |
| kube-proxy vs CNI 自带转发 | 节点组件可裁剪 |
| cloud-controller-manager 拆分 | 云相关控制与通用控制分离 |
| 小集群混部 vs 生产专用控制面节点 | 规模驱动的布局策略 |

## 显式模式名
- Control Loop / Reconciliation（控制器）
- Gateway（API Server）
- Layered：API → 控制器 → 节点代理
- Sidecar/DaemonSet 类插件（addons）

## 决策与负面后果
- 逻辑上多控制器、物理上常塞进单一二进制 → 简化部署，耦合进程生命周期
- 强依赖 etcd → 备份与容量成为架构级风险（文档点名）

## 对写作规范的启示
- 组件清单之前先给**角色分工与真相源**
- 「Architecture variations」专节 = 策略目录范例
