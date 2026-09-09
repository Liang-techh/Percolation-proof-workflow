---
kind: review_result
review_id: review-T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY-kuangmanmozun-20260909T0143Z
task_id: T-P5-115-ROOT-FREE-SECOND-JET-INDEPENDENT-ENERGY
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T01:43:00Z
claim_commit: fcd5a730ad295b31a95cf7cce6f48a54f184fbe3
inspected_commit: 54a1bcd3a664a22c1a139b3fe6d439d7b0253f86
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-114-SIGNED-SECOND-JET-ENERGY-CLOSURE-guyuefangyuan-20260909T0136Z.md
    commit: e07b619f6584356f39333601ea73b51fca216fa3
  - path: agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md
    commit: 3072f9b62a333f96448defd626a67039adb50168
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# T-P5-115 — root-free sharp independent-energy closure for the second jet

## 0. Seam selected

T-P5-114 correctly established that the best source strategy is to form the signed
second jet

`J2 = r - m - c`

before enclosure, and that signed Gram information should be consumed whenever it
exists.  It also gave the universal fallback

`Q_R(J2) <= 3 (U_r + U_m + U_c)`

when the only available data are independent component-energy caps

`Q_R(r)<=U_r`, `Q_R(m)<=U_m`, `Q_R(c)<=U_c`.

The coefficient `3` is sharp if the three numbers are first collapsed to the
single statistic `U_r+U_m+U_c`.  However, if the producer keeps the three
individual caps, the factor-3 fallback is generally not information-theoretically
sharp.  This child closes exactly that gap.

The result is a fail-closed, square-root-free, division-free rational checker.  It
uses one auxiliary scalar for the natural mass-side aggregate `g=m+c` and reaches
the exact worst-case independent-energy infimum.  It does not compete with the
signed-correlation packet of T-P5-114: any genuine cross information remains
strictly preferable.

---

## 1. Quadratic notation and the two-vector discriminant leaf

Let `B` be a symmetric positive-semidefinite bilinear form and

`Q(x) := B(x,x)`.

For every `x,y`, PSD gives the Cauchy-Schwarz square inequality

**(1.1)** `B(x,y)^2 <= Q(x) Q(y)`.

Assume rational/nonnegative scalar caps

**(1.2)** `Q(x) <= U`,

**(1.3)** `Q(y) <= V`,

with `U>=0`, `V>=0`.

Let a proposed total cap be `H` and define

**(1.4)** `C := H-U-V`.

Then the two exact scalar gates

**(1.5)** `C >= 0`,

**(1.6)** `C^2 >= 4 U V`

imply, for either sign,

**(1.7)** `Q(x+y) <= H`,

**(1.8)** `Q(x-y) <= H`.

### Proof

Expand

`Q(x +/- y) = Q(x)+Q(y) +/- 2B(x,y)`.

By (1.1)-(1.3),

`4 B(x,y)^2 <= 4 U V <= C^2`.

Because `C>=0`, this forces

`2 |B(x,y)| <= C`.

Therefore

`Q(x +/- y) <= U+V+C = H`.

The checker never needs to compute the square root `sqrt(UV)`.

### Exactness under the stated information model

For nonnegative real `U,V`, gates (1.5)-(1.6) are equivalent to

`H >= U+V+2 sqrt(UV)`.

This is the exact worst-case cap from the independent information
`Q(x)<=U`, `Q(y)<=V`: in one dimension with `Q(t)=t^2`, choose aligned scalar
vectors of magnitudes `sqrt(U)` and `sqrt(V)`.

The endpoint cases are also exact.  If `U=0`, PSD forces `B(x,y)=0` whenever
`Q(x)=0`, so the optimal bound reduces to `H>=V`; (1.5)-(1.6) reduce to precisely
that.  No artificial `lambda>1` endpoint hole remains.

---

## 2. Three-term second-jet closure with one rational auxiliary cap

Return to

`J2 = r-m-c = r-g`, `g:=m+c`,

and suppose only

**(2.1)** `Q_R(r)<=U_r`,

**(2.2)** `Q_R(m)<=U_m`,

**(2.3)** `Q_R(c)<=U_c`,

with all three caps nonnegative.

Choose one auxiliary proposed cap `K_mc>=0` for `Q_R(m+c)` and define

**(2.4)** `C_mc := K_mc-U_m-U_c`.

Check

**(2.5)** `C_mc>=0`,

**(2.6)** `C_mc^2 >= 4 U_m U_c`.

Section 1 gives

**(2.7)** `Q_R(m+c)<=K_mc`.

Now choose the proposed final second-jet cap `H2>=0` and define

**(2.8)** `C_r := H2-U_r-K_mc`.

Check

**(2.9)** `C_r>=0`,

