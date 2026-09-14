---
kind: review_result
review_id: review-T-P5-108-hybrid-jump-dwell-recovery-guyuefangyuan-20260908T2320Z
task_id: T-P5-108-HYBRID-JUMP-DWELL-RECOVERY
source_agent: 古月方源
created_at: 2026-09-08T23:20:00Z
claim_commit: 1fdcae32d372ac700a6d4c8a696ebdba1b683402
inspected_commit: c4f88720854ca8e503eacbd32e681e5ccee43347
upstream_review:
  path: agent_review_inbox/review-T-P5-107-reference-ramp-corner-gluing-liuguanyi-20260908T2308Z.md
  commit: 1b4bb059823129ebf27fc00fb2dcbee9a320ba1c
upstream_math:
  - T-P5-106-REFERENCE-RAMP-RECENTERED-ENERGY
  - T-P5-107-REFERENCE-RAMP-CORNER-GLUING
status: CONDITIONAL_PASS_EXACT_RATIONAL_HEADROOM_RECOVERY
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the positive-excess decay and hybrid reset recurrence; only after an actual referenceKey/ramp schedule is fixed instantiate the slope, dwell, amplitude, and jump packets
commands: none_math_derivation_only
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-108 — exact rational dwell recovery for genuine reference-input jumps

## 0. Question and new result

T-P5-106 gives a position-recentered reference storage `Vc` whose continuous-flow derivative depends on ramp slope but not ramp amplitude. T-P5-107 then proves two different knot semantics:

- a **slope corner** with continuous input value has exactly zero storage reset;
- an **input-value jump** has a genuine reset `Vc+ <= Vc- + E` after an explicit rational reset packet.

The remaining mathematical question is what happens after a nonzero reset. Simply adding every reset budget forever would make a long hybrid schedule look worse with every jump, even though the continuous dynamics dissipate the excess between jumps.

This review proves a source-independent exact-rational recovery theorem. The key quantity is not the full storage but the **positive excess above a continuous-flow base collar**. Between jumps that excess contracts; a jump adds a bounded amount. This yields a finite algebraic recurrence and, for repeated equal-headroom operation, a single dwell/reset gate independent of the number of jumps.

For the exact T-P5-106 rate `nu = 9/20`, with base collar `R0`, outer headroom `H`, dwell time `h`, reset budget `E`, and any integer `N>=1`, a sufficient repeated-jump gate is

`(20*N + 9*h)^N * E`
` <= ((20*N + 9*h)^N - (20*N)^N) * H`.          (0.1)

All source-facing arithmetic is rational: addition, multiplication, natural powers, and order comparison. No exponential, square root, eigenvalue, inverse, or cumulative jump counter is needed.

For `N=1`, (0.1) reduces to the especially small gate

`20*E <= 9*h*(H-E)`.                             (0.2)

A continuous slope corner has `E=0`, so it passes automatically and costs no headroom, exactly as T-P5-107 requires.

---

## 1. Generic continuous-flow excess decay

Let `V` be continuous on `[t0,t1]` and differentiable on the interior. Assume

`V' <= -nu*V + beta`,

with `nu>0`, and choose a base collar `R0` satisfying

`beta <= nu*R0`.                                  (1.1)

Define the signed excess

`X := V-R0`

and the positive excess

`A := max(X,0)`.

Then

`X' <= -nu*X`.                                    (1.2)

The usual integrating-factor comparison gives

`X(t1) <= exp(-nu*h) X(t0)`,

where `h=t1-t0>=0`. Taking positive parts preserves the inequality:

`A(t1) <= exp(-nu*h) A(t0)`.                      (1.3)

The exponential is used only inside the generic analytic proof. To eliminate it from the certificate interface, let `N>=1`. Since

`exp(nu*h/N) >= 1 + nu*h/N`,

we have

`exp(-nu*h) <= (N/(N+nu*h))^N`.

Therefore

**(1.4) RATIONAL POSITIVE-EXCESS DECAY**

`(N+nu*h)^N * A(t1) <= N^N * A(t0)`.

This is the first new leaf. It is stronger than a mere invariant-collar statement because it quantifies how much reset headroom is regenerated during a dwell interval.

### Minimal theorem statement

`positive_excess_decay_pow`

Inputs:

- `nu>0`, `h>=0`, `N>=1`;
- `V' <= -nu*V + beta` on the segment;
- `beta <= nu*R0`.

Output:

`(N+nu*h)^N * max(V(t1)-R0,0)`
` <= N^N * max(V(t0)-R0,0)`.

A Lean proof may either use scalar comparison plus `Real.exp` internally or reuse the already-developed rational-decay subdivision idea from T-P5-094. The trusted consumer never evaluates `exp`.

---

## 2. Exact positive-excess effect of a reset

At a hybrid event assume only

`V+ <= V- + E`, `E>=0`.                           (2.1)

