# Active energy origin: normalization and source identity audit

Status: **OPEN_UNCOMPILED**. Only this new leaf and review were written.
External sources, prior leaves, state, registry and shared scripts were not
modified. No Julia audit script, Lean/Lake, simulation or wide regression ran.

## Finding

The inspected active barrier records `V<=1` but does not instantiate one
typed storage expression with a fixed additive constant. Its input chain
mixes a full physical-energy description with an initial bound produced for
a different targeted-gain, cross-term storage. Thus the actual active
candidate's `V(0,0)<=1` is **not established** by these files.

Exact arithmetic distinguishes the following expressions:

| Expression at `q=v=0`, with `cos=1,sin=0` | Exact value | At most 1? |
| --- | --- | --- |
| Fourier audit `K+Ugrav+Uctrl`, no additional constant | `2029689/400000` | No |
| Same expression plus recorded gravity shift `205029/40000` (controller shift recorded as zero) | `4079979/400000` | No |
| Literal exact-real DH midpoint-potential ledger, before any normalization | `3108789/400000` | No |
| Explicit normalized expression `K+U(q)-U(0)+Uctrl(q)` | `0` | Yes, for this definition |
| Normalized expression plus arbitrary constant `beta` | `beta` | Exactly when `beta<=1` |

The normalized row is a mathematical alternative with a proof attempt, not
an identification of the existing active candidate. Subtracting an energy
constant preserves derivative identities but changes a sublevel set at a
fixed threshold. It cannot silently repair `V<=1`, its initial budget, or
its positivity/coercivity claims.

## Source chain and mismatch

All external paths below are relative to
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

- `routeB_compact_block_energy_barrier_audit.py:18,50,54,92` loads
  `routeB_compact_energy_storage_to_block_audit.csv`, sets `V_BAR=1`, reads
  `initial_storage_upper`, and labels its domain as full physical energy
  `V<=1`. This scalar-budget script does not evaluate a concrete `V(q,v)`.
- `routeB_compact_energy_storage_to_block_audit.py:4,17,51,75,78,101`
  explicitly describes targeted-gain `V_eps`, uses cross coefficient
  `epsilon=1/1000`, and supplies the block-only initial bound
  `492033745203/25600000000000`. Remote initial coordinates are fixed zero.
  It does not prove that bound for an arbitrary full physical storage.
- `routeB_compact_targeted_gain_energy_audit.jl:7-10,16` identifies a
  design-only change `Delta K=(0,6,2,0,0,0)`. The corresponding positivity
  report explicitly says it does not change the active controller.
- `routeB_compact_energy_power_rewrite_audit.jl:102-109` fixes
  `A0=762237/200000`, `A=242307/200000`, `B=20601/400000` and
  `Ugrav=A0*c2+A*(c2*c3-s2*s3)+B*(c2*c3-s2*s3)*c5
  -B*(s2*c3+c2*s3)*c4*s5`. At the origin this is `A0+A+B`, not zero.
  The file describes the potential's additive constant as omitted.
- `routeB_compact_closed_loop_energy_audit.jl:16-19` adds the controller
  potential and records a gravity/controller shift. Its CSV records zero
  controller shift and `205029/40000` total shift.
- The regenerated DH audit independently writes the same gravity
  polynomial at `routeB_compact_dh_gain_descriptor_regeneration_audit.jl:51-57`.
  `routeB_compact_dh_full_energy_supply_split_audit.jl:19-21` defines
  `Vfull_DH=Kfull_DH+Ugrav_DH+Uctrl_DH`;
  `routeB_compact_dh_storage_shift_audit.jl` explicitly adds the gravity
  and controller constants. These formulas do not have value zero at origin.

This is an identified storage-binding gap. It is not a global declaration
that every artifact or every energy approach is invalid. In particular,
the current inspection cannot choose which normalization the active
candidate intends simply from the word `V`.

## Exact calculations and their verification boundary

At zero velocity, every kinetic quadratic term vanishes, irrespective of
the entries or definiteness of `M(0)`. At zero configuration, the quadratic
and linear controller potentials also vanish for arbitrary coefficients.
Consequently the Fourier origin computations require only the displayed
rational gravity coefficients and exact `sin(0)=0`, `cos(0)=1`.

A focused Python `Fraction` calculation also composed the six DH transforms
at zero, using exact quarter-turn sine/cosine values and the literal
`dhport_lib.jl` rationalized parameters. Frame-origin heights were

```text
0, 1/10, 31/100, 31/100, 1/2, 1/2, 57/100.
```

