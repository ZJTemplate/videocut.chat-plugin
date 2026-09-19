# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

为 **AI 编程智能体宿主**（Codex、Claude Code、Qwen Code 及任意 MCP 客户端）提供花字字幕、确定性视频合成与可编辑 SkyMedia 工程。底层是带许可证校验的 `template_generator` 原生引擎，运行在你自己的机器上。

**版本 0.3.1 · 受控内测 · 面向高级用户。**
如果你还没有在用支持 MCP 的编程智能体，请直接使用网页产品 [videocut.chat](https://videocut.chat)。本仓库不是双击即用的应用，未发布到 PyPI，也未上架官方插件市场。

## 工作流

1. **一次安装**（约 10 分钟，下文一条复制粘贴命令块；也可以把仓库 URL 丢给你的 agent，让它按"安装"一节执行并把生成的配置合并进宿主）。
2. **一次授权。** 首次渲染会打开 [platform.zjtemplate.com](https://platform.zjtemplate.com) 的审批页。0.3.x 起后台 keepers 会静默续期账号 token 和 SDK 租约（36 小时水位），不需要周期性重新登录。
3. **自然语言驱动**："给这段视频加中文花字字幕，工程保持可编辑。" agent 负责转录（本地 faster-whisper）、从已安装样式目录选花字、组工程并**本地渲染**；除非你明确允许云端处理，素材不出本机。
4. **迭代分两条轨**：文字/样式/时间轴改动在聊天里用 MCP 工具完成；**要"看着调"**时，插件给出 `edit.videocut.chat` 深链，浏览器编辑器直接导入这份工程（线上已验证，含 32MB 多素材包的 OPFS 导入）。
5. **回流闭环**：编辑器导出 `.saycut.zip` 工程包，同机场景把下载的文件路径给回 agent，即可在聊天里继续修改、重渲。

## 真实状态矩阵（能力现在到底在哪一步）

| 能力 | 状态 |
| --- | --- |
| 隔离环境安装 + 发行资源本地渲染（macOS） | ✅ 已验收（0.2.5 验收 + 0.3.1 全进程 serve e2e 进 CI） |
| 一次授权、token/许可证自动续期 | ✅ 0.3.1 实装（`TokenKeeper` / `LicenseKeeper`） |
| MCP 工具面：导入/转录/花字/组工程/渲染/取消/幂等重试 | ✅ 契约与 CI 验证；Claude/Qwen 等宿主自身的 OAuth UI 未实测 |
| 浏览器编辑器工程注入（`edit.videocut.chat/editor?file=…`） | ✅ 线上可用并公网验证 |
| SDK 路由 `GET /v1/jobs/{id}/editable-bundle` | ✅ 0.3.1 实装——但它由**你的** gateway 提供，公网浏览器访问不到本机，深链只对"浏览器可达的 gateway"生效 |
| 云端工程库往返（`saycut_save_to_edit`） | 🟡 SDK 客户端 + REST + MCP 三通道已完成；`mcp.zjtemplate.com` 的 `POST /mcp/v1/edit-projects` 受理端点尚未由平台方上线，跨设备交接被它卡住 |
| 聊天 ↔ 内嵌编辑器双通道（`postMessage`） | 🟡 Node 契约测试通过；只对带 webview 的宿主有意义——终端型 agent（Codex/CC CLI）请走导出文件回流 |
| `McpRender` 云端渲染（`mcp.zjtemplate.com`） | 🟡 3 个真实任务 66/66/96 秒完成，但用的是运营验收凭证；个人 OAuth + 计费闭环未验收；生产 worker 仍注册 legacy `GenVideo`（别名 `saycut_tools_v1` 过渡） |
| Windows / Linux 原生渲染 | ⬜ 有配置，未验收 |
| 预览段渲染（短时间窗试渲） | ⬜ 未实现——目前每次渲染都是全量 job |

样式目录共 224 个条目，本 wheel 打包了 211 个样式的资源和思源黑体回退字体，另外 13 个需要自备资源。"可用"不等于任何语言、任意字幕长度都有理想观感：长文案换行、缺字、装饰字裁切是已知缺陷；导入前请按 skill 内的 FFmpeg 流程归一化旋转元数据与非方形像素。

## 下载（0.3.1）

| 文件 | 用途 |
| --- | --- |
| [Python wheel](releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl) | `saycut-tools`：MCP 服务、本地 gateway、编辑器资产、样式资源 |
| [插件 ZIP](releases/v0.3.1/videocut-chat-plugin-0.3.1.zip) | 通用插件配置与视频 Skill |
| [SHA256SUMS](releases/v0.3.1/SHA256SUMS) | 两个发行包的校验和 |

下载后运行 `python3 scripts/verify_release.py` 校验。wheel 是可直接审阅的 Python，打包不等于加密。安装器显式下载：钉定的原生 SDK（`p-template-generator==1.2.17`，`native` extra）、可选 `faster-whisper`（`asr` extra）、运行时二进制与 ASR 模型。任何发行包都不含账号凭证或 SDK 证书。

## 安装（macOS / POSIX）

前提：Python ≥ 3.11；PATH 中有 FFmpeg 与 ffprobe；具备本地渲染权限的平台账号；下载与许可证校验需要联网。

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py

python3 scripts/install_isolated.py \
  --wheel releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl \
  --allow-root "/绝对路径/视频目录" \
  --download-resources --asr --download-model
```

安装过程在 `~/.local/share/saycut-plugin` 下创建私有环境（不碰全局 site-packages），完成后打印三个路径：`python`、`config`、`integrations`。就绪检查：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

资源与模型以后可再跑 `setup-resources`、`configure-asr --backend faster_whisper --model small --download-model` 补齐。诊断只检查前置条件，不代表每个特效或一次获授权的渲染成功。

## 接入你的智能体

使用 `integrations` 目录下**生成的**配置文件——不要原样使用仓库里的通用 manifest：

| 宿主 | 生成的配置 |
| --- | --- |
| Codex | `codex.toml`，或将 `plugins/videocut-chat/` 注册为本地插件源 |
| Claude Code | `claude-code.mcp.json` 或生成的插件目录 |
| Claude Desktop | `claude-desktop.json` |
| Qwen Code | `qwen.settings.json` |
| 其他 MCP 宿主 | 兼容的 stdio 生成配置 |

用宿主的 MCP 配置机制合并，勿覆盖无关设置；新开对话确认 `saycut_capabilities` 可见。首次渲染时插件会打开授权链接——自行登录并批准；凭证与短时效 SDK 证书只保存在私有运行时目录。

## 云端、编辑器桥与边界

云端提交统一走 `https://mcp.zjtemplate.com/mcp` 的 `McpRender`（0.2.3+ 支持 OAuth discovery、动态注册、PKCE、token 轮换/吊销）。网页登录 token 或本地授权不等于云端凭证；纯 stdio 宿主跑一次 `account login --cloud`。云端计费沿用平台 GenVideo 费率：自动 ASR 按配置时长上限预扣（当前 600 秒 × ¥0.01/秒），完成后按实际上报用量结算并退还差额——legacy worker 目前上报 `usage={}`，生产计量要等该 worker 升级。云端 legacy 链路只验证了单一 preset + MP4 输出；完整特效目录与可编辑云端工程尚不可用。

编辑器桥分两段看：**浏览器端**（工程注入 `edit.videocut.chat`、OPFS 导入、导出提示、字节级往返）已上线并公网验证；**平台端**（公共工程库 `POST /mcp/v1/edit-projects`）尚未开始受理，`saycut_save_to_edit` 目前只能对着 stub 完成。在此之前，指向非公网 gateway 的 `?file=` 链接不会在浏览器里加载——不要把交接链接当作会话可用的证据，同机导出回流是当前可靠路径。

本地渲染不会静默上传素材；但账号/许可证校验仍会联系授权服务：本地优先不等于完全离线。任何云端处理都需要显式同意（`allow_cloud_processing`）。不要把 token、证书、私有配置或客户素材提交进仓库。

## 支持

可复现问题请提 [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues)，附 OS、Python/包版本与脱敏诊断；切勿附上凭证或私有视频。凭证泄露先回平台吊销连接再报。验收记录：[0.2.5](docs/ACCEPTANCE-0.2.5.zh-CN.md)、[0.2.3](docs/ACCEPTANCE-0.2.3.zh-CN.md)、[2026-09-14](docs/ACCEPTANCE-2026-09-14.zh-CN.md)；安装指南见 [docs/INSTALL.zh-CN.md](docs/INSTALL.zh-CN.md)。
