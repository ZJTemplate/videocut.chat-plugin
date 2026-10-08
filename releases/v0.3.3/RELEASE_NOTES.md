# videocut.chat 0.3.3

本次发布更新面向用户的文档与视频剪辑 skill。插件 manifest、skill 元数据、SDK wheel 和下载包统一为 0.3.3。

## 更新内容

- README 改为产品定位、真实效果预览、核心能力、快速开始和分场景文档。
- Skill 默认中文，按安装、授权、字幕、样式、渲染和网页微调组织流程。
- 新增三种随包分发的官方样式预览：柔和淡入、滑动打字、逐词放大。
- 字幕编辑遵循 ASR 原句优先、必要时标点优先；普通字数目标只指导短句合并。
- 修正安装器输出字段和 MCP 配置指引，补充旧版本升级与宿主缓存说明。
- 修复本地 MCP 启用账户授权后的工具注册错误，并增加回归测试。
- 发布校验覆盖 wheel 元数据、各宿主 manifest 版本和 ZIP 与源码的一致性。

## 发布范围

本地 SDK 渲染实现与资源版本沿用 0.3.2。本版不包含在线字幕导演的服务端代码；在线断句修复已单独部署。本地 Agent 遵循更新后的字幕编辑指令，自动 ASR 行为仍以实际后端为准。

本次验证包括安装包与文档一致性、隔离安装及只读工具冒烟，不包含新的付费云渲染验收。

## 升级

在仓库执行 `git pull --ff-only` 和 `python3 scripts/verify_release.py`，使用新 wheel 重新运行隔离安装器，然后更新宿主中的插件 / skill 与生成的 MCP 配置，重新打开会话。已有账户配置可继续保留。

[完整安装与升级步骤](https://github.com/ZJTemplate/videocut.chat-plugin/blob/main/docs/INSTALL.zh-CN.md)

## 下载

- `videocut-chat-plugin-0.3.3.zip`：skill、预览和宿主配置。
- `saycut_tools-0.3.3-py3-none-any.whl`：本地 MCP / REST 工具。
- `SHA256SUMS`：两项下载文件的校验值。
