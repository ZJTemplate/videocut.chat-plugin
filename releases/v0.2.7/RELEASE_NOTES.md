# videocut.chat 0.2.7 (Beta)

[English](#english) | [简体中文](#简体中文)

## 简体中文

- 新增后台续期器（keepers）：MCP stdio 服务与本地网关在账号已授权时静默续期本地访问令牌与个人 SDK 租约；租约剩余不足 36 小时才触发续期，正常在线的机器不需要用户重新登录。
- 新增 `saycut_keeper_status` 诊断输出：`lease.remaining_seconds`、`license.last_action_at`、`last_error` 供宿主排障，不替代渲染成功证明。
- 渲染与账号操作集合与 0.2.5 完全一致（27 项，含 `editor_handoff`）；本地账号模式下因 `saycut_keeper_status` 净增 1 项诊断工具，计费、数据库、许可证策略与用户全局 pip 包均不变。
- 0.2.5 及更早发行文件保留，不覆盖旧二进制；未发布到 PyPI 或官方市场。

此版本仍为受控内测。续期器要求 `account_authorization=true`（个人 OAuth 连接）；未连接账号的旧授权文件不受影响。

## English

- New background keepers: with an authorized account, the MCP stdio server and local gateway silently renew the local access token and the personal SDK lease; renewal triggers below a 36-hour horizon so a healthy machine never asks the user to re-login.
- New `saycut_keeper_status` diagnostics (`lease.remaining_seconds`, `license.last_action_at`, `last_error`) for host-side troubleshooting.
- The render and account operation set is identical to 0.2.5 (27, including `editor_handoff`); local account mode nets one extra diagnostic tool, `saycut_keeper_status`. Billing, database, license policy and global Python packages are unchanged.
- Earlier release artifacts remain intact; no PyPI or official-marketplace publication.

Controlled beta. Keepers only act when `account_authorization=true`; legacy credential files without an account connection are untouched.