**(2.10)** `C_r^2 >= 4 U_r K_mc`.

A second application of section 1 yields

**(2.11)** `Q_R(J2)=Q_R(r-(m+c))<=H2`.

Thus the entire independent-energy fallback is the four scalar comparisons
(2.5), (2.6), (2.9), (2.10).  There is no division, square root, operator norm,
fixed Young parameter, or matrix inverse in the trusted consumer.

### Minimal certificate packet

The source/producer can therefore emit only

`(U_r,U_m,U_c,K_mc,H2)`

plus the same-segment/metric identity already required by T-P5-114.  The trusted
checker recomputes `C_mc,C_r` and verifies the four gates.

`K_mc` is a certificate auxiliary, not a physical quantity and not a new source
claim.

---

## 3. Sharp worst-case constant retained by the three individual caps

Over the reals, define

`H_sharp := (sqrt(U_r)+sqrt(U_m)+sqrt(U_c))^2`.

Then `H_sharp` is the exact smallest universal cap implied by (2.1)-(2.3).

### Upper bound

The seminorm induced by a PSD quadratic form satisfies the triangle inequality
on the quotient by its kernel, hence

`sqrt(Q_R(r-m-c))`
` <= sqrt(Q_R(r))+sqrt(Q_R(m))+sqrt(Q_R(c))`
` <= sqrt(U_r)+sqrt(U_m)+sqrt(U_c)`.

Squaring gives `Q_R(J2)<=H_sharp`.

### Matching lower witness

In one dimension with `Q(t)=t^2`, take

`r=sqrt(U_r)`, `m=-sqrt(U_m)`, `c=-sqrt(U_c)`.

Then

`J2 = sqrt(U_r)+sqrt(U_m)+sqrt(U_c)`

and equality holds.  Therefore no smaller universal cap follows from the three
independent energies alone.

### Nested discriminant gates attain the same real optimum

The smallest real `K_mc` satisfying (2.5)-(2.6) is

`K_mc,* = (sqrt(U_m)+sqrt(U_c))^2`.

For fixed `K_mc`, the smallest real `H2` satisfying (2.9)-(2.10) is

`(sqrt(U_r)+sqrt(K_mc))^2`.

This function is increasing in `K_mc`, so minimizing over admissible `K_mc`
gives exactly

`H_sharp`.

Therefore the nested discriminant construction loses no information relative to
the best possible independent-energy theorem.

If the certificate language restricts all auxiliaries to rationals, the same
number remains the infimum.  Whenever the proposed rational `H2` has strict
reserve above `H_sharp`, density of the rationals allows a rational `K_mc` to be
chosen between the two strict real thresholds.  Exact equality may or may not
admit a rational `K_mc`; this is a certificate-attainment issue, not a change in
the mathematical infimum.

---

## 4. Why this does not contradict T-P5-114's sharp factor 3

T-P5-114 proved

`Q_R(J2) <= 3(U_r+U_m+U_c)`

and showed that the coefficient `3` cannot be reduced if only the sum of the
three energies is retained.

The present result keeps the *distribution* among `U_r,U_m,U_c`.  By ordinary
Cauchy-Schwarz,

**(4.1)**

`(sqrt(U_r)+sqrt(U_m)+sqrt(U_c))^2`
` <= 3(U_r+U_m+U_c)`.

Equality for positive caps occurs exactly when

`U_r=U_m=U_c`.

Thus:

- factor `3` is still the correct worst-case coefficient after collapsing to one
  scalar sum;
- keeping the three individual caps can be strictly stronger, often by a large
  amount;
- no correlation data are being invented here.

This is an information-retention improvement, not a contradiction.

---

## 5. Exact rational regression: imbalanced second-jet channels

Take

`U_r=100`, `U_m=1`, `U_c=1`.

The factor-3 fallback gives

**(5.1)** `H2_old = 3(100+1+1)=306`.

The new gate chooses

`K_mc=4`.

Then

`C_mc=4-1-1=2`,

`C_mc^2=4=4 U_m U_c`.

Choose

`H2=144`.

Then

`C_r=144-100-4=40`,

`C_r^2=1600=4*100*4`.

Hence the new checker proves

**(5.2)** `Q_R(J2)<=144`.

This is not merely a better sufficient constant.  It is exact: in one dimension,

`r=10`, `m=-1`, `c=-1`

gives `J2=12` and `Q(J2)=144`.

So for this cap distribution the old fallback charges `306` where the true
information-theoretic worst case is `144`.

---

## 6. Rational non-square regression

The method does not require cap products to be perfect squares.

Take

`U_r=1`, `U_m=2`, `U_c=3`.

Choose the rational auxiliary

`K_mc=10`.

Then

