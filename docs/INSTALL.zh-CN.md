# 安装与首次运行

本文档面向第一次安装 `videocut.chat` 插件的用户，配合 [README](../README.zh-CN.md) 的能力介绍阅读。

## 1. 安装

```bash
# 1. 安装 SDK（包含 native 渲染、ASR、可选 cloud 适配）
pip install --user "saycut-tools[asr]"

# 2. 安装本插件
解压 videocut-chat-plugin-<version>.zip 后，把 plugins/videocut-chat/ 目录
放到你的 Agent 客户端的插件目录（Codex/Qwen/Codex 等相同）。
```

> **不要**安装到全局 Python。建议使用 `pip install --user` 或 venv。

## 2. 首次运行：登录 + 续期

打开任意 Agent 客户端并发出指令（例如“给这个本地视频添加花字字幕”）。第一次会让模型
调用 `saycut_account_login`，按提示在浏览器完成授权。

授权完成后，本机 **会自动**：

- **Token**：在 MCP stdio server 与 FastAPI gateway 进程内，每 30 分钟通过后台守护
  线程 (`saycut_tools.keepers.TokenKeeper`) 调用一次轻量 `/mcp/v1/session` 校验，
  检测 token 被吊销；真正需要刷新时由 `AccountClient.authorized` 在 401 触发。
- **License (SDK)**：每 6 小时通过后台守护线程 (`saycut_tools.keepers.LicenseKeeper`)
  检查一次租约；当剩余 TTL 低于 **36 小时** 时，自动向 `/mcp/v1/license/issue`
  申请新租约并写入私有凭据目录，无需用户介入。

> **不要问用户“license 即将过期”**：先调 `saycut_keeper_status` 看一下
> `lease.remaining_seconds`。正常机器永远大于 36h。

## 3. 验证自动续期生效

```bash
# 看 keepers 是否在后台启动
saycut-tools mcp --print-status
# 或重启后：
saycut-tools serve # 起 FastAPI gateway
```

查看日志会看到 `saycut.keepers` 模块的初始化。断网 5 秒再恢复，下次 tick
应当能恢复到 `running=True, last_error=None`。

## 4. 离线 / 沙盒环境

- 离线时 license 自动续期会失败（`last_error = account_unavailable`）。
  这时本地渲染用的是磁盘上的旧 lease，**只要 lease 还没过期就能继续用**。
- 真正过期后再恢复网络，下一次 MCP 调用会自动重新拉新 license。

## 5. 排错

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| MCP 一直在 unauthorized | OAuth 连接断了 | `saycut-tools account status`，必要时重新走一遍 `login` |
| `keeper_status.license.last_error` 是 `entitlement_required` | 账号订阅暂停 | 联系平台端 |
| `keeper_status.token.detail.revoked=true` | token 被吊销（最常见的：用户主动改密） | 重新走 `login` |
| 渲染时 `invalid_personal_license` | lease 文件损坏或没写 | `rm ~/.local/share/saycut/private/sdk/license.txt` 然后重渲一次 |

## 6. 跑单元测试（可选）

```bash
cd path/to/videocut.chat-server
python3 scripts/verify_all.py
```

跑通即代表本机 keepers + 编辑器入口 + MCP render 三组契约都符合预期。

## 7. 云端渲染协议

- 本地 SDK 0.3.0+ 的云端提交走 `mcp.zjtemplate.com`，widget 名 = `tid` = `McpRender`
- 不再使用 `api.dalipen.com` / `GenVideo`
- 同一份工程文件会通过 `editable-bundle` 路由传到浏览器端编辑器，用户既能继续在 chat 里微调也能打开网页精修
- 老 worker（tid=`saycut_tools_v1`）0.3.0 仍兼容作为过渡别名

## 8. 上传到云端工程库：`saycut_save_to_edit`

需要把本地渲染结果同步到 `mcp.zjtemplate.com` 的 edit-project 库时调：

```bash
saycut-tools mcp
# 在对话里调用 saycut_save_to_edit { project_id, revision }
```

返回结构：

```json
{
  "project_id": "proj_demo",
  "revision": 1,
  "cloud_edit_project_id": "edit-proj-007",
  "created": true,
  "bytes": 158
}
```

后续同 `project_id` 再发起云端渲染，`mcp.zjtemplate.com` 后端会自动读取最新配置。

## 9. chat ↔ editor 双通道

当 chat 在右侧面板打开 `edit.videocut.chat/editor?file=…` 时，会自动走双通道：
- `editor → host`: iframe 在每次编辑后发 `editor:dirty`，宿主通过 `host_bridge.js` 把它转成 `saycut_edit_project`
- `host → editor`: chat 端发 `chat:apply_project` 推送最新工程到 iframe

完整的 envelope 协议在 `verify_dual_channel.py` (Node) 里被测试过，确保双向消息都能正确传递。
