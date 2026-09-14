---
kind: review_result
review_id: review-T-P5-111-flow-domain-recenter-design-liuguanyi-20260909T0003Z
task_id: T-P5-111-FLOW-DOMAIN-RECENTER-DESIGN
source_agent: 柳冠一
created_at: 2026-09-09T00:03:00Z
claim_commit: 612cec99a8c1603a31f36e0d3abdb645c1da16e7
inspected_commit: 6a106e20730829cce2848d9f6fe41ce96f0af521
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-106-reference-ramp-recentered-energy-honglianmozun-20260908T2256Z.md
    blob_sha: 7a8fe4d1f404a86e3695cd602f9691399fdefa52
  - path: agent_review_inbox/review-T-P5-109-sharp-reference-jump-reset-kuangmanmozun-20260908T2329Z.md
    blob_sha: 32a521fc93a800636a7654f1cf42341a3d504db0
  - path: agent_review_inbox/review-T-P5-110-approximate-reference-recentering-honglianmozun-20260908T2358Z.md
    blob_sha: 9ff5e8d7a7fbce4888aa9759c1d2117924cac16a
status: CONDITIONAL_PASS_EXACT_RATIONAL_FLOW_DOMAIN_BRIDGE
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the 6x6 rational domain-transport quadratic form and then expose recenter selection as a typed quadratic design packet; bind actual reference/source caps only upstream
commands: exact rational hand derivation / Sylvester replay; no Lean compile or source execution
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-111 — arbitrary recenter: exact flow-to-absolute-domain quadratic bridge

## 0. Why this child is new

T-P5-110 makes the recenter vector `a` a real design parameter. Its continuous-flow cost is the exact convex quadratic

`L_eta(a)`
` = eta W (g-Ba)^T H_delta (g-Ba)`
`   + S a^T H_s a`.

But the absolute P5 block budget is written in the physical coordinates

`q=z+a w`, `v=s`,

so changing `a` also changes domain placement. T-P5-106 has one fixed-
`a_eq` certificate

`pB <= (67/2) Vc + (41/200) w^2`,

but that coefficient cannot be reused for an arbitrary `a` selected by
T-P5-110.

This child closes that mathematical interface. For the current exact rational
storage it proves one **uniform-in-`a`** quadratic transport theorem:

**(0.1)**

`pB(z+a w,s)`
` <= 34 Vc(z,s)`
`    + w^2 * ((13/8) a_1^2 + 2 a_2^2)`.

The certificate is a single 6x6 rational positive-definite matrix. It needs no
matrix inverse, square root, eigenvalue, or runtime/source assumption.

Combining (0.1) with T-P5-110 turns continuous-flow forcing cost plus absolute
reference placement into a typed rational quadratic design problem. In the
forcing-limited branch, the best `a` for this combined objective is again
characterized by a linear normal equation, so the checker can verify a supplied
rational `a_*` without inverting anything.

No jump reset is re-proved here; T-P5-109 remains the jump consumer and must be
re-instantiated with the selected `a`.

---

## 1. Storage and physical block weight

Use the exact T-P5-106/T-P5-109 storage packet

`M = diag(350003/3000000, 200739/4000000)`,

`D = diag(4/5,13/20)`,

`K = [[3/4,-3/400],[-3/400,29/50]]`.

Write

`x=(z_1,z_2,s_1,s_2)^T`,

`P = [[K+D,M],[M,M]]`,

so

`Vc(x)=1/2 x^T P x`.

The absolute P5 block weight is

`pB(q,v) = (3/2)||q||^2 + (4/5)||v||^2`.

For an arbitrary displacement vector `u in R^2`, set

`q=z+u`, `v=s`.

Define

`R_B = diag(3/2,3/2,4/5,4/5)`,

`L = [[3/2,0],`
`     [0,3/2],`
`     [0,0],`
`     [0,0]]`.

Then the exact expansion is

**(1.1)**

`pB(z+u,s)`
` = x^T R_B x + 2 x^T L u + (3/2) u^T u`.

This identity is the source-to-math seam. The displacement `u` may later be
instantiated as `a w`; no source semantics are needed to prove it.

---

## 2. One 6x6 exact rational certificate

Take

`G = diag(13/8, 2)`.

Consider the symmetric block matrix

**(2.1)**

`H_dom = [[17 P - R_B,       -L],`
`         [     -L^T, G-(3/2)I]]`.

Because `34 Vc = 17 x^T P x`, the quadratic identity is

**(2.2)**

`34 Vc(x) + u^T G u - pB(z+u,s)`
` = [x;u]^T H_dom [x;u]`.

The six leading principal minors of `H_dom`, in the coordinate order
`(z1,z2,s1,s2,u1,u2)`, are exactly

`497/20`,

