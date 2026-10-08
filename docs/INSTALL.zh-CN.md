# 安装、授权与升级

[返回 README](../README.md) · [宿主接入](INTEGRATIONS.zh-CN.md)

## 安装本地工具

要求 Python 3.11+、一个已有的素材目录，以及用于渲染授权的平台账户。当前版本为 **0.3.3**，通过本仓库或 [GitHub Release](https://github.com/ZJTemplate/videocut.chat-plugin/releases/tag/v0.3.3) 分发，未发布到 PyPI。

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py
python3 scripts/install_isolated.py \
  --wheel releases/v0.3.3/saycut_tools-0.3.3-py3-none-any.whl \
  --allow-root "/你的素材目录" \
  --download-resources
```

`--allow-root` 指定允许读取的媒体目录，可重复传入；不是安装目录。安装器在 `~/.local/share/saycut-plugin` 创建私有 Python 环境，不修改全局 Python。

`--download-resources` 下载版本固定的本地运行时、FFmpeg / ffprobe、特效与字体，不上传用户素材。通常无需单独安装系统 FFmpeg。本地语音识别另加 `--asr --download-model`，会下载识别依赖和模型；已有字幕或只用云端识别时不需要。

安装器最后输出：

```json
{
  "python": "/绝对路径/私有环境/bin/python",
  "config": "/绝对路径/saycut.json",
  "integrations": "/绝对路径/integrations",
  "wheel_sha256": "安装包校验值",
  "global_python_modified": false
}
```

本文后续的 `<python>`、`<config>`、`<integrations>` 均替换为这些实际路径。宿主配置和可安装的本地插件位于 `<integrations>`，接入步骤见[接入文档](INTEGRATIONS.zh-CN.md)。

## 账户授权

本地渲染登录：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login
"<python>" -I -m saycut_tools.cli --config "<config>" account status
```

在浏览器里由账户持有人确认授权。已有有效连接无需重复登录；授权成功也不代表账户已开通所有付费样式或本地渲染权益。

本地工具需要调用云端渲染或远端编辑库时，另行开通云端授权：

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud
```

云端上传和处理需明确同意，调用时传入 `allow_cloud_processing: true`。费用与额度以当前能力查询和任务结算结果为准。本地 SDK 授权不能代替云端消费授权。

## 检查安装

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
"<python>" -I -m saycut_tools.cli --config "<config>" call saycut_capabilities --json '{}'
```

`saycut_capabilities` 返回工具能力和缺失项。缺少运行时、模型或权益时，工具仍可能正常连接，但尚不能渲染；以实际渲染任务成功为准。

## 从旧版本升级

1. 在克隆的仓库执行 `git pull --ff-only`，再执行 `python3 scripts/verify_release.py`。
2. 重新运行上面的安装命令，使用 `0.3.3` wheel 和原素材目录。安装器保留现有账户配置，按新 wheel 建立独立环境。
3. 用新生成的 `<integrations>` 配置替换宿主中 videocut.chat 对应的旧条目，保留其他 MCP 服务配置。
4. 已安装插件的宿主还需从新的 `<integrations>/plugins/videocut-chat` 更新插件；直接安装 skill 文件夹的用户需更新整个文件夹及其 references / assets。
5. 重新打开会话，确认插件版本为 `0.3.3`，并再次调用 `saycut_capabilities`。

GitHub 更新不会自动替换宿主缓存。不要直接修改 `~/.codex/plugins/cache` 中的文件。只更新服务端也不会改变本机 skill 版本。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| 找不到 `saycut_*` 工具 | 检查宿主是否加载生成的配置，确认使用私有 Python 的绝对路径，重新打开会话 |
| 提示需要 FFmpeg | 先运行私有解释器的 `setup-resources`，检查是否已配置 SDK 私有媒体工具 |
| 本地识别不可用 | 重新安装时加入 `--asr --download-model`，或提供带时间码的字幕文件 |
| `entitlement_required` | 查看账户状态并确认对应权益；重复登录不会自动开通权益 |
| `insufficient_scope` | 需要云端操作时执行 `account login --cloud` |
| 授权续期失败 | 查询 `saycut_keeper_status` 和账户状态，按实际错误恢复网络或授权 |
| 安装后仍显示旧版 | 更新宿主中的插件来源或 skill 文件夹；重启宿主并检查加载路径 |

首次下载需要网络。本地渲染仍需有效 SDK 授权，不能把“素材不上传”等同于“永不联网”。
