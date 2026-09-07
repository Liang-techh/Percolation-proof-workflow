---
kind: review_result
review_id: review-T-P5-026-guyuefangyuan-20260907T1031
task_id: T-P5-026
source_agent: 古月方源
agent: 古月方源
claimed_at: 2026-09-07T10:19:00-06:00
created_at: 2026-09-07T10:31:00-06:00
inspected_commit: e01810e282b824c3c2ab0e99352989750f44381d
continuation_of:
  - review-T-P5-025-liuguanyi-20260907T1020
  - review-T-P5-024-kuangmanmozun-20260907T0945
  - review-T-P5-020-guyuefangyuan-20260907T0743
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_feasible_cone_reduction_and_optional_spn_certificate_consumer_for_K_path_before_fallback_scalar_collapse
---

# T-P5-026 — exact feasible-cone reduction and SPN certificate for the direct `K_path` small-gain route

## 0. Result in one sentence

`T-P5-025` already removes the Frobenius collapse of the transported component matrix `K_path`, but it still checks every formal sign pair and asks the corresponding quadratic matrix to be globally PSD.  Both requirements are stronger than the mathematics needs.  For block-(4,5), the absolute-value geometry has an **exact 18-cone reduction up to global sign reversal**, and on each cone the required matrix only needs to be nonnegative on the nonnegative orthant.  A rational **PSD + entrywise-nonnegative (SPN)** decomposition is therefore a strictly weaker checker-friendly sufficient certificate than global PSD.

This is source-independent mathematics.  It does not certify a concrete `K_path`, Julia/Float64 Jacobian, P8 cell chain, flowpipe coverage, provenance, P5/P8/M4 closure, or registry admission.

---

## 1. Starting point from T-P5-025

Use the same state ordering

```text
z = (x4, x5, y4, y5)^T in R^4,
```

and

```text
L z = (x4 + y4, x5 + y5)^T,

L = [1 0 1 0
     0 1 0 1].
```

The exact block dissipation is

```text
Q(z) = z^T P z,
```

with the already-frozen rational matrix

```text
P =
[ 3/4      -3/400       0          1/800      ]
[-3/400     29/50      -1/800      0          ]
[ 0        -1/800       2049997/3000000  0    ]
[ 1/800     0           0          2399261/4000000 ].
```

Let the centered force residual be `r=(r4,r5)^T`.  The typed component envelope is

```text
|r_a| <= sum_k K[a,k] |z_k|,            a=1,2,          (1)
```

for a nonnegative `2 x 4` matrix `K`.

Exactly as in `T-P5-025`, triangle inequality gives

```text
|(Lz)^T r| <= |Lz|^T K |z|.                              (2)
```

So the only remaining mathematical problem is to certify

```text
|Lz|^T K |z| <= mu Q(z)                                  (3)
```

for all `z`.

`T-P5-025` fixes signs of `z` and `Lz`, symmetrizes the resulting quadratic form, and asks `mu P - B_{sigma,tau}` to be globally PSD.  The present child keeps the same exact identity but uses the fact that `tau` is not independent of `sigma`: it is the sign of the relevant sum `x+y`.

---

## 2. One-channel sign geometry has six feasible cones, not eight sign triples

Consider one channel with real coordinates `(x,y)` and sum

```text
s = x+y.
```

Ignoring zero-boundary nonuniqueness, a formal sign triple is

```text
(sign x, sign y, sign s) in {+,-}^3.
```

The triples

```text
(+,+,-)
(-,-,+)
```

are impossible.  The remaining six triples are feasible, and every `(x,y)` belongs to at least one of the following six closed cones.

Introduce `a,b >= 0`.  Define six integer parametrizations:

```text
C1: (++,+)    (x,y) = ( a,       b      )
                 G1 = [ 1  0
                        0  1 ]

C2: (--,-)    (x,y) = (-a,      -b      )
                 G2 = [-1  0
                        0 -1 ]

C3: (+-,+)    (x,y) = ( a+b,    -a      )
                 G3 = [ 1  1
                       -1  0 ]

C4: (+-,-)    (x,y) = ( a,      -a-b    )
                 G4 = [ 1  0
                       -1 -1 ]

C5: (-+,+)    (x,y) = (-a,       a+b    )
                 G5 = [-1  0
                        1  1 ]

C6: (-+,-)    (x,y) = (-a-b,     a      )
                 G6 = [-1 -1
                        1  0 ].
```

