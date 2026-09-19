# 安装与首次运行

本文档面向第一次安装 `videocut.chat` 插件的用户，配合 [README](../README.zh-CN.md) 的能力介绍阅读。目标体验是：**高级用户把仓库地址交给 Codex / Claude Code 这类 agent，agent 自动完成安装、映射与一次浏览器授权**；本文同时给出人工等价步骤。

## 1. 安装（隔离环境，一条命令）

SDK **没有发布到 PyPI**，不要执行 `pip install saycut-tools`（含 `--user`）。唯一受支持的本地安装方式是仓库自带隔离安装器 + GitHub Release 里的 wheel：

```bash
git clone --depth 1 https://github.com/ZJTemplate/videocut.chat-plugin.git ~/videocut.chat-plugin
cd ~/videocut.chat-plugin
python3 scripts/install_isolated.py \
  --wheel releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl \
  --allow-root ~/Movies --download-resources
```

- 前置条件：Python ≥ 3.11、`ffmpeg`/`ffprobe` 在 PATH。
- `--allow-root` 是**媒体授权根目录**（可多次传入，必须已存在），不是安装位置；安装固定落在 `~/.local/share/saycut-plugin`，全程不碰全局 Python。
- `--download-resources` 下载钉死版本的 native runtime、特效与字体（不上传任何素材）；离线或内网机器可省略，之后随时补跑 `setup-resources`。
- 需要离线语音转写再加 `--asr --download-model`（会额外拉 Whisper small 模型，体积较大，建议先问用户）。
- 发布包校验：与同目录 `SHA256SUMS` 比对 wheel/zip 哈希后再安装。

命令输出三段 JSON：`setup-resources` 结果（如 `styles_available: 211, native_runtime_configured: true`）、`integrations` 生成物目录，以及核心 manifest：

```json
{
  "python": "/Users/<you>/.local/share/saycut-plugin/python-<hash>/bin/python",
  "config": "/Users/<you>/.local/share/saycut-plugin/saycut.json",
  "integrations": "/Users/<you>/.local/share/saycut-plugin/integrations",
  "wheel_sha256": "…",
  "global_python_modified": false
}
```

## 2. 映射到宿主（agent 合并，用户零手工）

`integrations/` 内是宿主用的 MCP 配置片段。把 MCP server 指向私有解释器即可（stdio）：

```
command: <manifest.python>
args: ["-I", "-m", "saycut_tools.mcp_server", "--config", "<manifest.config>"]
```

- **Codex**：合并 `[mcp_servers.videocut]` 段到 `~/.codex/config.toml`（含 `"initialize_timeout_ms": 120000`）；已有相同段则跳过。
- **Claude Code**：`claude mcp add-json videocut '<mcp_config 内容>'`。
- 其他宿主：写入其 MCP server 配置的同一组 command/args。

agent 驱动安装（README 五步工作流的第 0 步）与人工执行完全等价；SKILL.md 的 Bootstrap 章节就是给 agent 的说明书。

## 3. 首次运行：登录 + 续期

重连宿主会话（Codex：`/mcp reconnect`），先调 `saycut_capabilities` 确认可用，然后发一条真实指令（例如"给这个本地视频添加花字字幕"）。第一次渲染会以 `entitlement_required` 拒绝——这是许可设计，不是安装失败。让模型走 `saycut_account_login`：它会返回 `platform.zjtemplate.com/mcp/authorize?user_code=…` 的授权链接和 user code，**用户在浏览器里批准一次**，模型用 `saycut_account_complete_login` 轮询直到连接建立。人工等价命令：

```bash
<manifest.python> -I -m saycut_tools.cli --config <manifest.config> account --no-browser start
<manifest.python> -I -m saycut_tools.cli --config <manifest.config> account --no-browser complete   # 重复直至非 pending
<manifest.python> -I -m saycut_tools.cli --config <manifest.config> account status
```

授权完成后，MCP stdio server 与本地网关进程内会自动：

