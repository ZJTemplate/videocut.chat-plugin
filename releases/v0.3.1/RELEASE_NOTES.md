# videocut.chat 0.3.1 (Beta)

[English](#english) | [简体中文](#简体中文)

## 简体中文

- 新增 `saycut_save_to_edit`：把工程修订版镜像到 `mcp.zjtemplate.com` 的 McpRender 编辑库并返回 `cloud_edit_project_id`，用于跨设备继续剪辑。该云端受理端点由平台侧发布，未受理时工具会明确报错，不影响本地链路。
- 新增随包编辑器桥 `data/editor/host_bridge.js`：内嵌编辑器场景下的双通道 postMessage（`editor:dirty` → `saycut_edit_project`、`chat:apply_project` 回推）。仅对把编辑器作为 iframe 承载的宿主有意义；CLI 宿主（Codex/Claude Code）请使用编辑器导出的工程包回流，技能文档给出了解包配方。
- 承接 0.3.0：`GET /v1/jobs/{job_id}/editable-bundle` 导出 + `edit.videocut.chat` 的 `?file=` 深链注入；编辑器导入侧已支持 SDK 可编辑包、云端 project.json、可编辑 bundle、裸 `.sky` 与 legacy 共五种格式，无需转换器。
- 承接 0.2.7：token/租约静默续期（keepers）与 `saycut_keeper_status` 诊断；本地工具面为 24 项渲染操作 + 4 项账号操作 + `saycut_keeper_status`（0.3.1 净增 `save_to_edit`）。
- CI 将本地 `serve` 端到端流程纳入回归；不覆盖 0.2.x 发行文件；未发布到 PyPI 或官方市场。

此版本仍为受控内测。`save_to_edit` 的跨设备验收依赖平台侧端点上线；编辑器 `?file=` 注入要求文件 URL 公网可读且不带 bearer。本地渲染计时表另行记录，未实测前不对外承诺秒数。

## English

- New `saycut_save_to_edit`: mirrors a project revision to the McpRender edit-library on `mcp.zjtemplate.com` and returns a `cloud_edit_project_id` for cross-device continuation. The acceptance endpoint is platform-owned; until it is live the tool fails loudly without disturbing local flows.
- New bundled editor bridge `data/editor/host_bridge.js`: dual-channel postMessage (`editor:dirty` → `saycut_edit_project`, `chat:apply_project` pushback) for hosts that embed the editor as an iframe. CLI hosts (Codex/Claude Code) should use the exported project-bundle reflow recipe documented in the skill.
- Carries 0.3.0's `GET /v1/jobs/{job_id}/editable-bundle` export plus `edit.videocut.chat` `?file=` deep-link injection; the editor import path now recognizes SDK editable bundles, cloud project.json, editable bundles, bare `.sky` and legacy formats — no converter required.
- Carries 0.2.7's silent token/lease keepers and `saycut_keeper_status`; local tool surface is 24 render operations + 4 account operations + `saycut_keeper_status` (0.3.1 nets `save_to_edit`).
- The isolated `serve` end-to-end flow is covered in CI; 0.2.x artifacts remain intact; no PyPI or marketplace publication.

Controlled beta. Cross-device `save_to_edit` acceptance depends on the platform endpoint going live; `?file=` injection requires a public, bearer-free file URL. Local render timing is tracked separately and is not a marketing claim until measured.