The corresponding sums are

```text
C1:  a+b >= 0
C2: -a-b <= 0
C3:  b   >= 0
C4: -b   <= 0
C5:  b   >= 0
C6: -b   <= 0.
```

### Lemma 2.1 — exact one-channel cone cover

For every `(x,y) in R^2`, there exists `j in {1,...,6}` and `a,b >= 0` such that

```text
(x,y)^T = Gj (a,b)^T,                                  (4)
```

and the sign of `x+y` is the sign prescribed by cone `Cj`.

### Proof

There are only three cases.

1. `x,y` have the same weak sign.  Use `C1` with `(a,b)=(x,y)` when both are nonnegative, and `C2` with `(a,b)=(-x,-y)` when both are nonpositive.

2. `x>=0>=y`.  If `x+y>=0`, set

```text
a = -y,
b = x+y.
```

Then `a,b>=0` and `(x,y)=(a+b,-a)`, so `C3` applies.  If `x+y<=0`, set

```text
a = x,
b = -(x+y),
```

so `(x,y)=(a,-a-b)` and `C4` applies.

3. `x<=0<=y` is symmetric.  If `x+y>=0`, set `a=-x`, `b=x+y` and use `C5`; if `x+y<=0`, set `a=y`, `b=-(x+y)` and use `C6`.

Zero coordinates or zero sum can lie in more than one cone.  This overlap is harmless: the result is a cover, not a disjoint partition.  QED.

Every `Gj` is unimodular: `det Gj = +/-1`.  Thus the parametrizations are exact integer coordinate changes, with no denominator or square root.

---

## 3. Two channels give 36 feasible cones, then only 18 distinct certificates

The two physical channels are independent at the level of absolute-value sign geometry:

```text
channel 4: (x4,y4),
channel 5: (x5,y5).
```

Choose one cone index `j4 in {1,...,6}` for channel 4 and one `j5 in {1,...,6}` for channel 5.  Their product gives

```text
6 * 6 = 36                                              (5)
```

closed feasible cones covering all `R^4`.

For each pair `C=(j4,j5)`, interleave the two `2 x 2` maps into an integer `4 x 4` matrix `T_C` so that

```text
z = T_C u,

u = (a4,a5,b4,b5)^T >= 0                                (6)
```

(componentwise), with `(x4,y4)=Gj4(a4,b4)` and `(x5,y5)=Gj5(a5,b5)`.

Let `sigma_C in {+/-1}^4` be the fixed signs of the four `z` coordinates on cone `C`, and let `tau_C in {+/-1}^2` be the fixed signs of the two sums `Lz`.  On the entire cone,

```text
|z|  = D_sigma_C z,
|Lz| = D_tau_C Lz.                                      (7)
```

Global sign reversal pairs the cones:

```text
C1 <-> C2,
C3 <-> C6,
C4 <-> C5.                                              (8)
```

For the two-channel product, simultaneously reversing both channels sends

```text
T_C -> -T_C,
sigma_C -> -sigma_C,
tau_C -> -tau_C.                                        (9)
```

The sign-fixed quadratic matrix is unchanged because

```text
D_{-tau} K D_{-sigma}
= (-D_tau) K (-D_sigma)
= D_tau K D_sigma.                                      (10)
```

The congruence is also unchanged because `(-T_C)^T H (-T_C)=T_C^T H T_C`.

Therefore the 36 feasible cones form 18 global-sign pairs with **identical certificate matrices**.  A checker needs at most

```text
18 distinct cone certificates,                         (11)
```

not the 32 distinct all-sign matrices of `T-P5-025`.

This reduction is exact.  It does not throw away any state: it removes only sign combinations incompatible with `tau = sign(Lz)`.

---

## 4. Exact quadratic form on a feasible cone

For a feasible cone `C`, define

