# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

Animated captions and editable video composition for AI assistants, powered by the licensed `template_generator` engine.

**Version 0.2.5 · Controlled beta · Private installation and bundled-resource rendering verified on macOS.**

This is the public distribution repository for the plugin and Python tool package. It is not a one-click native application, a PyPI publication, or a listing in an official plugin marketplace.

## What You Can Do

- Transcribe local speech and add animated captions using installed text effects.
- Create and revise video compositions through MCP tools instead of writing native project JSON.
- Export MP4 videos and editable SkyMedia `.sky` projects with resource bundles.
- Check progress, cancel running jobs, and safely retry submissions using idempotency keys.
- Preserve local clip proportions with `fit=contain` (black space) or `fit=cover` (center crop); omitted fit preserves legacy behavior.
- Connect through local MCP, host-specific configurations, or the cloud gateway with separate personal authorization.

The catalog contains 224 entries. This wheel bundles resources for 211 styles and a fallback font; 13 additional entries require separately supplied resources. Availability is not a guarantee of visual quality for every language or caption length.

## Downloads

| File | Purpose |
| --- | --- |
| [Python wheel](releases/v0.2.5/saycut_tools-0.2.5-py3-none-any.whl) | The `saycut-tools` implementation, MCP server and style resources |
| [Plugin ZIP](releases/v0.2.5/videocut-chat-plugin-0.2.5.zip) | Portable plugin manifests and the video skill |
| [SHA256SUMS](releases/v0.2.5/SHA256SUMS) | Checksums for the two archives |
| [Release notes](releases/v0.2.5/RELEASE_NOTES.md) | Verified behavior and known limitations |

Installing the plugin ZIP alone does not install the rendering environment. The wheel contains Python code, effect resources and a Source Han Sans fallback font with its license. The installer downloads the SDK Python dependency separately; native binaries and the ASR model are explicit downloads. No account credentials or SDK certificate are bundled.

## Local Installation

### 1. Prerequisites

- Python 3.11 or newer, including `pip` and `venv` support.
- FFmpeg and ffprobe on your PATH.
- A platform account with local-render entitlement. SDK licensing remains required even with bundled resources.
- Network access for dependency installation, explicit model downloads, account authorization and license checks.

The installer can download and verify the pinned native runtime with `--download-resources`. An existing licensed runtime may instead be selected with `--runtime-dir` (its directory must contain `skymedia/`). Windows/Linux configurations exist but native rendering on those systems has not been accepted in this release.

### 2. Clone And Verify

```bash
git clone https://github.com/ZJTemplate/videocut.chat-plugin.git
cd videocut.chat-plugin
python3 scripts/verify_release.py
```

### 3. Run The Isolated Installer

Replace the example paths with existing directories. These commands target macOS/POSIX shells.

```bash
python3 scripts/install_isolated.py \
  --wheel releases/v0.2.5/saycut_tools-0.2.5-py3-none-any.whl \
  --allow-root "/absolute/path/to/videos" \
  --download-resources --asr --download-model
```

The installer creates a private environment under `~/.local/share/saycut-plugin`, installs the wheel and `p-template-generator==1.2.17`, and generates machine-specific integration files. `--asr` installs and enables local speech recognition; `--download-model` downloads the model. It does **not** overwrite global Python packages or an existing `template_generator`. Native SDK and cloud/deployment dependencies use separate environments because their Click requirements conflict.

Keep the returned `python`, `config` and `integrations` paths. The next commands use placeholders for those exact returned paths; they are not commands to paste unchanged.

### 4. Check Readiness

The command above prepares the standard resources. Check prerequisites before rendering:

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

Resource and ASR model downloads do not upload your video. To prepare resources later, run `setup-resources`; to prepare the model later, run `configure-asr --backend faster_whisper --model small --download-model` with the same Python/config prefix. Diagnostics check prerequisites, not every effect or a successful license-authorized render.

### 5. Connect Your Assistant

Use the files produced under the returned `integrations` directory, **not the generic manifests in this repository unchanged**:

| Host | Generated configuration |
| --- | --- |
| Codex | `codex.toml`, or `plugins/videocut-chat/` for a locally registered plugin |
| Claude Desktop | `claude-desktop.json` |
| Claude Code | `claude-code.mcp.json` or the generated plugin directory |
| Qwen Code | `qwen.settings.json` |
| Other MCP hosts | A compatible generated stdio configuration |

