# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

Animated captions ("花字"), deterministic video composition and editable SkyMedia projects **for AI coding-agent hosts** — Codex, Claude Code, Qwen Code and any MCP client. Powered by the licensed `template_generator` native engine running on your machine.

**Version 0.3.1 · Controlled beta · Built for agent power users.**
If you do not already run an MCP-capable coding agent, use the web product at [videocut.chat](https://videocut.chat) instead. This repository is not a one-click application, not a PyPI package, and not a marketplace listing.

## The Workflow

1. **Install once** (~10 minutes, one copy-paste block below, or hand the repo URL to your agent and ask it to run the installer steps and merge the generated config).
2. **Authorize once.** First render opens a browser approval at [platform.zjtemplate.com](https://platform.zjtemplate.com). From 0.3.x onward background keepers silently renew the account token and the SDK lease (~36h horizon) — no periodic re-login.
3. **Ask in natural language**: "Add animated Chinese captions to this video and keep the project editable." The agent transcribes (local faster-whisper), picks styles from the installed catalog, builds the project and renders **locally**; your media does not leave the machine unless you explicitly allow cloud processing.
4. **Iterate in chat** (style/text/timing edits via MCP tools) — or **hand off for visual polish**: the plugin gives you an `edit.videocut.chat` URL that imports the exact project into the browser editor (production-verified, including 32 MB multi-material bundles via OPFS).
5. **Export round-trip.** The editor exports a `.saycut.zip` project bundle; hand the downloaded file back to your agent (same machine) to continue revising and re-rendering in chat.

## What Is Actually Where (honest status matrix)

| Capability | State |
| --- | --- |
| Isolated-install + local render with bundled resources (macOS) | ✅ Verified (0.2.5 acceptance; 0.3.1 full-serve e2e in CI) |
| One-time authorization, automatic token/license renewal | ✅ Implemented 0.3.1 (`TokenKeeper` / `LicenseKeeper`) |
| MCP tool surface: import / transcribe / style / compose / render / cancel / idempotent retry | ✅ Contract- and CI-verified; Claude/Qwen/other hosts' own OAuth UI untested |
| Browser editor project import (`edit.videocut.chat/editor?file=…`) | ✅ Live and production-verified |
| SDK route `GET /v1/jobs/{id}/editable-bundle` | ✅ Implemented in 0.3.1 — but served from **your** gateway; a public browser cannot reach a local machine, so handoff URLs only resolve for browser-reachable gateways |
| Cloud project store round-trip (`saycut_save_to_edit`) | 🟡 SDK client + REST + MCP channels done; the `POST /mcp/v1/edit-projects` endpoint on `mcp.zjtemplate.com` is not yet served by the platform — cross-device handoff is blocked on it |
| Chat ↔ embedded-editor dual channel (`postMessage`) | 🟡 Contract-tested (Node CI); meaningful only for webview-capable hosts — terminal agents (Codex/CC CLI) use the export-file round-trip instead |
| Cloud rendering via `McpRender` on `mcp.zjtemplate.com` | 🟡 3 real tasks finished in 66/66/96 s using an operator acceptance credential; personal OAuth + billing acceptance is not complete; legacy worker still registers `GenVideo` (alias `saycut_tools_v1`) |
| Windows / Linux native rendering | ⬜ Config exists, not acceptance-tested |
| Preview-segment rendering (short time window) | ⬜ Not implemented — every render is a full job today |

The catalog contains 224 entries; this wheel bundles resources for 211 styles plus a Source Han Sans fallback font, 13 entries require separately supplied resources. Availability is not a guarantee of visual quality for every language or caption length — long-caption wrapping, missing glyphs and decorative clipping are known limits. Normalize rotation metadata and non-square pixels with FFmpeg before import (the skill documents the procedure).

## Downloads (0.3.1)

| File | Purpose |
| --- | --- |
| [Python wheel](releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl) | `saycut-tools`: MCP server, local gateway, editor assets, style resources |
| [Plugin ZIP](releases/v0.3.1/videocut-chat-plugin-0.3.1.zip) | Portable plugin manifests and the video skill |
| [SHA256SUMS](releases/v0.3.1/SHA256SUMS) | Checksums for both archives |

Verify after downloading: `python3 scripts/verify_release.py`. The wheel is inspectable Python; packaging is not encryption. The installer fetches the pinned native SDK (`p-template-generator==1.2.17`, `native` extra), optionally `faster-whisper` (`asr` extra), the runtime binaries and the ASR model as explicit downloads. Nothing bundles account credentials or SDK certificates.

## Install (macOS / POSIX)

Prerequisites: Python ≥ 3.11, FFmpeg + ffprobe on PATH, a platform account with local-render entitlement, network access for downloads and license checks.

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py

python3 scripts/install_isolated.py \
  --wheel releases/v0.3.1/saycut_tools-0.3.1-py3-none-any.whl \
  --allow-root "/absolute/path/to/videos" \
  --download-resources --asr --download-model
```

This creates a private environment under `~/.local/share/saycut-plugin` (nothing touches global site-packages), then prints three paths: `python`, `config`, `integrations`. Check readiness:

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

`setup-resources` and `configure-asr --backend faster_whisper --model small --download-model` can re-run the same downloads later. Diagnostics check prerequisites, not every effect or a license-authorized render.

## Connect Your Assistant

Use the **generated** files under the returned `integrations` directory — not the generic manifests in this repo unchanged:

| Host | Generated configuration |
| --- | --- |
| Codex | `codex.toml`, or register `plugins/videocut-chat/` as a local plugin source |
| Claude Code | `claude-code.mcp.json` or the generated plugin directory |
| Claude Desktop | `claude-desktop.json` |
| Qwen Code | `qwen.settings.json` |
| Other MCP hosts | Compatible generated stdio configuration |

Merge with your host's MCP configuration mechanism without overwriting unrelated settings, start a new conversation, and confirm `saycut_capabilities` is listed. On first render the plugin opens the authorization link — sign in and approve it yourself; credentials and the short-lived SDK certificate stay in the private runtime directory.

## Cloud, Editor Bridge, Limits

Cloud submissions flow through `McpRender` on `https://mcp.zjtemplate.com/mcp` (0.2.3+ supports OAuth discovery, dynamic registration, PKCE, token rotation/revocation). A website login token or a local-only grant is not a cloud credential; stdio-only hosts run `account login --cloud` once. Cloud generation uses platform GenVideo rates: automatic ASR reserves against the duration ceiling (currently 600 s × CNY 0.01/s), settles reported usage on completion and refunds the remainder — the legacy worker currently reports `usage={}`, so final production metering awaits that worker's usage upgrade. One preset and MP4 output are verified in the legacy cloud path; the full effect catalog and editable cloud projects are not available yet.

The editor bridge is **split across two halves**: the browser side (project import into `edit.videocut.chat`, OPFS-backed, export toast flow, byte-verified round-trips) is live and production-verified; the platform side (public edit-project store behind `POST /mcp/v1/edit-projects`) is not yet accepting requests, so `saycut_save_to_edit` only completes against a stub. Until then, a `?file=` URL pointing at a non-public gateway will not load in the browser — do not treat a handoff link as proof of a working session, and prefer the same-machine export round-trip.

Local rendering never silently uploads media; license/account checks still contact the authorization service (local-first ≠ fully offline). Explicit consent is required for any cloud processing (`allow_cloud_processing`). Do not commit tokens, certificates, private configs or customer media to repositories.

## Support

Report reproducible issues through [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues) with OS, Python/package versions and sanitized diagnostics. Never attach credentials or private videos; if credentials leaked, revoke the connection on the platform before filing. Acceptance records: [0.2.5](docs/ACCEPTANCE-0.2.5.zh-CN.md), [0.2.3](docs/ACCEPTANCE-0.2.3.zh-CN.md), [2026-09-14](docs/ACCEPTANCE-2026-09-14.zh-CN.md) · Install guide (zh-CN): [docs/INSTALL.zh-CN.md](docs/INSTALL.zh-CN.md)
