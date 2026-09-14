# videocut.chat 0.2.3

2026-09-14. Controlled beta / 受控内测。Does not replace the immutable 0.2.2 archives.

## Changes / 变更

- Personal cloud OAuth: discovery, registration, PKCE, explicit platform consent, rotating tokens and revocation. Existing local grants stay local-only.
- GenVideo pricing comes from the main API. Reservation, settlement and refunds share the task transaction; idempotent retries do not charge twice. Current legacy empty usage settles to zero under the existing platform rule.
- Wheel bundles the resources for 211 styles and a licensed Source Han Sans fallback font. Native SDK/runtime, ASR dependencies/model and user licenses remain separate.
- Isolated installer supports explicit resource/model downloads and enables ASR on an existing disabled configuration without changing global pip packages.
- HTTP patch fields preserve omitted versus null values. n8n handles empty JSON, offers personal OAuth and exposes all 23 video operations; OAuth examples target the remote gateway.

## Verified / 已验证

- Private wheel installation, dependency consistency, native runtime download/checksum, and 211 configured styles.
- Real local MCP: Chinese ASR, animated captions, color/scale revision, two MP4 renders and an editable ZIP with 332 files. H.264/AAC, 640x360, 5.417 seconds; representative frame inspected.
- 29 isolated OAuth/scope/tenant/billing regression checks; 8 n8n request/auth/error contract checks. These are not all real production identity tests.
- Main API pricing, frontend and single FC deployment completed; public health/OAuth discovery and anonymous-request rejection passed.

## Limits / 边界

The production legacy worker still offers one preset and MP4 only; no full local style catalog, per-caption controls or editable cloud output. `edit.videocut.chat` needs its editor bridge deployed. Windows/Linux native rendering, consumer chat clients, and user-approved n8n OAuth UI are not accepted by these checks. See [the acceptance report](../../docs/ACCEPTANCE-0.2.3.zh-CN.md) for the latest user-consent test status.

线上旧 worker 仍需补充真实用量和完整工程协议；不能把预扣当作最终价格，也不能将本地能力宣传成已全部云端开放。未绕过 SDK license、平台授权或厂商地区审核。
