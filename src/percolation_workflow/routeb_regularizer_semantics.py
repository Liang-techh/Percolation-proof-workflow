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
    # A numeric bound is only a candidate until its exact-real proof receipt
    # is explicitly attached by the caller.
    proves_exact_real_bound: bool = False


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


@dataclass(frozen=True)
class RouteBWeightedPortMetricConversion:
    """Conditional conversion from an unweighted port bound to a metric bound."""

    status: str
    unweighted_port_bound: Fraction | None
    sqrt_metric_lower_bound: Fraction | None
    weighted_port_bound: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    metric_relation: str = "B_up >= beta I and sqrt_metric_lower_bound^2 <= beta"
    schur_margin_consumed: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBInfinityToL2WeightedConversion:
    """Conditional conversion with an explicit output-norm factor.

    A bound in induced infinity norm controls ``||R a||_infinity``.  For a
    two-dimensional output it does not directly control ``||R a||_2``; a
    proved factor (for example the safe rational factor ``2``) must be
    supplied.  This separate type prevents the older scalar metric helper
    from silently relabelling output norms.
    """

    status: str
    unweighted_infinity_bound: Fraction | None
    output_norm_factor: Fraction | None
    sqrt_metric_lower_bound: Fraction | None
    weighted_l2_bound: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    output_dimension: int = 2
    output_norm_conversion_proven: bool = False
    metric_lower_bound_proven: bool = False
    schur_margin_consumed: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBRootWitness:
    """Exact root witness for a squared baseline candidate.

    This object certifies only the scalar relation ``g <= rho^2``.  It does
    not certify that ``g`` bounds the physical baseline map or that its source
    and metric are authoritative.
    """

    status: str
    squared_bound: Fraction | None
    root_bound: Fraction | None
    slack: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    squared_bound_proven: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBAffineBiasGain:
    """Conditional exact gain for a relative residual plus an affine bias.

    If ``r = R_rel*a + b`` and the relative and bias terms are separately
    bounded in the same quadratic metric, Young's inequality yields
    ``gamma_bias = (1+tau)*rho_rel^2 + (1+1/tau)*beta_bias``.  This helper
    checks only that scalar interface and an optional exact root witness; it
    never invents a homogeneous bound when the bias premise is absent.
    """

    status: str
    rho_relative: Fraction | None
    beta_bias: Fraction | None
    tau: Fraction | None
    effective_squared_gain: Fraction | None
    rho_bias: Fraction | None
    root_slack: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    relative_bound_proven: bool = False
    bias_bound_proven: bool = False
    root_bound_proven: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBPhysicalBaselineFactor:
    """Conditional exact ratio from a physical mass lower bound to ``A_up``.

    The scalar ratio is useful for the O0 frontier, but it is not a physical
    theorem until the mass enclosure, symmetry, energy identity, and metric
    binding are all supplied under one source key.  This object deliberately
    keeps those premises explicit and never consumes a Schur margin by itself.
    """

    status: str
    mass_lower: Fraction | None
    metric_upper: Fraction | None
    L_base: Fraction | None
    theta: Fraction | None
    rho_rounded: Fraction | None
    strict_margin: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    mass_enclosure_proven: bool = False
    symmetry_proven: bool = False
    energy_identity_proven: bool = False
    metric_binding_proven: bool = False
    baseline_bound_proven: bool = False
    strict_margin_proven: bool = False
    schur_margin_consumed: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBZeroShiftWeightedPerturbation:
    """Conditional weighted perturbation bound when both off-diagonal shifts vanish."""

    status: str
    delta: Fraction | None
    inverse_bound: Fraction | None
    inverse_difference_bound: Fraction | None
    b_r_norm_bound: Fraction | None
    c_f_norm_bound: Fraction | None
    sqrt_metric_lower_bound: Fraction | None
    unweighted_bound: Fraction | None
    weighted_bound: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    exact_inverse_proven: bool = False
    zero_offdiagonal_shift_proven: bool = False
    metric_lower_bound_proven: bool = False
    formal_certificate_allowed: bool = False
    registry_eligible: bool = False


