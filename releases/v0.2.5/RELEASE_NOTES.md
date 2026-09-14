# videocut.chat 0.2.5 (Beta)

[English](#english) | [简体中文](#简体中文)

## 简体中文

- 修复新安装默认连接 MCP 域名后，SDK 校验仍请求不存在的旧业务路径的问题。插件适配层使用现有 `/mcp/v1/license/check`，强制 HTTPS 校验、禁止重定向，仅接受布尔校验结果。不修改 C++ 或 SDK 包文件。
- 两个官方域名兼容共用旧连接，保留旧插件能够读取的授权来源记录；其他域名仍隔离。
- 本地视频和图片增加 `fit=contain` 留边和 `fit=cover` 居中裁切，保持原比例；旧工程省略该字段仍按原方式合成。
- 拒绝未经标准化的旋转/非方形像素输入用于显式适配，Skill 提供 FFmpeg 标准化步骤。标准化重新编码视频并保留原件。
- 包含 0.2.4 的输入校验、空/损坏字幕拒绝、明确的厂商调用授权、原生进度容错、字幕重叠和可读性风险提示。
- 不改变原有计费、数据库、许可证续期和用户全局 pip 包。0.2.2、0.2.3 发行文件保留，不覆盖旧二进制。

此版本仍为受控内测。211 个样式可用不代表任意文本都可读；长字幕、字形覆盖、装饰越界仍需检查。云端旧 worker 仍只提供一个预设和 MP4，不具备本地全部效果、逐句编辑、完整计量或在线编辑桥接。不要把运营凭据测试描述为个人 OAuth/扣费验收。

验收范围及限制见 [0.2.5 验收记录](../../docs/ACCEPTANCE-0.2.5.zh-CN.md)。使用仓库独立安装器选择本版本 wheel，校验 `SHA256SUMS`，再将生成的配置合并到宿主。不会自动更新已有宿主的插件缓存，也未发布到 PyPI 或官方市场。

## English

- Fix fresh-install SDK verification on the MCP domain by adapting the existing `/mcp/v1/license/check` response. TLS verification, disabled redirects and strict boolean validation remain enforced. No C++ or installed SDK files are modified.
- Preserve shared legacy credentials across the two exact official account origins without relaxing third-party isolation.
- Add local `clip.fit=contain` and `cover` through the native renderer's existing transforms. Omitted fit preserves previous project behavior.
- Require normalization of rotation metadata and non-square pixels before explicit fitting; the skill documents a local FFmpeg procedure that retains the original.
- Include 0.2.4 validation, provider approval/error handling, subtitle parsing, progress-file fault tolerance and visual warnings.
- No database, pricing, renewal-policy or global Python-package changes. Existing public releases remain intact.

This is a controlled beta, not a universal visual-quality or production-SLA guarantee. The legacy cloud worker still exposes one preset and MP4 output; full effects, per-caption controls, personal billing acceptance and editor handoff remain incomplete. Host configurations are provided, not certification of every vendor's model or consumer chat UI. Install the new wheel using the isolated installer and merge generated host configuration; existing host caches are not automatically updated. No PyPI or official-marketplace publication is implied.
