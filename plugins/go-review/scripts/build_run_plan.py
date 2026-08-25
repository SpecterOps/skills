#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build a deterministic go-review run plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, NoReturn


THREAT_MODELS = {"REMOTE", "LOCAL_UNPRIVILEGED", "BOTH"}
SEVERITY_FILTERS = {"all", "medium", "high"}
CAPABILITY_FLAGS = (
    "has_service",
    "has_outbound_http",
    "has_sql",
    "has_exec",
    "has_fs_archive",
    "has_template",
    "has_crypto_auth",
    "has_concurrency",
    "has_unsafe_cgo",
)
GATE_VALUES = {"always", *CAPABILITY_FLAGS}
KNOWN_REQUIRES = set(CAPABILITY_FLAGS)


def fail(message: str) -> NoReturn:
    print(f"build_run_plan.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got {value!r}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--threat-model", required=True, choices=sorted(THREAT_MODELS))
    parser.add_argument("--severity-filter", required=True, choices=sorted(SEVERITY_FILTERS))
    parser.add_argument("--scope-subpath", required=True)
    parser.add_argument("--context-roots", default=".")
    for flag in CAPABILITY_FLAGS:
        parser.add_argument(f"--{flag.replace('_', '-')}", required=True, type=parse_bool)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--cache-primer", type=parse_bool, default=True)
    parser.add_argument("--max-passes-per-worker", type=int, default=4)
    args = parser.parse_args(argv)
    if args.max_passes_per_worker < 0:
        fail("--max-passes-per-worker must be >= 0")
    return args


def gate_passes(cluster: dict[str, Any], *, flags: dict[str, bool]) -> bool:
    gate = cluster.get("gate")
    gate_any = cluster.get("gate_any")
    if gate is not None and gate_any is not None:
        fail(f"cluster {cluster.get('cluster_id', '?')!r}: cannot declare both gate and gate_any")
    if gate_any is not None:
        if not isinstance(gate_any, list) or not gate_any:
            fail(f"cluster {cluster.get('cluster_id', '?')!r}: gate_any must be a non-empty list")
        for item in gate_any:
            if item not in KNOWN_REQUIRES:
                fail(f"cluster {cluster.get('cluster_id', '?')!r}: unknown gate_any flag {item!r}")
        return any(flags[item] for item in gate_any)
    if gate not in GATE_VALUES:
        fail(f"cluster {cluster.get('cluster_id', '?')!r}: invalid gate {gate!r}")
    return gate == "always" or flags[gate]


def pass_filtered_out(entry: dict[str, Any], *, flags: dict[str, bool], threat_model: str) -> bool:
    for requirement in entry.get("requires", []) or []:
        if requirement not in KNOWN_REQUIRES:
            fail(f"pass {entry.get('bug_class', '?')!r}: unknown requires flag {requirement!r}")
        if not flags[requirement]:
            return True
    return threat_model in (entry.get("skip_threat_models", []) or [])


def cluster_max_passes_per_worker(cluster: dict[str, Any], *, cid: str) -> int | None:
    value = cluster.get("max_passes_per_worker")
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"cluster {cid!r}: max_passes_per_worker must be a positive integer")
    return value


