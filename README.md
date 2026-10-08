<div align="center">

# videocut.chat

**用自然语言剪辑，交付视频与可编辑工程。**

面向 Agent 的视频工具，支持字幕、花字、时间轴编辑与本地 / 云端渲染。

[![Release](https://img.shields.io/github/v/release/ZJTemplate/videocut.chat-plugin?color=16875d)](https://github.com/ZJTemplate/videocut.chat-plugin/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](docs/INSTALL.zh-CN.md)
[![MCP](https://img.shields.io/badge/MCP-stdio%20%7C%20HTTP-555555)](docs/INTEGRATIONS.zh-CN.md)

[快速开始](#快速开始) · [效果预览](#效果预览) · [接入文档](docs/INTEGRATIONS.zh-CN.md) · [更新记录](CHANGELOG.md) · [在线剪辑](https://videocut.chat)

</div>

在 Codex、Claude、Cursor、Qwen Code 或 WorkBuddy 中描述剪辑需求，由工具处理素材、字幕和渲染；也可以通过 MCP、REST 或 n8n 把同一套能力接入业务流程。输出 MP4，并在所选渲染后端支持时保留工程，继续修改字幕、样式和时间轴。

## 效果预览

| 柔和淡入 · Soft Fade In | 滑动打字 · Slide Typewriter | 逐词放大 · Word Zoom |
| :---: | :---: | :---: |
| ![柔和淡入](plugins/videocut-chat/skills/videocut-chat-video/assets/previews/SoftFadeIn.webp) | ![滑动打字](plugins/videocut-chat/skills/videocut-chat-video/assets/previews/SlideTypewriter.webp) | ![逐词放大](plugins/videocut-chat/skills/videocut-chat-video/assets/previews/WordZoom.webp) |

预览来自官方样式资源，随 skill 一起分发。实际可用样式及账户权限以工具查询结果为准。用户按中英文名称和效果选择，内部模板映射由 SDK 处理。

## 核心能力

| 能力 | 交付内容 |
| --- | --- |
| 字幕与花字 | 语音识别、SRT / VTT / ASS 导入、样式预览，以及颜色、字号、位置调整 |
| 视频编排 | 组合素材、修改字幕和时间轴，保存可继续编辑的项目修订版 |
| 本地渲染 | 在已授权的本机运行时导出 MP4；媒体默认留在本机 |
| 云端渲染 | 用户同意上传后提交任务，查询进度并下载结果；按账户权益和用量结算 |
| 网页微调 | 获取支持的工程交接链接，或把本地工程包导入 [网页编辑器](https://edit.videocut.chat) |
| 工作流接入 | stdio / HTTP MCP、REST，以及可导入的 n8n 工作流 |

## 快速开始

当前发布：**[v0.3.3](https://github.com/ZJTemplate/videocut.chat-plugin/releases/tag/v0.3.3)**。本地安装需要 Python 3.11+；渲染需要平台账户及对应权益。安装器可下载私有 FFmpeg / ffprobe，无需先安装系统 FFmpeg。

### 1. 安装

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py
python3 scripts/install_isolated.py \
  --wheel releases/v0.3.3/saycut_tools-0.3.3-py3-none-any.whl \
  --allow-root "/你的素材目录" \
  --download-resources
```

将素材目录替换为已存在的绝对路径。安装器会创建私有环境，并输出 `python`、`config`、`integrations` 三个路径。需要本地语音识别时，再加 `--asr --download-model`；已有字幕无需下载识别模型。

### 2. 接入并授权

按[接入文档](docs/INTEGRATIONS.zh-CN.md)使用 `integrations` 中生成的宿主配置和插件，重新打开会话。先运行 `saycut_capabilities` 检查环境，再按工具返回的链接完成账户授权。

也可以在终端使用安装器输出的路径登录：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login
```

只使用云端 MCP 时，可直接连接 `https://mcp.zjtemplate.com/mcp` 并完成 OAuth 授权，无需安装本地渲染运行时。见[云端接入](docs/INTEGRATIONS.zh-CN.md#云端-mcp)。

### 3. 开始剪辑

向已接入工具的 Agent 提出具体需求，例如：

> 给这个视频加中文字幕，先展示三种可用样式。选好后在本地渲染，返回 MP4 和可编辑工程。

> 把第二句字幕放大 20%，保留其他字幕和时间轴，重新导出。

> 我同意上传这个视频进行云端处理。生成字幕视频，完成后提供可用的网页微调入口。

工具会返回任务 ID；任务成功后才有可下载的成片。云端自定义字幕、工程导出和网页交接能力以 `saycut_capabilities` 与任务返回值为准。

## 接入方式

| 使用场景 | 入口 |
| --- | --- |
| Codex / Claude / Cursor / Qwen Code | [本地 MCP 与 skill 配置](docs/INTEGRATIONS.zh-CN.md#本地-mcp-与-skill) |
| WorkBuddy | [自定义 MCP 接入](docs/INTEGRATIONS.zh-CN.md#workbuddy) |
| 支持 HTTP MCP 的客户端 | [云端 MCP 与 OAuth](docs/INTEGRATIONS.zh-CN.md#云端-mcp) |
| 脚本和业务服务 | [REST API](docs/INTEGRATIONS.zh-CN.md#rest-api) |
| n8n 自动化 | [连接检查与云端渲染示例](examples/n8n/README.md) |

## 文档

- [安装、授权与升级](docs/INSTALL.zh-CN.md)
- [接入配置与常用工具](docs/INTEGRATIONS.zh-CN.md)
- [字幕样式与参数](plugins/videocut-chat/skills/videocut-chat-video/references/caption-styling.md)
- [版本变更](CHANGELOG.md) · [下载与校验文件](releases/v0.3.3/)

本地渲染需要 SDK 授权；云端处理需要单独的云端授权。服务端更新与本地 skill 安装包分别发布，旧安装需按升级文档更新。本仓库未声明开源许可证，运行时与平台服务的使用受相应授权约束。

## 问题反馈

通过 [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues) 提交复现步骤、操作系统、插件版本及脱敏错误信息。请勿附带账户凭据或私有素材。