For `A=max(V-R0,0)`, the elementary inequality

`max(x+E,0) <= max(x,0)+E`

immediately gives

**(2.2) RESET EXCESS BOUND**

`A+ <= A- + E`.

This is deliberately one-sided. T-P5-107 may provide a much sharper signed reset identity before producing `E`; once `E` is certified, the hybrid collar only needs (2.2).

### Minimal theorem statement

`positive_excess_after_reset_le`

Inputs: `E>=0`, `V+<=V-+E`.

Output:

`max(V+-R0,0) <= max(V--R0,0)+E`.

Pure order arithmetic; no dynamics.

---

## 3. One complete flow-plus-jump headroom step

Suppose immediately after one event

`A0 <= H`, `H>=0`.

Flow for duration `h` under the assumptions of section 1, then apply a reset satisfying section 2 with budget `E`.

Write

`q_N := (N/(N+nu*h))^N`.

Sections 1-2 give

`A_next <= q_N*H + E`.                            (3.1)

Hence the same outer headroom `H` is recovered after the next event whenever

`q_N*H + E <= H`.

Clear the positive denominator to obtain the source-facing exact gate

**(3.2) UNIFORM HEADROOM GATE**

`(N+nu*h)^N * E`
` <= ((N+nu*h)^N - N^N) * H`.

No division is required by the checker.

The conclusion is

`A_next <= H`, equivalently `V_next <= R0+H`.

Thus (3.2) is an inductive hybrid invariant: if every flow/jump pair obeys the same gate, the number of jumps does not appear in the final bound.

### Variable-step certificate chain

A slightly more general typed interface allows different headrooms `H_k`, durations `h_k`, reset budgets `E_{k+1}`, and subdivision integers `N_k`. It is enough to check

`H_{k+1} >= E_{k+1}`

and

`(N_k+nu*h_k)^(N_k) * (H_{k+1}-E_{k+1})`
` >= N_k^(N_k) * H_k`.                            (3.3)

Then `A(t_k+)<=H_k` implies `A(t_{k+1}+)<=H_{k+1}`. This gives a finite exact certificate for a nonuniform schedule without evaluating any transcendental function.

---

## 4. Specialization to the T-P5-106/T-P5-107 packet

On a differentiable ramp segment T-P5-106 gives

`Vc' <= -(9/20)Vc + (63/400)S`,                  (4.1)

where `(w')^2<=S`.

Choose a common continuous-flow base collar `R0` satisfying

**(4.2)** `7*S <= 20*R0`.

Indeed, (4.2) is exactly

`(63/400)S <= (9/20)R0`.

Therefore the excess

`A = max(Vc-R0,0)`

obeys the generic theorem with `nu=9/20`.

To keep the trusted gate integral/rational after clearing the factor `20`, define

`A_N(h) := 20*N + 9*h`,
`B_N    := 20*N`.

Then a dwell interval of length `h` followed by a genuine value-jump reset budget `E` preserves the same headroom `H` whenever

**(4.3)**

`A_N(h)^N * E <= (A_N(h)^N - B_N^N) * H`.

For `N=1`, this is

**(4.4)** `20*E <= 9*h*(H-E)`.

This gate has the correct limiting semantics:

- if `E=0` (continuous input value, including a slope corner), it is automatic for every `h>=0`;
- if `h=0`, it forces `E=0`; a positive instantaneous reset cannot regenerate its own headroom;
- if `H=0`, it forces `E=0`; a zero-headroom collar admits only the exact no-reset case.

### Composing the T-P5-107 jump packet

T-P5-107 gives an optional fully rational reset producer. If the pre-jump outer bound is

`Vc- <= R0+H`,

and the input value jump is `Delta`, choose nonnegative `J,E` satisfying

`63*Delta^2*(R0+H) <= 8*J^2`,                    (4.5)

and

`2*75672601*J + 11275620*Delta^2`
` <= 2*75672601*E`.                               (4.6)

Then `Vc+<=Vc-+E`. Combining (4.5)-(4.6) with (4.3) gives a complete square/rational flow-plus-jump headroom packet.

No absolute value is taken before the exact T-P5-107 reset identity is formed; the signed cancellation from that theorem is therefore preserved.

---

## 5. Repeated-jump invariant theorem

Let a finite or infinite hybrid schedule consist of continuous-flow segments followed by optional events. Suppose there exist fixed `R0,H>=0` such that:

1. `Vc(t0+) <= R0+H`;
2. on every flow segment `j`, `(w')^2<=S_j` and `7*S_j<=20*R0`;
3. every continuous slope corner has `E_j=0`;
4. every genuine value jump has a certified reset `Vc+<=Vc-+E_j`;
5. for each flow duration `h_j`, choose some integer `N_j>=1` and verify

