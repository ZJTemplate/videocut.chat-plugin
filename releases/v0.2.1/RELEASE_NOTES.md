# videocut.chat 0.2.1

[English](../../README.md) | [简体中文](../../README.zh-CN.md)

## English

Controlled-beta distribution for users with a provisioned, licensed native runtime.

- Real Codex MCP acceptance covered Chinese ASR, animated captions, editable output, caption revision and rerendering, idempotent submissions, revision conflicts and running cancellation.
- Representative local outputs were H.264/AAC, 640x360, 24 fps, with CRC-validated editable bundles. Authenticated artifact downloads and SDK certificate isolation were checked.
- The rebuilt wheel exports a contained executable POSIX launcher that uses the private interpreter without a host Python lookup. Fresh private installation verified both MCP protocol modes with an empty PATH.
- Regression verification: 164 Python tests and 7 Node tests passed. This is not a claim that these tests run in this distribution-only repository.
- Installation downloads `p-template-generator==1.2.17` into a private environment. The plugin ZIP remains a generic template; the installer creates machine-specific manifests and the launcher.

Known limits: native rendering was accepted on provisioned macOS only; not every catalog effect was visually checked. Native resources, fonts, SDK certificates and speech models are not bundled. Cloud public OAuth, payment/refund integration and hosted editor handoff are incomplete. This release does not establish official marketplace availability or consumer-chat compatibility.

Upload the wheel, plugin ZIP and `SHA256SUMS` as assets when creating a GitHub Release. Users of the isolated installer also need this repository's `scripts/` and `plugins/` directories, available by cloning or downloading the repository archive. Do not replace an already published archive under the same version with different bytes; issue a new version instead. Checksums detect changed bytes but are not a digital signature.

## 简体中文

面向已配置并授权原生运行时用户的受控内测版本。

- 真实 Codex MCP 验收覆盖中文识别、花字字幕、可编辑输出、字幕修改重渲染、幂等提交、版本冲突与运行中取消。
- 抽查输出为 H.264/AAC、640x360、24 fps，可编辑 ZIP 通过 CRC 检查；已检查下载鉴权及 SDK 证书隔离。
- 重建后的 wheel 可导出 POSIX 私有解释器启动脚本，不依赖宿主查找 Python。全新独立安装在空 PATH 下通过两种 MCP 协议模式验证。
- 回归验证为 164 项 Python、7 项 Node 测试通过；并不表示这些测试源码包含在本发行仓库中。
- 安装时将 `p-template-generator==1.2.17` 下载到私有环境。插件 ZIP 是通用模板，由安装器生成机器专属配置与启动器。

已知限制：目前仅在配置完整的 macOS 环境验收原生合成，未逐一视觉验证全部效果。不包含原生资源、字体、SDK 证书或语音模型。云端公开 OAuth、支付退款和在线编辑桥接尚未完成，不代表已上架官方市场或兼容所有消费者聊天入口。

创建 GitHub Release 时，将 wheel、插件 ZIP、`SHA256SUMS` 作为附件上传。独立安装器还需要仓库内的 `scripts/` 和 `plugins/`，用户可 clone 或下载仓库归档。正式发布后不要在同一版本下替换不同内容的包，应发布新版本。校验和用于检测内容变化，不是数字签名。
