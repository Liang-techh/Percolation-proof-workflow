"""Convention arithmetic only; consume, do not rerun, the raw envelope audit.

Read-only stdout. No source execution, numerical trig, admission or file writes.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path('C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq')
PRIOR_HASH = '71743ce600e1caaf8bd4f8a4a1e55d7c6972b3644c03374ba4b0323f5dbb88f5'
EXTRA_PINS = {
    'routeB_compact_dh_storage_shift_audit.jl': 'aa3957f714f86c631a55fb8e7cc190fc98918a9cc04d148adcd7a28141cb9fec',
    'routeB_compact_block_energy_barrier_audit.py': '62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927',
    'routeB_compact_targeted_nonlinear_strictification_audit.jl': '41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1',
    'routeB_compact_energy_power_rewrite_audit.jl': '7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf',
}


def check_hash(path, expected):
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected:
        raise ValueError('source/evidence drift: ' + str(path))
    return raw


def audit():
    prior = json.loads(check_hash(HERE / 'NEW_RESULT.json', PRIOR_HASH))
    pins = {**prior['source_sha256'], **EXTRA_PINS}
    for name, digest in pins.items():
        check_hash(ROOT / name, digest)
    # Previously established mass/trig lower proof is consumed, not repeated.
    L = Q(prior['uniform_W_lower'])
    u = Q(prior['recorded_initial_upper'])
    m = Q(prior['mass_operator_upper'])
    r = Q(prior['radius'])
    assert all(Q(g) == 0 for g in prior['analytic_g0'])
    # Source coefficients and conventions inspected in the pinned definitions.
    A0, A, B = Q(762237, 200000), Q(242307, 200000), Q(20601, 400000)
    anchor = A0 + A + B
    shift = A0 + A + 2*B  # controller square shift is zero for THIS analytic g0.
    eps = Q(1, 1000)
    delta = eps*m*r*r/2
    centered = max(Q(3, 5)/2, m/2)*r*r
    quantities = {
        'raw_uniform_lower_consumed': L, 'recorded_initial_upper': u,
        'active_threshold': Q(1), 'anchor': anchor,
        'gravity_additive_shift': shift, 'controller_square_shift': Q(0),
        'shifted_anchor': anchor+shift,
        'shifted_uniform_lower': L+shift,
        'cross_absolute_loss': delta, 'cross_raw_uniform_lower': L-delta,
        'raw_threshold_gap': L-1, 'shifted_threshold_gap': L+shift-1,
        'cross_raw_threshold_gap': L-delta-1,
        'centered_W_upper': centered, 'centered_T_upper': centered+delta,
        'centered_W_slack_to_recorded': u-centered,
        'centered_T_slack_to_recorded': u-centered-delta,
        'raw_equivalent_centered_threshold': 1-anchor,
        'shifted_equivalent_centered_threshold': 1-anchor-shift,
    }
    assert L > 1 > u > centered+delta >= centered
    assert L-delta > 1 and shift > 0
    return {
        'status': 'pending', 'scope': 'conditional ideal-function convention comparison only',
        'prior_result_sha256': PRIOR_HASH, 'source_sha256': pins,
        'fixed_domain': prior['domain'],
        'configuration_policy': 'same analytic M/U/g/gains and X0; convention functions explicitly distinguished; targeted dynamics not imported',
        'quantities': {k: str(v) for k, v in quantities.items()},
        'prior_envelope_rerun': False, 'python_convention_assertions_pass': True,
        'julia_execution': False, 'lean_lake_execution': False,
        'runtime_observation': None, 'source_binding_proven': False,
        'active_function_selected': None, 'registry_eligible': False,
        'formal_certificate_allowed': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
