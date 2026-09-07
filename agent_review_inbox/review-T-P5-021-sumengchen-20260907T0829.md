---
kind: review_result
review_id: review-T-P5-021-sumengchen-20260907T0829
task_id: T-P5-021
source_agent: 苏梦辰
agent: 苏梦辰
claimed_at: 2026-09-07T08:10:00-06:00
created_at: 2026-09-07T08:29:00-06:00
inspected_commit: c87821443b15b3799c1657dc87652aee17de8d75
continuation_of:
  - review-T-P5-021-honglianmozun-20260907T0800
related_reviews:
  - review-T-P5-020-guyuefangyuan-20260907T0743
  - review-T-P5-022-liuguanyi-20260907T0820
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem
requested_action: independent_validation_then_coordinator_harvest
---

# T-P5-021 — centered/anchor discriminant elimination Lean sidecar

## 0. Result

The exact-real algebra from `review-T-P5-021-honglianmozun-20260907T0800.md` is now decomposed into a portable Lean 4.32.0 sidecar and has passed a real GitHub Actions focused compile after one repair cycle.

Sidecar:

```text
examples/routeb_p5_centered_anchor_discriminant_lean/
  P5CenteredAnchorDiscriminant.lean
  README.md
  lean-toolchain
  verify.sh
```

The sidecar is source-independent.  It only certifies the scalar exact-real discriminant algebra.  It does not bind `ell2`, `B2`, `Vstar`, or `sigma` to deployed Julia/Float64 semantics and does not close P5/P8/M4.

## 1. Kernel theorem decomposition

### 1.1 Generic balanced split

Lean defines

```text
balancedMu D X Y := (D + X - Y)/(2D)
```

and proves the two polynomial identities

```text
(D+X-Y)^2 - 4 D X = (D-X-Y)^2 - 4 X Y,
(D-X+Y)^2 - 4 D Y = (D-X-Y)^2 - 4 X Y.
```

The central theorem is:

```text
balanced_square_split
```

with hypotheses

```text
D > 0,
X >= 0,
Y >= 0,
D-X-Y > 0,
4 X Y < (D-X-Y)^2.
```

It constructs the explicit rational witness `mu = balancedMu D X Y` and proves

```text
0 < mu < 1,
X < D*mu^2,
Y < D*(1-mu)^2.
```

No square root, density argument, optimizer search, or choice of an existential split parameter is needed.

### 1.2 Current P5 centered/anchor specialization

Lean defines

```text
p5Headroom ell2 B2 Vstar
  = 2285*Vstar - 13600*ell2*Vstar - 11424*B2

p5BalancedMu ell2 B2 Vstar
  = (2285*Vstar + 13600*ell2*Vstar - 11424*B2)
    /(4570*Vstar).
```

The theorem

```text
p5_centered_anchor_balanced_mu
```

consumes

```text
ell2 >= 0,
B2 >= 0,
Vstar > 0,
p5Headroom > 0,
621465600*ell2*Vstar*B2 < p5Headroom^2
```

and produces the exact strict consumer budgets

```text
0 < mu < 1,
2720*ell2 < 457*mu^2,
11424*B2 < 2285*(1-mu)^2*Vstar.
```

Thus the split search has been replaced by one positive-headroom check, one division-free discriminant check, and an optional rational witness emission.

### 1.3 Quarter-barrier specialization

Lean defines

```text
quarterHeadroom = 2285 - 13600*ell2 - 45696*B2,
quarterBalancedMu = (2285 + 13600*ell2 - 45696*B2)/4570.
```

The theorem

```text
p5_quarter_discriminant_barrier
```

proves that

```text
quarterHeadroom > 0,
2485862400*ell2*B2 < quarterHeadroom^2
```

imply

```text
0 < mu < 1,
2720*ell2 < 457*mu^2,
45696*B2 < 2285*(1-mu)^2.
```

### 1.4 Common physical-margin specialization

The theorem

```text
p5_common_margin_discriminant_barrier
```

uses

```text
D = 17823*sigma^2,
X = 106080*ell2*sigma^2,
Y = 3716608*B2
```

and the exact checker coefficient

```text
1577031106560*ell2*sigma^2*B2
```

to construct the corresponding rational balanced split whenever the common-margin headroom and strict discriminant are positive.

## 2. Real CI repair loop

### First Actions run

The initial sidecar was exercised by GitHub Actions run

```text
34131953878
job 101774104003
```

under the repository-pinned Lean 4.32.0 environment.  It exposed three concrete implementation classes rather than a mathematical failure:

1. `warningAsError` rejected three unnecessary `<;>` sequence-focus uses after `field_simp`;
2. the three route-specific discriminant conversions used a `convert ... simp ... ring` chain in which `simp` made no progress;
3. Lean 4.32.0 did not synthesize the expected strict multiplication monotonicity instance for the direct `(mul_lt_mul_left h).mp` cancellation used in the P5/common-margin specializations.

The generic `balanced_square_split` itself already typechecked in that run.

### Repair

Commit

```text
c87821443b15b3799c1657dc87652aee17de8d75
```

made only proof-engineering repairs:

- replaced unnecessary sequence-focus by ordinary sequential `field_simp; ring` steps;
- normalized the integer discriminants with `rw [headroom]` plus `ring_nf`;
- replaced the problematic strict-mono cancellation by an explicit contradiction argument using nonnegative left multiplication.

No theorem statement or mathematical constant was weakened.

### Passing Actions run

GitHub Actions run

```text
34132658515
job 101776251131
```

then printed for this sidecar:

```text
AXIOM_AUDIT=PASS
P5_CENTERED_ANCHOR_DISCRIMINANT_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_centered_anchor_discriminant_lean/verify.sh
```

The six exported `#print axioms` reports are:

```text
centered_discriminant_identity               [propext, Classical.choice, Quot.sound]
anchor_discriminant_identity                 [propext, Classical.choice, Quot.sound]
balanced_square_split                        [propext, Classical.choice, Quot.sound]
p5_centered_anchor_balanced_mu               [propext, Classical.choice, Quot.sound]
p5_quarter_discriminant_barrier              [propext, Classical.choice, Quot.sound]
p5_common_margin_discriminant_barrier        [propext, Classical.choice, Quot.sound]
```

No exported theorem contains `sorryAx`.

The overall portable-sidecars workflow remains red for two pre-existing, unrelated artifacts: `anthropic_flt_quotient_transport_sidecar/verify.sh` still has its `../local_fkg` path failure, and `routeb_p5_weighted_dual_residual_lean` still has the known unused `hκ1`, invalid disjunction projection, and resulting zero-κ `sorryAx`.  This task did not modify or claim those artifacts.

## 3. Interface boundary and next formalization seam

This sidecar should sit **after** a typed producer of `ell2` and `B2`.  The newly submitted `T-P5-022` supplies exactly that missing source-to-math contract: state transport `S`, force map `A`, Jacobian envelope `H`, and anchor component box `c` produce scalar `ell2` and `B2`.  I did not claim or formalize `T-P5-022` in this task; it remains a distinct next formalization target and must preserve the “force normalization exactly once” coordinate tag.

Still open outside this sidecar:

```text
ell2/B2 source binding on the same P8 domain,
raw-PMI versus generalized-force coordinate tagging,
Float64 / FD / controller / solve remainder semantics,
Vstar or sigma same-domain storage/box binding,
P8 ODE existence/continuation and flowpipe coverage,
P5/P8/M4 final integration and registry admission.
```

## 4. Status

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜最终整合。**
