"""Exact/Float64 seam for the Route-B mass regularizer.

This module is intentionally smaller than the deployed evaluator.  It records
the already established binary64 value of ``1e-6`` and exposes the conditional
matrix/block propagation that follows when the unregularized base matrix is
the same on both sides.  It does not model Julia arithmetic, libm, finite
differences, or a linear solve.

The inverse/port helper is separate and requires an explicit exact-real
resolvent premise.  Merely having a positive regularizer, or having a matrix
entry inclusion, never supplies that premise.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any


Matrix = tuple[tuple[Fraction, ...], ...]

REGULARIZER_SEMANTICS_SCHEMA = "routeb.regularizer_semantics.v1"
FLOAT64_MU_BITS_HEX = "0x3eb0c6f7a0b5ed8d"
FLOAT64_MU = Fraction(4722366482869645, 4722366482869645213696)
EXACT_MU = Fraction(1, 1_000_000)
MU_DELTA = EXACT_MU - FLOAT64_MU
DEFAULT_BLOCK_COORDS = (4, 5)
DEFAULT_REMOTE_COORDS = (1, 2, 3, 6)


def _exact_scalar(value: Any, name: str) -> Fraction:
    """Convert only exact integer/rational input; reject an implicit float seam."""
    if isinstance(value, bool):
        raise TypeError(f"{name}: bool is not an exact scalar")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(
        f"{name}: expected int or Fraction; convert Float64 through an explicit "
        "exact-rational binding first"
    )


def _matrix(value: Sequence[Sequence[Any]], name: str) -> Matrix:
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name}: matrix must be a square sequence")
    try:
        rows = tuple(
            tuple(_exact_scalar(entry, f"{name}[{row},{col}]")
                  for col, entry in enumerate(line))
            for row, line in enumerate(value)
        )
    except TypeError:
        raise TypeError(f"{name}: matrix must be a square sequence") from None
    if not rows or any(len(line) != len(rows) for line in rows):
        raise ValueError(f"{name}: expected a non-empty square matrix")
    return rows


def _add_diagonal(matrix: Matrix, scalar: Fraction) -> Matrix:
    return tuple(
        tuple(value + (scalar if row == col else 0)
              for col, value in enumerate(line))
        for row, line in enumerate(matrix)
    )


def _subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(a - b for a, b in zip(row_left, row_right))
        for row_left, row_right in zip(left, right)
    )


def _select(matrix: Matrix, rows: tuple[int, ...], cols: tuple[int, ...]) -> Matrix:
    return tuple(tuple(matrix[row - 1][col - 1] for col in cols) for row in rows)


def _coords(value: Sequence[int], dimension: int, name: str) -> tuple[int, ...]:
    coords = tuple(value)
    if not coords or len(set(coords)) != len(coords):
        raise ValueError(f"{name}: coordinates must be non-empty and distinct")
    if any(not isinstance(item, int) or isinstance(item, bool)
           or not 1 <= item <= dimension for item in coords):
        raise ValueError(f"{name}: coordinate outside 1..{dimension}")
    return coords


@dataclass(frozen=True)
class RouteBRegularizerFact:
    """The scalar seam, with both values represented as exact rationals."""

    schema: str
    float64_bits_hex: str
    mu_float64: Fraction
    mu_exact_real: Fraction
    delta_exact: Fraction
    outward_interval: tuple[Fraction, Fraction]
    status: str = "EXACT_FLOAT64_FACT"
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBRegularizerInclusion:
    """Entrywise outward inclusion for two already-bound exact matrices."""

    status: str
    dimension: int
    float64_matrix: Matrix | None
    exact_real_matrix: Matrix | None
    lower_matrix: Matrix | None
    upper_matrix: Matrix | None
    difference_matrix: Matrix | None
    delta_exact: Fraction
    errors: tuple[str, ...] = ()
    common_base_binding_required: bool = True
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBRegularizerDiagonalPropagation:
    """Regularizer-only propagation through the full matrix and B/D blocks."""

    status: str
    base_matrix: Matrix
    float64_matrix: Matrix
    exact_real_matrix: Matrix
    inclusion: RouteBRegularizerInclusion
    block_coords: tuple[int, ...]
    remote_coords: tuple[int, ...]
    float64_BB: Matrix
    exact_real_BB: Matrix
    float64_DD: Matrix
    exact_real_DD: Matrix
    float64_BD: Matrix
    exact_real_BD: Matrix
    float64_DB: Matrix
    exact_real_DB: Matrix
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBExactResolventPremise:
    """A caller-supplied exact-real bound for the regularized D block inverse."""

    source_key: str
    norm_convention: str
    inverse_norm_bound: Fraction
    proves_exact_real_bound: bool = True


@dataclass(frozen=True)
class RouteBResolventPortPropagation:
    """Conditional resolvent and port bounds; never a standalone inverse proof."""

    status: str
    delta_exact: Fraction
    inverse_norm_bound_exact: Fraction | None
    inverse_norm_bound_float64: Fraction | None
    inverse_difference_bound: Fraction | None
    port_difference_bound: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    exact_resolvent_premise_required: bool = True
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBGeneralResolventPortPropagation:
    """Conditional perturbation bound for independently rounded blocks.

    This is the O0-R1/O0-R2 algebraic seam.  ``epsilon_a`` bounds the full
    D-block perturbation, while the B/C terms allow the rounded evaluator to
    differ off the diagonal.  All bounds are exact rationals supplied by an
    upstream source/interval proof; this helper does not infer them.
    """

    status: str
    epsilon_a: Fraction | None
    inverse_norm_bound_exact: Fraction | None
    inverse_norm_bound_float64: Fraction | None
    inverse_difference_bound: Fraction | None
    port_difference_bound: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    norm_convention: str | None = None
    weighted_port_bound_required: bool = True
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


def routeb_regularizer_fact() -> RouteBRegularizerFact:
    """Return the recorded scalar fact without evaluating deployed code."""
    if MU_DELTA <= 0 or FLOAT64_MU >= EXACT_MU:
        raise AssertionError("recorded regularizer ordering is inconsistent")
    return RouteBRegularizerFact(
        schema=REGULARIZER_SEMANTICS_SCHEMA,
        float64_bits_hex=FLOAT64_MU_BITS_HEX,
        mu_float64=FLOAT64_MU,
        mu_exact_real=EXACT_MU,
        delta_exact=MU_DELTA,
        outward_interval=(FLOAT64_MU, EXACT_MU),
    )


def audit_routeb_regularizer_inclusion(
    float64_matrix: Sequence[Sequence[Any]],
    exact_real_matrix: Sequence[Sequence[Any]],
) -> RouteBRegularizerInclusion:
    """Check ``M_f = M_r - delta*I`` and expose its entrywise interval.

    Inputs must already be exact integer/rational representations.  Passing a
    Python ``float`` is rejected so this function cannot silently turn a
    machine result into an exact-real claim.
    """
    try:
        float_matrix = _matrix(float64_matrix, "float64_matrix")
        exact_matrix = _matrix(exact_real_matrix, "exact_real_matrix")
    except (TypeError, ValueError) as error:
        return RouteBRegularizerInclusion(
            status="OPEN_FAIL_CLOSED",
            dimension=0,
            float64_matrix=None,
            exact_real_matrix=None,
            lower_matrix=None,
            upper_matrix=None,
            difference_matrix=None,
            delta_exact=MU_DELTA,
            errors=(str(error),),
        )

    errors: list[str] = []
    if len(float_matrix) != len(exact_matrix):
        errors.append("matrix_dimension_mismatch")
    else:
        difference = _subtract(exact_matrix, float_matrix)
        expected = _add_diagonal(
            tuple(tuple(Fraction(0) for _ in row) for row in float_matrix),
            MU_DELTA,
        )
        if difference != expected:
            errors.append("regularizer_difference_is_not_delta_identity")
    difference = (_subtract(exact_matrix, float_matrix)
                  if len(float_matrix) == len(exact_matrix) else None)
    status = "EXACT_OUTWARD_INCLUSION" if not errors else "OPEN_FAIL_CLOSED"
    return RouteBRegularizerInclusion(
        status=status,
        dimension=len(float_matrix),
        float64_matrix=float_matrix,
        exact_real_matrix=exact_matrix,
        lower_matrix=float_matrix,
        upper_matrix=exact_matrix,
        difference_matrix=difference,
        delta_exact=MU_DELTA,
        errors=tuple(errors),
    )


def propagate_routeb_regularizer_diagonal(
    base_matrix: Sequence[Sequence[Any]],
    *,
    block_coords: Sequence[int] = DEFAULT_BLOCK_COORDS,
    remote_coords: Sequence[int] = DEFAULT_REMOTE_COORDS,
) -> RouteBRegularizerDiagonalPropagation:
    """Propagate the scalar seam from one common exact base matrix.

    The returned ``float64_matrix`` is the exact-rational interpretation of
    the deployed binary64 regularizer added to the supplied base.  It is not a
    claim that a Julia Float64 computation produced that base or those entries.
    """
    base = _matrix(base_matrix, "base_matrix")
    block = _coords(block_coords, len(base), "block_coords")
    remote = _coords(remote_coords, len(base), "remote_coords")
    if set(block) & set(remote) or set(block) | set(remote) != set(range(1, len(base) + 1)):
        raise ValueError("block_coords and remote_coords must partition the matrix")
    float_matrix = _add_diagonal(base, FLOAT64_MU)
    exact_matrix = _add_diagonal(base, EXACT_MU)
    inclusion = audit_routeb_regularizer_inclusion(float_matrix, exact_matrix)
    return RouteBRegularizerDiagonalPropagation(
        status="CONDITIONAL_COMMON_BASE_OUTWARD_INCLUSION",
        base_matrix=base,
        float64_matrix=float_matrix,
        exact_real_matrix=exact_matrix,
        inclusion=inclusion,
        block_coords=block,
        remote_coords=remote,
        float64_BB=_select(float_matrix, block, block),
        exact_real_BB=_select(exact_matrix, block, block),
        float64_DD=_select(float_matrix, remote, remote),
        exact_real_DD=_select(exact_matrix, remote, remote),
        float64_BD=_select(float_matrix, block, remote),
        exact_real_BD=_select(exact_matrix, block, remote),
        float64_DB=_select(float_matrix, remote, block),
        exact_real_DB=_select(exact_matrix, remote, block),
    )


def derive_routeb_resolvent_port_propagation(
    premise: RouteBExactResolventPremise | None,
    *,
    mbd_norm_bound: Fraction | int | None = None,
    delta_m_db_norm_bound: Fraction | int | None = None,
    source_key: str | None = None,
) -> RouteBResolventPortPropagation:
    """Apply the resolvent identity only after an explicit exact-real premise.

    If ``K >= ||M_DD(mu_exact)^{-1}||`` and ``delta*K < 1``, then
    ``||M_DD(mu_float)^{-1}|| <= K/(1-delta*K)`` and the inverse difference is
    at most ``delta*K^2/(1-delta*K)``.  The port bound additionally needs
    same-key bounds for ``M_BD`` and ``DeltaM_DB``.  No matrix invertibility or
    coupling bound is inferred by this helper.
    """
    if premise is None:
        return RouteBResolventPortPropagation(
            status="PENDING_RESOLVENT_PREMISE",
            delta_exact=MU_DELTA,
            inverse_norm_bound_exact=None,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=None,
            errors=("exact_real_inverse_norm_bound_missing",),
        )
    errors: list[str] = []
    if not premise.source_key:
        errors.append("resolvent_source_key_missing")
    if premise.norm_convention not in {"induced_2", "induced_infinity"}:
        errors.append("unsupported_norm_convention")
    try:
        inverse_bound = _exact_scalar(premise.inverse_norm_bound, "inverse_norm_bound")
        mbd_bound = (_exact_scalar(mbd_norm_bound, "mbd_norm_bound")
                     if mbd_norm_bound is not None else None)
        db_bound = (_exact_scalar(delta_m_db_norm_bound, "delta_m_db_norm_bound")
                    if delta_m_db_norm_bound is not None else None)
    except TypeError as error:
        errors.append(str(error))
        inverse_bound = mbd_bound = db_bound = None
    if not premise.proves_exact_real_bound:
        errors.append("exact_real_inverse_bound_not_authoritatively_supplied")
    if inverse_bound is not None and inverse_bound < 0:
        errors.append("inverse_norm_bound_negative")
    if mbd_bound is not None and mbd_bound < 0:
        errors.append("mbd_norm_bound_negative")
    if db_bound is not None and db_bound < 0:
        errors.append("delta_m_db_norm_bound_negative")
    coupling_bounds_supplied = mbd_bound is not None or db_bound is not None
    if coupling_bounds_supplied:
        if not source_key:
            errors.append("coupling_source_key_missing")
        elif source_key != premise.source_key:
            errors.append("coupling_source_key_mismatch")
    if errors or inverse_bound is None:
        return RouteBResolventPortPropagation(
            status="OPEN_FAIL_CLOSED" if errors else "PENDING_RESOLVENT_PREMISE",
            delta_exact=MU_DELTA,
            inverse_norm_bound_exact=inverse_bound,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=premise.source_key,
            errors=tuple(errors) or ("exact_real_inverse_norm_bound_missing",),
        )
    contraction = MU_DELTA * inverse_bound
    if contraction >= 1:
        return RouteBResolventPortPropagation(
            status="OPEN_FAIL_CLOSED",
            delta_exact=MU_DELTA,
            inverse_norm_bound_exact=inverse_bound,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=premise.source_key,
            errors=("resolvent_neumann_condition_failed",),
        )
    denominator = 1 - contraction
    float_bound = inverse_bound / denominator
    inverse_difference = MU_DELTA * inverse_bound * inverse_bound / denominator
    port_difference = (
        mbd_bound * db_bound * inverse_difference
        if mbd_bound is not None and db_bound is not None else None
    )
    return RouteBResolventPortPropagation(
        status=("CONDITIONAL_RESOLVENT_PORT_BOUND"
                if port_difference is not None else "CONDITIONAL_RESOLVENT_BOUND"),
        delta_exact=MU_DELTA,
        inverse_norm_bound_exact=inverse_bound,
        inverse_norm_bound_float64=float_bound,
        inverse_difference_bound=inverse_difference,
        port_difference_bound=port_difference,
        source_key=premise.source_key,
        errors=(),
    )


def derive_routeb_general_resolvent_port_propagation(
    premise: RouteBExactResolventPremise | None,
    *,
    epsilon_a: Fraction | int | None = None,
    b_r_norm_bound: Fraction | int | None = None,
    b_difference_norm_bound: Fraction | int | None = None,
    c_f_norm_bound: Fraction | int | None = None,
    c_difference_norm_bound: Fraction | int | None = None,
    source_key: str | None = None,
) -> RouteBGeneralResolventPortPropagation:
    """Compute the exact three-term port perturbation estimate.

    With ``A_r``'s inverse norm bounded by ``K`` and
    ``||A_f-A_r|| <= epsilon_a``, this requires ``epsilon_a*K < 1`` and
    returns ``K_f``, the inverse difference bound, and

    ``||B_f-B_r||*K_f*||C_f|| + ||B_r||*DeltaK*||C_f||
    + ||B_r||*K*||C_f-C_r||``.

    The result is unweighted.  A caller must separately convert it to the
    ledger's energy metric (or provide a direct weighted bound), so this
    function can never silently discharge a Schur/PMI obligation.
    """
    if premise is None:
        return RouteBGeneralResolventPortPropagation(
            status="PENDING_RESOLVENT_PREMISE",
            epsilon_a=None,
            inverse_norm_bound_exact=None,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=None,
            errors=("exact_real_inverse_norm_bound_missing",),
        )

    errors: list[str] = []
    if not premise.source_key:
        errors.append("resolvent_source_key_missing")
    if premise.norm_convention not in {"induced_2", "induced_infinity"}:
        errors.append("unsupported_norm_convention")
    names = {
        "inverse_norm_bound": premise.inverse_norm_bound,
        "epsilon_a": epsilon_a,
        "b_r_norm_bound": b_r_norm_bound,
        "b_difference_norm_bound": b_difference_norm_bound,
        "c_f_norm_bound": c_f_norm_bound,
        "c_difference_norm_bound": c_difference_norm_bound,
    }
    values: dict[str, Fraction | None] = {}
    for name, value in names.items():
        try:
            values[name] = (_exact_scalar(value, name) if value is not None else None)
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    inverse_bound = values["inverse_norm_bound"]
    epsilon = values["epsilon_a"]
    if not premise.proves_exact_real_bound:
        errors.append("exact_real_inverse_bound_not_authoritatively_supplied")
    if inverse_bound is not None and inverse_bound < 0:
        errors.append("inverse_norm_bound_negative")
    for name in ("epsilon_a", "b_r_norm_bound", "b_difference_norm_bound",
                 "c_f_norm_bound", "c_difference_norm_bound"):
        value = values[name]
        if value is not None and value < 0:
            errors.append(f"{name}_negative")
    required = ("epsilon_a", "b_r_norm_bound", "b_difference_norm_bound",
                "c_f_norm_bound", "c_difference_norm_bound")
    for name in required:
        if values[name] is None:
            errors.append(f"{name}_missing")
    if source_key is None:
        errors.append("coupling_source_key_missing")
    elif source_key != premise.source_key:
        errors.append("coupling_source_key_mismatch")
    if errors or inverse_bound is None or epsilon is None:
        return RouteBGeneralResolventPortPropagation(
            status="OPEN_FAIL_CLOSED" if errors else "PENDING_RESOLVENT_PREMISE",
            epsilon_a=epsilon,
            inverse_norm_bound_exact=inverse_bound,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=premise.source_key,
            errors=tuple(dict.fromkeys(errors)) or ("resolvent_bounds_missing",),
            norm_convention=premise.norm_convention,
        )
    contraction = epsilon * inverse_bound
    if contraction >= 1:
        return RouteBGeneralResolventPortPropagation(
            status="OPEN_FAIL_CLOSED",
            epsilon_a=epsilon,
            inverse_norm_bound_exact=inverse_bound,
            inverse_norm_bound_float64=None,
            inverse_difference_bound=None,
            port_difference_bound=None,
            source_key=premise.source_key,
            errors=("resolvent_neumann_condition_failed",),
            norm_convention=premise.norm_convention,
        )
    denominator = 1 - contraction
    float_bound = inverse_bound / denominator
    inverse_difference = epsilon * inverse_bound * inverse_bound / denominator
    port_difference = (
        values["b_difference_norm_bound"] * float_bound * values["c_f_norm_bound"]
        + values["b_r_norm_bound"] * inverse_difference * values["c_f_norm_bound"]
        + values["b_r_norm_bound"] * inverse_bound * values["c_difference_norm_bound"]
    )
    return RouteBGeneralResolventPortPropagation(
        status="CONDITIONAL_GENERAL_RESOLVENT_PORT_BOUND",
        epsilon_a=epsilon,
        inverse_norm_bound_exact=inverse_bound,
        inverse_norm_bound_float64=float_bound,
        inverse_difference_bound=inverse_difference,
        port_difference_bound=port_difference,
        source_key=premise.source_key,
        errors=(),
        norm_convention=premise.norm_convention,
    )


__all__ = [
    "DEFAULT_BLOCK_COORDS",
    "DEFAULT_REMOTE_COORDS",
    "EXACT_MU",
    "FLOAT64_MU",
    "FLOAT64_MU_BITS_HEX",
    "MU_DELTA",
    "REGULARIZER_SEMANTICS_SCHEMA",
    "RouteBExactResolventPremise",
    "RouteBRegularizerDiagonalPropagation",
    "RouteBRegularizerFact",
    "RouteBRegularizerInclusion",
    "RouteBResolventPortPropagation",
    "RouteBGeneralResolventPortPropagation",
    "audit_routeb_regularizer_inclusion",
    "derive_routeb_general_resolvent_port_propagation",
    "derive_routeb_resolvent_port_propagation",
    "propagate_routeb_regularizer_diagonal",
    "routeb_regularizer_fact",
]
