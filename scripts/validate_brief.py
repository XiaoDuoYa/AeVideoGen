#!/usr/bin/env python3
"""Validate an AeVideoGen v1.0.1 brief and its permission-to-assume contract."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def get(data: dict, dotted: str):
    value = data
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def validate(data: dict, final: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "product.name",
        "product.type",
        "product.sourcePath",
        "product.sourceVersion",
        "audience.primary",
        "audience.platform",
        "story.primaryPromise",
        "story.featurePriority",
        "story.mustShow",
        "brand.language",
        "music.path",
        "music.rightsConfirmed",
        "music.allowedRange",
        "music.climaxIntent",
        "output.durationSeconds",
        "output.aspectRatio",
        "output.width",
        "output.height",
        "output.fps",
        "output.format",
        "constraints.forbidden",
        "constraints.privacy",
        "constraints.approvalRequired",
    ]
    for field in required:
        if missing(get(data, field)):
            errors.append(f"missing blocking field: {field}")

    if data.get("skillVersion") != "1.0.1":
        errors.append("skillVersion must be 1.0.1")

    for field in ("output.durationSeconds", "output.width", "output.height", "output.fps"):
        value = get(data, field)
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            errors.append(f"{field} must be a positive number")

    if get(data, "music.rightsConfirmed") is not True:
        errors.append("music.rightsConfirmed must be true or the music must be replaced")
    if get(data, "constraints.approvalRequired") is not True:
        warnings.append("approvalRequired is not true; confirm that the user explicitly waived preview approval")
    forbidden = get(data, "constraints.forbidden")
    if isinstance(forbidden, list) and not any(str(item).lower() == "hyperframes" for item in forbidden):
        errors.append("constraints.forbidden must include HyperFrames")

    assumptions = data.get("assumptions", [])
    if not isinstance(assumptions, list):
        errors.append("assumptions must be an array")
    else:
        for index, item in enumerate(assumptions):
            if not isinstance(item, dict):
                errors.append(f"assumptions[{index}] must be an object")
                continue
            for key in ("field", "value", "reason", "confidence", "impact"):
                if missing(item.get(key)):
                    errors.append(f"assumptions[{index}].{key} is required")
            if item.get("authorizedByUser") is not True:
                errors.append(f"assumptions[{index}] lacks explicit user authorization")

    references = data.get("references", [])
    if references is not None and not isinstance(references, list):
        errors.append("references must be an array")
    elif isinstance(references, list):
        for index, item in enumerate(references):
            if not isinstance(item, dict) or missing(item.get("path")) or missing(item.get("role")):
                errors.append(f"references[{index}] requires path and role")

    if data.get("status") != "complete":
        errors.append("brief status must be complete before implementation")
    if final and assumptions:
        warnings.append("final brief contains assumptions; surface them during approval")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", help="Path to brief.json")
    parser.add_argument("--final", action="store_true", help="Apply final-delivery warnings")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()
    path = Path(args.brief)
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