@dataclass(frozen=True)
class RouteBSchurMarginConsumption:
    """Conditional Young/Schur budget after a weighted port perturbation."""

    status: str
    rho_baseline: Fraction | None
    epsilon_port: Fraction | None
    rho_rounded: Fraction | None
    theta: Fraction | None
    added_young_charge: Fraction | None
    remaining_margin: Fraction | None
    source_key: str | None
    errors: tuple[str, ...] = ()
    margin_consumed: bool = False
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


def convert_routeb_port_bound_to_weighted_metric(
    unweighted_port_bound: Fraction | int | None,
    sqrt_metric_lower_bound: Fraction | int | None,
    *,
    source_key: str | None,
    metric_source_key: str | None,
    metric_lower_bound_proven: bool = False,
) -> RouteBWeightedPortMetricConversion:
    """Convert ``||R||`` to a conservative ``B_up``-weighted port bound.

    The caller must supply an exact rational ``s > 0`` with a proved relation
    ``s^2 <= beta`` and ``B_up >= beta I``.  Then ``||R B_up^(-1/2)||`` is at
    most ``||R|| / s``.  This helper only performs that conditional arithmetic;
    it does not prove the metric inequality or consume a Schur/Young margin.
    """
    errors: list[str] = []
    try:
        unweighted = (_exact_scalar(unweighted_port_bound, "unweighted_port_bound")
                      if unweighted_port_bound is not None else None)
        metric_root = (_exact_scalar(sqrt_metric_lower_bound, "sqrt_metric_lower_bound")
                       if sqrt_metric_lower_bound is not None else None)
    except TypeError as error:
        errors.append(str(error))
        unweighted = metric_root = None
    if unweighted is None:
        errors.append("unweighted_port_bound_missing")
    elif unweighted < 0:
        errors.append("unweighted_port_bound_negative")
    if metric_root is None:
        errors.append("sqrt_metric_lower_bound_missing")
    elif metric_root <= 0:
        errors.append("sqrt_metric_lower_bound_not_positive")
    if not source_key or not metric_source_key:
        errors.append("metric_source_key_missing")
    elif source_key != metric_source_key:
        errors.append("metric_source_key_mismatch")
    if not metric_lower_bound_proven:
        errors.append("metric_lower_bound_not_authoritatively_supplied")
    if errors:
        return RouteBWeightedPortMetricConversion(
            status="OPEN_FAIL_CLOSED",
            unweighted_port_bound=unweighted,
            sqrt_metric_lower_bound=metric_root,
            weighted_port_bound=None,
            source_key=source_key,
            errors=tuple(dict.fromkeys(errors)),
        )
    return RouteBWeightedPortMetricConversion(
        status="CONDITIONAL_WEIGHTED_PORT_BOUND",
        unweighted_port_bound=unweighted,
        sqrt_metric_lower_bound=metric_root,
        weighted_port_bound=unweighted / metric_root,
        source_key=source_key,
        errors=(),
    )