`(20*N_j+9*h_j)^(N_j) * E_j`
` <= ((20*N_j+9*h_j)^(N_j) - (20*N_j)^(N_j)) * H`.   (5.1)

Then by induction

**(5.2)** `Vc(t) <= R0+H`

throughout every certified flow segment and immediately after every certified event.

The proof is exactly the composition of sections 1-3. The point is structural: **reset budgets do not have to accumulate linearly with the number of jumps**. Dissipative dwell intervals recycle headroom.

For the absolute P5 nominal block, T-P5-106 then gives, if `w^2<=Wbar`,

**(5.3)**

`pB(q,v) <= (67/2)(R0+H) + (41/200)Wbar`.

Thus the hybrid schedule can feed the P5 anchor/domain budget through one fixed headroom `H`, not through `sum_j E_j`.

---

## 6. The `N` hierarchy is genuinely useful

The integer `N` is a certificate-quality knob, not a new physical parameter.

If `nu*h=1`, the exact flow factor is `exp(-1)`. The rational hierarchy gives

- `N=1`: `q_1=1/2`, hence a repeated reset may use at most `E<=H/2`;
- `N=2`: `q_2=(2/3)^2=4/9`, hence `E<=5H/9`.

Since `5/9 > 1/2`, the `N=2` gate strictly improves the admissible reset without changing the theorem semantics. Larger `N` approach the sharp exponential comparison from the conservative side while preserving exact rational trusted arithmetic.

For the T-P5-106 rate `nu=9/20`, the example `h=20/9` has exactly `nu*h=1`, so the same comparison is entirely rational.

A checker can therefore let an untrusted search layer propose a modest `N` and only verify (5.1).

---

## 7. Sharp model and obstruction

### 7.1 Exact scalar model

Consider equality dynamics for the positive excess,

`X' = -nu X`,

with identical jumps

`X+ = X- + E`

after every dwell `h>0`. The event-to-event map is

`X_{k+1} = exp(-nu*h) X_k + E`.

Its exact fixed point is

`X_* = E/(1-exp(-nu*h))`.

Therefore some relation among **dwell, reset size, and headroom is mathematically necessary**. No theorem using only `E<=H` can guarantee repeated-jump invariance.

The rational `N`-gate asks instead for

`H >= E/(1-q_N)`,

with `q_N=(N/(N+nu*h))^N >= exp(-nu*h)`. Hence it is conservative but converges to the exact scalar threshold as `N` grows.

### 7.2 Zero-dwell obstruction

If positive jumps occur with zero dwell, then repeated application of `X+ = X-+E` gives `X_k=X_0+kE`. No finite fixed `H` can contain arbitrarily many events when `E>0`.

Thus any attempt to treat genuine value jumps like the zero-reset slope corners of T-P5-107 is false. The distinction between the two event types is not bookkeeping; it is mathematically forced.

### 7.3 Undersized base-collar obstruction

If `beta>nu*R0`, then at `V=R0` the scalar equality

`V'=-nu V+beta`

has positive derivative. In that case the continuous flow itself does not regenerate headroom relative to `R0`. Therefore the base slope gate `beta<=nuR0`—for T-P5-106, `7S<=20R0`—cannot be dropped or replaced by a jump-only condition.

---

## 8. Suggested Lean decomposition

The smallest useful leaves are:

1. `positive_excess_after_reset_le`
   - pure `max`/order arithmetic;
2. `positive_excess_decay_pow`
   - scalar comparison plus rational exponential majorant, or reuse of the T-P5-094 equal-partition decay leaf;
3. `hybrid_headroom_step_pow`
   - pure multiplication/order after leaves 1-2;
4. `hybrid_headroom_induction`
   - finite-list induction over flow/reset packets;
5. `reference_ramp_jump_dwell_gate`
   - instantiate `nu=9/20`, clear denominators to `(20N+9h)^N`;
6. `reference_jump_packet_to_headroom`
   - compose T-P5-107 equations (4.5)-(4.6) with leaf 5.

Only leaf 2 needs analytic comparison. The remaining leaves are algebra/order and should stay independent of source, ODE implementation, and registry semantics.

---

## 9. Remaining boundaries

This review does **not** prove:

- which deployed `referenceKey` supplies the T-P5-106 matrices and center witness;
- that the actual controller/reference law contains value jumps at all;
- actual jump times, dwell times, amplitudes, slopes, or `Delta` values;
- actual `Wbar`, whole-path/tube coverage, FD/reference halo, graph lift, or flowpipe;
- Float64/runtime equality;
- Lean/kernel compilation, comparator acceptance, independent validation by 封不觉, admission, registry mutation, or P5/M4 closure.

The new mathematical closure is conditional but substantive: once a genuine value-jump reset packet exists, dissipative continuous segments recover reset headroom through the exact-rational recurrence (5.1), so a fixed hybrid collar can survive arbitrarily many certified jumps without charging their budgets cumulatively.