Their midpoint heights are
`(1/20,41/200,31/100,81/200,1/2,107/200)`. Multiplication by the six masses
and `981/100` gives `3108789/400000`. The difference from the Fourier
polynomial's origin value is `10791/4000`. This is an **origin-only**
calculation: it does not prove that the two potential functions differ by
this constant globally. A derivative identity alone would still require
domain/connectedness and normalization evidence to establish that claim.

The leaf includes the rational COM-height ledger and its finite-sum proof
attempt; it does not assert a compiled binding of that ledger to
`sourceContract` origins or to Julia Float64 evaluation. No rounding claim
is made. No old Julia scripts were executed; several of them write output
files when included, so inspection remained textual.

## Typed witnesses and BODY6 composition

`normalized_origin_attempt` proves the algebraic value zero for the
explicit normalized definition. `offset_origin_admissible_iff_attempt`
isolates the additive-constant condition. The raw and shifted origin lemmas
give exact rational values and reject the **specified lifted origin**.

The active lifted predicate is `V(q,v)<=1` together with circle equations.
The canonical witness is `(q,v,cosine,sine)=(0,0,1,0)`, not the all-zero
lift. The actual Fourier exporter has four active pairs, for joints 2-5;
the imported six-pair witness restricts to these four. The configuration
projection existentially quantifies velocity and lift coordinates. Rejection
of the particular lifted origin is therefore not asserted as rejection of
every point with `q=0`; that stronger conclusion would need additional
energy information such as kinetic nonnegativity.

`bound_active_origin_attempt` transfers the normalized witness only after
receiving the pointwise equality
`V(0,0)=normalizedEnergy(M,U,kp,linear)(0,0)`.
`bound_active_body6_obstruction_attempt` then composes it with
`activeQDomain V subset D`, `Body6RAtZeroBinding R`, and
`CenterOffsetTarget`. The prior leaf supplies the physical-weight proof
attempt. Its conclusion is the conditional impossibility of positive
`UniformMargin D R mu` for the **unregularized BODY6 remainder** only.

No equality or inclusion between active `V<=1` and delivery
`p_B<=28/5` is introduced. No full regularized M/C/G Schur complement is
identified with the body-only 3-by-3 remainder. No positivity, invariance,
coverage or controller conclusion follows from normalization alone.

## Minimal remaining binding

For the origin step alone, supply the actual typed `V`, its configuration
and velocity/lift map, and either its exact origin value `<=1` or an
origin-preserving equality to an explicit normalized expression. A global
storage equality is sufficient but stronger than needed for this point.

For the candidate/domain transfer, supply `0 in D` directly or the stated
projection inclusion, including any additional restrictions. For the BODY6
contradiction, additionally supply the exact `R(0)` source equality and
center geometry. Full C/G bindings are not needed for this algebraic step.

For the broader active barrier, separately bind its initial upper bound,
coercivity/energy inequality and threshold to **the same** storage, gains,
constant, cross term and initial set. Those fields cannot be repaired by
reusing the targeted `V_eps` scalar as if its storage identity were proved.

## Provenance and static checks

| Inspected source | SHA-256 |
| --- | --- |
| `routeB_compact_block_energy_barrier_audit.py` | `62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927` |
| `routeB_compact_energy_storage_to_block_audit.py` | `80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9` |
| `routeB_compact_closed_loop_energy_audit.jl` | `9631e727a76ea32651ba7ca8e175e632d1ded6cda98bba2fd81e33d24f959c09` |
| `routeB_compact_energy_power_rewrite_audit.jl` | `7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf` |
| `routeB_compact_dh_gain_descriptor_regeneration_audit.jl` | `04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9` |
| `routeB_compact_dh_full_energy_supply_split_audit.jl` | `d6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632` |
| `routeB_compact_dh_storage_shift_audit.jl` | `aa3957f714f86c631a55fb8e7cc190fc98918a9cc04d148adcd7a28141cb9fec` |
| `dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |

The new Lean leaf has 135 lines and no `sorry`, `admit` or `axiom` tokens.
Its source and arithmetic were inspected; it has not been elaborated or
kernel-checked, including its imported dependency chain.
SHA-256: `c8b1dabcd19491495ee5ff39bff4337851c2224d6f938848988b279246a4f883`.

Final status: **OPEN_UNCOMPILED**. A conditional normalized-origin witness
and minimal BODY6 composition are present. The actual active candidate's
origin membership remains open because its storage identity/constant is
not bound; the explicitly inspected raw/shifted formulas do not provide it.
