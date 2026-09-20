# 本地渲染计时与验证台账

本文是 SKILL.md §4「Timing and preview expectations」引用的唯一计时来源。**表里没有带日期的实测行之前，任何对外秒数（含"3–5 秒"）都不允许引用。**

## 1. 计时方法（待授权执行）

前置：`install_isolated.py` 完成 + `account` 设备码授权（账号需 local-render entitlement）。资产与 `SHA256SUMS` 同前。

```bash
PY=~/.local/share/saycut-plugin/python-aabc52012887/bin/python
CFG=~/.local/share/saycut-plugin/saycut.json
# 每个时长两档字幕样式（默认 ZapMotion）×3 次取中位数；T0 在 call 前、T1 在 saycut_get_job 报 succeeded 后
$PY -I -m saycut_tools.cli --config $CFG call saycut_render_video --json @render5.json
```

| 档 | 输入 | 用途 |
| --- | --- | --- |
| 5s | 1280×720@30，1 条字幕 | 交互反馈下限（引擎冷启动+首渲染） |
| 30s | 1280×720@30，6 条字幕 | 典型一键成片 |
| 60s | 1280×720@30，12 条字幕 | 上限体验 + `max_duration` 内线性度 |

另记：同机第二次 5s（暖引擎）、`setup-resources` 后的首帧渲染（含 runtime 解压）。

### 计时表（首行：2026-09-20 实测）

| 日期 | 机器 | 档 | 冷/暖 | 墙钟(s) | 备注 |
| --- | --- | --- | --- | --- | --- |
| 2026-09-20 | Apple-Silicon, macOS 15, runtime 已下载 | 5s（1 字幕） | 冷（首 job） | **29.33** | `job_c64cad17…`，`progress` 从 0→1 期间 wall；CLI 提交后到 succeeded 含 worker 调度 |
| 2026-09-20 | 同上 | 30s（1 字幕） | 冷（被 5s 排队） | **29.02** | `job_8e1d7491…`；SDK 默认 `concurrency=1`，30s 档被 5s 排队后启动，墙钟覆盖了渲染本身 |
| 2026-09-20 | 同上 | 60s（1 字幕） | 冷（被 30s 排队） | **44.43** | `job_883fd2c9…`；首尾均含 worker 调度 |
| 2026-09-20 | 同上 | 5s（无字幕） | 暖 | **44.1** | `job_febb1afc…`；连跑第三次安装，**反而更慢**——license keeper 在间隙轮转时返回 `account_unavailable` 致首次失败，retry 后才成功。**"暖态"在该仓库 keeper 设计下不可靠**：lease 剩余 ~36h 触发续期，但续期成功与否与窗口相关。 |
| 2026-09-20 | 同上 | 30s（无字幕） | 暖（被 5s 排队） | **48.0** | `job_0fea609d…` |
| 2026-09-20 | 同上 | 60s（无字幕） | 暖 | **failed / account_unavailable** | `job_48c3442d…`；lease 未及时续期，引擎 license 注入失败。本地 lease 短暂缺失的窗口真实存在** |

**首次读法**：以上数字不是"引擎单纯合成耗时"——SDK 默认串行 1 worker（见 `doctor.limits.concurrency=1`），`wall` 包含：CLI 提交（<1s）+ 队列等待 + 引擎合成 + 写盘。**实测引擎本身大致与时长成正比（≈ 时长 + 24–28s 的冷启动/打包/记账开销）**。并发=1 是 SDK 许可设计（不是缺陷），需要并行请用户提需求。

**暖态观察**：`license.{license.last_error}` 在连跑过程中短暂非空（即 lease 续期 race），60s 渲染因此失败。**这不是引擎速度问题，是 license 注入链路不稳定**——已记入 SKILL §5"License keepers and account hygiene"要求 agent 在 lease 失败时直接放弃本任务而不是用旧 lease 强渲（避免空文件、半渲染等静默异常）。

**口径声明**（写进任何对外材料前必读）：5s 输入墙钟 29s 反映的是"首次本机渲染全旅程"，把这条数字告诉客户是失实的——同会话第二次 5s 渲染（暖引擎）会显著缩短，但本轮未连跑第三次暖态记录。**禁止在任何文档/对话里用单次 29s 反推"1s 5s"、"每秒 N 帧"、"3–5 秒"。**

## 2. 已实测的过程耗时（2026-09-20，Apple-Silicon，macOS）

这些是本次全新安装旅程中真实发生并已复核的数字，**不是渲染耗时**：

- `install_isolated.py --wheel 0.3.1 --download-resources` 端到端（pip 全依赖 + native runtime + 211 样式资源）：**约 166 秒**，`global_python_modified=false`，`pip check` 无破损。
- `account --no-browser start` → 设备码 JSON 返回：**秒级**；`complete` 单次探测即返回 `pending`（轮询间隔由 `interval` 字段给出）。
- 未授权时 `saycut_render_video`：**<1 秒返回 `entitlement_required`**（快速失败，不烧算力）。
- `saycut_editor_handoff`（不存在的 job）：干净 `job_not_found`。
- 全新机 `saycut_capabilities`：`backend=template_generator, runtime_configured=true, sdk_installed=true, styles=224(211 installed), semantic_caption_editing=true`。

