# videocut.chat 0.2.2

Release date: 2026-09-14. Controlled beta; macOS local rendering verified.

## English

- Added `saycut_inspect_caption_style` and `saycut_style_captions` for inspecting effective caption settings and changing selected captions' size, color, position, opacity and supported outline properties.
- Added per-caption effect parameters and merge/delete patches with revision checks. Partial text edits preserve omitted timestamps; text/timing changes clear stale word alignment.
- Added bounded visual warnings for long text, short cues, narrow canvases, off-canvas placement, transparent text and unverified font coverage. Warnings do not guarantee readable output.
- Improved malformed input, missing/corrupt media, network and no-audio errors. Staging estimates now account for copied caption fonts.
- Updated the shared video skill and caption styling reference. These semantic editing tools are local-only; cloud feature parity is not claimed.

Validation: 211 installed styles rendered with 633 sampled frames, 35 interface/concurrency/fault checks, and actual MCP stdio, local Chinese ASR and editable ZIP checks passed in the configured macOS environment. Sampled nonblank frames do not constitute complete visual or transcription-quality acceptance.

Known limits: very long text, extremely narrow canvases and very short animated cues can produce unreadable or invisible captions; tested fonts did not cover every script. Windows/Linux, fresh-machine onboarding, every vendor client, cloud rendering/billing and browser editor import have not been accepted in this release.

The wheel and plugin ZIP do not bundle the native runtime, effect/font resources, SDK licenses or ASR model weights. Optional ASR dependencies require `--asr`; model download is explicit. Existing private configuration is preserved. Installing the ZIP alone does not provision a rendering environment.

The Python distribution/command remain `saycut-tools`; the plugin identifier remains `videocut-chat`. No C++ SDK, license-renewal or billing-rule changes are included. Version 0.2.1 archives are retained unchanged.

## 简体中文

- 新增 `saycut_inspect_caption_style` 和 `saycut_style_captions`，支持查看字幕实际生效参数，并按指定字幕修改字号、颜色、位置、透明度和受支持的描边属性。
- 支持逐句效果参数、合并/删除参数及版本冲突校验。局部修改文字保留未提供的时间；文字或时间变动会清除旧逐词对齐数据。
- 增加长文字、短字幕、窄画布、画布外定位、透明文字和字体覆盖风险提示。风险提示不是可读性保证。
- 改进异常输入、缺失/损坏媒体、网络和无音轨错误处理；暂存空间估算计入字幕字体副本。
- 更新共享 Skill 和花字参数参考文档。新增语义编辑工具仅支持本地，不代表云端功能已同步。

验证范围：已配置的 macOS 环境下，211 个已安装样式完成渲染并检查 633 个采样帧，35 组接口/并发/故障检查通过；真实 MCP stdio、本地中文 ASR 和可编辑 ZIP 检查通过。采样非空不代表全部文字可读，也不代表全面的识别准确率验收。

已知限制：超长文字、极窄画布和过短动画字幕可能不可读或不可见；测试字体不能覆盖所有文字系统。尚未完成 Windows/Linux、新电脑首次安装、各厂商真实客户端、云端合成/计费及网页编辑器导入验收。

wheel 和插件 ZIP 不包含原生运行时、效果/字体资源、SDK 证书和 ASR 模型权重。可选识别依赖需要 `--asr`，模型须明确下载，已有私有配置会保留。仅安装 ZIP 不会完成合成环境配置。

Python 包和命令保持 `saycut-tools`，插件标识保持 `videocut-chat`。本版不修改 C++ SDK、证书续期或计费规则，0.2.1 历史发行包保持不变。
