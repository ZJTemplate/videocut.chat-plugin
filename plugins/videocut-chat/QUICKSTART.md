# videocut.chat 快速开始

当前版本：`0.3.2`。

## 1. 安装

在仓库根目录执行：

```bash
python3 scripts/verify_release.py
python3 scripts/install_isolated.py \
  --wheel releases/v0.3.2/saycut_tools-0.3.2-py3-none-any.whl \
  --allow-root "/绝对路径/视频目录" \
  --download-resources \
  --asr \
  --download-model
```

安装完成后记录脚本打印的 `python`、`config`、`integrations` 三个路径。

## 2. 检查环境

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
"<python>" -I -m saycut_tools.cli --config "<config>" call saycut_capabilities --json '{}'
```

如果缺少本地渲染资源，命令会告诉你缺哪一项。这个状态下仍可做工具发现、字幕解析和项目准备。

## 3. 授权

本地渲染：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login
"<python>" -I -m saycut_tools.cli --config "<config>" account status
```

云端渲染：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud
```

云端处理必须在调用参数中显式传入：

```json
{
  "allow_cloud_processing": true
}
```

## 4. 配置 MCP

使用 `integrations` 目录里生成的文件：

- Codex：`codex.toml`
- Claude Desktop：`claude-desktop.json`
- Claude Code：`claude-code.mcp.json`
- Cursor：`cursor.mcp.json`
- Qwen Code：`qwen.settings.json`

不要直接复制别人的绝对路径。

## 5. REST 和 n8n

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" serve --host 127.0.0.1 --port 8765
```

n8n 按“上传素材 -> 渲染 -> 查询任务 -> 下载结果”接入。HTTP 或远端工作流不能直接传本机文件路径，必须先上传素材拿到 `asset_id`。