def convert_routeb_infinity_port_bound_to_weighted_l2(
    unweighted_infinity_bound: Fraction | int | None,
    output_norm_factor: Fraction | int | None,
    sqrt_metric_lower_bound: Fraction | int | None,
    *,
    source_key: str | None,
    metric_source_key: str | None,
    output_norm_conversion_proven: bool = False,
    metric_lower_bound_proven: bool = False,
    output_dimension: int = 2,
) -> RouteBInfinityToL2WeightedConversion:
    """Convert an induced-infinity bound only after an explicit norm proof.

    If ``||R a||_infinity <= U ||a||_infinity`` and a proved factor ``c``
    satisfies ``||y||_2 <= c ||y||_infinity`` on the output space, then the
    weighted bound is ``c*U/s`` when ``s ||a||_2`` is controlled by the metric.
    The default factor ``2`` is intentionally not itself a proof; callers must
    set ``output_norm_conversion_proven=True`` after supplying that premise.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in (
        ("unweighted_infinity_bound", unweighted_infinity_bound),
        ("output_norm_factor", output_norm_factor),
        ("sqrt_metric_lower_bound", sqrt_metric_lower_bound),
    ):
        try:
            values[name] = _exact_scalar(value, name) if value is not None else None
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    infinity_bound = values["unweighted_infinity_bound"]
    factor = values["output_norm_factor"]
    root = values["sqrt_metric_lower_bound"]
    if infinity_bound is None:
        errors.append("unweighted_infinity_bound_missing")
    elif infinity_bound < 0:
        errors.append("unweighted_infinity_bound_negative")
    if factor is None:
        errors.append("output_norm_factor_missing")
    elif factor <= 0:
        errors.append("output_norm_factor_not_positive")
    if root is None:
        errors.append("sqrt_metric_lower_bound_missing")
    elif root <= 0:
        errors.append("sqrt_metric_lower_bound_not_positive")
    if output_dimension != 2:
        errors.append("output_dimension_not_supported")
    if not source_key or not metric_source_key:
        errors.append("metric_source_key_missing")
    elif source_key != metric_source_key:
        errors.append("metric_source_key_mismatch")
    if not output_norm_conversion_proven:
        errors.append("output_norm_conversion_not_authoritatively_supplied")
    if not metric_lower_bound_proven:
        errors.append("metric_lower_bound_not_authoritatively_supplied")
    if errors:
        return RouteBInfinityToL2WeightedConversion(
            status="OPEN_FAIL_CLOSED",
            unweighted_infinity_bound=infinity_bound,
            output_norm_factor=factor,
            sqrt_metric_lower_bound=root,
            weighted_l2_bound=None,
            source_key=source_key,
            errors=tuple(dict.fromkeys(errors)),
            output_dimension=output_dimension,
            output_norm_conversion_proven=output_norm_conversion_proven,
            metric_lower_bound_proven=metric_lower_bound_proven,
        )
    assert infinity_bound is not None and factor is not None and root is not None
    return RouteBInfinityToL2WeightedConversion(
        status="CONDITIONAL_INFINITY_TO_L2_WEIGHTED_BOUND",
        unweighted_infinity_bound=infinity_bound,
        output_norm_factor=factor,
        sqrt_metric_lower_bound=root,
        weighted_l2_bound=factor * infinity_bound / root,
        source_key=source_key,
        output_dimension=output_dimension,
        output_norm_conversion_proven=True,
        metric_lower_bound_proven=True,
    )


def derive_routeb_zero_shift_weighted_perturbation(
    delta: Fraction | int | None,
    inverse_bound: Fraction | int | None,
    b_r_norm_bound: Fraction | int | None,
    c_f_norm_bound: Fraction | int | None,
    sqrt_metric_lower_bound: Fraction | int | None,
    *,
    source_key: str | None,
    metric_source_key: str | None,
    exact_inverse_proven: bool = False,
    zero_offdiagonal_shift_proven: bool = False,
    metric_lower_bound_proven: bool = False,
) -> RouteBZeroShiftWeightedPerturbation:
    """Derive the reduced O0-R1/R2 bound under explicit zero-shift premises.

    When ``dB=dC=0`` is authoritative, the general three-term estimate reduces
    to ``Br * Cf * delta*K^2/(1-delta*K)``.  All inputs remain conditional
    receipt fields; this helper never proves the zero-shift or physical map
    identity itself.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in (
        ("delta", delta), ("inverse_bound", inverse_bound),
        ("b_r_norm_bound", b_r_norm_bound), ("c_f_norm_bound", c_f_norm_bound),
        ("sqrt_metric_lower_bound", sqrt_metric_lower_bound),
    ):
        try:
            values[name] = _exact_scalar(value, name) if value is not None else None
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    for name in values:
        value = values[name]
        if value is None:
            errors.append(f"{name}_missing")
        elif value < 0:
            errors.append(f"{name}_negative")
    if not source_key or not metric_source_key:
        errors.append("zero_shift_source_key_missing")
    elif source_key != metric_source_key:
        errors.append("zero_shift_metric_source_key_mismatch")
    if not exact_inverse_proven:
        errors.append("exact_inverse_not_authoritatively_supplied")
    if not zero_offdiagonal_shift_proven:
        errors.append("zero_offdiagonal_shift_not_authoritatively_supplied")
    if not metric_lower_bound_proven:
        errors.append("metric_lower_bound_not_authoritatively_supplied")
    delta_value = values["delta"]
    inverse = values["inverse_bound"]
    root = values["sqrt_metric_lower_bound"]
    if root is not None and root <= 0:
        errors.append("sqrt_metric_lower_bound_not_positive")
    if errors:
        return RouteBZeroShiftWeightedPerturbation(
            status="OPEN_FAIL_CLOSED", delta=delta_value, inverse_bound=inverse,
            inverse_difference_bound=None, b_r_norm_bound=values["b_r_norm_bound"],
            c_f_norm_bound=values["c_f_norm_bound"],
            sqrt_metric_lower_bound=root, unweighted_bound=None, weighted_bound=None,
            source_key=source_key, errors=tuple(dict.fromkeys(errors)),
            exact_inverse_proven=exact_inverse_proven,
            zero_offdiagonal_shift_proven=zero_offdiagonal_shift_proven,
            metric_lower_bound_proven=metric_lower_bound_proven,
        )
    assert delta_value is not None and inverse is not None and root is not None
    contraction = delta_value * inverse
    if contraction >= 1:
        return RouteBZeroShiftWeightedPerturbation(
            status="OPEN_FAIL_CLOSED", delta=delta_value, inverse_bound=inverse,
            inverse_difference_bound=None, b_r_norm_bound=values["b_r_norm_bound"],
            c_f_norm_bound=values["c_f_norm_bound"],
            sqrt_metric_lower_bound=root, unweighted_bound=None, weighted_bound=None,
            source_key=source_key, errors=("resolvent_neumann_condition_failed",),
            exact_inverse_proven=True, zero_offdiagonal_shift_proven=True,
            metric_lower_bound_proven=True,
        )
    delta_inverse = delta_value * inverse * inverse / (1 - contraction)
    unweighted = values["b_r_norm_bound"] * values["c_f_norm_bound"] * delta_inverse
    assert unweighted is not None
    return RouteBZeroShiftWeightedPerturbation(
        status="CONDITIONAL_ZERO_SHIFT_WEIGHTED_PORT_BOUND", delta=delta_value,
        inverse_bound=inverse, inverse_difference_bound=delta_inverse,
        b_r_norm_bound=values["b_r_norm_bound"],
        c_f_norm_bound=values["c_f_norm_bound"],
        sqrt_metric_lower_bound=root, unweighted_bound=unweighted,
        weighted_bound=unweighted / root, source_key=source_key,
        exact_inverse_proven=True, zero_offdiagonal_shift_proven=True,
        metric_lower_bound_proven=True,
    )


