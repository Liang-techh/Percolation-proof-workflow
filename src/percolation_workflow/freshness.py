"""Fail-closed freshness bindings for reusable verification evidence."""
from __future__ import annotations

import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind_freshness(project: Path, source_hashes: dict[str, str], *,
                   olean_paths: list[str] | tuple[str, ...]) -> dict:
    """Create an explicit replay binding for all inputs used by a closure."""
    project = project.resolve()
    def digest(relative: str) -> str:
        path = (project / relative).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError(f'freshness input is missing: {relative}')
        return sha256(path)

    comparator = 'comparator.json' if (project / 'comparator.json').is_file() else None
    return {
        'source_hashes': dict(source_hashes),
        'lean_pin': {'path': 'lean-toolchain', 'sha256': digest('lean-toolchain')},
        'comparator': ({'path': comparator, 'sha256': digest(comparator)}
                       if comparator else None),
        'olean_hashes': {path: digest(path) for path in sorted(set(olean_paths))},
    }


def audit_freshness(project: Path, expected: dict) -> tuple[bool, tuple[str, ...]]:
    """Recompute every bound hash; malformed or incomplete bindings are stale."""
    if not isinstance(expected, dict):
        return False, ('freshness binding missing',)
    reasons: list[str] = []
    project = project.resolve()
    actual_sources = {}
    for relative, value in expected.get('source_hashes', {}).items() \
            if isinstance(expected.get('source_hashes'), dict) else ():
        path = (project / relative).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            reasons.append(f'source missing: {relative}')
        elif sha256(path) != value:
            reasons.append(f'source hash changed: {relative}')
        actual_sources[relative] = value
    if not actual_sources:
        reasons.append('source hashes missing')

    pin = expected.get('lean_pin')
    if not isinstance(pin, dict) or pin.get('path') != 'lean-toolchain':
        reasons.append('Lean pin binding missing')
    elif not (project / 'lean-toolchain').is_file() or sha256(project / 'lean-toolchain') != pin.get('sha256'):
        reasons.append('Lean pin hash changed')

    comparator = expected.get('comparator')
    if comparator is not None:
        if not isinstance(comparator, dict) or comparator.get('path') != 'comparator.json':
            reasons.append('comparator binding malformed')
        elif not (project / 'comparator.json').is_file() or sha256(project / 'comparator.json') != comparator.get('sha256'):
            reasons.append('comparator hash changed')

    olean = expected.get('olean_hashes')
    if not isinstance(olean, dict) or not olean:
        reasons.append('.olean bindings missing')
    else:
        for relative, value in olean.items():
            path = (project / relative).resolve()
            if not path.is_relative_to(project) or not path.is_file():
                reasons.append(f'.olean missing: {relative}')
            elif sha256(path) != value:
                reasons.append(f'.olean hash changed: {relative}')
    return not reasons, tuple(reasons)
