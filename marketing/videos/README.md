# Valley Notary Services — Generated Marketing Videos

Full watchable MP4s produced via **Edge TTS + ffmpeg Ken Burns** pipeline (see `build-explainer.py`).

## Outputs

| File | Format | Duration | Resolution |
|------|--------|----------|------------|
| `video-01-mobile-notary-modesto.mp4` | A — General mobile notary | ~3:50 | 1920×1080 @ 30fps |
| `video-02-loan-signing.mp4` | B — Loan & real estate | ~1:47 | 1920×1080 @ 30fps |
| `video-03-estate-family.mp4` | C — Estate & family at home | ~1:28 | 1920×1080 @ 30fps |

Copies for site embed: `../../public/videos/`

## Rebuild

```bash
cd marketing/videos
python3 -m venv .venv && .venv/bin/pip install edge-tts pillow
.venv/bin/python build-explainer.py briefs/video-01.json video-01-mobile-notary-modesto.mp4
```

## Briefs

- `briefs/video-01.json` — Format A (from `video-01-script.md`)
- `briefs/video-02-loan-signing.json` — Format B
- `briefs/video-03-estate-family.json` — Format C

## Brand

- Navy `#0f172a`, gold `#d97706`
- Voice: Edge TTS `en-US-AndrewNeural`
- CTA: info@valleynotaryservices.com · subject **Notary Appointment Request**
- No invented person name — narrated as “Valley Notary Services / your local California notary”

## QC (2026-07-23)

Video 01 frame review at 0/25/50/75/99%: navy/gold branding, chapter cards, caption bars, end card with email CTA — no black frames. Audio: intelligible TTS, no dropouts (afplay + RMS check).

## Next steps (human)

1. Upload to Google Business Profile, YouTube, Facebook
2. Add phone number to end cards when published on site
3. Replace with face-on-camera footage when available (higher conversion for notary niche)
