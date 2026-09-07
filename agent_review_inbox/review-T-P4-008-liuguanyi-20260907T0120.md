---
kind: review_result
review_id: review-T-P4-008-liuguanyi-20260907T0120
task_id: T-P4-008
source_agent: 柳冠一
claimed_at: 2026-09-07T01:15:00-06:00
created_at: 2026-09-07T01:20:00-06:00
inspected_commit: b6d36869320feb913a9180cf4f91fe4949a6b43e
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: split_raw_pmi_kc_from_force_kc_and_add_remote_action_contract_before_P4_consumption
---

# T-P4-008 — typed `kc` normalization theorem and remote-`M_BD a_D` obstruction

## Question

The current P4 frontier needs a precise interface between three objects that must not be conflated:

1. the PMI polynomial coordinate `f_B`;
2. the generalized-force residual `l_F := I_B f_B - M0_BB a_B`;
3. the deployed full-state block dynamics, which contains the remote action `M_BD(q) a_D`.

This pass proves the exact algebraic bridge, fixes the sign/index of the `kc` contribution in `l_F`, and gives a countermodel showing that a local `(q4,q5,dq4,dq5,w)` adapter cannot absorb the remote action without an extra contract.

No provenance/admission/receipt claim and no P4/M4 closure is made.

## Inspected source boundary

At the inspected commit:

- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl`
  - blob `207b6b361eeb465aee8933cff8b9f41a1b17a89f`;
  - defines `Ival=[1,3/5,7/20,1/5,1/10,1/20]`, `kc=1/20`;
  - defines the block polynomial coordinates
    `f4=-(15/4)q4-4 dq4+(1/20)q5+w`,
    `f5=-(29/5)q5-(13/2)dq5+(1/20)q4+w`;
  - its PMI energy expressions explicitly use `Ival[ja]*f1` and `Ival[jb]*f2`.
- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`
  - blob `27cf497b6f27919eb5b554369fb1444f4314c942`;
  - defines the same `I_val`, and deployed
    `tau=-Kp*q-(Kd+b_fr)*dq+G0v+(gw_coef.*I_val)*w`,
    `a=M(q)\\(tau-Cdq-Gq)`;
  - deployed `tau` contains no `kc` term.
- `docs/routeb-c2-d-normalization-audit.md`
  - blob `8d16673467c8612764a6afef7a85a1b9b2ede781`;
  - explicitly defines `I_B=diag(1/5,1/10)` and
    `l_F=I_B f_B-M0_BB a_B`, and records the full block identity with `M_BD a_D`.
- `docs/routeb-p4-kc-force-contract.md`
  - blob `99e21a32b2acc7302e4f676098047a9e34ef12a3`;
  - currently calls `(q5/20,q4/20)` a generalized-force `rho_kc`. The calculation below shows that this is the raw PMI-`f` contribution; the `l_F` generalized-force contribution is its `I_B` image.

## 1. The two `kc` vectors are different typed objects

Let block order be `B=(4,5)` and define the swap map

```text
S(q4,q5) := (q5,q4).
```

The PMI source has

```text
kc = 1/20,
I_B = diag(1/5,1/10).
```

Hence the `kc` contribution inside the normalized polynomial coordinate `f_B` is

```text
rho_kc^f(q_B)
  := kc S(q_B)
   = (q5/20, q4/20).                                      (1)
```

But P4's force residual is defined after multiplication by `I_B`:

```text
l_F := I_B f_B - M0_BB a_B.
```

Therefore the `kc` contribution to this generalized-force residual is

```text
rho_kc^F(q_B)
  := I_B rho_kc^f(q_B)
   = (q5/100, q4/200).                                    (2)
```

The sign in `l_F` is **positive** under this residual convention, because `kc S(q_B)` enters `f_B` positively and the deployed `tau_B` has no `kc` term.

Thus `(q5/20,q4/20)` and `(q5/100,q4/200)` are not competing numerical approximations. They live on opposite sides of the normalization map:

```text
raw PMI f-coordinate       -- I_B -->       generalized force
(q5/20,q4/20)                             (q5/100,q4/200).   (3)
```

A theorem consuming `l_F` must use (2), unless it explicitly changes variables and carries the corresponding inverse normalization everywhere else.

### Exact equality obstruction

The difference between the raw and force vectors is

```text
rho_kc^f-rho_kc^F = (q5/25, 9 q4/200).                    (4)
```

For example, at `(q4,q5)=(0,1)` the difference is `(1/25,0) != 0`.
Hence no typed adapter may identify the two vectors globally.

This does not invalidate an abstract Schur theorem written in raw `f` coordinates. It means such a theorem needs an explicit normalization adapter before it is advertised as a theorem about `l_F` generalized force. Numerically using the larger raw coefficient does not repair the type/unit mismatch.

## 2. Exact deployed block residual identity

The PMI coefficients were built from

```text
a_i = (Kp_i+mgl_i)/I_i,
c_i = (Kd_i+bfr_i)/I_i,
gw_i = graw_i/I_i.
```

Consequently

```text
I_B f_B
 = -Kp_B q_B - mgl_B q_B - (Kd_B+bfr_B)v_B
   + graw_B w + rho_kc^F(q_B).                             (5)
```

The deployed controller has

```text
tau_B
 = -Kp_B q_B - (Kd_B+bfr_B)v_B + G0_B + graw_B w,         (6)
```

so subtracting gives the exact source-independent controller bridge

```text
I_B f_B - tau_B
 = -mgl_B q_B - G0_B + rho_kc^F(q_B).                     (7)
```

Now partition the deployed dynamics into local block `B=(4,5)` and distal block `D`:

```text
M_BB a_B + M_BD a_D + C_B + G_B = tau_B.                 (8)
```

Using `l_F=I_B f_B-M0_BB a_B`, equations (7)--(8) give

```text
l_F
 = (M_BB-M0_BB) a_B
   + M_BD a_D
   + C_B
   + (G_B-G0_B)
   - mgl_B q_B
   + rho_kc^F(q_B).                                      (9)
```

This fixes both disputed structural points:

- the remote term is `+ M_BD a_D`, not the stale-comment expression `(M-M0)_BD a_D`;
- the `kc` term in the force residual is `+(q5/100,q4/200)` for the current `l_F` convention.

If a future residual is defined with opposite sign, `M0_BB a_B-I_B f_B`, every term in (9) flips; the present task and normalization audit use `I_B f_B-M0_BB a_B`.

## 3. Remote-action obstruction: local P4 variables cannot determine `l_F`

The current PMI polynomial variables expose the block state `(q4,q5,dq4,dq5)`, time/ramp variables, and Schur auxiliaries, but they do not expose `a_D` as an independent typed input. Equation (9) shows why this matters.

A one-dimensional block/distal countermodel already suffices. Take

```text
I=1, M0=1, MBB=1, MBD=1,
f=0, tau=0,
C=G=G0=mgl=kc=0.
```

The full dynamics reduces to

```text
a_B + a_D = 0.
```

Case A: `a_D=0`, so `a_B=0` and `l_F=0`.

Case B: `a_D=1`, so `a_B=-1` and

```text
l_F = I f - M0 a_B = 1.                                  (10)
```

Both cases can have exactly the same local `(q_B,v_B,w)=(0,0,0)`. Therefore no function of local `(q_B,v_B,w)` alone can equal `l_F` for all full-state solutions unless an additional contract determines/bounds the remote action.

The obstruction is even sharper for a local Schur envelope whose right-hand side vanishes with a local coordinate such as `y=q_cross`: in Case B, set `q_B=0`, hence `kc=0` and `y=0`, while `l_F=1`. Any proposed universal bound of the form

```text
|l_F|^2 <= K y^2                                          (11)
```

fails immediately (`1 <= 0`). Thus proving the `y <-> q_cross` adapter from `T-P4-011` is necessary for its own `kc` lane but is **not sufficient** to source-bind the complete P4 residual; the remote action remains an independent obligation.