Merge the generated server entry using your host's MCP configuration mechanism; do not overwrite unrelated settings. For the full Codex skill workflow, register the **generated plugin directory** as a local plugin source. Merely cloning this repository does not install or register it. Start a new conversation and verify that `saycut_capabilities` is available.

On first use, follow the authorization link opened by the plugin, sign in at [the platform](https://platform.zjtemplate.com), and approve the requested connection yourself. Credentials and the short-lived SDK certificate stay in the private runtime directory, not in plugin manifests.

Try: “Add animated Chinese captions to this local video and keep the project editable.” Review the recognized text, select an available style, and wait for the returned job to finish.

## Privacy And Licensing

Local rendering does not automatically upload your media or fall back to cloud rendering. Account/license checks still contact the authorization service: local-first does not mean fully offline. Explicit approval is required for cloud processing. Local inputs and outputs are not automatically deleted.

Do not commit tokens, SDK certificates, private configuration or customer media. Publicly readable files do not grant an open-source or commercial redistribution license to the SDK, fonts or effect assets. Their respective terms still apply. Python wheel contents are inspectable; packaging is not encryption.

## Cloud And Compatibility Limits

The cloud MCP endpoint is `https://mcp.zjtemplate.com/mcp`. Version 0.2.3 adds OAuth discovery, dynamic registration, PKCE, token rotation/revocation and an explicit platform consent page. Request `account:read video:cloud`; a website login token or an existing local-only grant is not a cloud credential. Do not distribute administrator tokens.

For a stdio-only host, run `"<python>" -I -m saycut_tools.cli --config "<config>" account login --cloud`, approve the connection yourself, then use the generated `remote-mcp` configuration. Its separate personal cloud credential can refresh automatically without replacing the local SDK authorization.

Cloud generation uses the platform's existing GenVideo rates and balance. Automatic ASR reserves against the configured duration ceiling: the current 600-second ceiling at CNY 0.01/second reserves CNY 6, **not a flat final price**. Completion settles reported module usage; excess reservation and failed/cancelled tasks are refunded. The current legacy worker reports `usage={}`, which produces a zero final charge under the existing rule. Full production metering depends on upgrading that worker's usage reporting.

The verified legacy cloud workflow exposes one preset and MP4 output. It does not yet provide the full local effect catalog or editable cloud projects. Opening a handoff URL does not establish a working session at `edit.videocut.chat`; the editor bridge is not deployed.

Three real remote tasks completed after the 0.2.5 deployment in approximately 66, 66 and 96 seconds, covering MCP, REST and idempotent submission. Chinese inputs were about 5 seconds; the English input was about 86 seconds. These used an operator acceptance credential, not a completed personal OAuth/billing acceptance, and do not establish a production SLA. Short clips still take roughly a minute; see the acceptance record for cloud capability limits.

Version 0.2.5 also includes validation and native progress-file hardening. Aspect fitting does not solve long-caption wrapping, missing glyphs or decorative clipping. Normalize rotation metadata and non-square pixels with the skill's FFmpeg procedure before import; this re-encodes video without overwriting the original. See the [0.2.5 acceptance record](docs/ACCEPTANCE-0.2.5.zh-CN.md).

Host-specific adapters are provided. Actual MCP Client and HTTP cloud-render workflows were verified in an isolated n8n 2.38.7 environment using an operator-provisioned credential; 0.2.3 also supplies personal OAuth2 configurations. This does not certify every host's OAuth UI: Claude/Qwen clients, n8n Cloud, AI Agent tool selection and consumer DeepSeek/Doubao chat integrations remain unverified.

See the [n8n setup guide](examples/n8n/README.md), [0.2.3 acceptance report](docs/ACCEPTANCE-0.2.3.zh-CN.md) and [historical 0.2.2 report](docs/ACCEPTANCE-2026-09-14.zh-CN.md). MCP compatibility does not imply official marketplace availability or video-attachment support in every chat application.

## Support

Report reproducible issues through [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues), including your OS, Python/package versions and sanitized diagnostics. Never attach credentials or private videos. For credential exposure, revoke the affected connection through your platform account before sharing a sanitized report.