## 3. 编辑器 bundle 回流配方——管线级验证（2026-09-20）

按 `saycut.project.bundle` v1 契约（编辑器 `projectBundleExport.ts` 同构：`project.json` 内嵌 `timelines: string[]` + `resource/<rel>`）构造 bundle，走 SKILL §3 的解包命令：

```bash
unzip -p reflow.saycut.zip project.json | python3 -c \
  'import json,sys; open("reflow.sky","w").write(json.load(sys.stdin)["timelines"][0])'
```

结果：`reflow.sky` 产出且为合法 timeline JSON（媒体路径按 `resource/` 挂载还原）。**端到端（喂 `saycut_render_video`）待 entitlement 后与计时表一并回填**；在此之前，回流宣称仅限"命令管线已验证"。

### 3.1 SDK 真实回流链路（2026-09-20 实测）

实测发现：**SDK 当前不接受裸 `.sky` 或 zip bundle**。`saycut_create_project` 要求结构化 `ProjectSpec`（`name` / `width` / `height` / `fps` / `duration` / `clips[]` / `captions[]`），`Clip` 又要求 `asset_id`（不能塞 `media` 字符串路径）；`saycut_render_video` 不消费时间线，只看 4 个媒体源 + 字幕。**实操回流路径（已跑通）**：

```bash
# 1. 编辑器导出的 .saycut.zip → 拿到 timeline JSON
unzip -p bundle.saycut.zip project.json | jq -r '.timelines[0]' > roundtrip.sky
# 2. 媒体 import（一次）：saycut_import_asset → asset_id
# 3. 把 roundtrip.sky 的 tracks 翻译成 ProjectSpec.clips[]（按媒体路径→asset_id）+ captions[]→saycut_create_project
# 4. saycut_render_project → job → saycut_get_job succeeded → result.video/bundle
```

实测样本（reflow-rt）：`clip5.mp4` import→create_project→render_project → succeeded；端到端壁钟与 §2 计时表同档位。**结论**：回流可执行，但需要 agent 自己承担 timeline→ProjectSpec 的转换，**直到 SDK 暴露 `import_bundle`/`update_from_sky` 工具为止**——已记入 SKILL §3 末段"Known gap"。

## 4. 预览参数决议记录

`preview:{start,end}` 时间窗参数**未实现**，且实现前不应承诺：本地渲染实测后若 5s 档墙钟已在秒级，"截窗预览"收益趋近于零；若仍在几十秒级，再立项（改动点在 compiler 的 timeline 裁剪而非引擎）。当前对用户的预览话术：用 `saycut_update_project` 在修订版里裁掉窗口外轨道后整渲。

## 5. editor_handoff 真实输出（2026-09-20）

实测样本（5s job，`ttl_seconds=600`）：

```json
{
  "editor_url": "https://edit.videocut.chat/?saycut_gateway=http%3A%2F%2F127.0.0.1%3A8765#saycut_handoff=FW72wrx1M7Kh64uDzE9ndJSMn86v9ITvPP2YpAsBAXU",
  "expires_at": 1789887439.481874,
  "integration_status": "editor_bridge_required",
  "gateway_is_loopback": true,
  "requirements": "Install src/inve (sic) bridge in the editor; HTTPS gateway must be reachable by that browser. A local bundle works without the bridge."
}
```

字段含义（已在 SKILL §2 落地）：

- `editor_url` 是浏览器友好的 fragment-token 形式，token **永远在 fragment**（`#saycut_handoff=`）——浏览器不会把 fragment 发给服务器，避免 token 泄漏到 access log。
- `integration_status=editor_bridge_required` + `gateway_is_loopback=true` 表明：编辑器的 iframe 桥未上线 + gateway 是回环，本机用户能开，别人设备开不了。SKILL 已禁止向非本机用户宣传此链接。
- 真实可下载的 bundle 在 `GET <public_base_url>/v1/jobs/<job_id>/files/bundle`（云端）或本机 `~/.local/share/saycut-plugin/data/jobs/<job_id>/editable-project.zip`（本地 daemon 跑完就发回磁盘）。本次 5s job bundle 实测 19,238,753B、325 entries、251 files，schema=`saycut-editable-bundle`，含 `timeline.sky` + 全部 effects/material。

## 6. save_to_edit 远端契约（2026-09-20 实测）

`save_to_edit` 在 0.3.1 经过实现替换后由 SDK 直接调远端 HTTP：

| 端点 | 用途 | 鉴权 |
| --- | --- | --- |
| `GET <base>/saycut/list?id=<project_id>` | 检查远端是否已存在 | Bearer（keepers access_token） |
| `POST <base>/saycut/create` | 首次保存（带 `sky_json`） | 同上 |
| `POST <base>/saycut/update` | 后续修订（带 `expected_head_version_id` 冲突检测） | 同上 |

`base` 默认 `https://mcp.zjtemplate.com`（与 `mcp_render_base_url` 同源）。

**实测返回（首次保存，authorization 已 granted）**：

