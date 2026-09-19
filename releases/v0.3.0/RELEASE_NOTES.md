# videocut.chat 0.3.0 (Beta)

[English](#english) | [简体中文](#简体中文)

## 简体中文

- 新增 McpRender 编辑库客户端（`mcp_render.py`）：向 `mcp.zjtemplate.com` 的 `POST /mcp/v1/edit-projects` 镜像工程修订版的传输层，为跨设备继续剪辑做铺垫。该端点由平台侧控制发布，本仓库不宣称其已对公网受理。
- 本地网关新增 `GET /v1/jobs/{job_id}/editable-bundle`：渲染成功的任务可直接导出可编辑工程 ZIP，编辑器 `?file=` 深链可凭票据拉取，无需重复上传素材。
- MCP 工具面与 0.2.7 一致（渲染/账号 27 项 + `saycut_keeper_status`）——`saycut_save_to_edit` 工具的对外暴露发生在 0.3.1；keepers 续期能力随包保留。
- 计费、数据库、许可证策略、全局 Python 包均不变；不覆盖旧发行文件；未发布到 PyPI 或官方市场。

## English

- New McpRender edit-library client (`mcp_render.py`): transport for mirroring project revisions to `POST /mcp/v1/edit-projects` on `mcp.zjtemplate.com`. The endpoint's public availability is owned by the platform; this release does not claim it is accepting traffic.
- Local gateway route `GET /v1/jobs/{job_id}/editable-bundle`: a succeeded render exports its editable project ZIP, and the editor `?file=` deep link can pull it with the job ticket without re-uploading media.
- MCP tool surface unchanged from 0.2.7 (27 render/account operations plus `saycut_keeper_status`); `saycut_save_to_edit` becomes a callable tool in 0.3.1. Keepers renewal ships along.
- No changes to billing, database, license policy or global Python packages; earlier artifacts remain; no PyPI or marketplace publication.
