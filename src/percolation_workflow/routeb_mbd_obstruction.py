"""Exact Route-B ``M_BD a_D`` projection obstruction checker.

The checker re-sums the rational Fourier mass snapshot at ``q=0``.  A nonzero
column of ``M_BD(0)`` gives an exact countermodel to any remote-residual bound
whose premises mention only the currently projected block variables: keep the
projection fixed and scale ``a_D = lambda * e_j``.

This is negative evidence, not a claim about which states a physical
trajectory can reach.  A full-state descriptor or an equivalent remote
enclosure is still required.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
import io
from typing import Mapping


BLOCK_ROWS = (4, 5)
REMOTE_COLS = (1, 2, 3, 6)


@dataclass(frozen=True)
class RouteBProjectionObstruction:
    status: str
    matrix_at_zero: tuple[tuple[Fraction, ...], ...]
    first_column_vector: tuple[Fraction, Fraction]
    projection_factor: Fraction
    errors: tuple[str, ...] = ()
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def _zero_matrix() -> dict[tuple[int, int], Fraction]:
    return {(r, c): Fraction(0) for r in BLOCK_ROWS for c in REMOTE_COLS}


def audit_routeb_mbd_projection(csv_text: str) -> RouteBProjectionObstruction:
    """Re-sum one rational Fourier CSV at the exact point ``q=0``."""
    sums = _zero_matrix()
    errors: list[str] = []
    try:
        rows = csv.DictReader(io.StringIO(csv_text))
        if not rows.fieldnames or not {"row", "col", "real_num", "real_den", "imag_num", "imag_den"}.issubset(rows.fieldnames):
            errors.append("missing_fourier_columns")
        else:
            seen = 0
            imag = Fraction(0)
            for item in rows:
                r, c = int(item["row"]), int(item["col"])
                if (r, c) not in sums:
                    continue
                sums[(r, c)] += Fraction(int(item["real_num"]), int(item["real_den"]))
                imag += Fraction(int(item["imag_num"]), int(item["imag_den"]))
                seen += 1
            if seen == 0:
                errors.append("no_block_remote_rows")
            if imag != 0:
                errors.append(f"nonzero_imaginary_sum:{imag}")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"malformed_fourier_csv:{type(exc).__name__}")

    matrix = tuple(tuple(sums[(r, c)] for c in REMOTE_COLS) for r in BLOCK_ROWS)
    first = (matrix[0][0], matrix[1][0])
    factor = first[0] ** 2 + first[1] ** 2
    status = "PROJECTION_OBSTRUCTION_EXACT" if not errors and factor > 0 else "OPEN_FAIL_CLOSED"
    return RouteBProjectionObstruction(
        status=status,
        matrix_at_zero=matrix,
        first_column_vector=first,
        projection_factor=factor,
        errors=tuple(errors),
    )


__all__ = [
    "BLOCK_ROWS",
    "REMOTE_COLS",
    "RouteBProjectionObstruction",
    "audit_routeb_mbd_projection",
]