def build_selection(
    manifest: dict[str, Any],
    *,
    plugin_root: Path,
    flags: dict[str, bool],
    threat_model: str,
) -> list[dict[str, Any]]:
    if manifest.get("version") != 1:
        fail(f"unsupported manifest version: {manifest.get('version')!r}")
    if not isinstance(manifest.get("clusters"), list):
        fail("manifest.clusters must be a list")
    selected: list[dict[str, Any]] = []
    for cluster in manifest["clusters"]:
        cid = cluster.get("cluster_id")
        if not cid:
            fail("cluster missing cluster_id")
        if not gate_passes(cluster, flags=flags):
            continue
        try:
            max_passes = cluster_max_passes_per_worker(cluster, cid=cid)
        except ValueError as exc:
            fail(str(exc))
        prompt_rel = cluster.get("prompt")
        if not prompt_rel:
            fail(f"cluster {cid!r}: missing prompt")
        prompt_abs = (plugin_root / prompt_rel).resolve()
        if not prompt_abs.is_file():
            fail(f"cluster {cid!r}: prompt not found at {prompt_abs}")
        consolidated = bool(cluster.get("consolidated", False))
        passes: list[dict[str, Any]] = []
        for raw in cluster.get("passes", []) or []:
            bug_class = raw.get("bug_class")
            prefix = raw.get("prefix")
            if not bug_class or not prefix:
                fail(f"cluster {cid!r}: pass missing bug_class/prefix")
            if pass_filtered_out(raw, flags=flags, threat_model=threat_model):
                continue
            entry: dict[str, Any] = {"bug_class": bug_class, "prefix": prefix}
            if not consolidated:
                sub_prompt = raw.get("prompt")
                if not sub_prompt:
                    fail(f"cluster {cid!r}: non-consolidated pass {bug_class!r} missing prompt")
                sub_prompt_abs = (plugin_root / sub_prompt).resolve()
                if not sub_prompt_abs.is_file():
                    fail(f"cluster {cid!r}: pass prompt not found at {sub_prompt_abs}")
                entry["prompt"] = str(sub_prompt_abs)
            passes.append(entry)
        if not passes:
            continue
        selected.append(
            {
                "cluster_id": cid,
                "consolidated": consolidated,
                "cluster_prompt": str(prompt_abs),
                "passes": passes,
                "max_passes_per_worker": max_passes,
            }
        )
    return selected


def split_oversized_clusters(
    selected: list[dict[str, Any]], *, max_passes: int
) -> list[dict[str, Any]]:
    if max_passes < 0:
        raise ValueError("max_passes must be >= 0")
    if max_passes == 0:
        return selected
    out: list[dict[str, Any]] = []
    for cluster in selected:
        override = cluster_max_passes_per_worker(cluster, cid=str(cluster["cluster_id"]))
        if cluster.get("consolidated"):
            out.append(cluster)
            continue
        effective = override if override is not None else max_passes
        passes = cluster["passes"]
        if len(passes) <= effective:
            out.append(cluster)
            continue
        chunks = []
        for index in range(0, len(passes), effective):
            chunks.append(
                {
                    "cluster_id": f"{cluster['cluster_id']}-{len(chunks) + 1}",
                    "consolidated": False,
                    "cluster_prompt": cluster["cluster_prompt"],
                    "passes": passes[index : index + effective],
                }
            )
        assert [entry for chunk in chunks for entry in chunk["passes"]] == passes
        out.extend(chunks)
    return out


def _shared_prompt_lines(
    *,
    output_dir: Path,
    scope_subpath: str,
    context_roots: str,
    threat_model: str,
    severity_filter: str,
    flags: dict[str, bool],
    context_body: str,
) -> list[str]:
    return [
        "You are a go-review worker in a Go package security review.",
        "Follow the worker protocol in your system prompt verbatim.",
        "",
        f"Output directory: {output_dir}",
        f"Finding scope root: {scope_subpath}",
        f"Context roots: {context_roots}",
        f"Threat model: {threat_model}",
        f"Severity filter: {severity_filter}",
        "Go capabilities: "
        + ", ".join(f"{flag}={'true' if flags[flag] else 'false'}" for flag in CAPABILITY_FLAGS),
        "",
        "<context>",
        context_body.rstrip(),
        "</context>",
        "",
    ]


def render_worker_prompt(
    *,
    worker_n: int,
    cluster: dict[str, Any],
    output_dir: Path,
    scope_subpath: str,
    context_roots: str,
    threat_model: str,
    severity_filter: str,
    flags: dict[str, bool],
    context_body: str,
) -> str:
    lines = _shared_prompt_lines(
        output_dir=output_dir,
        scope_subpath=scope_subpath,
        context_roots=context_roots,
        threat_model=threat_model,
        severity_filter=severity_filter,
        flags=flags,
        context_body=context_body,
    )
    lines.extend(
        [
            "- assignment -",
            f"Worker id: worker-{worker_n}",
            f"Cluster id: {cluster['cluster_id']}",
            f"Cluster prompt: {cluster['cluster_prompt']}",
        ]
    )
    if not cluster["consolidated"]:
        lines.append("Sub-prompt paths:")
        lines.extend(f"  - {entry['prompt']}" for entry in cluster["passes"])
    lines.append("Pass bug classes: " + ", ".join(entry["bug_class"] for entry in cluster["passes"]))
    lines.append("Pass prefixes: " + ", ".join(entry["prefix"] for entry in cluster["passes"]))
    lines.append("Skip subclasses: (none)")
    lines.append("")
    return "\n".join(lines)


