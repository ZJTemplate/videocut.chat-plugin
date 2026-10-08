# videocut.chat

让剪辑能力进入 Codex、MCP 和自动化流程。

这个插件把 `videocut.chat` 的字幕解析、项目编辑、花字样式、本地渲染、云端渲染和编辑器交接能力暴露给 Codex、Claude、Cursor、Qwen Code、n8n 和其他 MCP/REST 客户端。

当前版本：`0.3.2`

## 支持什么

- 本地剪辑：读取本机素材，创建项目，修改字幕、样式和时间轴。
- 本地渲染：在已授权的本机运行时里导出 MP4 和可编辑工程。
- 云端渲染：上传素材后由云端处理，适合自动化、批量任务和无本地渲染环境的场景。
- 字幕处理：解析 SRT、VTT、ASS。
- 花字样式：查询样式，检查字幕样式，调整颜色、大小、透明度和位置。
- MCP 接入：支持 Codex、Claude Desktop、Claude Code、Cursor、Qwen Code 和其他 stdio MCP 客户端。
- REST 和 n8n：启动 HTTP 服务后，可上传素材、提交渲染、轮询任务并下载成片。
- 编辑器交接：渲染后保存到远端编辑流程，继续人工微调。

底层命令仍叫 `saycut-tools`，工具名仍使用 `saycut_*` 前缀，这是为了兼容已有集成；对外产品名是 `videocut.chat`。

## 安装

推荐使用仓库根目录的安装脚本：

```bash
python3 scripts/verify_release.py
python3 scripts/install_isolated.py \
  --wheel releases/v0.3.2/saycut_tools-0.3.2-py3-none-any.whl \
  --allow-root "/绝对路径/视频目录" \
  --download-resources \
  --asr \
  --download-model
```

安装完成后脚本会打印：

- `python`：私有 Python 解释器。
- `config`：当前机器的 `saycut.json`。
- `integrations`：为 Codex、Claude、Cursor、Qwen 等宿主生成的配置文件。

检查环境：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
"<python>" -I -m saycut_tools.cli --config "<config>" call saycut_capabilities --json '{}'
```

如果机器上还没有本地渲染资源，能力检查仍然会返回，并说明缺少哪些前置条件。这不是安装失败，只是表示当前不能直接本地导出视频。

## 授权

本地渲染需要本机运行时、SDK、样式资源、媒体工具和账户授权都可用。媒体工具可由 `setup-resources` 自动准备：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login
"<python>" -I -m saycut_tools.cli --config "<config>" account status
```

云端渲染使用云端账户或网关 token。本地 SDK 授权不等于云端消费授权。纯 stdio 宿主可以先跑：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud
```

涉及上传素材或云端渲染时，调用参数必须显式带上：

```json
{
  "allow_cloud_processing": true
}
```

## 在 Codex 里使用

安装并启用插件后，可以直接描述剪辑需求：

```text
读取这个视频，给 0-2 秒加一句“新品上线”，使用可用的动效字幕样式，渲染一个竖屏 MP4。
```

推荐调用顺序：

1. `saycut_capabilities` 检查环境。
2. `saycut_list_styles` 找到真实可用样式。
3. `saycut_parse_subtitles` 或 `saycut_create_project` 准备字幕和项目。
4. `saycut_render_video` 或 `saycut_render_project` 提交渲染。
5. `saycut_get_job` 查询任务状态和结果。

## 配置 MCP

使用安装脚本生成的配置文件，不要直接复制别人的绝对路径：

- Codex：`codex.toml`
- Claude Desktop：`claude-desktop.json`
- Claude Code：`claude-code.mcp.json`
- Cursor：`cursor.mcp.json`
- Qwen Code：`qwen.settings.json`

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

n8n 建议按“上传素材 -> 渲染 -> 查询任务 -> 下载结果”的流程接：

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

## 使用边界

- 本地渲染不会静默上传素材。
- 云端处理必须由用户明确同意。
- 不要把 token、证书、私有配置或客户素材提交到仓库。
- 不要把网关 Bearer token 附加到 OSS 签名下载地址。
- 不要编造字幕时间轴或字级对齐。
- 只有 `saycut_editor_handoff` 返回 `integration_status: ready` 时，才说明可以打开远端编辑器继续微调。
