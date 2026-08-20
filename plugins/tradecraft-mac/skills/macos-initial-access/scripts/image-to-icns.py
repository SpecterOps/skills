#!/usr/bin/env python3
"""Create a complete macOS ICNS file from an image that sips can read."""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


RENDITIONS = (
    (b"icp4", 16, "icon_16x16.png"),
    (b"ic11", 32, "icon_16x16@2x.png"),
    (b"icp5", 32, "icon_32x32.png"),
    (b"ic12", 64, "icon_32x32@2x.png"),
    (b"ic07", 128, "icon_128x128.png"),
    (b"ic13", 256, "icon_128x128@2x.png"),
    (b"ic08", 256, "icon_256x256.png"),
    (b"ic14", 512, "icon_256x256@2x.png"),
    (b"ic09", 512, "icon_512x512.png"),
    (b"ic10", 1024, "icon_512x512@2x.png"),
)


class ConversionError(Exception):
    pass


def run_sips(sips: str, *arguments: object, capture: bool = False) -> str:
    result = subprocess.run(
        [sips, *(str(argument) for argument in arguments)],
        check=False,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip()
        raise ConversionError(detail or "sips failed")
    return result.stdout or ""


def image_size(sips: str, image: Path) -> tuple[int, int]:
    properties = run_sips(
        sips, "-g", "pixelWidth", "-g", "pixelHeight", image, capture=True
    )
    values = {}
    for line in properties.splitlines():
        key, separator, value = line.strip().partition(":")
        if separator:
            values[key] = value.strip()
    try:
        width = int(values["pixelWidth"])
        height = int(values["pixelHeight"])
    except (KeyError, ValueError) as error:
        raise ConversionError("input has no valid pixel dimensions") from error
    if width < 1 or height < 1:
        raise ConversionError("input has no valid pixel dimensions")
    return width, height


def make_master(sips: str, source: Path, destination: Path, work: Path) -> None:
    width, height = image_size(sips, source)
    if width > height:
        run_sips(
            sips,
            "--setProperty",
            "format",
            "png",
            "--resampleHeight",
            1024,
            source,
            "--out",
            work,
        )
        run_sips(sips, "--cropToHeightWidth", 1024, 1024, work, "--out", destination)
    elif height > width:
        run_sips(
            sips,
            "--setProperty",
            "format",
            "png",
            "--resampleWidth",
            1024,
            source,
            "--out",
            work,
        )
        run_sips(sips, "--cropToHeightWidth", 1024, 1024, work, "--out", destination)
    else:
        run_sips(
            sips,
            "--setProperty",
            "format",
            "png",
            "--resampleHeightWidth",
            1024,
            1024,
            source,
            "--out",
            destination,
        )


def make_renditions(sips: str, master: Path, iconset: Path) -> None:
    iconset.mkdir()
    for _, size, name in RENDITIONS:
        run_sips(
            sips,
            "--resampleHeightWidth",
            size,
            size,
            master,
            "--out",
            iconset / name,
        )


def build_icns(iconset: Path) -> bytes:
    chunks = []
    for kind, _, name in RENDITIONS:
        data = (iconset / name).read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ConversionError(f"generated rendition is not PNG: {name}")
        chunks.append(kind + struct.pack(">I", len(data) + 8) + data)
    body = b"".join(chunks)
    return b"icns" + struct.pack(">I", len(body) + 8) + body


def write_new_file(path: Path, data: bytes) -> None:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as error:
        raise ConversionError(f"output already exists: {path}") from error
    with os.fdopen(descriptor, "wb") as output:
        output.write(data)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a complete macOS ICNS file. Non-square input is "
            "center-cropped; existing output is never overwritten."
        )
    )
    parser.add_argument("input_image", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    return parser.parse_args()


def convert(source: Path, output: Path) -> None:
    sips = shutil.which("sips")
    if sips is None:
        raise ConversionError("required macOS command not found: sips")
    if not source.is_file():
        raise ConversionError(f"input is not a readable file: {source}")
    if output.suffix != ".icns":
        raise ConversionError("output path must end in .icns")
    if not output.parent.is_dir():
        raise ConversionError(f"output directory does not exist: {output.parent}")
    if output.exists():
        raise ConversionError(f"output already exists: {output}")

    with tempfile.TemporaryDirectory(prefix="image-to-icns.") as temporary:
        root = Path(temporary)
        master = root / "master.png"
        make_master(sips, source, master, root / "working.png")
        iconset = root / "AppIcon.iconset"
        make_renditions(sips, master, iconset)
        data = build_icns(iconset)

    write_new_file(output, data)
    try:
        properties = run_sips(sips, "-g", "format", output, capture=True)
        if "format: icns" not in properties:
            raise ConversionError("output is not a valid ICNS file")
    except ConversionError:
        output.unlink(missing_ok=True)
        raise


def main() -> int:
    arguments = parse_arguments()
    source = arguments.input_image
    output = arguments.output or source.with_suffix(".icns")
    try:
        convert(source, output)
    except (ConversionError, OSError) as error:
        print(f"image-to-icns: {error}", file=sys.stderr)
        return 1
    print(f"Created {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
