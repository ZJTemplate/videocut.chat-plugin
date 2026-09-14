# n8n + videocut.chat

The operator-token workflows were executed with n8n 2.38.7 on 2026-09-14. Version 0.2.3 adds personal OAuth examples. Files contain no credentials and do not install a community node.

## English

**Separate cloud consent:** use an OAuth token with `account:read video:cloud`, not a website login token or local-only SDK grant. Generation uses the platform balance and existing GenVideo rates. Automatic ASR currently reserves CNY 6 against the duration ceiling, then settles reported usage and refunds the difference; failed/cancelled tasks refund the reservation. Legacy `usage={}` settles to zero until the worker reports real usage.

### Personal OAuth (0.2.3)

Import `mcp-check.oauth.json`. Select an **MCP OAuth2 API** credential, enable dynamic registration, and set Server URL and Resource URL to `https://mcp.zjtemplate.com/mcp`. Connect through the platform consent page and approve it yourself. This matches n8n's [MCP OAuth2 credential definition](https://github.com/n8n-io/n8n/blob/master/packages/%40n8n/nodes-langchain/credentials/McpOAuth2Api.credentials.ts).

For `cloud-render.oauth.json` or the optional custom node, create a generic **OAuth2 API** credential. Copy its displayed callback URL, then register exactly that URL:

```bash
curl --fail-with-body https://mcp.zjtemplate.com/register \
  -H 'Content-Type: application/json' \
  --data '{"client_name":"My n8n","redirect_uris":["https://YOUR-N8N-HOST/rest/oauth2-credential/callback"],"grant_types":["authorization_code","refresh_token"],"response_types":["code"],"token_endpoint_auth_method":"client_secret_basic","scope":"account:read video:cloud"}'
```

Use the returned client ID/secret only in n8n's credential store. Configure Grant Type **PKCE**, Authorization URL `https://mcp.zjtemplate.com/authorize`, Access Token URL `https://mcp.zjtemplate.com/token`, scope `account:read video:cloud`, and Authentication **Header**. Add Auth URI Query Parameters `resource=https%3A%2F%2Fmcp.zjtemplate.com%2Fmcp`. Do not disable TLS verification. n8n's [generic OAuth2 credential fields](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/credentials/OAuth2Api.credentials.ts) include PKCE and client authentication.

OAuth endpoint/security regression checks and both custom-node request branches passed. An actual user-approved n8n OAuth UI session has not yet been accepted; do not interpret these templates as that result.

### Operator Token Compatibility

1. Import `mcp-check.json` into n8n.
2. Create a Header Auth credential with name `Authorization` and value `Bearer <your separately provisioned gateway token>`.
3. Select that credential in all three MCP Client nodes, then run manually.
4. Expect capabilities, the available style list and parsed SRT captions. This workflow does not upload media or submit a render.

Use HTTP Streamable and endpoint `https://mcp.zjtemplate.com/mcp`. MCP node output wraps tool results in `structuredContent` and/or `content`; it is not identical to a REST response. This token-based example is for existing operator-managed deployments, not public account onboarding.

### Render a video

Import `cloud-render.oauth.json` for personal OAuth or `cloud-render.json` for an operator token. These are sub-workflows, not file-upload forms. Assign the appropriate credential to Start Render and Check Job. Call from a parent workflow with:

```json
{
  "asset_id": "<asset ID returned by complete_upload>",
  "style_id": "runtime/ZapMotion",
  "allow_cloud_processing": true
}
```

Do not supply `captions`, custom effect parameters or language selection to the currently deployed legacy worker. It performs automatic ASR and returns MP4, not an editable project. Available styles must be discovered from the service.

The video must already be uploaded: call `saycut_prepare_upload`, PUT the exact binary bytes to the returned upload URL with its returned headers, then call `saycut_complete_upload`. Do not attach the gateway Authorization header to the OSS PUT. A path on your laptop is not readable by an n8n Cloud instance or the FC gateway.

The workflow polls every three seconds, outputs the completed job on success and fails on a terminal error or its polling timeout. If it times out, check/cancel the existing job before starting again. Its submission key uses the n8n execution ID; restarting the entire workflow creates a new key and can create another paid task. Download URLs in results must not receive the gateway token.

### Scope

Actual n8n MCP Client and HTTP Request workflow execution were verified. This does not establish n8n Cloud plan availability, AI Agent model selection quality, or a public npm/community-node listing. The source project's custom node is optional and is not needed for these workflows.

## 简体中文

个人用户需要单独确认 `account:read video:cloud` 云端授权，不能直接使用网站登录 token 或旧本地 SDK 凭据。云端沿用平台余额与 GenVideo 价格：自动 ASR 当前预留 6 元，结束后按上报用量结算，失败或取消退款；旧 worker 的空用量按原规则结算为 0。

- 个人 MCP：导入 `mcp-check.oauth.json`，创建 MCP OAuth2 API 凭据，开启动态注册，Server URL / Resource URL 均填写 `https://mcp.zjtemplate.com/mcp`，打开平台亲自授权。
- 个人 HTTP：导入 `cloud-render.oauth.json`，按上方步骤使用 n8n 实际回调地址注册客户端。通用 OAuth2 API 选择 PKCE、Header、对应授权/令牌地址和云端 scope，Client ID/Secret 仅存入 n8n 凭据管理。
- 0.2.3 自定义节点修复空 JSON 请求体，并增加 OAuth2 选项和两个字幕参数操作；节点包含 23 个操作，但云端旧 worker 不支持的操作仍会明确拒绝。它没有发布到 npm，也未作为社区节点上架。

- `mcp-check.json`：手动运行，依次检查能力、样式和 SRT 解析，不上传视频、不生成任务。给三个 MCP Client 节点选择 Header Auth 凭据，字段名为 `Authorization`，字段值为 `Bearer <单独开通的网关 token>`。
- `cloud-render.json`：由父工作流调用的子流程，输入已上传完成的 `asset_id`、可用 `style_id` 和明确的 `allow_cloud_processing: true`。给 Start Render、Check Job 两个节点设置凭据。
- 远程地址为 `https://mcp.zjtemplate.com/mcp`，传输选择 HTTP Streamable。无 `.oauth` 后缀的示例保留给已有运营凭据使用，不适合直接作为普通用户开通流程。
- 上传顺序是申请上传地址、向 OSS PUT 视频二进制、确认上传。OSS 请求只用上传授权返回的头信息，不带网关 token。本机路径不能直接传给云端读取。
- 目前线上旧版 worker 自动识别字幕，只输出 MP4，不接受自定义字幕、语言选择、效果参数，也不输出可编辑工程。
- 工作流每三秒查询一次。超时后先检查/取消旧任务，不能盲目重跑。整个 n8n 工作流重新执行会生成新幂等键，可能产生新任务和费用。
- 已在 n8n 2.38.7 使用运营凭据实际运行 MCP Client 和完整 HTTP 合成工作流；本轮 OAuth/请求分支回归不等于用户亲自授权的 n8n OAuth UI 已验收，也不代表 n8n Cloud、AI Agent 或社区节点上架已验收。
