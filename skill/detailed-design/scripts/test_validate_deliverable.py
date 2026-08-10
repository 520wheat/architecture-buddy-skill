import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().with_name("validate-deliverable.py")


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def overview(
    *,
    status: str = "design-ready",
    include_contract: bool = True,
    include_fallback: bool = True,
    pending_fact_ok: bool = True,
) -> str:
    pending_row = (
        "| PF-1 | 待确认事实 | 默认值 | 原因 | 验证条件 | 回退路径 | 重新打开条件 |"
        if pending_fact_ok
        else "| PF-1 | 待确认事实 |  | 原因 | 验证条件 | 回退路径 | 重新打开条件 |"
    )
    contract = (
        "- 契约要点：A 与 B 通过消息交互\n- 禁止边：A 不直接调用 C"
        if include_contract
        else "- 契约要点："
    )
    fallback = "- 回退动作：回到 architecture-buddy" if include_fallback else "- 回退动作："
    return f"""# 详细设计总览

## 元数据与架构输入

- 状态：{status}
- 项目：示例
- 版本：v1
- 架构输入：
  - 来源：architecture.md
  - 已确认范围：示例范围
  - 已确认非目标：示例非目标
  - 已确认设计单元：auth、billing
  - 架构回退引用：architecture-handoff.md

## 设计范围与非目标

- 设计范围：示例范围
- 非目标：示例非目标
- 约束：无外部依赖
- 默认值：待确认

## 设计单元索引

| 顺序 | 单元 | 责任 | 产物 |
| --- | --- | --- | --- |
| 1 | auth | 鉴权 | auth.md |
| 2 | billing | 计费 | billing.md |

## 架构反馈索引

| 编号 | 标题 | 影响模块 | 当前状态 | 反馈文档引用 |
| --- | --- | --- | --- | --- |
| AF-1 | 输入校验 | auth | resolved | architecture-feedback.md |

## 单元关系

- 上游单元：auth
- 下游单元：billing
- 依赖顺序：auth -> billing
- 共享能力：日志

## 跨模块契约

{contract}

## 端到端流程

1. auth 接收输入
2. billing 处理
3. 写回结果

## 统一规则

### 故障

- 失败分类：超时
- 降级策略：回退
- 重试边界：1 次

### 并发

- 并发模型：串行
- 锁 / 令牌 / 乐观冲突：无
- 幂等约束：请求幂等

### 安全

- 权限边界：auth
- 审计要求：记录
- 敏感数据处理：脱敏

### 可观测性

- 日志：结构化
- 指标：成功率
- 链路追踪：开启
- 告警：失败报警

## 测试策略

- 单元测试：有
- 集成测试：有
- 端到端测试：有
- 回归点：回退项

## 实现顺序

1. auth
2. billing

## 待确认事实

| 编号 | 事实 | 单阶段默认值 | 默认原因 | 验证条件 | 回退路径 | 重新打开条件 |
| --- | --- | --- | --- | --- | --- | --- |
{pending_row}

## 回退项

| 编号 | 回退触发事实 | 回退目标 | 回退动作 | 恢复条件 | 关联待确认事实 |
| --- | --- | --- | --- | --- | --- |
| RB-1 | PF-1 | architecture-buddy | {fallback} | 恢复后继续 | PF-1 |

## 完成状态

- 状态：{status}
- 完成证据：overview + module
- 未完成项：无
- 审阅结论：待审阅
"""


def module_doc(*, name: str = "auth", include_fallback: bool = True, pending_fact_ok: bool = True) -> str:
    pending_row = (
        "| PF-1 | 事实 | 默认值 | 原因 | 验证条件 | 回退路径 | 重新打开条件 |"
        if pending_fact_ok
        else "| PF-1 | 事实 | 默认值 | 原因 |  | 回退路径 | 重新打开条件 |"
    )
    fallback = "- 回退动作：回滚" if include_fallback else "- 回退动作："
    return f"""# 模块详细设计

## 职责与边界

- 模块名：{name}
- 责任：鉴权
- 处理边界：输入验证
- 明确不负责：计费

## 依赖与禁止边

- 依赖模块：billing
- 依赖能力：日志
- 禁止依赖：外部状态
- 禁止调用方向：billing -> auth

## 外部接口与内部接口

- 外部接口：HTTP
- 内部接口：函数
- 调用者：API
- 被调用者：service

## 请求 / 响应与字段约束

- 请求结构：request
- 响应结构：response
- 字段约束：必填
- 默认值：无
- 兼容策略：向后兼容

## 错误语义

- 错误分类：输入错误
- 失败返回：400
- 可重试错误：超时
- 不可重试错误：校验失败

## 状态机与不变量

- 状态：draft
- 状态转换：created -> done
- 不变量：幂等
- 终止条件：完成

## 行为与时序

- 核心行为：处理请求
- 顺序步骤：校验 -> 执行
- 关键分支：失败回退

## 超时 / 重试 / 幂等 / 并发

- 超时：3s
- 重试：1 次
- 幂等：request id
- 并发控制：单线程

## 权限 / 审计 / 日志 / 指标 / 追踪 / 配置

- 权限：鉴权
- 审计：记录
- 日志：结构化
- 指标：成功率
- 追踪：开启
- 配置：静态

## 测试

- 单元测试：有
- 集成测试：有
- 失败场景测试：有
- 回归测试：有

## 验收条件

- 业务验收：通过
- 技术验收：通过
- 观察窗口：24h

## 回退项

| 编号 | 回退触发事实 | 回退目标 | 回退动作 | 恢复条件 | 关联待确认事实 |
| --- | --- | --- | --- | --- | --- |
| RB-1 | PF-1 | architecture-buddy | {fallback} | 恢复后继续 | PF-1 |

## 待确认事实

| 编号 | 事实 | 单阶段默认值 | 默认原因 | 验证条件 | 回退路径 | 重新打开条件 |
| --- | --- | --- | --- | --- | --- | --- |
{pending_row}
"""


class ValidateDeliverableCLITest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_exists(self) -> None:
        result = self.run_validator("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())

    def test_accepts_valid_overview_and_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview())
            write_file(root / "architecture-feedback.md", "# 架构反馈\n")
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())
            write_file(modules / "billing.md", module_doc(name="billing"))

            result = self.run_validator(str(root))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("详细设计校验通过", result.stdout)

    def test_rejects_missing_overview(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("overview", result.stderr.lower())

    def test_rejects_missing_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview())
            (root / "modules").mkdir()

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("module", result.stderr.lower())

    def test_rejects_blocked_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview(status="blocked"))
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("blocked", result.stderr.lower())

    def test_rejects_missing_cross_module_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview(include_contract=False))
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("跨模块", result.stderr)

    def test_rejects_missing_fallback_section_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview(include_fallback=False))
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc(include_fallback=False))

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("回退", result.stderr)

    def test_rejects_incomplete_pending_fact_closure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_file(root / "detailed-design-overview.md", overview(pending_fact_ok=False))
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("待确认", result.stderr)

    def test_rejects_missing_module_coverage_and_broken_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            content = overview()
            content = content.replace("- 模块 A：auth\n- 模块 B：billing", "- 模块 A：ghost\n- 模块 B：billing")
            content = content.replace("| RB-1 | PF-1 |", "| RB-1 | PF-999 |")
            write_file(root / "detailed-design-overview.md", content)
            modules = root / "modules"
            modules.mkdir()
            write_file(modules / "auth.md", module_doc())

            result = self.run_validator(str(root))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("模块", result.stderr)


if __name__ == "__main__":
    unittest.main()