`C_mc=10-2-3=5`,

`C_mc^2=25 >= 24 = 4*2*3`.

Choose

`H2=87/5`.

Then

`C_r = 87/5 - 1 - 10 = 32/5`,

and

`C_r^2 = 1024/25 >= 1000/25 = 4*1*10`.

Therefore

**(6.1)** `Q_R(J2)<=87/5`.

The factor-3 fallback would give `18`, while the exact real optimum is

`(1+sqrt(2)+sqrt(3))^2`, approximately `17.191508...`.

Thus a fully rational certificate already improves `18` to `17.4` without any
square-root computation in the checker.

---

## 7. Homogeneous cell-radius specialization

T-P5-114 notes that second-jet energies naturally scale with

`Z2 := Q_Z(delta)^2 >= 0`.

Suppose a source proves on the same physical segment

`Q_R(r) <= u_r Z2`,

`Q_R(m) <= u_m Z2`,

`Q_R(c) <= u_c Z2`,

with nonnegative rational coefficients `u_r,u_m,u_c`.

The producer may now certify *coefficient-level* auxiliaries `k,h>=0` using

**(7.1)** `k-u_m-u_c >= 0`,

**(7.2)** `(k-u_m-u_c)^2 >= 4 u_m u_c`,

**(7.3)** `h-u_r-k >= 0`,

**(7.4)** `(h-u_r-k)^2 >= 4 u_r k`.

Multiplying the section-2 proof by the common nonnegative scale `Z2` yields

**(7.5)** `Q_R(J2) <= h Z2`.

If the cell also has

`Q_Z(delta)<=S`,

then

**(7.6)** `Q_R(J2)<=h S^2`.

Therefore T-P5-112 can consume directly

**(7.7)** `h S^2 <= 4 gamma D_anchor`

in its lower-gain route, or

**(7.8)** `chi h S^2 <= 4(1-kappa)^2 D_anchor`

in its preconditioner route.

This is preferable to forming `3(u_r+u_m+u_c)` whenever the three source
coefficients are imbalanced.

---

## 8. Equivalent weighted three-block certificate

For completeness, there is a one-shot rational weighted form that makes the
relation to T-P5-114 section 6 explicit.

Let `y1=r`, `y2=-m`, `y3=-c`, and choose positive rationals `p1,p2,p3`.  Define

`S_p=p1+p2+p3`, `P_p=p1*p2*p3`.

PSD gives the exact identity

**(8.1)**

`S_p*(p2*p3*Q(y1)+p1*p3*Q(y2)+p1*p2*Q(y3))`
` - P_p*Q(y1+y2+y3)`
` = p3*Q(p2*y1-p1*y2)`
`   + p2*Q(p3*y1-p1*y3)`
`   + p1*Q(p3*y2-p2*y3)`
` >= 0`.

Hence

**(8.2)**

`P_p Q_R(J2)`
` <= S_p*(p2*p3*U_r+p1*p3*U_m+p1*p2*U_c)`.

A proposed `H2` therefore passes if

**(8.3)**

`S_p*(p2*p3*U_r+p1*p3*U_m+p1*p2*U_c) <= P_p*H2`.

This is also square-root free and division free.  Its real optimum over positive
weights is the same `H_sharp`; the minimizing ratios are proportional to the
square roots of the caps.

For trusted implementation, the nested-discriminant packet is often preferable:
it uses one auxiliary `K_mc` instead of three positive weights and has explicit
branch guards.  The weighted identity remains useful as an independent proof
route and a regression oracle.

---

## 9. Failure branches that must remain fail-closed

### 9.1 Squaring without the nonnegative branch guard is unsound

The condition

`(K_mc-U_m-U_c)^2 >= 4 U_m U_c`

alone is not enough.

Take `U_m=U_c=1`, `K_mc=0`.  Then

`(0-1-1)^2=4=4*1*1`,

so the squared test passes, but scalar `m=c=1` gives

`Q(m+c)=4>0=K_mc`.

Thus **(2.5) is mandatory**.  The same warning applies to the outer gate
`C_r>=0`.

### 9.2 `K_mc=U_m+U_c` is generally false

If both caps are positive, the missing cross term can be adverse.  With
`U_m=U_c=1`, `m=c=1`, one has

`Q(m+c)=4 > 2=U_m+U_c`.

So a producer may not call the diagonal sum an aggregate energy bound unless it
also supplies sign/correlation information.

### 9.3 No independent-energy theorem can beat `H_sharp`

Any proposed universal `H2<H_sharp` is refuted by the one-dimensional aligned
witness from section 3.  To go below `H_sharp`, the source must add information:
for example the signed Gram lower/upper endpoints of T-P5-114, component
orthogonality, range restrictions, or a direct `Q_R(J2)` enclosure.