def render_cache_primer_prompt(**kwargs: Any) -> str:
    lines = _shared_prompt_lines(**kwargs)
    lines.extend(["Cache primer: true", "worker-PRIMER abort: cache primer (no analysis performed)", ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    plugin_root = args.plugin_root.resolve()
    output_dir = args.output_dir.resolve()
    if not plugin_root.is_dir():
        fail(f"plugin root not found: {plugin_root}")
    if not output_dir.is_dir():
        fail(f"output directory not found: {output_dir}")
    manifest_path = (args.manifest or plugin_root / "prompts/clusters/manifest.json").resolve()
    if not manifest_path.is_file():
        fail(f"manifest not found: {manifest_path}")
    context_path = output_dir / "context.md"
    if not context_path.is_file():
        fail(f"context.md not found: {context_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    flags = {flag: getattr(args, flag) for flag in CAPABILITY_FLAGS}
    selected = build_selection(
        manifest,
        plugin_root=plugin_root,
        flags=flags,
        threat_model=args.threat_model,
    )
    selected = split_oversized_clusters(selected, max_passes=args.max_passes_per_worker)
    context_body = context_path.read_text(encoding="utf-8")
    prompt_dir = output_dir / "worker-prompts"
    prompt_dir.mkdir(exist_ok=True)
    workers = []
    for worker_n, cluster in enumerate(selected, start=1):
        prompt_path = prompt_dir / f"worker-{worker_n}.txt"
        prompt_path.write_text(
            render_worker_prompt(
                worker_n=worker_n,
                cluster=cluster,
                output_dir=output_dir,
                scope_subpath=args.scope_subpath,
                context_roots=args.context_roots,
                threat_model=args.threat_model,
                severity_filter=args.severity_filter,
                flags=flags,
                context_body=context_body,
            ),
            encoding="utf-8",
        )
        workers.append(
            {
                "worker_n": worker_n,
                "cluster_id": cluster["cluster_id"],
                "consolidated": cluster["consolidated"],
                "cluster_prompt": cluster["cluster_prompt"],
                "sub_prompt_paths": [entry["prompt"] for entry in cluster["passes"] if "prompt" in entry],
                "pass_bug_classes": [entry["bug_class"] for entry in cluster["passes"]],
                "pass_prefixes": [entry["prefix"] for entry in cluster["passes"]],
                "spawn_prompt_path": str(prompt_path),
            }
        )
    primer_path: Path | None = None
    if args.cache_primer and workers:
        primer_path = prompt_dir / "cache-primer.txt"
        primer_path.write_text(
            render_cache_primer_prompt(
                output_dir=output_dir,
                scope_subpath=args.scope_subpath,
                context_roots=args.context_roots,
                threat_model=args.threat_model,
                severity_filter=args.severity_filter,
                flags=flags,
                context_body=context_body,
            ),
            encoding="utf-8",
        )
    plan = {
        "version": 1,
        "run": {
            "output_dir": str(output_dir),
            "finding_scope_root": args.scope_subpath,
            "context_roots": args.context_roots,
            "threat_model": args.threat_model,
            "severity_filter": args.severity_filter,
            "plugin_root": str(plugin_root),
            "manifest_path": str(manifest_path),
            "cache_primer": bool(primer_path),
            **flags,
        },
        "workers": workers,
    }
    if primer_path:
        plan["cache_primer"] = {"spawn_prompt_path": str(primer_path)}
    plan_path = output_dir / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "plan_path": str(plan_path),
                "worker_count": len(workers),
                "cluster_ids": [worker["cluster_id"] for worker in workers],
                "cache_primer_path": str(primer_path) if primer_path else None,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
