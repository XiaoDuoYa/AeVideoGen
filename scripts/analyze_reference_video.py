#!/usr/bin/env python3
"""Extract dense, timestamped frames and transition windows from a reference video."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


PTS_RE = re.compile(r"pts_time:([0-9.]+)")


def executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found in PATH")
    return path


def run(command: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(command, check=False, capture_output=capture, text=capture)
    if result.returncode != 0:
        detail = result.stderr.strip() if capture else "command failed"
        raise RuntimeError(f"{command[0]} exited with {result.returncode}: {detail}")
    return result


def probe(path: Path) -> dict:
    result = run(
        [
            executable("ffprobe"), "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(path),
        ],
        capture=True,
    )
    return json.loads(result.stdout)


def duration_seconds(metadata: dict) -> float:
    duration = metadata.get("format", {}).get("duration")
    if duration is not None:
        return float(duration)
    for stream in metadata.get("streams", []):
        if stream.get("duration") is not None:
            return float(stream["duration"])
    raise RuntimeError("could not determine video duration")


def detect_scenes(path: Path, threshold: float) -> list[float]:
    result = subprocess.run(
        [
            executable("ffmpeg"), "-hide_banner", "-loglevel", "info", "-i", str(path),
            "-vf", f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"scene detection failed: {result.stderr.strip()}")
    return sorted({round(float(match), 4) for match in PTS_RE.findall(result.stderr)})


def extract_frames(path: Path, output_pattern: Path, fps: float, width: int, start=None, length=None):
    command = [executable("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y"]
    if start is not None:
        command += ["-ss", f"{start:.6f}"]
    command += ["-i", str(path)]
    if length is not None:
        command += ["-t", f"{length:.6f}"]
    command += [
        "-vf", f"fps={fps:.8f},scale={width}:-2:flags=lanczos",
        "-q:v", "3", "-start_number", "0", str(output_pattern),
    ]
    run(command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Reference video supported by ffmpeg")
    parser.add_argument("--output-dir", default="reference-analysis")
    parser.add_argument("--overview-fps", type=float, default=4.0)
    parser.add_argument("--dense-fps", type=float, default=10.0)
    parser.add_argument("--dense-radius", type=float, default=0.9)
    parser.add_argument("--scene-threshold", type=float, default=0.28)
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--max-overview-frames", type=int, default=1800)
    parser.add_argument("--max-dense-windows", type=int, default=80)
    args = parser.parse_args()
    if min(args.overview_fps, args.dense_fps, args.dense_radius, args.scene_threshold, args.width) <= 0:
        parser.error("fps, radius, scene threshold, and width must be positive")

    source = Path(args.input).expanduser().resolve()
    output = Path(args.output_dir).expanduser().resolve()
    if not source.is_file():
        print(f"error: input not found: {source}", file=sys.stderr)
        return 1
    if output.exists() and any(output.iterdir()):
        print(f"error: refusing to reuse non-empty output directory: {output}", file=sys.stderr)
        return 1

    try:
        metadata = probe(source)
        duration = duration_seconds(metadata)
        effective_fps = min(args.overview_fps, args.max_overview_frames / max(duration, 0.001))
        overview = output / "overview"
        dense = output / "dense-transitions"
        overview.mkdir(parents=True, exist_ok=True)
        dense.mkdir(parents=True, exist_ok=True)
        extract_frames(source, overview / "%06d.jpg", effective_fps, args.width)
        scene_times = detect_scenes(source, args.scene_threshold)[: args.max_dense_windows]
        windows = []
        for index, center in enumerate(scene_times, start=1):
            start = max(0.0, center - args.dense_radius)
            end = min(duration, center + args.dense_radius)
            folder = dense / f"{index:03d}_{center:010.4f}s"
            folder.mkdir(parents=True, exist_ok=True)
            extract_frames(source, folder / "%04d.jpg", args.dense_fps, args.width, start, end - start)
            windows.append({"center": center, "start": round(start, 4), "end": round(end, 4), "folder": str(folder)})

        warnings = []
        if effective_fps < 2:
            warnings.append("Overview extraction fell below 2fps because of max-overview-frames; increase the cap or obtain user approval before style analysis.")
        result = {
            "skillVersion": "1.0.1",
            "source": str(source),
            "duration": round(duration, 4),
            "metadata": metadata,
            "overview": {
                "requestedFps": args.overview_fps,
                "effectiveFps": round(effective_fps, 6),
                "folder": str(overview),
            },
            "sceneThreshold": args.scene_threshold,
            "sceneChangeTimes": scene_times,
            "denseFps": args.dense_fps,
            "denseWindows": windows,
            "warnings": warnings,
            "nextStep": "Inspect extracted frames, then watch the full source at normal speed with audio and write a motion-language ledger.",
        }
        (output / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output / 'analysis.json'}")
        print(f"overview: {effective_fps:.3f} fps; transitions: {len(windows)} windows at {args.dense_fps:.3f} fps")
        for warning in warnings:
            print(f"warning: {warning}")
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
