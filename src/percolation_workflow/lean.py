from __future__ import annotations

from dataclasses import dataclass
import os
import subprocess
from pathlib import Path


@dataclass
class LeanResult:
    ok: bool
    command: list[str]
    stdout: str
    stderr: str
    exit_code: int


def run_lean(project_dir: str | Path, command: list[str] | None = None, timeout: int = 600) -> LeanResult:
    cmd = command or ["lake", "build"]
    environment = dict(os.environ)
    # A candidate bundle is compiled one source at a time.  Lake's default
    # search path contains only built libraries, so explicitly expose the
    # coordinator-owned project root where the preceding support step wrote
    # its .olean file.  This is an execution-environment detail, not a proof
    # dependency or an imported external cache.
    project = Path(project_dir).resolve()
    prior_path = environment.get("LEAN_PATH")
    environment["LEAN_PATH"] = str(project) + (os.pathsep + prior_path if prior_path else "")
    try:
        proc = subprocess.run(cmd, cwd=project_dir, text=True, encoding="utf-8", errors="replace",
                              capture_output=True, timeout=timeout, env=environment)
        return LeanResult(proc.returncode == 0, cmd, proc.stdout, proc.stderr, proc.returncode)
    except FileNotFoundError as exc:
        return LeanResult(False, cmd, "", str(exc), 127)
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else (value or '')
        return LeanResult(False, cmd, decoded(exc.stdout), "timeout: " + decoded(exc.stderr), 124)
