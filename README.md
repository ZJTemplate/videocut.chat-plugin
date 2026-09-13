# videocut.chat

[English](README.md) | [简体中文](README.zh-CN.md)

Animated captions and editable video composition for AI assistants, powered by the licensed `template_generator` engine.

**Version 0.2.1 · Controlled beta · Native rendering verified on a provisioned macOS environment.**

This is the public distribution repository for the plugin and Python tool package. It is not a one-click native application, a PyPI publication, or a listing in an official plugin marketplace.

## What You Can Do

- Transcribe local speech and add animated captions using installed text effects.
- Create and revise video compositions through MCP tools instead of writing native project JSON.
- Export MP4 videos and editable SkyMedia `.sky` projects with resource bundles.
- Check progress, cancel running jobs, and safely retry submissions using idempotency keys.
- Connect through local MCP, host-specific configurations, or a separately provisioned cloud gateway.

The catalog contains 224 entries; availability depends on installed resources. The test environment had 211 available entries, not 211 individually verified visual effects.

## Downloads

| File | Purpose |
| --- | --- |
| [Python wheel](releases/v0.2.1/saycut_tools-0.2.1-py3-none-any.whl) | The `saycut-tools` implementation and MCP server |
| [Plugin ZIP](releases/v0.2.1/videocut-chat-plugin-0.2.1.zip) | Portable plugin manifests and the video skill |
| [SHA256SUMS](releases/v0.2.1/SHA256SUMS) | Checksums for the two archives |
| [Release notes](releases/v0.2.1/RELEASE_NOTES.md) | Verified behavior and known limitations |

Installing the plugin ZIP alone does not install the rendering environment. The wheel contains Python code; it does not embed the native SDK, native runtime, fonts, effects, a license, or an ASR model.

## Local Installation

### 1. Prerequisites

- Python 3.11 or newer, including `pip` and `venv` support.
- FFmpeg and ffprobe on your PATH.
- A licensed, OS-compatible TemplateProcess runtime. The runtime directory must contain `skymedia/` and its required native dependencies.
- Authorized effect resources and fonts, plus a platform account with local-render entitlement.
- Network access for dependency installation, explicit model downloads, account authorization and license checks.

Obtain missing runtime/resources through your videocut.chat SDK distribution or support contact before attempting native rendering. They are not provided by this repository. Windows/Linux configurations exist but native rendering on those systems has not been accepted in this release.

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
  --wheel releases/v0.2.1/saycut_tools-0.2.1-py3-none-any.whl \
  --allow-root "/absolute/path/to/videos" \
  --runtime-dir "/absolute/path/to/runtime" \
  --asr
```

The installer creates a private environment under `~/.local/share/saycut-plugin`, installs the wheel and `p-template-generator==1.2.17`, and generates machine-specific integration files. `--asr` also installs local speech-recognition dependencies. It does **not** overwrite your global Python packages or an existing `template_generator` installation.

Keep the returned `python`, `config` and `integrations` paths. The next commands use placeholders for those exact returned paths; they are not commands to paste unchanged.

### 4. Prepare Effects And Speech Recognition

Bind a trusted, licensed effect file and fallback font:

```bash
"<python>" -I -m saycut_tools.cli --config "<config>" catalog bind \
  --style runtime/ZapMotion \
  --path "/absolute/path/to/ZapMotion/text.fceffect" \
  --fallback-font "/absolute/path/to/licensed-font.ttf"

"<python>" -I -m saycut_tools.cli --config "<config>" configure-asr \
  --backend faster_whisper --model small --download-model

"<python>" -I -m saycut_tools.cli --config "<config>" doctor --check
```

The ASR model download is explicit. It does not upload your video. Diagnostics check prerequisites, not the validity of every effect or a successful license-authorized render. A fresh environment without native resources should fail readiness checks.

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

The cloud MCP endpoint is `https://mcp.zjtemplate.com/mcp`. Access is provisioned separately; do not use a shared administrator token. Public per-user OAuth, billing/refunds and general-availability onboarding are not complete.

The verified legacy cloud workflow exposes one preset and MP4 output. It does not yet provide the full local effect catalog or editable cloud projects. Opening a handoff URL does not establish a working session at `edit.videocut.chat`; the editor bridge is not deployed.

Host-specific adapters are provided, but Claude/Qwen app sessions, live n8n and consumer DeepSeek/Doubao chat integrations have not been verified by this release. MCP compatibility does not imply official marketplace availability or video-attachment support in every chat application.

## Support

Report reproducible issues through [GitHub Issues](https://github.com/ZJTemplate/videocut.chat-plugin/issues), including your OS, Python/package versions and sanitized diagnostics. Never attach credentials or private videos. For credential exposure, revoke the affected connection through your platform account before sharing a sanitized report.