def derive_routeb_root_witness(
    squared_bound: Fraction | int | None,
    root_bound: Fraction | int | None,
    *,
    source_key: str | None,
    squared_bound_proven: bool = False,
) -> RouteBRootWitness:
    """Check an exact candidate ``rho`` against a squared bound ``g``.

    The relation is checked before the provenance flag.  Thus an invalid root
    is rejected even when the upstream receipt claims authority, while a valid
    scalar pair without an authoritative upstream bound remains conditional.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in (("squared_bound", squared_bound), ("root_bound", root_bound)):
        try:
            values[name] = _exact_scalar(value, name) if value is not None else None
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    g = values["squared_bound"]
    rho = values["root_bound"]
    if g is None:
        errors.append("squared_bound_missing")
    elif g < 0:
        errors.append("squared_bound_negative")
    if rho is None:
        errors.append("root_bound_missing")
    elif rho < 0:
        errors.append("root_bound_negative")
    if not source_key:
        errors.append("root_witness_source_key_missing")
    if errors:
        return RouteBRootWitness(
            status="OPEN_FAIL_CLOSED", squared_bound=g, root_bound=rho,
            slack=None, source_key=source_key,
            errors=tuple(dict.fromkeys(errors)),
            squared_bound_proven=squared_bound_proven,
        )
    assert g is not None and rho is not None
    slack = rho * rho - g
    if slack < 0:
        return RouteBRootWitness(
            status="OPEN_FAIL_CLOSED", squared_bound=g, root_bound=rho,
            slack=slack, source_key=source_key,
            errors=("root_bound_squared_below_squared_bound",),
            squared_bound_proven=squared_bound_proven,
        )
    if not squared_bound_proven:
        return RouteBRootWitness(
            status="CONDITIONAL_ROOT_WITNESS", squared_bound=g, root_bound=rho,
            slack=slack, source_key=source_key,
            errors=("squared_bound_not_authoritatively_supplied",),
            squared_bound_proven=False,
        )
    return RouteBRootWitness(
        status="CONDITIONAL_ROOT_WITNESS", squared_bound=g, root_bound=rho,
        slack=slack, source_key=source_key, squared_bound_proven=True,
    )


def derive_routeb_affine_bias_gain(
    rho_relative: Fraction | int | None,
    beta_bias: Fraction | int | None,
    tau: Fraction | int | None,
    rho_bias: Fraction | int | None = None,
    *,
    source_key: str | None,
    relative_bound_proven: bool = False,
    bias_bound_proven: bool = False,
    root_bound_proven: bool = False,
) -> RouteBAffineBiasGain:
    """Derive the exact Young gain for an affine residual interface.

    The returned result is conditional even when all scalar checks pass.  A
    caller still has to supply authoritative source/metric statements and the
    physical residual identity before any Schur consumer can use it.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in (("rho_relative", rho_relative), ("beta_bias", beta_bias),
                        ("tau", tau), ("rho_bias", rho_bias)):
        try:
            values[name] = (_exact_scalar(value, name) if value is not None else None)
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    rho = values["rho_relative"]
    beta = values["beta_bias"]
    tau_value = values["tau"]
    root = values["rho_bias"]
    if rho is None:
        errors.append("rho_relative_missing")
    elif rho < 0:
        errors.append("rho_relative_negative")
    if beta is None:
        errors.append("beta_bias_missing")
    elif beta < 0:
        errors.append("beta_bias_negative")
    if tau_value is None:
        errors.append("tau_missing")
    elif tau_value <= 0:
        errors.append("tau_not_positive")
    if root is not None and root < 0:
        errors.append("rho_bias_negative")
    if not source_key:
        errors.append("affine_bias_source_key_missing")
    if not relative_bound_proven:
        errors.append("relative_residual_bound_not_authoritatively_supplied")
    if not bias_bound_proven:
        errors.append("bias_bound_not_authoritatively_supplied")
    gamma: Fraction | None = None
    slack: Fraction | None = None
    if rho is not None and beta is not None and tau_value is not None and not any(
        error in {"rho_relative_negative", "beta_bias_negative", "tau_not_positive"}
        for error in errors
    ):
        gamma = (1 + tau_value) * rho * rho + (1 + 1 / tau_value) * beta
        if root is None:
            errors.append("rho_bias_root_witness_missing")
        else:
            slack = root * root - gamma
            if slack < 0:
                errors.append("rho_bias_squared_below_effective_gain")
            if not root_bound_proven:
                errors.append("rho_bias_root_not_authoritatively_supplied")
    if errors and any(
        token in error for error in errors
        for token in ("malformed", "negative", "not_positive", "below_effective", "missing")
    ):
        status = "OPEN_FAIL_CLOSED"
    else:
        status = "CONDITIONAL_AFFINE_BIAS_GAIN"
    return RouteBAffineBiasGain(
        status=status,
        rho_relative=rho,
        beta_bias=beta,
        tau=tau_value,
        effective_squared_gain=gamma,
        rho_bias=root,
        root_slack=slack,
        source_key=source_key,
        errors=tuple(dict.fromkeys(errors)),
        relative_bound_proven=relative_bound_proven,
        bias_bound_proven=bias_bound_proven,
        root_bound_proven=root_bound_proven,
    )