```text
A_C := L^T D_tau_C K D_sigma_C,

B_C := sym(A_C)
     = (A_C + A_C^T)/2.                                 (12)
```

Then on that cone,

```text
|Lz|^T K |z|
= (D_tau_C Lz)^T K (D_sigma_C z)
= z^T A_C z
= z^T B_C z.                                            (13)
```

For a proposed relative dissipation budget `mu`, define the cone matrix in nonnegative coordinates

```text
H_C(mu)
:= T_C^T (mu P - B_C) T_C.                              (14)
```

Because `z=T_Cu`, inequality (3) restricted to cone `C` is **exactly**

```text
u^T H_C(mu) u >= 0    for every u>=0.                  (15)
```

This is a copositivity-on-the-nonnegative-orthant statement.  No global PSD condition is mathematically necessary.

### Theorem 4.1 — exact feasible-cone reduction

Assume `K[a,k]>=0`.  Then the following are equivalent:

```text
(A)  for every z in R^4,
       |Lz|^T K |z| <= mu z^T P z;

(B)  for every feasible cone C and every u>=0,
       u^T H_C(mu) u >= 0.                              (16)
```

It is enough in (B) to check one representative from each of the 18 global-sign pairs.

### Proof

`(A) => (B)`: for any feasible `C` and `u>=0`, put `z=T_Cu`.  Formula (13) turns (A) into (15).

`(B) => (A)`: given arbitrary `z`, Lemma 2.1 applied independently to the two channels supplies a feasible product cone `C` and `u>=0` with `z=T_Cu`.  Apply (15) and reverse (13).

Global-sign paired cones have identical `B_C` and identical congruence matrix `H_C`, by (9)-(10), so one representative suffices.  QED.

This theorem is the clean mathematical target.  It is stronger than any particular sufficient checker representation.

---

## 5. A rational checker-friendly sufficient certificate: PSD + entrywise nonnegative

Direct copositivity checking is not the desired trusted interface.  For each representative cone `C`, ask the checker to exhibit two symmetric rational matrices

```text
S_C, N_C in Q^{4 x 4}                                   (17)
```

such that

```text
H_C(mu) = S_C + N_C,                                    (18)

S_C is positive semidefinite,                           (19)

N_C[i,j] >= 0 for every i,j.                            (20)
```

Call this an SPN certificate here: PSD plus entrywise-nonnegative.

### Lemma 5.1 — entrywise-nonnegative quadratic is nonnegative on the orthant

If `u_i>=0` and every `N_ij>=0`, then

```text
u^T N u = sum_{i,j} N_ij u_i u_j >= 0.                 (21)
```

### Lemma 5.2 — SPN implies cone nonnegativity

Under (18)-(20), for every `u>=0`,

```text
u^T H_C(mu) u
= u^T S_C u + u^T N_C u
>= 0.                                                    (22)
```

The first term is nonnegative by PSD; the second by Lemma 5.1.

Combining Theorem 4.1 and Lemma 5.2 gives the practical consumer.

### Theorem 5.3 — feasible-cone SPN small gain

Assume:

```text
(1) K[a,k] >= 0,
(2) |r_a| <= sum_k K[a,k]|z_k|  for a=1,2,
(3) for each of the 18 feasible cone representatives,
    H_C(mu)=S_C+N_C,
    S_C >= 0 (PSD),
    N_C >= 0 entrywise.                                 (23)
```

Then for every state `z` and every residual satisfying the component envelope,

```text
|(Lz)^T r| <= mu Q(z).                                  (24)
```

### Proof

From the component envelope,

```text
|(Lz)^T r| <= |Lz|^T K|z|.                             (25)
```

Choose a feasible cone containing `z`; write `z=T_Cu` with `u>=0`.  By Lemma 5.2 and (13),

```text
|Lz|^T K|z|
= z^T B_C z
<= mu z^T P z
= mu Q(z).                                               (26)
```

Combine (25)-(26).  QED.

If the existing P5 derivative ledger has

```text
Vdot <= -Q(z) + (Lz)^T r + anchor_bias_terms,            (27)
```

then (24) consumes at most `mu Q`.  With zero anchor bias and `mu<1`,

