# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

让 AI 助手为视频添加花字字幕、编排画面，并保留可编辑工程。底层使用带许可证校验的 `template_generator` 原生引擎。

**当前版本：0.2.2 · 受控内测 · 已在配置完整的 macOS 环境验证原生合成。**

这是插件和 Python 工具包的公开发行仓库，不是双击即用的原生应用，也不代表已经发布到 PyPI 或上架官方插件市场。

## 能做什么

- 本地识别语音，使用已安装的花字与动效资源添加字幕。
- 通过 MCP 创建、读取和修改视频工程，无需模型直接编写底层工程 JSON。
- 导出 MP4、SkyMedia `.sky` 工程及包含引用资源的可编辑 ZIP。
- 查询进度、取消运行中的任务，通过幂等键避免重试重复创建任务。
- 通过本地 MCP、多宿主配置，或另行开通的云端网关接入。

目录包含 224 个条目，实际可用数量由资源安装情况决定。测试环境有 211 个可用条目，不代表逐一完成了 211 个效果的视觉验收。

## 下载

| 文件 | 用途 |
| --- | --- |
| [Python wheel](releases/v0.2.2/saycut_tools-0.2.2-py3-none-any.whl) | `saycut-tools` 工具程序及 MCP 服务 |
| [插件 ZIP](releases/v0.2.2/videocut-chat-plugin-0.2.2.zip) | 通用插件配置与视频 Skill |
| [SHA256SUMS](releases/v0.2.2/SHA256SUMS) | 两个发行包的校验和 |
| [版本说明](releases/v0.2.2/RELEASE_NOTES.md) | 验证范围和已知限制 |

**只安装插件 ZIP 不会完成合成环境安装。** wheel 包含 Python 工具代码，不内置原生 SDK、运行时、字体、效果资源、许可证或语音识别模型。

## 本地安装

### 1. 准备依赖

- Python 3.11 或更新版本，支持 `pip` 和 `venv`。
- PATH 中可访问的 FFmpeg、ffprobe。
- 有效授权且匹配操作系统的 TemplateProcess 运行时；运行时目录内应包含 `skymedia/` 及所需原生依赖。
- 已获使用授权的效果资源和字体，以及有本地合成权益的平台账号。
- 用于安装依赖、明确下载模型、账号授权和许可证校验的网络连接。

缺少运行时或资源时，请先通过 videocut.chat 的 SDK 分发渠道或支持联系人获取；本仓库不提供这些资源。Windows/Linux 有配置适配，但本版本尚未完成这些系统的原生合成验收。

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
  --wheel releases/v0.2.2/saycut_tools-0.2.2-py3-none-any.whl \
  --allow-root "/absolute/path/to/videos" \
  --runtime-dir "/absolute/path/to/runtime" \
  --asr
```

安装器在 `~/.local/share/saycut-plugin` 下创建私有环境，安装 wheel 和 `p-template-generator==1.2.17`，并生成匹配当前电脑路径的接入文件。`--asr` 同时安装本地语音识别依赖。**不会覆盖全局 pip 包，也不会替换用户已有的 `template_generator`。**

记录安装器返回的 `python`、`config`、`integrations` 路径。下面的占位符必须替换成这些真实路径，不能原样执行。

### 4. 配置效果和识别模型

绑定可信且已授权的效果文件与回退字体：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" catalog bind \
  --style runtime/ZapMotion \
  --path "/absolute/path/to/ZapMotion/text.fceffect" \
  --fallback-font "/absolute/path/to/licensed-font.ttf"

"<python>" -I -m saycut_tools.cli --config "<config>" configure-asr \
  --backend faster_whisper --model small --download-model

"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

模型需要明确下载，不会因此上传用户视频。诊断检查的是前置条件，不代表所有效果正常或许可证授权下的真实渲染已经成功。未配置原生运行时与资源的新环境应当返回未就绪。

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

云端 MCP 地址为 `https://mcp.zjtemplate.com/mcp`，访问权限另行开通，不能共用管理员 token。公开用户 OAuth、支付退款及全面开放的接入流程尚未完成。

已验证的旧版云端链路开放一个预设及 MP4 输出，尚未提供本地全部效果或可编辑云端工程。`edit.videocut.chat` 尚未部署编辑器桥接，不能把生成交接链接描述为已经实现在线编辑。

本版本提供多宿主适配文件，但尚未验收 Claude/Qwen 客户端会话、真实 n8n 环境或 DeepSeek/豆包消费者聊天入口。协议兼容不代表已上架官方市场，也不保证每个聊天客户端都支持视频附件。

## 支持

通过 [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues) 提交可复现问题，附操作系统、Python/包版本及脱敏诊断。不要上传凭据或私人视频。若凭据泄露，应先通过平台账号撤销对应连接，再提供脱敏报告。