`77171559/160000`,

`74160523104355139/150000000000000`,

`371173377691919122727626123`
` / 48000000000000000000000000`,

`60755172909964656269626123`
` / 384000000000000000000000000`,

`12864166380277214447626123`
` / 768000000000000000000000000`.

Every numerator and denominator is strictly positive. Sylvester therefore gives

**(2.3)** `H_dom > 0`.

Substituting (2.3) into (2.2) proves, for every real `x,u`,

**(2.4)**

`pB(z+u,s) <= 34 Vc(z,s) + (13/8)u_1^2 + 2u_2^2`.

This theorem is stronger as an interface than the fixed-center T-P5-106 packet:
it is valid simultaneously for every future recenter vector.

### Minimal theorem statement

`routeb_reference_absolute_weight_arbitrary_shift`

Inputs: `x=(z,s)`, `u`, the exact rational `P,R_B,G`, and positivity of the six
leading minors above.

Output: (2.4).

A checker implementation can avoid any spectral API and consume only rational
matrix multiplication plus the six positive scalar witnesses.

---

## 3. Recenter corollary

Put

`u=a w`.

Then (2.4) becomes

**(3.1)**

`pB(z+a w,s)`
` <= 34 Vc(z,s)`
`    + w^2 a^T G a`,

where

**(3.2)**

`a^T G a = (13/8)a_1^2 + 2a_2^2`.

Hence if the source-facing amplitude cap gives

`w^2 <= W`, `W>=0`,

and a reference collar gives

`Vc <= R`,

then

**(3.3)**

`pB <= 34 R + W a^T G a`.

The roles remain cleanly separated:

- `R` is the centered dynamic collar;
- `W a^T G a` is the absolute moving-center placement charge.

No slope cap is used by this theorem.

---

## 4. Direct composition with T-P5-110

T-P5-110 assumes

`Qd >= lambda Vc`, `lambda>0`,

and for `eta>0` defines

`L_eta(a)`
` = eta W (g-Ba)^T H_delta (g-Ba)`
`   + S a^T H_s a`.

Its square-only collar gate is

**(4.1)**

`(1+eta) L_eta(a) <= eta lambda R`.

Together with (3.3), a completely division-free P5 reference-budget handoff is:

**(4.2) CENTERED FLOW GATE**

`(1+eta)L_eta(a) <= eta lambda R`,

**(4.3) ABSOLUTE BLOCK GATE**

`34 R + W a^T G a <= PBbar`.

Then throughout the covered flow segment,

**(4.4)** `pB <= PBbar`,

provided the usual initial/collar and path-coverage premises are supplied.

For the existing hybrid P5 budget, if an independent remote-state consumer gives

`pD <= PDbar`

and the target is

`pD+pB <= rho`,

it is enough to verify the two gates

`(1+eta)L_eta(a) <= eta lambda R`,

`PDbar + 34 R + W a^T G a <= rho`.

This is the clean typed contract. It does not conflate a flow derivative cap
with absolute domain placement.

---

## 5. Forcing-limited branch: one convex quadratic design objective

There is one useful stronger statement when the chosen collar level is limited
by the continuous forcing floor rather than by a larger initial-state or reset
requirement.

Multiply the resulting physical block bound by the positive scalar
`eta lambda`. The quantity to minimize over `a` is equivalent to

**(5.1)**

`J_tilde(a)`
` = 34(1+eta) L_eta(a)`
`   + eta lambda W a^T G a`.

Expanding gives

`J_tilde(a)`
` = const - 2 a^T h_* + a^T R_* a`,

where

**(5.2)**

`R_*`
` = 34(1+eta)`
`     [eta W B^T H_delta B + S H_s]`
`   + eta lambda W G`,

and

**(5.3)**

`h_*`
` = 34(1+eta) eta W B^T H_delta g`.

Suppose a supplied exact witness `a_*` satisfies

**(5.4)** `R_* a_* = h_*`.

Then a ring expansion yields

**(5.5)**

`J_tilde(a)-J_tilde(a_*)`
` = (a-a_*)^T R_* (a-a_*)`.

Therefore if `R_* >= 0`, `a_*` is a global minimizer of this combined
continuous-flow-plus-domain objective. If `R_*>0`, it is unique.

### Why this is an interface theorem rather than an optimizer implementation

The checker never computes `R_*^{-1}`. A source/design stage may propose any
rational `a_*`; the trusted layer checks only

- the linear identity `R_* a_*=h_*`;
- PSD/PD of `R_*`;
- the already-separated source caps and domain premises.

This extends the T-P5-110 normal equation by including the absolute physical
state budget that T-P5-110 explicitly left outside its flow-only optimizer.

### Important boundary

(5.1)-(5.5) are **not** the global hybrid optimum if any of the following are
active:

- an initial-state lower bound forces `R` above the forcing floor;
- T-P5-109 jump headroom is active;
- a separate coordinate/domain cap is tighter than `pB`;
- the actual source changes `W,S` or coefficient semantics across segments.

In those cases use the two-witness gates (4.2)-(4.3), and treat the selected
`a` as a constrained design parameter instead of silently eliminating `R`.

---

## 6. Exact comparison with the old fixed-center domain packet

For the old exact center

`a_eq=(2340/8699,1520/8699)`,

our new arbitrary-shift charge is

**(6.1)**

`a_eq^T G a_eq`
` = 13518650/75672601`
` ~= 0.17864656191743694`.

The T-P5-106 fixed-center packet used

`(41/200) ~= 0.205`.

The new charge is smaller by the exact amount

**(6.2)**

`41/200 - 13518650/75672601`
` = 398846641/15134520200 > 0`.

The trade is that the centered multiplier increases from `67/2=33.5` to `34`.
Therefore neither packet uniformly dominates the other. On caps

`Vc<=R`, `w^2<=W`,

the new packet is strictly better exactly whenever

**(6.3)**

`R/W < 398846641/7567260100`
`    ~= 0.052706876165126135`

(for `W>0`; handle `W=0` separately).

Using the sharper exact-center continuous-flow coefficient from T-P5-110,

`R_exact_center >=`
` 380929949728094229955039`
` /1094723642897539156030450 * S`
` ~= 0.34796905337665 S`,

this implies that, on the forcing-limited exact-center branch, the new absolute
packet beats the old one whenever

**(6.4)**

`S/W <`
`115398926962472718374969`
`/761859899456188459910078`
` ~= 0.1514700104899127`.

This is only a packet-selection boundary, not a deployed schedule claim.

---

## 7. How jumps enter without duplicating T-P5-109

T-P5-109 already proves the sharp jump translation theorem for the recentered
storage. For an arbitrary selected `a`, its jump direction is still

`e(a)=(a,0)`,

and its scalar geometry is controlled by

`A_jump(a)=a^T(K+D)a`.

So the correct downstream composition is:

1. choose/prove the flow-domain packet `(a,R)` using (4.2)-(4.3);
2. re-instantiate T-P5-109 with the same `a` and the same storage `P`;
3. charge the actual jump amplitude/dwell headroom there.

Do **not** add an ad hoc jump term to `J_tilde` and call it the T-P5-109 exact
reset theorem. Its sharp ellipsoid-translation gate is a separate nonlinear
scalar constraint and remains owned by that child.

---

## 8. Exact obstruction / typed boundary

The main interface obstruction is now precise:

> A flow-only optimizer for `a` is not enough. The physical-domain cost is an
> independent quadratic in the same `a`, and any deployed recenter choice must
> be checked against both.

Conversely, one no longer needs a fresh 5x5 PSD search every time `a` changes.
The single 6x6 matrix `H_dom` proves a uniform family for all `a` and all `w`.

This separates three layers cleanly:

- source layer: actual `B,g,W,S`, reference law, initial/path/jump data;
- mathematical design layer: choose `a,R` satisfying the quadratic gates;
- trusted checker layer: rational matrix/order identities only.

---

## 9. Suggested minimal formalization surface

Recommended leaves:

1. `physical_block_weight_shift_expansion` — identity (1.1).
2. `routeb_reference_domain_Hdom_pos` — six rational leading-minor facts.
3. `routeb_reference_absolute_weight_arbitrary_shift` — (2.4).
4. `routeb_reference_absolute_weight_recenter` — (3.1)-(3.3).
5. `flow_domain_recenter_budget` — compose T-P5-110 (4.1) with (3.3).
6. `flow_domain_recenter_normal_equation_minimizer` — completion (5.5).

The first four are source-independent and very small. The fifth should keep
`W,S,eta,lambda,R` typed and explicit. The sixth must be labeled
forcing-limited, not global-hybrid.

## 10. Status

`CONDITIONAL_PASS_EXACT_RATIONAL_FLOW_DOMAIN_BRIDGE / pending`.

Closed mathematically in this child:

- one uniform arbitrary-`a` absolute-weight theorem;
- exact 6x6 rational positivity certificate;
- exact composition with the T-P5-110 flow collar;
- inverse-free combined normal equation in the forcing-limited branch;
- exact packet-selection crossover for the old fixed center.

Still open and intentionally not claimed:

- actual `referenceKey` / source coefficient binding;
- actual `W,S`, initial collar, segment/path/FD/reference halo coverage;
- T-P5-109 jump/dwell instantiation for the selected `a`;
- Float64/controller/runtime semantics;
- Lean/kernel receipt and independent verification;
- comparator/admission/registry and parent P5/P8 closure.
