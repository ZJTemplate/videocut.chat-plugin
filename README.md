# videocut.chat

让剪辑能力进入 Codex、MCP 和自动化流程。

`videocut.chat` 是给 Codex、Claude、Cursor、Qwen Code、n8n 和自有服务使用的视频工具插件。它把字幕解析、项目编辑、花字样式、本地渲染、云端渲染和编辑器交接封装成 MCP/REST 可调用能力，让视频生产可以进入聊天、脚本和工作流。

当前版本：`0.3.1`

## 适合谁

- 想在 Codex 或其他 MCP 宿主里用自然语言修改视频的人。
- 想把字幕、花字、渲染任务接入 n8n 或内部系统的团队。
- 已经有 videocut.chat / platform.zjtemplate.com 账户，需要本地或云端渲染能力的用户。
- 需要保留可编辑工程，而不只是拿到一个最终 MP4 的视频生产流程。

如果你只想在线剪一个视频，可以直接使用 [videocut.chat](https://videocut.chat) 或 [edit.videocut.chat](https://edit.videocut.chat)。这个仓库面向插件、MCP 和自动化接入。

## 支持什么

- 本地剪辑：读取本机素材，创建项目，修改字幕、样式和时间轴。
- 本地渲染：在已授权的本机运行时里导出 MP4 和可编辑工程。
- 云端渲染：上传素材后由云端处理，适合 n8n、服务端和无本地渲染环境的场景。
- 字幕处理：解析 SRT、VTT、ASS，并把字幕放进项目。
- 花字样式：查询可用样式，检查单条字幕样式，调整颜色、大小、透明度、位置等参数。
- MCP 接入：支持 Codex、Claude Desktop、Claude Code、Cursor、Qwen Code 和其他 stdio MCP 客户端。
- REST 接入：启动本地或远端 HTTP 服务，让脚本和业务系统调用同一套工具。
- n8n 自动化：上传素材、提交渲染、轮询任务、下载成片。
- 编辑器交接：渲染后保存到远端编辑流程，继续在网页编辑器里微调。

底层命令仍叫 `saycut-tools`，工具名仍使用 `saycut_*` 前缀，这是为了兼容已有集成；对外产品名是 `videocut.chat`。

## 下载

当前 release 文件在 [releases/v0.3.1](releases/v0.3.1/)：

| 文件 | 用途 |
| --- | --- |
| [saycut_tools-0.3.1-py3-none-any.whl](releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl) | MCP 服务、本地 REST 网关、样式资源和命令行工具 |
| [videocut-chat-plugin-0.3.1.zip](releases/v0.3.1/videocut-chat-plugin-0.3.1.zip) | 可分发的插件配置和 skill |
| [SHA256SUMS](releases/v0.3.1/SHA256SUMS) | 文件校验和 |

下载后建议先校验：

```bash
python3 scripts/verify_release.py
```

## 安装

前提：

- Python 3.11 或更新版本。
- FFmpeg 和 ffprobe 在 PATH 中。
- 一个可用于授权的 platform.zjtemplate.com 账户。
- 如果要本地渲染，还需要本机运行时、SDK、样式资源和对应权益。

安装到隔离目录：

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py

python3 scripts/install_isolated.py \
  --wheel releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl \
  --allow-root "/绝对路径/视频目录" \
  --download-resources \
  --asr \
  --download-model
```

安装脚本会在 `~/.local/share/saycut-plugin` 创建私有 Python 环境，不会修改全局 site-packages。完成后会打印三个路径：

- `python`：私有 Python 解释器。
- `config`：当前机器的 `saycut.json`。
- `integrations`：为 Codex、Claude、Cursor、Qwen 等宿主生成的配置文件。

检查环境：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
"<python>" -I -m saycut_tools.cli --config "<config>" call saycut_capabilities --json '{}'
```

如果机器上还没有本地渲染资源，能力检查仍然应该返回，并说明缺少哪些前置条件。这表示工具安装成功，但还不能本地导出视频。

## 授权

本地渲染需要本机运行时、SDK、样式资源、FFmpeg 和账户授权都可用：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login
"<python>" -I -m saycut_tools.cli --config "<config>" account status
```

云端渲染使用云端账户或网关 token。本地 SDK 授权不等于云端消费授权。纯 stdio 宿主可以先跑：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud
```

任何上传素材或云端渲染都必须显式同意：

```json
{
  "allow_cloud_processing": true
}
```

## 接入 MCP 宿主

使用安装脚本生成的配置文件，不要直接复制别人的绝对路径：

| 宿主 | 生成文件 |
| --- | --- |
| Codex | `codex.toml`，或注册 `plugins/videocut-chat/` 为本地插件源 |
| Claude Desktop | `claude-desktop.json` |
| Claude Code | `claude-code.mcp.json` |
| Cursor | `cursor.mcp.json` |
| Qwen Code | `qwen.settings.json` |
| 其他 MCP 客户端 | 使用生成的 stdio MCP 配置 |

手写 stdio MCP 配置时，结构如下：

```json
{
  "mcpServers": {
    "videocut-chat": {
      "command": "/absolute/path/to/python",
      "args": [
        "-m",
        "saycut_tools.cli",
        "--config",
        "/absolute/path/to/saycut.json",
        "mcp"
      ]
    }
  }
}
```

新开一个对话后，先确认 `saycut_capabilities` 可见，再开始渲染任务。

## REST 和 n8n

启动本地 REST 服务：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" serve --host 127.0.0.1 --port 8765
TOKEN=$(cat "$(jq -r .data_dir "<config>")/api-token")
curl -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://127.0.0.1:8765/v1/tools/saycut_capabilities \
  -d '{}'
```

n8n 建议按这个流程接：

1. 上传素材到 `/v1/assets/upload`，拿到 `asset_id`。
2. 调用 `saycut_render_video` 或 `saycut_render_project`。
3. 用 `saycut_get_job` 轮询状态。
4. 任务成功后用返回的下载地址取回结果。

HTTP 或远端工作流不能直接传本机文件路径，必须先上传素材。

## 常用工具

- `saycut_capabilities`：查看环境、限制和缺失项。
- `saycut_list_styles` / `saycut_get_style`：查询样式。
- `saycut_parse_subtitles`：解析字幕。
- `saycut_create_project` / `saycut_edit_project` / `saycut_update_project` / `saycut_get_project`：创建和修改项目。
- `saycut_inspect_caption_style` / `saycut_style_captions`：查看和调整字幕样式。
- `saycut_render_video` / `saycut_render_project`：提交渲染任务。
- `saycut_get_job` / `saycut_cancel_job` / `saycut_job_events`：查询、取消和订阅任务。
- `saycut_prepare_upload` / `saycut_complete_upload`：云端上传流程。
- `saycut_editor_handoff` / `saycut_save_to_edit`：保存到远端编辑流程。

## 边界

- 本地渲染不会静默上传素材。
- 云端处理必须由用户明确同意。
- 不要把 token、证书、私有配置或客户素材提交到仓库。
- 不要把网关 Bearer token 附加到 OSS 签名下载地址。
- 不要编造字幕时间轴或字级对齐。
- 只有 `saycut_editor_handoff` 返回 `integration_status: ready` 时，才说明可以打开远端编辑器继续微调。

## 支持

可复现问题请提交 [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues)，附 OS、Python 版本、插件版本和脱敏诊断。不要上传凭证或私有视频；如果凭证已经泄露，先在平台撤销后再反馈问题。
