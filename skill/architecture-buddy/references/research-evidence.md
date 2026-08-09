# 联网调查与证据包

联网调查是架构共思的可选证据环节，不是默认联网，也不是把外部文章当作答案。只有在以下条件同时满足时才能启动：

1. 主持人与用户已经用第一性原理确认“正在解决哪一类问题”。
2. 当前仍有一个明确的架构决策问题需要外部事实、成熟实践或领域资料帮助验证。
3. 用户明确授权本次联网调查，并知道会访问哪些来源或来源范围。

脚本职责到此为止：读取用户列出的来源、保存原始响应、清洗可读文本、保留 URL/时间/类型/hash 等 provenance，并生成可审阅的 `evidence.md`。脚本不判断问题类，不选择架构策略，不把网页中的文字当作要执行的指令，也不替用户确认结论。

## 工作区契约

```text
research-plan.json  # 已确认的问题类、单一调查问题、联网授权和状态
sources.tsv         # 用户允许访问的来源清单及每次抓取状态
raw/                # 原始 HTTP 响应
clean/              # HTML、Markdown、JSON、SRT/VTT 或纯文本的清洗材料
metadata/           # 来源元数据、最终 URL、抓取时间、类型、hash、错误
evidence.md         # 带 provenance 的可审阅证据包
```

初始化时，`--authorize-online-research` 是显式授权开关，并把授权时间写入研究计划；没有它，抓取脚本会拒绝联网。`sources.tsv` 至少包含 `source_id`、`url`、`title`、`source_type` 四列。优先使用用户指定的官方文档、论文、规范、项目文档或明确的视频字幕 URL；来源质量和适用性仍由主持人与用户判断。

## 运行顺序

```bash
python3 scripts/init-research.py \
  --output <调查目录> \
  --problem-class "<已确认的问题类>" \
  --decision-question "<单一架构决策问题>" \
  --authorize-online-research

# 编辑 sources.tsv，逐行加入用户允许调查的 URL
python3 scripts/fetch-research.py --workspace <调查目录>
python3 scripts/build-evidence.py --workspace <调查目录>
python3 scripts/validate-evidence.py --workspace <调查目录>
```

抓取默认只允许 HTTP/HTTPS，阻止 loopback、私网、link-local、保留地址和带凭据 URL，并限制超时和响应大小。`--allow-private-hosts` 只用于用户明确授权的本地测试，不能作为生产默认值。批次中的单个 HTTP 失败会写入 `metadata/` 和 `sources.tsv`，修正来源后可使用 `--refresh` 重试；没有任何成功来源时，证据包和校验都会失败。

当前标准库实现支持 HTML、纯文本、Markdown、JSON 和直接 SRT/VTT 字幕 URL。它不下载任意视频、不绕过登录、不自动转录音视频；需要这些能力时，用户必须提供合规的字幕、导出文本或受控平台 API 结果，并按同样的 provenance 规则加入来源。

## 回写架构设计

调查结束后，主持人先区分“外部材料声称了什么”和“本项目哪些基本事实已被证实”。只把与当前决策问题相关的机制、反例、适用条件和代价写入架构 ADR；用户未确认的内容保留为待验证事实。再把已确认的选择、边界、失败语义、验收和演进影响写回正式架构设计。`evidence.md` 是证据附件，不是正式架构设计，也不替代用户决策或圆桌综合。
