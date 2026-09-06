"""Fail-closed admission checks for a named Lean theorem.

This module is deliberately independent of the workflow state and reduction
code.  It records evidence only; callers decide whether to attach the result
to a registry receipt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import re
import tempfile

from .lean import LeanResult, run_lean

_ALLOWED_AXIOMS = frozenset(("propext", "Quot.sound", "Classical.choice"))
_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*$")
_FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom)\b")
_AXIOMS_LINE = re.compile(r"^axioms\s+(.+?)\s+uses:\s*(.*)$")
_LEAN_AXIOMS = re.compile(
    r"'([A-Za-z_][A-Za-z0-9_'.]*)'\s+depends on axioms:\s*\[(.*?)\]",
    re.DOTALL,
)
_LEAN_NO_AXIOMS = re.compile(
    r"'([A-Za-z_][A-Za-z0-9_'.]*)'\s+does not depend on any axioms"
)
_MODULE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*$")


@dataclass(frozen=True)
class StrictAdmission:
    accepted: bool
    theorem_names: tuple[str, ...]
    axioms: dict[str, tuple[str, ...]] = field(default_factory=dict)
    toolchain: str = ""
    toolchain_sha256: str = ""
    lake_manifest_sha256: str = ""
    reasons: tuple[str, ...] = ()
    command: tuple[str, ...] = ()
    stdout: str = ""
    stderr: str = ""


def _source_tokens(project: Path, excluded_modules: set[str] | None = None) -> list[str]:
    excluded_modules = excluded_modules or set()
    hits: list[str] = []
    for path in sorted(project.rglob("*.lean")):
        relative = path.relative_to(project)
        if ".lake" in relative.parts or ".git" in relative.parts:
            continue
        if relative.with_suffix('').as_posix() in excluded_modules:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if _FORBIDDEN.search(text):
            hits.append(relative.as_posix())
    return hits


def _parse_axioms(stdout: str, theorem_names: tuple[str, ...]) -> dict[str, tuple[str, ...]]:
    parsed: dict[str, tuple[str, ...]] = {}
    for line in stdout.splitlines():
        match = _AXIOMS_LINE.match(line.strip())
        if not match:
            continue
        name, values = match.groups()
        parsed[name] = tuple(value for value in values.split() if value)
    for match in _LEAN_AXIOMS.finditer(stdout):
        name, values = match.groups()
        parsed[name] = tuple(value.strip("'\" ,\r\n\t")
                              for value in re.split(r"[,\s]+", values)
                              if value.strip("'\" ,\r\n\t"))
    for match in _LEAN_NO_AXIOMS.finditer(stdout):
        parsed[match.group(1)] = ()
    return {name: parsed[name] for name in theorem_names if name in parsed}


def audit_strict_admission(project: str | Path, theorem_names: list[str] | tuple[str, ...], *,
                           solution_module: str | None = None,
                           challenge_module: str | None = None,
                           expected_toolchain: str | None = None,
                           timeout: int = 600) -> StrictAdmission:
    """Audit theorem axioms, forbidden proof placeholders, and pinned inputs.

    Missing or unparsable evidence is rejection.  The audit runs a generated
    file with ``#print axioms`` under the project's own Lake environment, so it
    cannot silently inspect a different checkout/toolchain.
    """
    root = Path(project).resolve()
    names = tuple(theorem_names)
    reasons: list[str] = []
    if not names or len(set(names)) != len(names) or any(not _NAME.fullmatch(n) for n in names):
        reasons.append("invalid theorem name list")
    if solution_module is not None and not _MODULE.fullmatch(solution_module):
        reasons.append("invalid solution module")
    if challenge_module is not None and not _MODULE.fullmatch(challenge_module):
        reasons.append("invalid challenge module")
    toolchain_path = root / "lean-toolchain"
    manifest_path = root / "lake-manifest.json"
    toolchain = toolchain_path.read_text(encoding="utf-8").strip() if toolchain_path.is_file() else ""
    manifest_bytes = manifest_path.read_bytes() if manifest_path.is_file() else b""
    if not toolchain:
        reasons.append("missing pinned lean-toolchain")
    if expected_toolchain is not None and toolchain != expected_toolchain.strip():
        reasons.append("lean-toolchain does not match expected pin")
    if not manifest_bytes.strip():
        reasons.append("missing pinned lake-manifest.json")
    excluded = set()
    if challenge_module is not None:
        excluded.add(challenge_module.replace('.', '/'))
    forbidden = _source_tokens(root, excluded) if root.is_dir() else []
    if forbidden:
        reasons.append("forbidden sorry/admit/axiom token in: " + ", ".join(forbidden))

    result = LeanResult(False, [], "", "", 1)
    audit_path: Path | None = None
    if not reasons:
        if solution_module is not None:
            solution_path = root.joinpath(*solution_module.split('.')).with_suffix('.lean')
            if not solution_path.is_file():
                reasons.append("missing solution module source")
            else:
                # The generated audit file imports the solution by module name.
                # In a clean project that import needs the solution's .olean
                # first; existing projects may already have it, but compiling
                # here makes the check independent of stale build artifacts.
                compile_result = run_lean(
                    root, ["lake", "build", solution_module],
                    timeout=timeout,
                )
                if not compile_result.ok:
                    reasons.append("solution module compilation failed")
                    result = compile_result
        if reasons:
            parsed = _parse_axioms(result.stdout, names)
            return StrictAdmission(
                accepted=False,
                theorem_names=names,
                axioms=parsed,
                toolchain=toolchain,
                toolchain_sha256=hashlib.sha256(toolchain.encode()).hexdigest() if toolchain else "",
                lake_manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest() if manifest_bytes else "",
                reasons=tuple(reasons), command=tuple(result.command), stdout=result.stdout, stderr=result.stderr,
            )
        handle = tempfile.NamedTemporaryFile("w", suffix=".lean", prefix="strict_admission_",
                                             dir=root, delete=False, encoding="utf-8")
        audit_path = Path(handle.name)
        if solution_module is not None:
            handle.write(f"import {solution_module}\n")
        handle.write("\n".join(f"#print axioms {name}" for name in names) + "\n")
        handle.close()
        try:
            result = run_lean(root, ["lake", "env", "lean", audit_path.name], timeout=timeout)
        finally:
            audit_path.unlink(missing_ok=True)
        if not result.ok:
            reasons.append("#print axioms command failed")
    parsed = _parse_axioms(result.stdout, names)
    if not reasons:
        missing = [name for name in names if name not in parsed]
        if missing:
            reasons.append("missing #print axioms evidence for: " + ", ".join(missing))
        for name, axioms in parsed.items():
            unexpected = sorted(set(axioms) - _ALLOWED_AXIOMS)
            if unexpected:
                reasons.append(f"unexpected axioms for {name}: {', '.join(unexpected)}")
    return StrictAdmission(
        accepted=not reasons,
        theorem_names=names,
        axioms=parsed,
        toolchain=toolchain,
        toolchain_sha256=hashlib.sha256(toolchain.encode()).hexdigest() if toolchain else "",
        lake_manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest() if manifest_bytes else "",
        reasons=tuple(reasons), command=tuple(result.command), stdout=result.stdout, stderr=result.stderr,
    )