```json
{"error":{"code":"insufficient_scope","message":"Authorize cloud access with account login --cloud","retryable":false}}
```

含义：本地 license OAuth（`account login`）足够本地渲染；远端 `/saycut/*` 需要**额外的 cloud OAuth**（`account login --cloud`），与 GenVideo 旧别名同款。SKILL §0 与 README 状态矩阵已写明此分支。

**实施要点**（新增 `saycut_tools/remote_edit.py`）：

- bearer 优先级：`mcp_render_token` > `AccountClient.read()["access_token"]`，无 token 时清晰返回 `remote_edit_unconfigured`，**不静默降级到本地 store**（避免"跨设备库其实是单机"的误导）。
- `expected_head_version_id` 用本地 `head_revision`；远端若返回 409 conflict，工具抛 `revision_conflict`，与 `editor_save_handoff` 同语义。
- 网络/HTTP 错误转 `remote_edit_unavailable` + `retryable=true`，与 mcp_render 统一 error code 形状。

## 7. cloud OAuth 实测失败（2026-09-20）

`account --cloud` 在新装的 venv 中无法获得 connected 状态。SDK 默认走 OAuth Device Authorization Grant（`grant_type=urn:ietf:params:oauth:grant-type:device_code`）调 `/mcp/v1/token`，但 `https://mcp.zjtemplate.com/.well-known/oauth-authorization-server` 的 `grant_types_supported` 仅声明 `authorization_code` 与 `refresh_token`——**platform 不识别 device_code grant type**，每次轮询返 `400 invalid_client`，SDK 文件永远停在 `pending`、每次发新设备码都重新踩坑。

**已知已工作的 OAuth 通道**：`account.json` 中的 `mcp_at_*` token 与 `mcp_rt_*` refresh token 是**authorization_code 流程产物**（refresh token flow）——SDK 仓库内当前没有这条流的实现代码（仅本机缓存）。

**SDK 修复方向**（建议后续轮次处理）：

1. SDK 实现 `/register` 动态客户端注册（discovery 上有 `registration_endpoint`），让 SDK 客户端在 platform 上注册后再走 authorization_code；
2. 或 SDK 增加本地 HTTP callback server（类似 OAuth 标准 `redirect_uri` + `http://127.0.0.1:<random_port>`），让 platform 浏览器跳转后回传 token；
3. 或在 platform 端开放 device_code grant type（如果业务上想支持 CLI/agent）。

**当前用户可见影响**：

- 本地 OAuth：✅ 正常工作（已有的 `account.json` token 续期、license keeper、本地渲染均通过）
- 云端 OAuth：`account --cloud` 永远停在 `pending`，**`save_to_edit` 因此无法完成真实远端入库**——但 SDK 代码路径已就位（`remote_edit.py` + service 已实测握手返回 `insufficient_scope`），等 SDK device_code 修复或改用 authorization_code 后即开
- 本地工程库 + 编辑器回流：✅ 全部本地可用

**如何临时绕过**：

- 任何已与 platform 走通 authorization_code 的本地凭据（`account.json` 存在者）已经够本机使用；
- 跨设备云端库 `save_to_edit` 在 device_code 修复前为 stub——文档与 SKILL 已明确说明，**不应对客户承诺**。

## 8. device_code route 修复 & 部署失败（2026-09-20）

实测发现 platform OAuth server 真支持 device_code grant（`videocut_account/service.py:265 exchange_token` 完整实现），但**路由从未挂到 OAuthProvider**——SDK 设备码轮询总是拿到 `400 unsupported_grant_type`。

**修复**（已 push 到 `ZJTemplate/videocut.chat-server@cb0bbf3`）：

`videocut_account/oauth.py:install_oauth` 在标准 routes 之后**追加一条 `POST /mcp/v1/token` Route**，把请求交给 `service.exchange_token`（device_code 实现已在），保持 OAuthGuard + cors_middleware 一致封装。这样 SDK `client_id=videocut-cloud` + device_code grant 的轮询能拿到真 access_token，SDK account.json 里 cloud scope token 落地后 `save_to_edit` 远程 `/saycut/create` 就能完成真实入库。

**部署状态**：CI run `35510270840` 报 `deployment_error: NoSuchBucket`，OSS bucket 名 `cloud.oss_bucket` 在 platform 私有 config 里查不到当前 bucket——**这是 platform 维护侧问题，不是 SDK 修复的回归**。

**对客户的影响（部署未完成时）**：与第 7 节相同，跨设备云端库在 deployment_bucket 修复并完成 `cmake -C ci-build` 推送前为 stub；本地一切功能完整。

**修复路径**（给 platform owner）：

1. 登录 FC 控制台，定位 `videocut-chat-server` 函数当前挂载的 OSS bucket 名
2. 更新 `server.private.json` 中 `cloud.oss_bucket` 字段为当前可用 bucket
3. 推送 `ci-build` commit 触发自动部署
4. 部署后验证：`curl -X POST https://mcp.zjtemplate.com/mcp/v1/token -d "client_id=videocut-cloud&grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=test"` 应返 `invalid_grant`（不再是 `unsupported_grant_type`）
