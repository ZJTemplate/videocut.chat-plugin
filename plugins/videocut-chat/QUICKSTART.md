# 快速开始

当前插件版本：**0.3.3**。

1. 从[公开仓库](https://github.com/ZJTemplate/videocut.chat-plugin)获取源码及 wheel，按[安装文档](https://github.com/ZJTemplate/videocut.chat-plugin/blob/main/docs/INSTALL.zh-CN.md)运行隔离安装器。
2. 用安装器生成的 `integrations` 配置或插件接入宿主，重新打开会话。
3. 调用 `saycut_capabilities`，按工具返回的链接由用户完成账户授权。
4. 提供素材，例如：“给这个视频加中文字幕，先展示三种可用样式，选好后在本地渲染。”

需要本地识别时安装 ASR 依赖和模型；已有字幕则直接导入。云端上传和渲染需要单独云端授权及用户同意。

已安装旧版时，更新整个插件 / skill 和生成的 MCP 配置；只拉取仓库不会刷新宿主缓存。
