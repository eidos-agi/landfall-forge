"""Universal `landfall` command.

The command is intentionally small and stdlib-only. It does not contain
domain-specific landfall behavior; it finds repo-local `landfalls/*.yaml`
contracts and turns them into agent-readable briefs. When a repo has no
landfalls, it falls back through forge-forge so the agent can discover the
canonical landfall-forge patterns.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable

from . import __version__


FORGE_FALLBACK = Path.home() / "repos-eidos-agi" / "forge-forge" / ".venv" / "bin" / "forge"
LANDFALL_FORGE = Path.home() / "repos-eidos-agi" / "landfall-forge"
STOP_WORDS = {
    "and",
    "for",
    "the",
    "with",
    "from",
    "this",
    "that",
    "landfall",
    "please",
    "use",
    "run",
}


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def landfalls_dir(root: Path) -> Path:
    return root / "landfalls"


def landfall_files(root: Path) -> list[Path]:
    directory = landfalls_dir(root)
    if not directory.exists():
        return []
    return sorted(p for p in directory.glob("*.yaml") if p.is_file())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, str):
                return parsed
        except (SyntaxError, ValueError):
            pass
    return value.strip("\"'").replace(r"\"", "\"")


def scalar(text: str, key: str, default: str = "") -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return default
    value = match.group(1).strip()
    return clean_yaml_scalar(value)


def folded_value(text: str, key: str, default: str = "") -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(rf"^{re.escape(key)}:\s*[>|]\s*$", line):
            out: list[str] = []
            for child in lines[index + 1 :]:
                if child and not child.startswith(" "):
                    break
                stripped = child.strip()
                if stripped:
                    out.append(stripped)
            return " ".join(out).strip() or default
    return scalar(text, key, default)


def list_items(text: str, section: str | None = None) -> list[str]:
    if section:
        match = re.search(rf"(?ms)^{re.escape(section)}:\s*\n(.*?)(?=^[a-zA-Z0-9_-]+:|\Z)", text)
        if not match:
            return []
        text = match.group(1)
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip().strip("\"'"))
    return items


def list_values_for_key(text: str, key: str) -> list[str]:
    """Extract simple YAML list values immediately under repeated `key:` blocks."""
    lines = text.splitlines()
    values: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() != f"{key}:":
            continue
        indent = len(line) - len(line.lstrip(" "))
        for child in lines[index + 1 :]:
            child_indent = len(child) - len(child.lstrip(" "))
            stripped = child.strip()
            if stripped and child_indent <= indent:
                break
            if stripped.startswith("- "):
                values.append(clean_yaml_scalar(stripped[2:].strip()))
    return values


def scalar_values_for_key(text: str, key: str) -> list[str]:
    values = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            value = clean_yaml_scalar(stripped.split(":", 1)[1].strip())
            if value:
                values.append(value)
    return values


def metadata(path: Path) -> dict[str, str]:
    text = read_text(path)
    return {
        "file": str(path),
        "name": scalar(text, "name", path.stem),
        "size": scalar(text, "size", "unknown"),
        "purpose": folded_value(text, "purpose", ""),
    }


def forge_command() -> list[str] | None:
    path = shutil.which("forge")
    if path:
        return [path]
    if FORGE_FALLBACK.exists():
        return [str(FORGE_FALLBACK)]
    return None


def forge_info() -> tuple[int, str]:
    cmd = forge_command()
    if not cmd:
        return 127, "forge not found on PATH and fallback forge checkout is missing"
    proc = subprocess.run(
        [*cmd, "info", "landfall-forge"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def choose_landfall(files: Iterable[Path], request: str) -> Path | None:
    choices = list(files)
    if not choices:
        return None
    if not request:
        return choices[0] if len(choices) == 1 else None
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", request.lower())
        if len(token) >= 3 and token not in STOP_WORDS
    }
    scored: list[tuple[int, Path]] = []
    for path in choices:
        meta = metadata(path)
        identity = f"{path.stem} {meta['name']}".lower()
        haystack = f"{identity} {meta['purpose']} {read_text(path)}".lower()
        score = sum(5 for token in tokens if token in identity)
        score += sum(1 for token in tokens if token in haystack)
        scored.append((score, path))
    scored.sort(key=lambda item: (-item[0], item[1].name))
    if scored and scored[0][0] > 0:
        return scored[0][1]
    return None


def print_no_landfalls(root: Path) -> int:
    code, info = forge_info()
    print(f"No repo-local landfalls found in {root / 'landfalls'}")
    print()
    print("Forge fallback: landfall-forge")
    print(info if info else f"forge info exited {code}")
    print()
    print("Next agent move:")
    print("1. Read landfall-forge's map/design templates.")
    print("2. Create repo-local landfalls/README.md and landfalls/<job>.yaml.")
    print("3. Keep behavior local to the repo; keep this CLI generic.")
    return 2 if code else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.cwd or os.getcwd()))
    files = landfall_files(root)
    code, info = forge_info()
    print("landfall doctor")
    print(f"- version: {__version__}")
    print(f"- cwd repo: {root}")
    print(f"- repo landfalls: {len(files)}")
    print(f"- forge fallback: {'ok' if code == 0 else 'missing'}")
    if LANDFALL_FORGE.exists():
        print(f"- landfall-forge checkout: {LANDFALL_FORGE}")
    if files:
        print("- definitions:")
        for path in files:
            meta = metadata(path)
            print(f"  - {meta['name']} ({meta['size']}): {path.relative_to(root)}")
    else:
        print("- definitions: none")
    if code != 0:
        print(info)
    return 0 if files or code == 0 else 1


def cmd_list(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.cwd or os.getcwd()))
    files = landfall_files(root)
    if not files:
        return print_no_landfalls(root)
    for path in files:
        meta = metadata(path)
        print(f"{meta['name']}\t{meta['size']}\t{path.relative_to(root)}")
        if args.verbose and meta["purpose"]:
            print(f"  {meta['purpose']}")
    return 0


def resolve_file(root: Path, name: str | None, *, fuzzy: bool = True) -> Path | None:
    files = landfall_files(root)
    if not name:
        return files[0] if len(files) == 1 else None
    wanted = name.removesuffix(".yaml")
    for path in files:
        meta = metadata(path)
        if wanted in {path.stem, meta["name"], meta["name"].removesuffix(".yaml")}:
            return path
    return choose_landfall(files, name) if fuzzy else None


def cmd_show(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.cwd or os.getcwd()))
    files = landfall_files(root)
    if not files:
        return print_no_landfalls(root)
    path = resolve_file(root, args.name)
    if not path:
        print("Ambiguous landfall. Available:")
        for item in files:
            print(f"- {metadata(item)['name']}")
        return 2
    print(read_text(path))
    return 0


def cmd_brief(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.cwd or os.getcwd()))
    files = landfall_files(root)
    if not files:
        return print_no_landfalls(root)
    request_text = " ".join(([args.name] if args.name else []) + (args.request or []))
    path = resolve_file(root, args.name, fuzzy=False) or choose_landfall(files, request_text)
    if not path:
        print("I need a landfall name or a clearer request. Options:")
        for item in files:
            meta = metadata(item)
            print(f"- {meta['name']} ({meta['size']}): {meta['purpose']}")
        return 2
    text = read_text(path)
    meta = metadata(path)
    print(f"Landfall: {meta['name']} ({meta['size']})")
    print(f"File: {path.relative_to(root)}")
    if meta["purpose"]:
        print(f"Purpose: {meta['purpose']}")
    stops = list_items(text, "stop_conditions")
    qs = scalar_values_for_key(text, "prompt")
    cmds = list_values_for_key(text, "commands")
    print()
    print("Agent brief:")
    print("- Read this YAML as the contract; do not invent a second task system.")
    print("- Refresh the listed sources, answer the listed questions, and write only to declared targets.")
    print("- Record weak evidence as uncertainty instead of closing tasks.")
    if stops:
        print()
        print("Stop before:")
        for item in stops:
            print(f"- {item}")
    if cmds:
        print()
        print("Source commands to consider:")
        for item in cmds:
            print(f"- {item}")
    if qs:
        print()
        print("Questions to answer:")
        for item in qs:
            print(f"- {item}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.cwd or os.getcwd()))
    files = landfall_files(root)
    if not files:
        return print_no_landfalls(root)
    required = ["landfall_version", "name", "size", "purpose", "sources", "questions", "write_targets", "stop_conditions", "done_when"]
    failed = False
    for path in files:
        text = read_text(path)
        missing = [key for key in required if not re.search(rf"(?m)^{re.escape(key)}:", text)]
        meta = metadata(path)
        if missing:
            failed = True
            print(f"FAIL {meta['name']}: missing {', '.join(missing)}")
        else:
            print(f"PASS {meta['name']} ({meta['size']})")
    return 1 if failed else 0


def cmd_forge_info(args: argparse.Namespace) -> int:
    code, info = forge_info()
    if args.json and info.startswith("{"):
        print(json.dumps(json.loads(info), indent=2))
    else:
        print(info)
    return code


def build_parser() -> argparse.ArgumentParser:
    cwd_parent = argparse.ArgumentParser(add_help=False)
    cwd_parent.add_argument("--cwd", help="repo or subdirectory to inspect")
    parser = argparse.ArgumentParser(
        prog="landfall",
        description="Universal front door for repo-local landfall rituals.",
        parents=[cwd_parent],
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="check repo landfalls and forge fallback", parents=[cwd_parent]).set_defaults(func=cmd_doctor)

    list_p = sub.add_parser("list", help="list repo-local landfalls", parents=[cwd_parent])
    list_p.add_argument("-v", "--verbose", action="store_true")
    list_p.set_defaults(func=cmd_list)

    show_p = sub.add_parser("show", help="print a landfall YAML", parents=[cwd_parent])
    show_p.add_argument("name", nargs="?")
    show_p.set_defaults(func=cmd_show)

    brief_p = sub.add_parser("brief", help="turn a landfall into an agent execution brief", parents=[cwd_parent])
    brief_p.add_argument("name", nargs="?")
    brief_p.add_argument("request", nargs="*")
    brief_p.set_defaults(func=cmd_brief)

    run_p = sub.add_parser("run", help="alias for brief; the LLM executes the brief safely", parents=[cwd_parent])
    run_p.add_argument("name", nargs="?")
    run_p.add_argument("request", nargs="*")
    run_p.set_defaults(func=cmd_brief)

    sub.add_parser("audit", help="check landfall YAML has required sections", parents=[cwd_parent]).set_defaults(func=cmd_audit)

    forge_p = sub.add_parser("forge-info", help="call forge-forge for landfall-forge", parents=[cwd_parent])
    forge_p.add_argument("--json", action="store_true")
    forge_p.set_defaults(func=cmd_forge_info)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
