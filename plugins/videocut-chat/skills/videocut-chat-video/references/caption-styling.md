# Caption Styling

## Discover and Inspect

Search `saycut_list_styles` with a short category or name such as `花字`, `动态字幕`, `描边`, or `flower`, and `available_only=true`. Tags come from resource names and defaults, not visual review. Do not treat them as verified aesthetic labels. Search the category first, then apply a requested color; free-form phrases such as "yellow flower captions" are not a semantic search API. Paginate the results.

Use the exact returned ID with `saycut_get_style`. Its `defaults` describe the resource, not the project's rendered settings. For a 640-pixel-wide canvas, an original Size of 140 may become 58 through automatic layout. On an existing project, use `saycut_get_project` to identify captions by text and timeline order, then `saycut_inspect_caption_style` with the selected caption ID. The inspection returns effective native inputs and the semantic controls supported in the current mode. Do not infer IDs such as "2" from "the second sentence".

## Apply a Semantic Edit

Example tool arguments below use placeholders: replace project ID, revision and caption IDs with actual returned values.

`saycut_style_captions`:

```json
{
  "project_id": "project_example123",
  "expected_revision": 1,
  "caption_ids": ["second_caption"],
  "appearance": {
    "text_color": "#FFD900",
    "outline_color": "#0033B3",
    "position": "bottom"
  }
}
```

For "make it another 20% larger", read the current revision and call the same tool with `appearance: {"scale_by": 1.2}`. This scales the effective current font size, preserving the color, position, other captions and decorative layers. Do not use both `font_size` and `scale_by`, or both `position` and `x/y`.

The tool returns the saved revision, all `changed_caption_ids` and up to five `resolved_styles` inspections, avoiding a full parameter dump for every subtitle. `remaining_style_count` reports the rest; inspect an additional caption by ID when needed. Retrying the same expected revision cannot double-apply a relative change. On a conflict or uncertain response, reread the project and compare against the intended result before deciding whether another edit is needed. Do not automatically reapply a multiplier to the latest revision.

## Units and Boundaries

- Colors are opaque `#RRGGBB`. The adapter writes RGBA values to the active native fill or gradient corners.
- `font_size` is native font size, not final glyph height. Auto-fitting and effect scaling can limit visible enlargement.
- `scale_by` multiplies font size only, not timing, outline thickness or animation strength.
- `position` horizontally centers the effect and offsets Y by -32%, 0%, or +32% of canvas height. This is not a guaranteed text bounding-box alignment. Use explicit `x/y` for finer adjustment; positive values move right/down.
- `outline_color` and `outline_width` modify the first outline only. Other decorative outlines remain. Zero width disables only the first outline.
- Semantic controls currently require a single filter and a single text slot with suitable parameters. Unsupported controls fail before saving. For a multi-label template, inspect `label_suffixes` and the native schema instead of guessing a slot mapping.
- Cloud `semantic_caption_editing=false` means these controls are unavailable there. Do not silently drop them or upload local media as a workaround.

## Advanced Native Patches

Use only keys from the selected style's `parameter_schema`. In `saycut_edit_project`, legacy `effect_params` replaces every project override. Prefer `effect_params_patch` for a partial merge. Each item in `captions` also accepts `effect_params_patch` for a targeted edit. A null value removes that override and restores the next value in the precedence order: resource, canvas layout, project, caption.

Changing a style does not translate incompatible native overrides; inspect the new schema and remove incompatible keys explicitly. Files, shader/script parameters, ASR bindings and font paths are compiler-owned, not arbitrary tool arguments. Import a font asset through the supported asset interface.

## Render and Verify

On `unsupported_media_geometry` or `media_geometry_unverified`, the input carries rotation metadata or non-square pixels that the bundled native engine may ignore. With permission to create a derived local file, use FFmpeg's autorotation and a square-pixel conversion, for example `ffmpeg -i input.mp4 -vf "scale=trunc(iw*sar/2)*2:ih,setsar=1" -c:v libx264 -crf 18 -c:a copy normalized.mp4`, then import that new file and verify its orientation. This re-encodes video; retain the original. Do not run this on cloud media without consent, overwrite an existing file, discard an audio error, or merely clear rotation metadata without rotating pixels. Reimport older stored assets before using the new geometry checks.

Extremely short cues can finish before an entrance animation becomes visible. Preserve user timing or real word alignment when choosing a faster style; do not silently stretch captions. On `no_audio_stream`, request timed captions instead of repeatedly retrying ASR.

When returned, `caption_overlap` flags captions sharing an effect center during overlapping time ranges. Inspect whether the overlap is intentional before changing timing or positioning. `aspect_ratio_mismatch` means the current clip layout stretches the source. If `capabilities.clip_fit_modes` supports it, set a visual clip's `fit` to `contain` (whole image with black space) or `cover` (center crop, may remove edge content). An omitted fit preserves legacy stretching. Replacing `clips` in an edit replaces the entire list: read the current project and retain other clips, source ranges, volume and timing. Fitting is not automatic subject tracking or decorative-caption safe-area layout, and is not currently supported by the cloud worker. `small_caption_text` and `motion_exceeds_caption` require a readability check. These warnings neither auto-correct the project nor measure final glyph bounds. `warnings` contains at most 20 entries; `warning_count` includes omitted entries.

Empty or unparseable subtitle files return `invalid_subtitles`; do not treat them as a successful subtitle import. Zero-width-only text and unsupported control characters are rejected, while valid joining characters within real text are preserved. Put each caption ID only once in an edit request. On `invalid_tool_result` or `tool_execution_failed`, an operation may already have started: query known job/project state and retain the original render key instead of blindly submitting a new job.

Read `warnings` and `warning_count` on project edits, estimates and local render results. They flag known risks, not measured visual bounds. The 4,000-character caption limit is an input limit, not a readability guarantee: very long captions and very narrow canvases can successfully render with invisible text. Split long captions using provided timestamps or ASR word alignment, never invented timing. With the currently bundled fonts, Arabic, Devanagari and emoji may be omitted even when CJK and Latin render correctly; verify every requested script and select a suitable licensed font without promising universal shaping support. Setting text opacity to zero does not necessarily hide independent flower decorations. Resource quotas count per-caption copies of user and fallback fonts, so 1,000 valid caption IDs do not imply that every such project fits the configured staging budget.

An edit saves a project; it does not produce a new MP4. Render the returned revision, reuse its render idempotency key on network retries, and wait for the job to finish. Inspect representative frames at the relevant caption times. Confirm text, contrast, position, clipping and motion before claiming the requested visual result. Decorative elements can extend far beyond the text: a bottom-positioned Flower preset can have readable text while its lower decorations clip. When that matters to the request, move the effect inward using explicit y, rerender, and check again; do not claim automatic safe-area fitting. Keep the editable project ID and revision for subsequent turns. This reference does not bypass the main skill's account, license or cloud-consent requirements.