def derive_routeb_physical_baseline_factor(
    mass_lower: Fraction | int | None,
    metric_upper: Fraction | int | None,
    *,
    source_key: str | None,
    mass_enclosure_proven: bool = False,
    symmetry_proven: bool = False,
    energy_identity_proven: bool = False,
    metric_binding_proven: bool = False,
    theta: Fraction | int | None = None,
    rho_rounded: Fraction | int | None = None,
    strict_margin_proven: bool = False,
) -> RouteBPhysicalBaselineFactor:
    """Compute an exact conditional physical baseline factor.

    If ``mass_lower`` bounds ``a_Bᵀ M_BB a_B`` and ``metric_upper`` bounds
    ``A_up`` relative to the same ``||a_B||₂²``, the scalar candidate is their
    ratio.  The caller must explicitly bind all four physical premises before
    this can be treated as a baseline theorem.  When ``theta`` and
    ``rho_rounded`` are supplied, the strict Schur leftover is calculated but
    is never marked consumed by this helper.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in (("mass_lower", mass_lower), ("metric_upper", metric_upper),
                        ("theta", theta), ("rho_rounded", rho_rounded)):
        try:
            values[name] = _exact_scalar(value, name) if value is not None else None
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    mass = values["mass_lower"]
    metric = values["metric_upper"]
    theta_value = values["theta"]
    rho_value = values["rho_rounded"]
    if mass is None:
        errors.append("mass_lower_missing")
    elif mass < 0:
        errors.append("mass_lower_negative")
    if metric is None:
        errors.append("metric_upper_missing")
    elif metric <= 0:
        errors.append("metric_upper_not_positive")
    if not source_key:
        errors.append("baseline_source_key_missing")
    for flag, label in (
        (mass_enclosure_proven, "mass_enclosure"),
        (symmetry_proven, "symmetry"),
        (energy_identity_proven, "energy_identity"),
        (metric_binding_proven, "metric_binding"),
    ):
        if not flag:
            errors.append(f"{label}_not_authoritatively_supplied")
    if theta_value is not None and theta_value <= 0:
        errors.append("theta_not_positive")
    if rho_value is not None and rho_value < 0:
        errors.append("rho_rounded_negative")
    baseline_proven = all((mass_enclosure_proven, symmetry_proven,
                           energy_identity_proven, metric_binding_proven))
    L_base: Fraction | None = None
    strict_margin: Fraction | None = None
    if mass is not None and metric is not None and metric > 0:
        L_base = mass / metric
        if theta_value is not None and rho_value is not None and theta_value > 0 and rho_value >= 0:
            strict_margin = L_base - (1 + 1 / theta_value) * rho_value * rho_value
            if strict_margin_proven and (not baseline_proven or strict_margin <= 0):
                errors.append("strict_margin_not_proven_or_not_positive")
    invalid = any(
        token in error for error in errors
        for token in ("missing", "negative", "not_positive", "malformed")
    )
    status = "OPEN_FAIL_CLOSED" if invalid else "CONDITIONAL_EXACT_PHYSICAL_BASELINE"
    if not baseline_proven and status != "OPEN_FAIL_CLOSED":
        status = "CONDITIONAL_EXACT_PHYSICAL_BASELINE"
    return RouteBPhysicalBaselineFactor(
        status=status,
        mass_lower=mass,
        metric_upper=metric,
        L_base=L_base,
        theta=theta_value,
        rho_rounded=rho_value,
        strict_margin=strict_margin,
        source_key=source_key,
        errors=tuple(dict.fromkeys(errors)),
        mass_enclosure_proven=mass_enclosure_proven,
        symmetry_proven=symmetry_proven,
        energy_identity_proven=energy_identity_proven,
        metric_binding_proven=metric_binding_proven,
        baseline_bound_proven=baseline_proven,
        strict_margin_proven=(strict_margin_proven and baseline_proven
                              and strict_margin is not None and strict_margin > 0),
    )


def consume_routeb_schur_margin(
    rho_baseline: Fraction | int | None,
    epsilon_port: Fraction | int | None,
    theta: Fraction | int | None,
    remaining_schur_margin: Fraction | int | None,
    *,
    source_key: str | None,
    margin_source_key: str | None,
    baseline_bound_proven: bool = False,
    perturbation_bound_proven: bool = False,
    require_strict_remaining: bool = False,
) -> RouteBSchurMarginConsumption:
    """Consume the exact Young charge caused by a weighted port perturbation.

    For nonnegative ``rho_baseline`` and ``epsilon_port`` and ``theta > 0``,
    the added charge is

    ``(1 + 1/theta) * ((rho_baseline + epsilon_port)^2 - rho_baseline^2)``.

    This function only checks the scalar budget and matching provenance.  It
    does not prove the baseline port bound, the weighted perturbation bound,
    or any physical Schur/PMI statement.
    """
    errors: list[str] = []
    values: dict[str, Fraction | None] = {}
    for name, value in {
        "rho_baseline": rho_baseline,
        "epsilon_port": epsilon_port,
        "theta": theta,
        "remaining_schur_margin": remaining_schur_margin,
    }.items():
        try:
            values[name] = _exact_scalar(value, name) if value is not None else None
        except TypeError as error:
            errors.append(str(error))
            values[name] = None
    rho = values["rho_baseline"]
    epsilon = values["epsilon_port"]
    theta_value = values["theta"]
    margin = values["remaining_schur_margin"]
    for name, value in (("rho_baseline", rho), ("epsilon_port", epsilon),
                        ("remaining_schur_margin", margin)):
        if value is None:
            errors.append(f"{name}_missing")
        elif value < 0:
            errors.append(f"{name}_negative")
    if theta_value is None:
        errors.append("theta_missing")
    elif theta_value <= 0:
        errors.append("theta_not_positive")
    if not source_key or not margin_source_key:
        errors.append("schur_source_key_missing")
    elif source_key != margin_source_key:
        errors.append("schur_source_key_mismatch")
    if not baseline_bound_proven:
        errors.append("baseline_port_bound_not_authoritatively_supplied")
    if not perturbation_bound_proven:
        errors.append("weighted_port_perturbation_not_authoritatively_supplied")
    if errors:
        return RouteBSchurMarginConsumption(
            status="OPEN_FAIL_CLOSED",
            rho_baseline=rho,
            epsilon_port=epsilon,
            rho_rounded=(rho + epsilon if rho is not None and epsilon is not None else None),
            theta=theta_value,
            added_young_charge=None,
            remaining_margin=margin,
            source_key=source_key,
            errors=tuple(dict.fromkeys(errors)),
        )
    rho_rounded = rho + epsilon
    charge = (1 + 1 / theta_value) * (rho_rounded * rho_rounded - rho * rho)
    leftover = margin - charge
    if leftover < 0:
        return RouteBSchurMarginConsumption(
            status="OPEN_SCHUR_MARGIN_INSUFFICIENT",
            rho_baseline=rho,
            epsilon_port=epsilon,
            rho_rounded=rho_rounded,
            theta=theta_value,
            added_young_charge=charge,
            remaining_margin=leftover,
            source_key=source_key,
            errors=("young_charge_exceeds_remaining_schur_margin",),
        )
    if require_strict_remaining and leftover == 0:
        return RouteBSchurMarginConsumption(
            status="OPEN_SCHUR_MARGIN_NOT_STRICT",
            rho_baseline=rho,
            epsilon_port=epsilon,
            rho_rounded=rho_rounded,
            theta=theta_value,
            added_young_charge=charge,
            remaining_margin=leftover,
            source_key=source_key,
            errors=("strict_remaining_schur_margin_not_positive",),
        )
    return RouteBSchurMarginConsumption(
        status="CONDITIONAL_SCHUR_MARGIN_CONSUMED",
        rho_baseline=rho,
        epsilon_port=epsilon,
        rho_rounded=rho_rounded,
        theta=theta_value,
        added_young_charge=charge,
        remaining_margin=leftover,
        source_key=source_key,
        errors=(),
        margin_consumed=True,
    )


def consume_routeb_strict_schur_margin(
    rho_baseline: Fraction | int | None,
    epsilon_port: Fraction | int | None,
    theta: Fraction | int | None,
    remaining_schur_margin: Fraction | int | None,
    *,
    source_key: str | None,
    margin_source_key: str | None,
    baseline_bound_proven: bool = False,
    perturbation_bound_proven: bool = False,
) -> RouteBSchurMarginConsumption:
    """Consume a Schur budget only when its leftover is strictly positive."""
    return consume_routeb_schur_margin(
        rho_baseline,
        epsilon_port,
        theta,
        remaining_schur_margin,
        source_key=source_key,
        margin_source_key=margin_source_key,
        baseline_bound_proven=baseline_bound_proven,
        perturbation_bound_proven=perturbation_bound_proven,
        require_strict_remaining=True,
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
    "RouteBWeightedPortMetricConversion",
    "RouteBInfinityToL2WeightedConversion",
    "RouteBRootWitness",
    "RouteBAffineBiasGain",
    "RouteBPhysicalBaselineFactor",
    "RouteBZeroShiftWeightedPerturbation",
    "RouteBSchurMarginConsumption",
    "audit_routeb_regularizer_inclusion",
    "convert_routeb_port_bound_to_weighted_metric",
    "convert_routeb_infinity_port_bound_to_weighted_l2",
    "derive_routeb_root_witness",
    "derive_routeb_affine_bias_gain",
    "derive_routeb_physical_baseline_factor",
    "derive_routeb_zero_shift_weighted_perturbation",
    "consume_routeb_schur_margin",
    "derive_routeb_general_resolvent_port_propagation",
    "derive_routeb_resolvent_port_propagation",
    "propagate_routeb_regularizer_diagonal",
    "routeb_regularizer_fact",
]
