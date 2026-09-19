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

### 计时表（空）

| 日期 | 机器 | 档 | 冷/暖 | 墙钟(s) | 备注 |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | 待 entitlement 授权后回填 |

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

## 4. 预览参数决议记录

`preview:{start,end}` 时间窗参数**未实现**，且实现前不应承诺：本地渲染实测后若 5s 档墙钟已在秒级，"截窗预览"收益趋近于零；若仍在几十秒级，再立项（改动点在 compiler 的 timeline 裁剪而非引擎）。当前对用户的预览话术：用 `saycut_update_project` 在修订版里裁掉窗口外轨道后整渲。
