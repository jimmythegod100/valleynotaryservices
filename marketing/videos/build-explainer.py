#!/usr/bin/env python3
"""Build branded explainer videos for Valley Notary Services.

Pipeline: Edge TTS narration → branded slides (PIL) → Ken Burns segments (ffmpeg) → concat.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
VENV_EDGE = ROOT / ".venv" / "bin" / "edge-tts"
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

DEFAULT_FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
DEFAULT_FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines or [text]


def render_slide(
    section: dict,
    brief: dict,
    out_path: Path,
) -> None:
    w, h = brief["width"], brief["height"]
    navy = hex_to_rgb(brief["dark"])
    gold = hex_to_rgb(brief["accent"])
    img = Image.new("RGB", (w, h), navy)
    draw = ImageDraw.Draw(img)

    # Gold accent bar
    draw.rectangle([0, 0, w, 8], fill=gold)
    draw.rectangle([0, h - 8, w, h], fill=gold)

    title_font = load_font(DEFAULT_FONT, 72)
    sub_font = load_font(DEFAULT_FONT_REG, 42)
    brand_font = load_font(DEFAULT_FONT, 36)
    caption_font = load_font(DEFAULT_FONT, 48)

    stype = section.get("type", "broll")
    title = section.get("title", "")
    subtitle = section.get("subtitle", "")
    caption = section.get("caption", "")

    # Brand watermark top-right
    brand = brief["brand"]
    bw = draw.textlength(brand, font=brand_font)
    draw.text((w - bw - 60, 40), brand, fill=gold, font=brand_font)

    if stype == "intro":
        draw.text((80, h // 2 - 120), title, fill=(255, 255, 255), font=title_font)
        draw.text((80, h // 2 - 20), subtitle, fill=gold, font=sub_font)
        if caption:
            cap_lines = wrap_text(draw, caption, caption_font, w - 160)
            y = h // 2 + 80
            for line in cap_lines:
                draw.text((80, y), line, fill=(200, 210, 220), font=caption_font)
                y += 58
    elif stype == "chapter":
        # Large chapter card centered
        tw = draw.textlength(title, font=title_font)
        draw.text(((w - tw) // 2, h // 2 - 100), title, fill=(255, 255, 255), font=title_font)
        if subtitle:
            sw = draw.textlength(subtitle, font=sub_font)
            draw.text(((w - sw) // 2, h // 2 + 10), subtitle, fill=gold, font=sub_font)
        draw.rectangle([w // 2 - 120, h // 2 + 90, w // 2 + 120, h // 2 + 94], fill=gold)
    elif stype == "outro":
        lines = [
            brief["brand"],
            "Mobile Notary Public · Modesto, CA",
            "valleynotaryservices.com",
            "info@valleynotaryservices.com",
            'Subject: Notary Appointment Request',
            "Modesto · Ceres · Turlock · Stanislaus County",
        ]
        y = h // 2 - 180
        for i, line in enumerate(lines):
            f = title_font if i == 0 else (sub_font if i < 3 else caption_font)
            color = gold if i == 0 else (255, 255, 255)
            lw = draw.textlength(line, font=f)
            draw.text(((w - lw) // 2, y), line, fill=color, font=f)
            y += 70 if i == 0 else 52
        disclaimer = "Not an attorney. Cannot give legal advice."
        df = load_font(DEFAULT_FONT_REG, 28)
        dw = draw.textlength(disclaimer, font=df)
        draw.text(((w - dw) // 2, h - 120), disclaimer, fill=(120, 130, 140), font=df)
    else:
        # broll
        draw.text((80, 120), title, fill=(255, 255, 255), font=title_font)
        draw.text((80, 210), subtitle, fill=gold, font=sub_font)
        if caption:
            cap_lines = wrap_text(draw, caption, caption_font, w - 160)
            y = h - 280
            draw.rectangle([60, y - 20, w - 60, y + len(cap_lines) * 58 + 20], fill=(30, 41, 59))
            for line in cap_lines:
                draw.text((80, y), line, fill=(255, 255, 255), font=caption_font)
                y += 58

    img.save(out_path, "PNG")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)


def audio_duration(path: Path) -> float:
    out = run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return float(out.stdout.strip())


def generate_tts(text: str, voice: str, mp3: Path, vtt: Path) -> None:
    edge = str(VENV_EDGE) if VENV_EDGE.exists() else "edge-tts"
    run([edge, "--text", text, "--voice", voice, "--write-media", str(mp3), "--write-subtitles", str(vtt)])


def vtt_to_srt(vtt_path: Path, srt_path: Path) -> None:
    content = vtt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", content.strip())
    srt_lines: list[str] = []
    idx = 1
    for block in blocks:
        if block.startswith("WEBVTT") or "-->" not in block:
            continue
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        timing = lines[0].replace(".", ",")
        text = " ".join(lines[1:]).strip()
        if not text:
            continue
        srt_lines.append(str(idx))
        srt_lines.append(timing)
        srt_lines.append(text)
        srt_lines.append("")
        idx += 1
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")


def ken_burns_filter(effect: str, duration: float, fps: int, w: int, h: int) -> str:
    frames = max(int(duration * fps), 1)
    if effect == "pan-right":
        return (
            f"zoompan=z='1.1':x='iw/2-(iw/zoom/2)+on*{frames}/4':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={w}x{h}:fps={fps}"
        )
    if effect == "pan-left":
        return (
            f"zoompan=z='1.1':x='iw/4-on*{frames}/4':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={w}x{h}:fps={fps}"
        )
    if effect == "zoom-out":
        return f"zoompan=z='if(lte(on,1),1.3,max(1.0,zoom-0.0008))':d={frames}:s={w}x{h}:fps={fps}"
    # zoom-in default
    return f"zoompan=z='min(zoom+0.0008,1.25)':d={frames}:s={w}x{h}:fps={fps}"


def render_segment(
    slide: Path,
    audio: Path,
    srt: Path | None,
    out: Path,
    brief: dict,
    section: dict,
    duration: float,
) -> None:
    w, h, fps = brief["width"], brief["height"], brief["fps"]
    kb = ken_burns_filter(section.get("kenBurns", "zoom-in"), duration, fps, w, h)
    hold = float(section.get("holdSeconds", 0))
    total = duration + hold

    vf_parts = [f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", kb]
    # On-slide caption bars provide mute-viewing text; skip ffmpeg subtitles (macOS filter escaping).

    vf = ",".join(vf_parts)

    # Extend audio with silence for hold on outro
    audio_input = audio
    if hold > 0:
        silent = out.parent / f"{out.stem}_silence.wav"
        run(
            [
                FFMPEG,
                "-y",
                "-i",
                str(audio),
                "-f",
                "lavfi",
                "-i",
                f"anullsrc=r=44100:cl=stereo",
                "-filter_complex",
                f"[0:a][1:a]concat=n=2:v=0:a=1,apad=pad_dur={hold}[aout]",
                "-map",
                "[aout]",
                "-t",
                str(total),
                str(silent.with_suffix(".mp3")),
            ]
        )
        audio_input = silent.with_suffix(".mp3")

    cmd = [
        FFMPEG,
        "-y",
        "-loop",
        "1",
        "-i",
        str(slide),
        "-i",
        str(audio_input),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-t",
        str(total),
        str(out),
    ]
    run(cmd)


def build(brief_path: Path, output_path: Path) -> dict:
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    work = ROOT / "work" / brief["id"]
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    segments_dir = work / "segments"
    segments_dir.mkdir()

    segment_files: list[Path] = []
    total_duration = 0.0
    voice = brief.get("voice", "en-US-AndrewNeural")

    for i, section in enumerate(brief["sections"]):
        prefix = f"{i:02d}"
        slide = work / f"{prefix}_slide.png"
        mp3 = work / f"{prefix}_audio.mp3"
        vtt = work / f"{prefix}_audio.vtt"
        srt = work / f"{prefix}_audio.srt"
        seg = segments_dir / f"{prefix}.mp4"

        render_slide(section, brief, slide)
        narration = section.get("narration", "")
        if not narration.strip():
            continue
        generate_tts(narration, voice, mp3, vtt)
        vtt_to_srt(vtt, srt)
        dur = audio_duration(mp3)
        hold = float(section.get("holdSeconds", 0))
        total_duration += dur + hold
        render_segment(slide, mp3, srt, seg, brief, section, dur)
        segment_files.append(seg)
        print(f"  [{i + 1}/{len(brief['sections'])}] {section.get('title', prefix)} — {dur:.1f}s")

    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p}'" for p in segment_files), encoding="utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(output_path),
        ]
    )

    final_dur = audio_duration(output_path) if output_path.exists() else total_duration
    probe = run(
        [
            FFPROBE,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-of",
            "json",
            str(output_path),
        ]
    )
    meta = json.loads(probe.stdout)
    stream = meta["streams"][0]
    fps_parts = stream["r_frame_rate"].split("/")
    fps_val = int(fps_parts[0]) / int(fps_parts[1]) if len(fps_parts) == 2 else brief["fps"]

    return {
        "path": str(output_path),
        "duration": round(final_dur, 1),
        "width": stream["width"],
        "height": stream["height"],
        "fps": fps_val,
        "sections": len(segment_files),
    }


def resolve_path(p: Path, base: Path) -> Path:
    if p.is_absolute():
        return p
    cwd_candidate = Path.cwd() / p
    if cwd_candidate.parent.exists():
        return cwd_candidate
    return base / p.name if p.name == str(p) else base / p


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: build-explainer.py <brief.json> [output.mp4]")
        sys.exit(1)
    brief_path = resolve_path(Path(sys.argv[1]), ROOT)
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    if len(sys.argv) > 2:
        out = resolve_path(Path(sys.argv[2]), ROOT)
    else:
        out = ROOT / "output" / f"{brief['id']}.mp4"
    print(f"Building {brief_path.name} → {out}")
    meta = build(brief_path, out)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
