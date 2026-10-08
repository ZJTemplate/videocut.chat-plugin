# 网页微调与工程回流

## 打开工程

先检查任务是否真正生成了可编辑产物。

- 云端任务：调用 `saycut_editor_handoff`，检查 `integration_status`。仅在返回 `ready` 时提供其生成的 `editor_url`；其他状态如 `editor_bridge_required` 需如实说明。
- 本地任务：展示本机 editable bundle 路径，使用网页编辑器的导入工程功能。不要把 loopback 地址宣传为其他设备可访问的链接，也不要自动开隧道。
- 保存到云端编辑库：调用 `saycut_save_to_edit`，需要单独云端授权。根据返回值判断是否已保存，不能把保存成功等同于网页已成功打开。

使用工具返回的交接链接，不自行拼接账户 token 或签名下载地址。网关 Bearer 凭据不得发给 OSS 域名。云端能力随部署不同，以实时能力查询为准。

## 接收修改后的工程

网页导出包使用 `saycut.project.bundle` v1，包含 `project.json` 和 `resource/`。项目时间轴位于 `project.json` 的 `timelines` 中，通常是 JSON 字符串。

SDK 公共工具接收 `ProjectSpec`，没有通用 `sky_file` 参数，不能将原始 .sky 或工程 ZIP 当视频路径传给 `saycut_render_video`。

1. 读取工程，确认资源、轨道、字幕和时间码。多时间轴先确认要渲染哪个。
2. 将可表达的剪辑和字幕转换为 `ProjectSpec` 的 `clips`、`captions` 及已支持的样式参数。
3. 资源必须在已授权的本地根目录内；云端使用前须经用户同意上传。
4. 调用 `saycut_create_project` 或 `saycut_update_project`，再渲染返回的工程修订版。
5. 遇到 ProjectSpec 不能表达的原生效果或轨道结构，说明具体缺口，保留原包，不宣称无损回流。

只包含单视频和字幕的工程也可用 `saycut_render_video`，但其输入必须是媒体文件及结构化字幕。

内嵌网页宿主可以通过编辑器桥接同步修改；Codex / Claude Code 等 CLI 宿主没有 iframe，使用文件回流，不承诺实时双向同步。
