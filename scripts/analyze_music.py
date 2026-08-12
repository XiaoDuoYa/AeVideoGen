#!/usr/bin/env python3
"""Analyze musical energy, onsets, tempo, climax points, and candidate edit windows."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import statistics
import subprocess
import sys
from array import array
from pathlib import Path


def decode_mono(path: Path, sample_rate: int) -> list[float]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required but was not found in PATH")
    command = [
        ffmpeg,
        "-v",
        "error",
        "-i",
        str(path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "f32le",
        "pipe:1",
    ]
    result = subprocess.run(command, check=False, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip())
    samples = array("f")
    samples.frombytes(result.stdout)
    if sys.byteorder != "little":
        samples.byteswap()
    return list(samples)


def moving_average(values: list[float], radius: int) -> list[float]:
    if not values:
        return []
    prefix = [0.0]
    for value in values:
        prefix.append(prefix[-1] + value)
    output = []
    for index in range(len(values)):
        left = max(0, index - radius)
        right = min(len(values), index + radius + 1)
        output.append((prefix[right] - prefix[left]) / (right - left))
    return output


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    ordered = sorted(values)
    low = ordered[int(0.05 * (len(ordered) - 1))]
    high = ordered[int(0.95 * (len(ordered) - 1))]
    span = max(high - low, 1e-9)
    return [max(0.0, min(1.0, (value - low) / span)) for value in values]


def local_peaks(
    values: list[float], hop_seconds: float, minimum_distance: float, limit: int
) -> list[dict[str, float]]:
    candidates: list[tuple[float, int]] = []
    for index in range(1, len(values) - 1):
        if values[index] >= values[index - 1] and values[index] > values[index + 1]:
            candidates.append((values[index], index))
    candidates.sort(reverse=True)
    selected: list[tuple[float, int]] = []
    distance = max(1, round(minimum_distance / hop_seconds))
    for score, index in candidates:
        if all(abs(index - other_index) >= distance for _, other_index in selected):
            selected.append((score, index))
        if len(selected) >= limit:
            break
    selected.sort(key=lambda item: item[1])
    return [
        {"time": round(index * hop_seconds, 3), "score": round(score, 4)}
        for score, index in selected
    ]


def estimate_tempo(
    novelty: list[float], hop_seconds: float
) -> tuple[float | None, float, list[dict[str, float]]]:
    if len(novelty) < 20:
        return None, 0.0, []
    centered = [value - statistics.fmean(novelty) for value in novelty]
    scored: list[tuple[float, float]] = []
    minimum_lag = max(1, round((60.0 / 180.0) / hop_seconds))
    maximum_lag = max(minimum_lag, round((60.0 / 70.0) / hop_seconds))
    for lag in range(minimum_lag, maximum_lag + 1):
        if lag >= len(centered):
            continue
        bpm = 60.0 / (lag * hop_seconds)
        score = sum(
            max(centered[index], 0.0) * max(centered[index - lag], 0.0)
            for index in range(lag, len(centered))
        ) / max(1, len(centered) - lag)
        scored.append((score, bpm))
    if not scored:
        return None, 0.0, []
    scored.sort(reverse=True)
    global_best = scored[0]
    practical = [item for item in scored if 90 <= item[1] <= 150]
    selected = global_best
    if practical and not 90 <= global_best[1] <= 150:
        practical_best = max(practical)
        if practical_best[0] >= global_best[0] * 0.62:
            selected = practical_best
    best_score, best_bpm = selected
    confidence = 0.0
    scores = [item[0] for item in scored]
    if max(scores) > 0:
        confidence = min(1.0, best_score / (statistics.fmean(scores) + 1e-9) / 4)
    candidates = [
        {"bpm": round(bpm, 2), "score": round(score / (max(scores) + 1e-9), 4)}
        for score, bpm in scored[:5]
    ]
    return best_bpm, confidence, candidates


def recommend_windows(
    energy: list[float],
    novelty: list[float],
    hop_seconds: float,
    duration: float,
    target_duration: float,
) -> list[dict[str, float]]:
    if target_duration >= duration:
        peak_index = max(range(len(energy)), key=energy.__getitem__) if energy else 0
        return [
            {
                "start": 0.0,
                "end": round(duration, 3),
                "climax_time": round(peak_index * hop_seconds, 3),
                "climax_in_window": round(peak_index * hop_seconds, 3),
                "score": 1.0,
            }
        ]

    hop_count = max(1, round(target_duration / hop_seconds))
    step = max(1, round(0.5 / hop_seconds))
    candidates: list[dict[str, float]] = []
    for start_index in range(0, max(1, len(energy) - hop_count), step):
        end_index = min(len(energy), start_index + hop_count)
        segment = energy[start_index:end_index]
        segment_novelty = novelty[start_index:end_index]
        if len(segment) < hop_count * 0.95:
            continue
        local_peak = max(range(len(segment)), key=segment.__getitem__)
        peak_position = local_peak / max(1, len(segment) - 1)
        early = statistics.fmean(segment[: max(1, len(segment) // 3)])
        late_peak = max(segment[len(segment) // 2 :], default=max(segment))
        dynamic = statistics.pstdev(segment)
        onset_strength = statistics.fmean(segment_novelty)
        climax_shape = max(0.0, 1.0 - abs(peak_position - 0.64) / 0.64)
        score = (
            0.38 * max(0.0, late_peak - early)
            + 0.22 * dynamic
            + 0.18 * onset_strength
            + 0.22 * climax_shape
        )
        climax_time = (start_index + local_peak) * hop_seconds
        candidates.append(
            {
                "start": round(start_index * hop_seconds, 3),
                "end": round(min(duration, start_index * hop_seconds + target_duration), 3),
                "climax_time": round(climax_time, 3),
                "climax_in_window": round(local_peak * hop_seconds, 3),
                "score": round(score, 5),
            }
        )
    candidates.sort(key=lambda item: item["score"], reverse=True)
    selected = []
    for candidate in candidates:
        if all(abs(candidate["start"] - item["start"]) >= 3.0 for item in selected):
            selected.append(candidate)
        if len(selected) >= 5:
            break
    return selected


def analyze(args: argparse.Namespace) -> dict:
    path = Path(args.input).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    samples = decode_mono(path, args.sample_rate)
    duration = len(samples) / args.sample_rate
    hop_samples = max(1, round(args.hop * args.sample_rate))
    window_samples = max(hop_samples, round(0.1 * args.sample_rate))
    rms: list[float] = []
    for start in range(0, max(1, len(samples) - window_samples + 1), hop_samples):
        frame = samples[start : start + window_samples]
        if not frame:
            continue
        rms.append(math.sqrt(sum(value * value for value in frame) / len(frame)))

    smoothed = moving_average(rms, 2)
    energy = normalize(smoothed)
    novelty_raw = []
    for index, value in enumerate(smoothed):
        history = smoothed[max(0, index - 8) : index]
        baseline = statistics.fmean(history) if history else value
        novelty_raw.append(max(0.0, value - baseline))
    novelty = normalize(moving_average(novelty_raw, 1))
    combined = [
        0.62 * energy[index] + 0.38 * novelty[index]
        for index in range(min(len(energy), len(novelty)))
    ]

    tempo, confidence, tempo_candidates = estimate_tempo(novelty, args.hop)
    onsets = local_peaks(novelty, args.hop, 0.2, 80)
    climaxes = local_peaks(combined, args.hop, 3.0, 12)
    climaxes.sort(key=lambda item: item["score"], reverse=True)
    sections = local_peaks(moving_average(novelty, 8), args.hop, 4.0, 16)

    beat_times: list[float] = []
    if tempo:
        interval = 60.0 / tempo
        phase_candidates = onsets[: min(40, len(onsets))]
        phase = phase_candidates[0]["time"] if phase_candidates else 0.0
        if phase_candidates:
            phase = max(
                (item["time"] for item in phase_candidates),
                key=lambda candidate: sum(
                    1.0
                    for item in phase_candidates
                    if abs(((item["time"] - candidate) / interval) - round((item["time"] - candidate) / interval))
                    < 0.12
                ),
            )
        while phase - interval >= 0:
            phase -= interval
        current = phase
        while current <= duration:
            if current >= 0:
                beat_times.append(round(current, 3))
            current += interval

    return {
        "input": str(path),
        "duration": round(duration, 3),
        "sample_rate": args.sample_rate,
        "analysis_hop_seconds": args.hop,
        "estimated_bpm": round(tempo, 2) if tempo else None,
        "tempo_confidence": round(confidence, 3),
        "tempo_candidates": tempo_candidates,
        "climax_candidates": climaxes,
        "section_change_candidates": sections,
        "onset_candidates": onsets,
        "beat_times": beat_times,
        "recommended_windows": recommend_windows(
            energy, novelty, args.hop, duration, args.target_duration
        ),
        "note": "Use these markers as audition candidates; confirm the edit and climax by listening.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Audio file supported by ffmpeg")
    parser.add_argument("--target-duration", type=float, default=30.0)
    parser.add_argument("--sample-rate", type=int, default=8000)
    parser.add_argument("--hop", type=float, default=0.05)
    parser.add_argument("--output", help="Write JSON to this path; otherwise print to stdout")
    args = parser.parse_args()
    if args.target_duration <= 0 or args.sample_rate <= 0 or args.hop <= 0:
        parser.error("target duration, sample rate, and hop must be positive")
    try:
        result = analyze(args)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