- **Token**：后台守护线程（`saycut_tools.keepers` 的 token keeper）定期调用 `/mcp/v1/session` 轻量校验，检测吊销；真正需要刷新由 `AccountClient.authorized` 在 401 时触发。
- **License（SDK 租约）**：每 6 小时检查一次；剩余 TTL 低于 **36 小时**时自动向 `/mcp/v1/license/issue` 申请新租约并写入私有凭据目录，无需用户介入。

> **不要问用户"license 即将过期"**：先调 `saycut_keeper_status` 看 `lease.remaining_seconds`。正常机器应恒大于 36h。

## 4. 验证

- 宿主内调 `saycut_keeper_status`，`lease.remaining_seconds` 大、`last_error` 为 null 即健康。
- CLI 冒烟（不产生云端调用）：

  ```bash
  <manifest.python> -I -m saycut_tools.cli --config <manifest.config> doctor
  ```

- 仓库级回归（在 `videocut.chat-server` 源码树执行）：`python scripts/verify_all.py` 串起 keepers、编辑器入口、MCP render 与 save_to_edit 契约；`verify_serve_e2e.py` 覆盖本地网关端到端。

断网重连属正常场景：tick 期间 `last_error` 短暂非空，恢复后回到 `last_error=None`。

## 5. 离线 / 沙盒环境

- 离线时租约续期失败（`last_error = account_unavailable`）。本地渲染继续用磁盘上的旧 lease，**只要 lease 未过期就能继续渲染**。
- 真正过期后恢复网络，下一次 MCP 调用自动拉新租约。
- 完全无网络的构建机：预置 `--runtime-dir` 指向含 skymedia 的目录，可跳过 runtime 下载（仍需要有效租约才能本地渲染）。

## 6. 排错

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| MCP 一直 unauthorized | OAuth 连接断了 | `account status`，必要时重新 `start`/`complete` 走一遍登录 |
| 渲染返回 `entitlement_required` | 账号没有 local-render entitlement | 完成一次授权；仍失败则联系平台端开通 |
| `keeper_status.license.last_error = entitlement_required` | 账号订阅暂停 | 联系平台端 |
| `keeper_status.token.detail.revoked = true` | token 被吊销（常见：用户改密） | 重新走登录 |
| 渲染时 `invalid_personal_license` | 租约文件损坏或缺失 | 删除私有目录下的 `license` 文件后重渲一次（会自动重签） |
| 首跑 `install_isolated` 报 `sdk/plugins` 路径不存在 | ≤0.3.1 安装器默认 plugin-source 解析缺陷 | 已在仓库修复；旧脚本显式传 `--plugin-source plugins/videocut-chat` |

## 7. 微调回流与云端渲染协议

- 云端提交统一走 `mcp.zjtemplate.com`，widget 名 = `tid` = `McpRender`；不再使用 `api.dalipen.com` / `GenVideo`（老 worker 以 `saycut_tools_v1` 别名过渡兼容）。
- **注入编辑器**：云端任务用 `saycut_editor_handoff` 返回的链接或 `GET <public_base_url>/v1/jobs/<job_id>/editable-bundle` 拼 `edit.videocut.chat/editor?file=…`。该 URL 必须公网可读且不带 bearer。**本地任务不要伪造公网链接**——把渲染产物 editable bundle 路径交给用户，在编辑器里手动导入即可；浏览器禁止公网页面访问 `127.0.0.1`。
- **微调结果回流**：编辑器"导出工程包"（`saycut.project.bundle` v1 zip）交给 agent；`unzip -p <bundle> project.json` 取 `.timelines[0]` 写成 `.sky` 文件即可喂回 `saycut_render_video`/`saycut_update_project`，无需任何转换工具。
- `saycut_save_to_edit`：把工程修订版镜像到 `mcp.zjtemplate.com` 编辑库，返回 `{project_id, revision, cloud_edit_project_id, created, bytes}`。云端受理端点尚未对公网开放时工具会显式报错，改走本地 bundle 路径。
- 双通道 postMessage（`editor:dirty`/`chat:apply_project`）只在宿主以内嵌 iframe 承载编辑器 + `host_bridge.js` 时生效；CLI 宿主没有 iframe，走上面的文件回流即可，不要宣称实时同步。