```text
Vdot <= -(1-mu) Q.                                      (28)
```

Any separate `Q >= lambda V` bridge then gives strict exponential decay.  With an anchor bias, the existing additive-bias tube can be reused with the remaining `(1-mu)` margin.  This child does not re-derive that downstream bookkeeping.

---

## 6. Why this certificate class is genuinely weaker than global PSD

The old per-sign sufficient condition was

```text
mu P - B_{sigma,tau} >= 0 globally.                     (29)
```

On a feasible cone, congruence by the invertible integer `T_C` does **not** by itself weaken (29): because `T_C` is invertible, requiring

```text
T_C^T(mu P-B_C)T_C >= 0 globally                        (30)
```

is equivalent to global PSD of `mu P-B_C`.

The gain appears only when we use the true domain restriction

```text
u >= 0.                                                  (31)
```

The SPN certificate exploits this restriction through `N_C`.

Global PSD is recovered as the special case

```text
N_C = 0,
S_C = H_C(mu).                                           (32)
```

So every old PSD certificate on a feasible cone is accepted by the SPN consumer.

Conversely, SPN can certify matrices that are not PSD.  For example, take

```text
S = 0,

N =
[0 1 0 0
 1 0 0 0
 0 0 0 0
 0 0 0 0].                                               (33)
```

`N` is entrywise nonnegative, hence for every `u>=0`,

```text
u^T N u = 2 u1 u2 >= 0.                                 (34)
```

But `N` is not PSD, since at `v=(1,-1,0,0)`

```text
v^T N v = -2.                                            (35)
```

Thus the SPN condition is strictly weaker than global PSD **as a matrix certificate condition**.  This does not yet prove that the concrete future `K_path` will exploit the gap; that requires the actual source-bound `K_path`.

No theorem about all low-dimensional copositive matrices is used here.  SPN is only a transparent sufficient class.

---

## 7. Exact arithmetic / checker contract

A concrete checker can remain entirely rational.

Inputs:

```text
- rational mu,
- rational nonnegative K_path[2,4],
- frozen rational P,
- the six fixed integer Gj matrices above.
```

For each of 18 representative cone pairs:

1. Construct integer `T_C`.
2. Construct sign diagonals `D_sigma_C`, `D_tau_C`.
3. Compute rational `B_C` by (12).
4. Compute rational `H_C(mu)` by (14).
5. Search for a rational symmetric entrywise-nonnegative `N_C` such that

```text
S_C := H_C(mu)-N_C                                      (36)
```

is PSD.
6. Emit exact `N_C` and an exact PSD witness for `S_C`.

A convenient PSD witness is an exact rational `LDL^T` identity:

```text
S_C = R_C^T D_C R_C,                                    (37)
```

where every diagonal entry of rational diagonal `D_C` is nonnegative.  This avoids square roots.  The formal layer only needs to check the matrix identity and diagonal signs.

The checker may optimize `N_C` outside the trusted core; only the final rational identities and inequalities need to be consumed formally.

Fallback behavior should remain fail-closed:

```text
SPN success       -> consume direct cone certificate;
SPN not found     -> no mathematical rejection of (3);
                     optionally fall back to T-P5-025 global PSD or
                     T-P5-024 scalar ell2 route.
```

Failure to find an SPN decomposition is not a counterexample to copositivity and must not be recorded as one.

---

## 8. Suggested minimal Lean decomposition

The formalization should not begin with a 4x4 spectral API.  The following small algebraic leaves are enough.

### 8.1 `channel_cone_cover`

A theorem over reals stating that every `(x,y)` admits one of the six explicit `(a,b>=0)` parametrizations above.  This can be written as a six-way disjunction or via a six-element inductive cone index.

Suggested shape:

```text
theorem channel_cone_cover (x y : R) :
  exists c : Fin 6, exists a b : R,
    0 <= a /\ 0 <= b /\ pair x y = G c (a,b)
```

with the sign/sum equalities bundled in `G c` lemmas.

### 8.2 `two_channel_cone_cover`

Apply `channel_cone_cover` to `(x4,y4)` and `(x5,y5)` and interleave the results into `T_C u` with four nonnegative coordinates.

