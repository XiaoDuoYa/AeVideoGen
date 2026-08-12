#!/usr/bin/env python3
"""Validate an AeVideoGen production.json timeline and approval contract."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


def reading_seconds(text: str) -> float:
    cjk = len(re.findall(r"[\u3400-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z0-9]+", text))
    punctuation = len(re.findall(r"[，。！？；：,.!?;:]", text))
    return max(0.5, cjk / 6.0 + latin_words / 3.0 + punctuation * 0.08 + 0.25)


def number(value, fallback=None):
    return float(value) if isinstance(value, (int, float)) and math.isfinite(value) else fallback


def validate(data: dict, final: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    project = data.get("project", {})
    constraints = data.get("constraints", {})
    duration = number(project.get("duration"))
    fps = number(project.get("fps"))
    width = number(project.get("width"))
    height = number(project.get("height"))
    if not duration or duration <= 0:
        errors.append("project.duration must be positive")
    if not fps or fps <= 0:
        errors.append("project.fps must be positive")
    if not width or not height or width <= 0 or height <= 0:
        errors.append("project.width and project.height must be positive")
    if constraints.get("noHyperFrames") is not True:
        errors.append("constraints.noHyperFrames must be true")

    render = data.get("render", {})
    if isinstance(render, dict) and render:
        pixel_scale = number(render.get("pixelScale"), 1.0)
        output_width = number(render.get("outputWidth"))
        output_height = number(render.get("outputHeight"))
        if pixel_scale is None or pixel_scale <= 0:
            errors.append("render.pixelScale must be positive")
        if output_width is not None and width is not None and pixel_scale is not None:
            if abs(output_width - width * pixel_scale) > 0.5:
                errors.append("render.outputWidth must equal project.width * render.pixelScale")
        if output_height is not None and height is not None and pixel_scale is not None:
            if abs(output_height - height * pixel_scale) > 0.5:
                errors.append("render.outputHeight must equal project.height * render.pixelScale")

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a non-empty array")
        scenes = []
    ids: set[str] = set()
    scene_by_id: dict[str, dict] = {}
    parsed_scenes: list[tuple[float, float, dict]] = []
    max_static = number(constraints.get("maxStaticSeconds"), 0.65)
    min_hold = number(constraints.get("minSubjectHoldSeconds"), 1.2)
    primary_scenes = 0

    for index, scene in enumerate(scenes):
        prefix = f"scenes[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{prefix} must be an object")
            continue
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id.strip():
            errors.append(f"{prefix}.id is required")
            scene_id = f"invalid-{index}"
        elif scene_id in ids:
            errors.append(f"duplicate scene id: {scene_id}")
        ids.add(scene_id)
        scene_by_id[scene_id] = scene
        start = number(scene.get("start"))
        end = number(scene.get("end"))
        if start is None or end is None or start < 0 or end <= start:
            errors.append(f"{prefix} needs 0 <= start < end")
            continue
        if duration and end > duration + 1 / max(fps or 30, 1):
            errors.append(f"{prefix}.end exceeds project.duration")
        parsed_scenes.append((start, end, scene))
        scene_duration = end - start
        if scene.get("priority") == "primary":
            primary_scenes += 1
        motion = scene.get("motion", {})
        if isinstance(motion, dict) and motion.get("continuous") is False and scene_duration > max_static:
            errors.append(
                f"{scene_id} is static for {scene_duration:.2f}s; max is {max_static:.2f}s"
            )
        if isinstance(motion, dict):
            camera_moves = number(motion.get("cameraMoves"))
            if camera_moves is not None and camera_moves > 1:
                warnings.append(
                    f"{scene_id} has {camera_moves:.0f} camera destinations; prevent corrective recentering"
                )
        focus = scene.get("focus")
        if focus is not None:
            if not isinstance(focus, dict):
                errors.append(f"{scene_id}.focus must be an object")
            else:
                for axis in ("x", "y"):
                    value = number(focus.get(axis))
                    if value is None or not 0 <= value <= 1:
                        errors.append(f"{scene_id}.focus.{axis} must be normalized 0..1")
                scale = number(focus.get("scale"))
                if scale is None or scale < 1:
                    errors.append(f"{scene_id}.focus.scale must be >= 1")
                elif scale > 3.2:
                    warnings.append(f"{scene_id}.focus.scale={scale:.2f} needs readability review")
        text = scene.get("text")
        if isinstance(text, str) and text.strip():
            readable = number(scene.get("readabilitySeconds"), scene_duration)
            estimate = reading_seconds(text)
            if readable < estimate * 0.8:
                warnings.append(
                    f"{scene_id} exposes text for {readable:.2f}s; estimated reading time is {estimate:.2f}s"
                )
            line_policy = scene.get("linePolicy")
            if constraints.get("forbidAccidentalWrap", False) and not isinstance(line_policy, dict):
                warnings.append(f"{scene_id} has important text without linePolicy")
            elif isinstance(line_policy, dict):
                mode = line_policy.get("mode")
                if mode not in ("single-line", "exact-lines"):
                    errors.append(f"{scene_id}.linePolicy.mode must be single-line or exact-lines")
                if mode == "single-line" and ("\n" in text or "<br" in text.lower()):
                    errors.append(f"{scene_id} is single-line but text contains an explicit break")
                if mode == "exact-lines":
                    lines = line_policy.get("lines")
                    if not isinstance(lines, list) or not lines or any(not isinstance(line, str) or not line for line in lines):
                        errors.append(f"{scene_id}.linePolicy.lines must be a non-empty string array")
        if scene.get("kind") in ("ui", "chat", "interaction") and not scene.get("visualGroup"):
            warnings.append(f"{scene_id} has no visualGroup; verify the meaningful group is centered")

    parsed_scenes.sort(key=lambda item: item[0])
    if parsed_scenes and duration and fps:
        tolerance = 1 / fps + 1e-6
        coverage = 0.0
        for start, end, scene in parsed_scenes:
            if start > coverage + tolerance:
                errors.append(f"timeline gap from {coverage:.3f}s to {start:.3f}s")
            coverage = max(coverage, end)
        if coverage < duration - tolerance:
            errors.append(f"timeline ends at {coverage:.3f}s before duration {duration:.3f}s")

    for index in range(len(parsed_scenes) - 1):
        start, end, scene = parsed_scenes[index]
        next_scene = parsed_scenes[index + 1][2]
        if (
            end - start < min_hold
            and scene.get("subject")
            and next_scene.get("subject")
            and scene.get("subject") != next_scene.get("subject")
            and scene.get("kind") != "transition"
        ):
            warnings.append(
                f"{scene.get('id')} changes subject after {end - start:.2f}s; review center stability"
            )

    if primary_scenes != 1:
        errors.append(f"exactly one scene must have priority=primary; found {primary_scenes}")

    interactions = data.get("interactions", [])
    if not isinstance(interactions, list):
        errors.append("interactions must be an array")
        interactions = []
    for index, interaction in enumerate(interactions):
        prefix = f"interactions[{index}]"
        if not isinstance(interaction, dict):
            errors.append(f"{prefix} must be an object")
            continue
        timestamp = number(interaction.get("time"))
        if timestamp is None or timestamp < 0 or (duration and timestamp > duration):
            errors.append(f"{prefix}.time must be within the video")
        if interaction.get("action") == "click":
            if not interaction.get("target"):
                errors.append(f"{prefix}.target is required for a click")
            x = number(interaction.get("x"))
            y = number(interaction.get("y"))
            if x is None or y is None or not (0 <= x <= 1 and 0 <= y <= 1):
                errors.append(f"{prefix} click coordinates must be normalized 0..1")
            if interaction.get("coordinateSource") != "dom-rect":
                warnings.append(f"{prefix} should use coordinateSource=dom-rect")
            focus_scene_id = interaction.get("focusScene")
            focus_scene = scene_by_id.get(focus_scene_id)
            if focus_scene_id and not focus_scene:
                errors.append(f"{prefix}.focusScene does not exist: {focus_scene_id}")
            elif focus_scene and isinstance(focus_scene.get("focus"), dict) and x is not None and y is not None:
                focus = focus_scene["focus"]
                fx = number(focus.get("x"))
                fy = number(focus.get("y"))
                if fx is not None and fy is not None and math.hypot(x - fx, y - fy) > 0.18:
                    warnings.append(
                        f"{prefix} click and camera focus differ; verify that the zoom follows the target"
                    )

    audio = data.get("audio", {})
    climax = number(audio.get("climaxAt")) if isinstance(audio, dict) else None
    if climax is not None and duration and not 0 <= climax <= duration:
        errors.append("audio.climaxAt must be inside the video")
    if climax is not None:
        covering = [
            scene
            for start, end, scene in parsed_scenes
            if start <= climax <= end
        ]
        if not covering:
            errors.append("audio.climaxAt is not covered by a scene")
        elif not any(scene.get("priority") == "primary" for scene in covering):
            errors.append("the scene covering audio.climaxAt must have priority=primary")
    elif scenes:
        warnings.append("audio.climaxAt is missing; confirm how the main promise maps to the music")

    approval = data.get("approval", {})
    approval_required = constraints.get("approvalRequiredBeforeFinalRender", True)
    if final and approval_required:
        if not isinstance(approval, dict) or approval.get("status") != "approved":
            errors.append("final render is blocked until approval.status is approved")
        if not isinstance(approval, dict) or not approval.get("approvedVersion"):
            errors.append("final render requires approval.approvedVersion")
    if final:
        if not isinstance(approval, dict) or approval.get("exportRequested") is not True:
            errors.append("final render requires a separate explicit export request")
        if not isinstance(approval, dict) or approval.get("exportSpecConfirmed") is not True:
            errors.append("final render requires an explicitly confirmed export specification")
        export_spec = approval.get("exportSpec") if isinstance(approval, dict) else None
        if not isinstance(export_spec, dict):
            errors.append("final render requires approval.exportSpec")
        else:
            for field in ("width", "height", "fps", "format", "videoCodec", "audioCodec", "filename"):
                if export_spec.get(field) in (None, ""):
                    errors.append(f"approval.exportSpec.{field} is required")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to production.json")
    parser.add_argument("--final", action="store_true", help="Enforce final-render approval")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()
    path = Path(args.manifest)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    errors, warnings = validate(data, args.final)
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
