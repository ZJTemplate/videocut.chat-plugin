# 接入配置

[返回 README](../README.md) · [安装与升级](INSTALL.zh-CN.md)

## 本地 MCP 与 skill

安装器生成的 `<integrations>` 目录包含当前机器的绝对路径：

| 宿主 | 生成文件 |
| --- | --- |
| Codex | `codex.toml` |
| Claude Desktop | `claude-desktop.json` |
| Claude Code | `claude-code.mcp.json` |
| Cursor | `cursor.mcp.json` |
| Qwen Code | `qwen.settings.json` |

将所需配置合并到对应宿主的 MCP 配置，保留已有服务。Codex 可将 `codex.toml` 的服务条目合并到 `~/.codex/config.toml`。不要复制他人机器的 Python 路径或保留文档占位符。

MCP 提供工具，skill 提供使用流程。支持插件的宿主可安装 `<integrations>/plugins/videocut-chat`，其中包含机器适配后的 MCP 配置和 skill，无需再重复注册同一个 MCP 服务。

只安装 skill 时，完整目录为 `plugins/videocut-chat/skills/videocut-chat-video`，需保留 `references` 和 `assets`。Codex 支持将该目录放入 `~/.agents/skills/`；MCP 仍需单独配置。[Codex 官方 skill 文档](https://learn.chatgpt.com/docs/build-skills)

重新打开会话，确认 `saycut_capabilities` 可见。原始下载包里的通用 `saycut-tools` 命令依赖宿主 PATH，本地使用优先选择安装器生成的配置。

## WorkBuddy

在 WorkBuddy 的连接器管理中添加自定义 MCP。下面两种配置按需选择一种，合并时保留已有服务。

**本地剪辑**：先完成[隔离安装](INSTALL.zh-CN.md)，将 `<python>` 和 `<config>` 替换为安装器输出的绝对路径，再添加配置：

```json
{
  "mcpServers": {
    "videocut-chat": {
      "type": "stdio",
      "command": "<python>",
      "args": ["-I", "-m", "saycut_tools.cli", "--config", "<config>", "mcp"]
    }
  }
}
```

**云端剪辑**：无需本地渲染环境，使用远端地址并按客户端提示完成 OAuth 授权：

```json
{
  "mcpServers": {
    "videocut-chat": {
      "type": "streamableHttp",
      "url": "https://mcp.zjtemplate.com/mcp"
    }
  }
}
```

连接后先让 WorkBuddy 调用 `saycut_capabilities`，确认工具可见；授权和媒体上传要求见[安装与授权](INSTALL.zh-CN.md)及[云端 MCP](#云端-mcp)。不要把账户密钥写进共享配置。

需要 skill 时，使用仓库中 `plugins/videocut-chat/skills/videocut-chat-video` 的完整内容，通过 WorkBuddy 的技能导入功能安装，保留 `SKILL.md`、`references` 和 `assets`。仅安装 skill 不会自动安装渲染运行时或配置 MCP。

以上配置依据 [WorkBuddy 官方连接器文档](https://open.workbuddy.cn/docs/connector)；技能导入参见[官方技能说明](https://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)。这是自定义接入方式，不代表已上架 WorkBuddy 市场；本项目尚未完成 WorkBuddy 客户端内的端到端验收。

## 云端 MCP

在支持 Streamable HTTP 与 OAuth 的 MCP 客户端中添加：

```text
https://mcp.zjtemplate.com/mcp
```

由账户持有人在平台页面确认授权。云端消费需要 `account:read video:cloud` 权限及可用余额。只连接远端服务无需安装本地 Python、FFmpeg 或渲染运行时。

客户端需要 JSON 配置时，典型结构如下；字段以宿主格式为准：

```json
{
  "mcpServers": {
    "videocut-chat": {
      "type": "http",
      "url": "https://mcp.zjtemplate.com/mcp"
    }
  }
}
```

连接后先调用 `saycut_capabilities`。远端不能读取电脑上的本地路径，上传按 `saycut_prepare_upload` → 向返回地址上传二进制 → `saycut_complete_upload` 执行，再用 `asset_id` 提交任务。上传请求只使用上传授权返回的头信息。

## REST API

本地运行网关：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" serve --host 127.0.0.1 --port 8765
```

在另一个终端中调用工具，`GATEWAY_TOKEN` 使用当前网关生成的 token：

```bash
curl --fail http://127.0.0.1:8765/v1/tools/saycut_capabilities \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

本地 token 位于配置 `data_dir` 下的 `api-token` 文件。远端 REST 使用对应云端授权。下载 OSS 签名地址时不要附加网关凭据。

## 常用工具

| 操作 | 工具 |
| --- | --- |
| 检查环境与账户 | `saycut_capabilities`、`saycut_account_status` |
| 查找样式与预览 | `saycut_list_styles`、`saycut_get_style` |
| 导入字幕 | `saycut_parse_subtitles` |
| 创建、读取和修改工程 | `saycut_create_project`、`saycut_get_project`、`saycut_edit_project`、`saycut_update_project` |
| 调整字幕样式 | `saycut_inspect_caption_style`、`saycut_style_captions` |
| 渲染与查询 | `saycut_render_video`、`saycut_render_project`、`saycut_get_job`、`saycut_cancel_job` |
| 网页微调与保存 | `saycut_editor_handoff`、`saycut_save_to_edit` |

工具保留 `saycut_*` 名称以兼容已有集成。参数以当前服务返回的 schema 为准。

## 工程交接

云端任务使用 `saycut_editor_handoff` 返回的链接，并检查 `integration_status`；返回 `ready` 后才表示交接可用。本地任务可以把生成的工程包导入网页编辑器。工程保存、网页打开和渲染成功是不同状态。

`saycut_save_to_edit` 需要云端授权；跨设备访问和资源可达性以返回结果为准。不要自行拼接公开下载地址或把账户凭据放进 URL。

网页导出的工程包不能直接作为 `saycut_render_video` 的视频输入。需要读取工程后转换为工具支持的 `ProjectSpec`，再创建或更新工程并渲染；复杂原生效果未必可以无损映射。

## n8n

使用仓库的 [n8n 示例](../examples/n8n/README.md)：先运行连接检查，再执行上传、提交渲染和任务轮询。示例使用 MCP Client / HTTP Request 节点，不要求安装社区节点。