### 8.3 `sign_fixed_power_identity`

For a feasible cone,

```text
|L(T_Cu)|^T K |T_Cu|
= u^T (T_C^T B_C T_C) u.                               (38)
```

This theorem should use the fixed cone sign equations rather than a generic `sign` function, which makes the proof purely polynomial/ring-level.

### 8.4 `entrywise_nonnegative_quadratic_nonnegative`

For a finite matrix `N` and componentwise nonnegative `u`, prove

```text
(forall i j, 0 <= N i j) -> 0 <= sum_i sum_j u_i*N_ij*u_j.
```

This is a reusable finite-sum order lemma.

### 8.5 `spn_quadratic_nonnegative_on_orthant`

From

```text
H = S+N,
S PSD,
N entrywise nonnegative,
u>=0,
```

prove `0<=u^T H u`.

### 8.6 `feasible_cone_direct_small_gain`

Consume the 18 cone certificates plus the component residual envelope and conclude

```text
abs ((Lz) dot r) <= mu * Q z.                           (39)
```

### 8.7 Optional exact equivalence theorem

Once the cone cover is available, formalize Theorem 4.1 as

```text
direct_abs_envelope_for_all_z
  <->
all_feasible_cone_quadratics_nonnegative.               (40)
```

This cleanly separates the **exact mathematics** from the SPN checker representation.

---

## 9. Interaction with T-P5-024 and T-P5-025

The intended hierarchy is now:

```text
source/Jacobian path
      |
      v
component K_path envelope
      |
      +--> T-P5-026 feasible-cone SPN consumer   (most structured)
      |
      +--> T-P5-025 all-sign global-PSD consumer
      |
      `--> Frobenius ell2_path
             |
             `--> T-P5-024 joint scalar geometry consumer.
```

The upper branches should not erase the lower ones.  They are alternative certificate consumers with different checker cost/strength tradeoffs.

`T-P5-026` improves two independent sources of conservatism:

```text
formal sign pairs:       32 distinct -> 18 feasible distinct;
global condition:        PSD on R^4  -> nonnegative only on u>=0,
                          with SPN as a rational sufficient class.
```

It does **not** change `P`, `Q`, the physical residual definition, or the source-side component envelope.

---

## 10. Precise remaining obligations

This child leaves the following items open.

1. **Concrete `K_path` binding.**  The actual source/checker must produce the 2x4 nonnegative component matrix on the same first-exit/P8 domain.
2. **Float64 discontinuities.**  The smooth exact-real Jacobian path and IEEE/controller/solve defects remain separate.  A discontinuous rounding residual cannot be placed in `K_path` merely by differentiating the ideal real map.
3. **Cone-certificate search.**  No concrete SPN decomposition is claimed in this review because no source-bound `K_path` is yet fixed here.
4. **Anchor bias.**  Genuine additive bias still belongs in the additive tube branch, not in a centered component gain unless a centered bound is proved.
5. **P8 coverage / ODE continuation.**  The cone theorem is pointwise algebra; it does not show a trajectory stays in the source/Jacobian domain.
6. **Lean/kernel evidence.**  The suggested theorem statements are not a compile receipt.  They remain for a formalization Agent.
7. **Admission.**  No P5/P8/M4 parent, registry node, source-authentication gate, or overall conclusion changes in this review.

---

## 11. Recommended next action

Once a concrete rational `K_path` arrives from the source/Jacobian lane, do **not** immediately reduce it to `ell2_path`.  First run the 18-cone rational SPN search.  If it succeeds for a rational `mu<1`, export the 18 exact decompositions `H_C=S_C+N_C` plus exact `LDL^T` witnesses for the `S_C` pieces.  If it fails, keep the failure diagnostic but fall back to `T-P5-025`/`T-P5-024`; do not interpret search failure as mathematical non-copositivity.

The most useful immediate formal target is the source-independent theorem pair

```text
exact_feasible_cone_reduction
spn_feasible_cone_small_gain.
```

Status remains **pending — wait for formalization, independent verification by 封不觉, and final integration by 梁智炜**.
