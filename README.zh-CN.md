# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

让 AI 助手为视频添加花字字幕、编排画面，并保留可编辑工程。底层使用带许可证校验的 `template_generator` 原生引擎。

**当前版本：0.2.5 · 受控内测 · 已在 macOS 验证私有安装及发行资源的真实合成。**

这是插件和 Python 工具包的公开发行仓库，不是双击即用的原生应用，也不代表已经发布到 PyPI 或上架官方插件市场。

## 能做什么

- 本地识别语音，使用已安装的花字与动效资源添加字幕。
- 通过 MCP 创建、读取和修改视频工程，无需模型直接编写底层工程 JSON。
- 导出 MP4、SkyMedia `.sky` 工程及包含引用资源的可编辑 ZIP。
- 查询进度、取消运行中的任务，通过幂等键避免重试重复创建任务。
- 本地片段支持 `fit=contain` 留边和 `fit=cover` 居中裁切，保持比例；旧工程默认行为不变。
- 通过本地 MCP、多宿主配置，或单独授权的个人云端连接接入。

目录包含 224 个条目。新版 wheel 已包含 211 个样式所需的资源和回退字体，另 13 个条目需要另行提供资源。资源可用不等于所有语言、任意字幕长度都能得到理想视觉效果。

## 下载

| 文件 | 用途 |
| --- | --- |
| [Python wheel](releases/v0.2.5/saycut_tools-0.2.5-py3-none-any.whl) | `saycut-tools` 工具程序、MCP 服务和样式资源 |
| [插件 ZIP](releases/v0.2.5/videocut-chat-plugin-0.2.5.zip) | 通用插件配置与视频 Skill |
| [SHA256SUMS](releases/v0.2.5/SHA256SUMS) | 两个发行包的校验和 |
| [版本说明](releases/v0.2.5/RELEASE_NOTES.md) | 验证范围和已知限制 |

**只安装插件 ZIP 不会完成合成环境安装。** wheel 包含 Python 代码、效果资源和带许可文件的思源黑体回退字体。SDK Python 包由安装器另行安装；原生运行时和 ASR 模型通过明确的下载选项获取。不内置账号凭据或 SDK 证书。

## 本地安装

### 1. 准备依赖

- Python 3.11 或更新版本，支持 `pip` 和 `venv`。
- PATH 中可访问的 FFmpeg、ffprobe。
- 有本地合成权益的平台账号；附带资源不代表免除 SDK 许可证校验。
- 用于安装依赖、明确下载模型、账号授权和许可证校验的网络连接。

安装器通过 `--download-resources` 下载并校验固定版本的原生运行时。已有运行时可改用 `--runtime-dir` 指定包含 `skymedia/` 的目录。Windows/Linux 有配置适配，但本版本尚未完成这些系统的原生合成验收。

### 2. 下载并校验

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py
```

### 3. 运行独立安装器

将示例路径替换为实际存在的目录。以下命令适用于 macOS/POSIX shell。

```bash
python3 scripts/install_isolated.py \
  --wheel releases/v0.2.5/saycut_tools-0.2.5-py3-none-any.whl \
  --allow-root "/absolute/path/to/videos" \
  --download-resources --asr --download-model
