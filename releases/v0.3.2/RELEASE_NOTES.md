# videocut.chat 0.3.2 (Beta)

这一版把对外体验收拢到“用户能看懂、能安装、能授权、能直接跑”的状态。

## 更新内容

- 新增产品化字幕样式目录：默认返回 `style/*` 这类对外样式 ID，不再把 `runtime/*`、`motion/*` 等内部实现名直接暴露给用户。
- 字幕样式支持中英文展示名：例如 `简约弹跳 / Minimal Bounce`，方便中文用户和海外用户一起选择花字效果。
- 样式列表带预览图地址，Agent、MCP、n8n 可以把效果图展示给用户后再选择样式。
- 本地资源初始化改为使用 SDK 内置的 `ffmpeg` / `ffprobe`，不再要求用户额外安装系统 FFmpeg 才能完成插件资源准备。
- README、Quickstart、安装文档和插件 manifest 已同步到 `0.3.2`。

## Files

- `saycut_tools-0.3.2-py3-none-any.whl`
- `videocut-chat-plugin-0.3.2.zip`
- `SHA256SUMS`
