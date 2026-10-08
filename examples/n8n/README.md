# n8n 接入

[返回 README](../../README.md) · [MCP 与 REST 配置](../../docs/INTEGRATIONS.zh-CN.md)

示例使用 n8n 的 MCP Client 和 HTTP Request 节点，不需要额外安装社区节点。JSON 不含凭据；导入后需要自行选择账户凭据。

## 选择工作流

| 文件 | 用途 | 授权方式 |
| --- | --- | --- |
| [mcp-check.oauth.json](mcp-check.oauth.json) | 查询能力、样式并解析示例字幕，不渲染 | 个人 OAuth |
| [cloud-render.oauth.json](cloud-render.oauth.json) | 提交云端渲染、轮询并返回结果 | 个人 OAuth |
| [mcp-check.json](mcp-check.json) | 连接检查 | 已开通的网关 token |
| [cloud-render.json](cloud-render.json) | 云端渲染 | 已开通的网关 token |

后两项供已有运营网关凭据的部署使用。不要用网站登录 token 代替网关凭据。

## 个人 MCP 授权

导入 `mcp-check.oauth.json`，选择 MCP OAuth2 API 凭据，启用动态注册。Server URL 与 Resource URL 均为：

```text
https://mcp.zjtemplate.com/mcp
```

打开平台授权页面，由账户持有人确认。云端处理需要 `account:read video:cloud` 权限；本地 SDK 授权不能代替云端授权。

## HTTP 渲染授权

导入 `cloud-render.oauth.json`，创建通用 OAuth2 API 凭据。复制 n8n 显示的回调地址并注册：

```bash
curl --fail-with-body https://mcp.zjtemplate.com/register \
  -H 'Content-Type: application/json' \
  --data '{"client_name":"My n8n","redirect_uris":["https://YOUR-N8N-HOST/rest/oauth2-credential/callback"],"grant_types":["authorization_code","refresh_token"],"response_types":["code"],"token_endpoint_auth_method":"client_secret_basic","scope":"account:read video:cloud"}'
```

将返回的 Client ID / Secret 存入 n8n 凭据管理。配置：

| 字段 | 值 |
| --- | --- |
| Grant Type | PKCE |
| Authorization URL | `https://mcp.zjtemplate.com/authorize` |
| Access Token URL | `https://mcp.zjtemplate.com/token` |
| Scope | `account:read video:cloud` |
| Authentication | Header |
| Auth URI Query Parameters | `resource=https%3A%2F%2Fmcp.zjtemplate.com%2Fmcp` |

回调地址需与当前 n8n 实例完全一致。给 Start Render、Check Job 节点选择该凭据。

## 上传并渲染

渲染示例是子工作流，不是上传表单。先调用 `saycut_prepare_upload`，按返回地址和头信息上传原始二进制，再调用 `saycut_complete_upload`。远端不能读取电脑上的本地路径，OSS 请求不要附加网关 Bearer token。

从父工作流传入：

```json
{
  "asset_id": "<complete_upload 返回的 asset_id>",
  "style_id": "<saycut_list_styles 返回的可用 style_id>",
  "allow_cloud_processing": true
}
```

先查 `saycut_capabilities`：自定义字幕、效果参数、ASR 和可编辑工程是否支持，取决于当前云端后端。不要根据旧文档推断线上 worker 固定具备或缺少某项能力。费用与余额以能力查询和任务结算结果为准。

工作流每三秒查询任务；成功时返回任务结果，失败或超时则终止。超时后先核查已有任务，勿直接重新提交。幂等键包含 n8n execution ID，重新执行整个工作流可能新建任务并产生费用。

成片下载使用任务返回的实际地址，签名下载地址不附加网关 token。网页微调另行检查 `saycut_editor_handoff` 的状态。

## 验证范围

历史上已在 n8n 2.38.7 执行过运营凭据的 MCP / HTTP 示例；本版更新文档与公开样式默认值，不代表重新完成了真实付费渲染或 n8n OAuth 浏览器授权验收。具体环境需要运行连接检查后再提交业务任务。