```

安装器在 `~/.local/share/saycut-plugin` 下创建私有环境，安装 wheel 和 `p-template-generator==1.2.17`，并生成匹配当前电脑路径的接入文件。`--asr` 安装并启用本地识别，`--download-model` 下载模型。**不会覆盖全局 pip 包，也不会替换用户已有的 `template_generator`。** 原生 SDK 与 cloud/deploy 依赖需分开环境，其 Click 版本要求不兼容。

记录安装器返回的 `python`、`config`、`integrations` 路径。下面的占位符必须替换成这些真实路径，不能原样执行。

### 4. 检查就绪状态

以上命令已经准备标准资源。合成前检查依赖：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

下载资源或模型不会上传视频。需要稍后准备时，使用相同 Python/config 前缀运行 `setup-resources`，以及 `configure-asr --backend faster_whisper --model small --download-model`。诊断检查前置条件，不代表每个效果正常或许可证授权下的真实渲染已经成功。

### 5. 接入大模型

使用返回的 `integrations` 目录内生成的配置，**不要直接原样使用本仓库中的通用 manifest**：

| 宿主 | 生成的配置 |
| --- | --- |
| Codex | `codex.toml`；完整本地插件位于 `plugins/videocut-chat/` |
| Claude Desktop | `claude-desktop.json` |
| Claude Code | `claude-code.mcp.json` 或生成的插件目录 |
| Qwen Code | `qwen.settings.json` |
| 其他 MCP 宿主 | 兼容的 stdio 配置 |

通过宿主的 MCP 配置入口合并对应服务，不要覆盖其他设置。若要使用完整的 Codex Skill 流程，需将**安装器生成的插件目录**注册为本地插件来源。仅 clone 仓库不会自动安装或注册插件。新建对话，确认可以调用 `saycut_capabilities`。

首次使用时，按插件给出的授权链接打开[平台](https://platform.zjtemplate.com)，登录并亲自确认授权。凭据和短期 SDK 证书保存在插件私有目录，不写入插件 manifest。

可以这样开始：“为这个本地视频添加中文花字字幕，并保留可编辑工程。”请复核识别结果、选择可用样式，并等待返回的任务完成。

## 隐私与授权

本地合成不会自动上传视频，也不会在失败时静默转到云端。账号与许可证仍会在线校验，因此“本地优先”不等于完全离线。云端处理需明确授权，本地输入和输出不会自动删除。

不要提交 token、SDK 证书、私有配置或客户素材。公开可下载不代表 SDK、字体、效果素材已开放源码或允许商业再分发；分别遵循相应条款。wheel 内的 Python 代码可查看，打包不是加密。

## 云端与兼容性边界

云端 MCP 地址为 `https://mcp.zjtemplate.com/mcp`。0.2.3 已增加 OAuth 发现、动态客户端注册、PKCE、令牌轮换/撤销和平台确认页。请求 scope 为 `account:read video:cloud`；网站登录 token 和旧本地授权不能直接当云端凭据，也不能给用户分发管理员 token。

仅支持 stdio 的宿主，可先运行 `"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud`，亲自确认授权后使用生成的 `remote-mcp` 配置。它使用可自动续期的独立个人凭据，不替换原有本地 SDK 授权。

云端沿用平台 GenVideo 价格和余额体系。自动 ASR 按时长上限预留余额：目前默认 600 秒、0.01 元/秒时预留 6 元，**不是每次固定收 6 元**。结束后按模块实际用量结算，多余预留、失败及取消任务退回。当前旧 worker 上报 `usage={}`，按现有规则最终收费为 0；完整生产计量仍依赖 worker 上报真实用量。

已验证的旧版云端链路开放一个预设及 MP4 输出，尚未提供本地全部效果或可编辑云端工程。`edit.videocut.chat` 尚未部署编辑器桥接，不能把生成交接链接描述为已经实现在线编辑。

0.2.5 部署后的三个真实远端任务均完成，上传至下载约 66、66、96 秒，包括 MCP、REST 和幂等重试；中文素材约 5 秒，英文素材约 86 秒。使用的是运营验收凭据，不等于个人 OAuth、扣费已完成端到端验收，也不足以给出生产 SLA。短视频仍需约一分钟，云端能力边界见下方验收记录。

0.2.5 同时包含非法输入、字幕文件、厂商调用授权和原生进度文件容错修复。画面适配不会自动解决长字幕换行、字体缺字或装饰越界。非方形像素、带旋转信息的视频先按 Skill 的 FFmpeg 步骤标准化再导入；此步骤重新编码，不覆盖原片。详见 [0.2.5 验收](docs/ACCEPTANCE-0.2.5.zh-CN.md)。

本版本提供多宿主适配文件。已在独立的 n8n 2.38.7 环境验证原生 MCP Client 和 HTTP 云端合成工作流，使用的是运营配置的凭据；0.2.3 另提供个人 OAuth2 配置。这不代表每个宿主的 OAuth 界面均已验收：Claude/Qwen 客户端、n8n Cloud、AI Agent 自主选工具或 DeepSeek/豆包消费者聊天入口仍未验收。

参见 [n8n 示例和接入说明](examples/n8n/README.md)、[0.2.3 验收记录](docs/ACCEPTANCE-0.2.3.zh-CN.md)及[0.2.2 历史验收](docs/ACCEPTANCE-2026-09-14.zh-CN.md)。协议兼容不代表已上架官方市场，也不保证每个聊天客户端都支持视频附件。

## 支持

通过 [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues) 提交可复现问题，附操作系统、Python/包版本及脱敏诊断。不要上传凭据或私人视频。若凭据泄露，应先通过平台账号撤销对应连接，再提供脱敏报告。