## 4. Minimal bridge theorem package

The mathematically smallest useful decomposition is:

### A. `kc_normalization_bridge`

```text
I_B = diag(1/5,1/10), kc=1/20,
S(q4,q5)=(q5,q4)
-------------------------------------------------
I_B (kc S(q_B)) = (q5/100,q4/200).
```

Lean-friendly specialization:

```lean
theorem kc_force_normalization (q4 q5 : ℝ) :
  ((1/5 : ℝ) * ((1/20 : ℝ) * q5),
   (1/10 : ℝ) * ((1/20 : ℝ) * q4))
  = (q5/100, q4/200)
```

or preferably with a typed `Fin 2 -> ℝ` diagonal linear map so the raw/force spaces are distinct definitions.

### B. `block_force_residual_decomposition`

For compatible block vectors/matrices satisfying (8),

```text
l_F := I_B f_B-M0_BB a_B,
I_B f_B-tau_B := r_controller,
-------------------------------------------------
l_F = r_controller
      +(M_BB-M0_BB)a_B+M_BD a_D+C_B+G_B.           (12)
```

Then specialize `r_controller` using (7) to obtain (9). This separation is useful because future FD/analytic gravity conventions can change without touching the block algebra.

### C. `local_adapter_remote_counterexample`

A scalar theorem should encode the two cases above and conclude that a local-state-only residual map cannot represent every full-state residual when `MBD*aD` is unconstrained.

No topology, solver, interval, or source hash is needed for these three lemmas.

## 5. Consequence for the current P4 frontier

The current frontier should keep two separate adapter obligations:

```text
K1: normalized-PMI -> generalized-force map
    rho_kc^f  |->  rho_kc^F = I_B rho_kc^f;

K2: full-state remote action
    M_BD(q) a_D is either explicitly represented or bounded on the same domain.
```

Only after K1 and K2 are available does it make sense to ask whether the remaining terms in (9) fit the `c=1/4` sharp Schur budget.

In particular, the current statement in `docs/routeb-p4-kc-force-contract.md` that calls `(q5/20,q4/20)` a generalized-force contribution is incompatible with the separately frozen definition `l_F=I_B f_B-M0_BB a_B`. The fail-closed repair is not to choose one coefficient by convention; it is to name both typed quantities as in (1)--(3), then make downstream consumers state which one they use.

This also sharpens the status of `T-P4-011`: its mathematics for the raw vector `(q5/20,q4/20)` remains a valid source-independent inequality result, but it cannot by itself be consumed as the `l_F` force-coordinate `kc` cost without an explicit normalization theorem. Under the actual `I_B` map, the force-coordinate `kc` amplitudes are smaller by factors `1/5` and `1/10` respectively, but this numerical fact does not erase the type distinction.

## Remaining blockers

- Bind the full deployed `M_BD(q)a_D` term on the same P4/P8 covered domain, or enlarge the P4 theorem state to expose an explicit remote-action slack.
- Decide whether the P4 Schur auxiliary `y` lives in raw normalized-`f` coordinates or generalized-force coordinates; then apply the corresponding `I_B` transform consistently to `p,d,r`.
- Source-bind/estimate the other terms in (9): `(M_BB-M0_BB)a_B`, central-FD `C_B`, gravity/reference mismatch, and any Float64 solve defect introduced by an execution-level theorem.
- Keep force residual `l_F` distinct from any acceleration residual until a positive mass/inverse-mass conversion theorem is supplied.

## Recommended next step

Before further constant tuning, add the two typed spaces and the diagonal normalization map to the P4 interface. Then require the source lane to provide either a bound

```text
||M_BD(q)a_D|| <= R_remote(q_B,v_B,w,...)
```

on the same covered domain, or a larger state contract that carries `a_D`. If neither is available, the countermodel above rules out a complete local P4 residual theorem regardless of how favorable the `kc` Schur constants are.

Admission remains `pending`; this result is a mathematical/interface correction only, awaiting 梁智炜 integration and any later Lean formalization/独立验证.