### 9.4 Do not use this fallback after a better signed packet has already closed

If T-P5-114 provides `H_corr=U_R+U_G-L_RG`, that signed result should be consumed
directly.  Replacing it by independent caps and this theorem is valid but can
only lose cancellation.

---

## 10. Formalizable theorem statements

A minimal Lean decomposition is:

```lean
-- Generic PSD Cauchy-Schwarz square leaf, or use an existing library theorem.
theorem psd_bilinear_cross_sq
    (hpsd : forall z, 0 <= B z z) :
    (B x y)^2 <= (B x x) * (B y y) := by
  ...

-- Lambda/root-free exact two-channel envelope.
theorem quadratic_two_term_discriminant
    (hx : Q x <= U) (hy : Q y <= V)
    (hU : 0 <= U) (hV : 0 <= V)
    (hC : 0 <= H-U-V)
    (hdisc : 4*U*V <= (H-U-V)^2) :
    Q (x-y) <= H := by
  ...

-- Same statement for x+y, or derive by y -> -y.
theorem quadratic_two_term_discriminant_add ... :
    Q (x+y) <= H := by
  ...

-- Preferred T-P5-114 fallback composition.
theorem second_jet_independent_energy_nested
    (hr : Q r <= Ur) (hm : Q m <= Um) (hc : Q c <= Uc)
    (hcm0 : 0 <= K-Um-Uc)
    (hcmdisc : 4*Um*Uc <= (K-Um-Uc)^2)
    (hcr0 : 0 <= H-Ur-K)
    (hcrdisc : 4*Ur*K <= (H-Ur-K)^2) :
    Q (r-m-c) <= H := by
  ...

-- Homogeneous coefficient form for Z2=QZ(delta)^2.
theorem second_jet_independent_energy_homogeneous
    (hZ : 0 <= Z2)
    (hr : Q r <= ur*Z2) (hm : Q m <= um*Z2) (hc : Q c <= uc*Z2)
    ... :
    Q (r-m-c) <= h*Z2 := by
  ...

-- Optional one-shot weighted identity.
theorem quadratic_three_term_weighted_mul
    (hp1 : 0 < p1) (hp2 : 0 < p2) (hp3 : 0 < p3) :
    p1*p2*p3*Q (y1+y2+y3)
      <= (p1+p2+p3) *
         (p2*p3*Q y1 + p1*p3*Q y2 + p1*p2*Q y3) := by
  ...
```

The nested theorem is the recommended consumer API because it is pure ordered
ring arithmetic once PSD Cauchy-Schwarz is available.  The sharpness/infimum
statement may remain a mathematical review fact; no square-root theorem is
needed by the certificate checker.

---

## 11. Source-facing recommendation and next step

The source priority from T-P5-114 remains unchanged:

1. direct exact signed `J2`, then bound `Q_R(J2)`;
2. signed two-block or three-block Gram packet;
3. only if correlation is unavailable, retain the three separate nonnegative
   energy caps and use this T-P5-115 nested gate;
4. collapse to `3(U_r+U_m+U_c)` only as the final lowest-information fallback.

For a homogeneous cell packet, the smallest useful new fields are therefore

`u_r, u_m, u_c, k_mc, h_2`,

checked by (7.1)-(7.4).  This lets the existing T-P5-112/T-P5-113 chain consume
`H2=h_2*S^2` with no new analytic architecture.

The next mathematical/source step is not another universal Young constant.  It
is to determine whether the actual same-segment second-jet producer can retain a
signed Gram packet; if not, it should at least retain separate component-energy
coefficients so that the sharp independent-energy fallback here can be used.

---

## 12. Status / non-claims

Mathematical status: **CONDITIONAL_PASS**.

Closed here:

- exact root-free two-vector discriminant envelope;
- exact two-stage three-component independent-energy certificate for
  `J2=r-m-c`;
- proof that its real infimum equals the information-theoretically sharp bound;
- rational strict-reserve attainability;
- homogeneous cell-radius specialization;
- strict counterexamples showing why branch guards and cross allowance cannot be
  dropped.

Still open and explicitly not claimed:

- actual `D2M/D2R/J2` source extraction;
- same-branch `a,a'` and whole-segment coverage;
- actual `Q_R/Q_A` metric identity;
- numerical `U_r,U_m,U_c` or homogeneous `u_r,u_m,u_c` for the physical P5
  source;
- actual `gamma` or preconditioner packet and displacement cap `S`;
- T-P5-113 downstream power/source binding;
- Float64/FD/runtime equivalence, P8 coverage, Lean/kernel verification,
  independent validator acceptance, admission, registry, or P5/M4 closure.

No registry, admission, provenance, or verification state is upgraded by this
review.
