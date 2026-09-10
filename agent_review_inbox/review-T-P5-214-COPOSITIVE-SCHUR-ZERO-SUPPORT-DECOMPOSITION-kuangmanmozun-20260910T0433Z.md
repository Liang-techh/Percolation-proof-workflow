---
kind: review_result
review_id: review-T-P5-214-copositive-schur-zero-support-decomposition-kuangmanmozun-20260910T0433Z
task_id: T-P5-214-COPOSITIVE-SCHUR-ZERO-SUPPORT-DECOMPOSITION
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T04:33:00Z
claim_commit: 39b26a32b98a99ce7c5720b94e737cc1753dce08
inspected_commit: 4e7afb91ecafa45a0b75ed418b6b69348076adcd
upstream_commits:
  - 94648fb1f758e81f3755e839f98f55283a551d20  # T-P5-213 active-kernel debit dichotomy
  - 2f952c3ff2704671a74123e51d58e80f4b53b223  # T-P5-212 high-corank reduced-kernel bridge
  - 682b7bd77f7babedc1d0310091ce188a0767d3ba  # T-P5-211 corank-one Schur scalarization
  - 8cba2b2fa9bb7fc26803b26833df2c44e6cdc0b3  # T-P5-210 second-order threshold
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_copositive_zero_support_psd_lemma; add_finite_psd_support_union; add_zero_loaded_support_dispatcher; add_supportwise_debit_pullback; add_nonconic_zero_set_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/support algebra; exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-214 — copositive Schur zero-support decomposition

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-213 Boundary C deliberately leaves the case where the reduced Schur block `K` is copositive but not ordinary PSD. In that branch the endpoint zero set is no longer the single cone `ker(K) ∩ R_+^p`, so T-P5-212 cannot be applied globally.

The present child gives an exact replacement:

> Every nonnegative zero of a copositive symmetric matrix has an ordinary-PSD principal block on its **true positive support**. Consequently the complete zero set of an arbitrary copositive `K` is a finite union of PSD principal-kernel cones. After the T-P5-210 common-zero first-order filter is imposed, only supports contained in the zero-loaded coordinate set survive. Each surviving support then routes back to the existing T-P5-212/T-P5-213 PSD-kernel machinery.

Thus `K` being globally indefinite does **not** force a generic nonlinear zero-set optimizer. The price is finite support enumeration rather than one global kernel computation.

The crucial warning is that the zero set of an indefinite copositive matrix is generally **not convex and not a cone under addition of different zero rays**. Therefore generators from different supports must never be concatenated into one global `V` and freely mixed.

No actual P5 source identity, selector/cell/tube coverage, Float64/runtime semantics, Lean/kernel receipt, independent verification, registry admission, or parent closure is claimed.

---

## 1. Schur setup inherited from T-P5-178/T-P5-213

Write the endpoint critical quadratic as

`H = [[A,R^T],[R,C]]`,

on variables

`u ∈ R^m` signed, `eta ∈ R_+^p` one-sided.

Assume the already-established range/Schur hypotheses:

1. `A=A^T >= 0`;
2. `R n=0` for every `n∈ker(A)`;
3. choose one exact solve `A X=R^T`;
4. define `K:=C-RX`.

Then

`h(u,eta):=(u,eta)^T H(u,eta)`

`=(u+Xeta)^T A(u+Xeta)+eta^T K eta`.

Assume the endpoint critical block is nonnegative on the mixed cone:

`h(u,eta)>=0` for every signed `u` and every `eta>=0`.

Taking `u=-Xeta` gives

**`eta^T K eta>=0` for every `eta>=0`.**

Hence `K` is copositive. No ordinary PSD assumption on `K` is made.

Moreover `h(u,eta)=0` iff

`u+Xeta ∈ ker(A)`

and

`eta>=0`, `eta^T K eta=0`.

So the only new object is the copositive zero set

`Z_+(K):={eta>=0 : eta^T K eta=0}`.

---

## 2. T214-A — a strict-support copositive zero forces a PSD principal block

Let `K=K^T` be copositive and let `eta>=0`, `eta!=0`, satisfy

`eta^T K eta=0`.

Set

`S:=supp(eta)`, `xi:=eta_S`.

Then `xi>0` coordinatewise and

`xi^T K_SS xi=0`.

### Theorem A

**`K_SS` is ordinary PSD and `K_SS xi=0`.**

### Proof

Fix an arbitrary signed vector `d∈R^S`.

Because `xi>0`, there is `eps0>0` such that

`xi+t d>=0`

for every `|t|<=eps0`.

Copositivity of the principal block gives

`p_d(t):=(xi+t d)^T K_SS (xi+t d)>=0`

for both positive and negative sufficiently small `t`, while

`p_d(0)=0`.

Therefore `t=0` is a two-sided local minimum of the quadratic polynomial `p_d`. Its linear coefficient vanishes:

`d^T K_SS xi=0`.

Since this holds for every `d`,

`K_SS xi=0`.

The remaining quadratic coefficient must be nonnegative:

`d^T K_SS d>=0`

for every signed `d`. Hence

**`K_SS>=0`.**

QED.

This is the key local rigidity: global copositivity plus a zero in the relative interior of an orthant face upgrades the Hessian on that face from copositive to ordinary PSD.

---

## 3. T214-B — the omitted-row residual is automatically one-sided nonnegative

With the same `eta` and support `S`, for every `j notin S`, perturb only the inactive coordinate:

`eta+t e_j>=0`, `t>=0`.

Copositivity gives

`0 <= (eta+t e_j)^T K(eta+t e_j)`

`=2t (Keta)_j+t^2 K_jj`.

If `(Keta)_j<0`, the right-hand side would be negative for all sufficiently small positive `t`. Therefore

**`(Keta)_j>=0` for every `j notin S`.**

On `S`, Theorem A gives `(Keta)_S=0`. Thus every copositive zero satisfies the exact complementarity/KKT relations

**`Keta>=0`, `eta>=0`, `eta_i(Keta)_i=0` for all i.**

This does not mean `Keta=0`; the omitted-row residual may be strictly positive.

---

## 4. Exact finite union of PSD principal-kernel cones

For a nonempty support `S⊆{1,...,p}`, define

`C_S := { iota_S xi : xi>=0, K_SS xi=0 }`

whenever `K_SS>=0`, and `C_S:={0}` otherwise. Here `iota_S` denotes zero extension outside `S`.

### Theorem B — finite zero-set decomposition

For every symmetric copositive `K`,

**`Z_+(K) = union_{S⊆[p], K_SS>=0} C_S`.**

### Proof: `subset`

Take `eta∈Z_+(K)`, `eta!=0`, and let `S=supp(eta)`. By Theorem A,

`K_SS>=0`, `K_SS eta_S=0`.

Hence `eta∈C_S`.

### Proof: `superset`

Take `eta=iota_S xi∈C_S`. Since `K_SS xi=0`,

`eta^T K eta = xi^T K_SS xi=0`.

Also `eta>=0`, so `eta∈Z_+(K)`.

QED.

There are at most `2^p-1` nonempty supports. The decomposition is therefore finite and exact. It may be redundant because a vector on the boundary of one `C_S` has a smaller true support; redundancy is harmless for a fail-closed dispatcher.

A disjoint relative-interior version is obtained by replacing `xi>=0` with `xi>0` and indexing by the true support.

---

## 5. Why T-P5-212 fails globally but remains exact supportwise

T-P5-212 assumes a globally PSD reduced block, so

`Z_+(K)=ker(K)∩R_+^p`

is one polyhedral cone.

For a merely copositive indefinite `K`, a zero need not lie in the full kernel. Nevertheless Theorem A says its true support principal block **is** PSD. Therefore on each support `S`,

`C_S = iota_S(ker(K_SS)∩R_+^S)`,

which is exactly the PSD-kernel cone handled by T-P5-212.

Thus the correct replacement is

**one global PSD-kernel cone -> finite family of supportwise PSD-kernel cones.**

Nothing semialgebraic remains inside an individual support branch.

---

## 6. T214-C — common-zero first-order debit removes all positively loaded coordinates before support enumeration

Use the T-P5-210 debit partition

`Q=[[P,T^T],[T,U]]`

and reference common zero

`x_*=(z,0)`,

where `z>0` on the canonical active support. Assume `Q` is copositive and

`x_*^T Q x_*=0`.

As in T-P5-211/T-P5-213,

`P>=0`, `Pz=0`,

and

`g:=Tz>=0`.

For every endpoint zero tangent

`v=(N alpha-Xeta,eta)`,

the T-P5-210 first-order debit condition is

`(Qx_*)^T v = g^T eta=0`.

Since both `g` and `eta` are nonnegative,

`g^Teta=0`

iff

**`eta_i=0` for every i with `g_i>0`.**

Define the zero-loaded index set

`J0:={i:g_i=0}`.

Every bi-critical reduced direction therefore has support

**`S⊆J0`.**

This filter is exact and should be applied *before* the exponential support loop.

---

## 7. T214-D — flat active-kernel branch reduces each support to one copositive matrix

Let `N` be a complete basis of `ker(A)` and define, as in T-P5-213,

`E:=N^T P N`.

If `E!=0`, T-P5-213 already supplies a pure-active positive-debit witness. No reduced-support search is needed.

Now take the genuinely new branch

**`E=0`.**

T-P5-213 then gives `PN=0` and removes the active-kernel debit coupling on every valid bi-critical zero sheet.

Define

`G:=U+X^T P X-TX-X^T T^T`.

Fix one support `S⊆J0` with `K_SS>=0`. Let columns of

`V_S`

be a complete finite generator family of

`ker(K_SS)∩R_+^S`,

as supplied by T-P5-212's PSD support-descent theorem. Zero-extend the columns to the full inactive space; denote the resulting matrix by `W_S`.

Every `eta=W_S y`, `y>=0`, satisfies

`eta^T K eta=0`

and `g^Teta=0`, so it is a valid reduced bi-critical zero direction.

Set

**`M_S:=W_S^T G W_S`.**

The small-perturbation copositivity argument at the common zero implies

`y^T M_S y>=0` for every `y>=0`.

Hence

**`M_S` is copositive.**

By the elementary T-P5-212 criterion for a symmetric copositive matrix,

`exists y>=0 : y^T M_S y>0`

iff

**`M_S != 0`.**

Therefore this support contains a T-P5-210 second-order endpoint witness exactly when `M_S` is nonzero.

---

## 8. Main dispatcher theorem

### Theorem T214-E — indefinite-copositive Schur witness criterion

Assume:

1. the T-P5-178 endpoint completed-square/range hypotheses;
2. mixed-cone endpoint nonnegativity, hence `K` copositive;
3. the T-P5-210 copositive common-zero debit hypotheses at a strict-positive canonical active contact;
4. a complete active kernel basis `N`;
5. for each support used below, a complete T-P5-212 generator packet for `ker(K_SS)∩R_+^S`.

Let

`E=N^TPN`, `J0={i:(Tz)_i=0}`.

Then a bi-critical tangent `v` exists with

`v^T H v=0 < v^T Q v`

iff either

**(A) `E!=0`,**

or, if `E=0`,

**(B) there exists a nonempty `S⊆J0` with `K_SS>=0` and `M_S!=0`.**

### Proof

- If `E!=0`, T-P5-213 gives a pure active-kernel witness.
- Assume `E=0`. Any witness has some true reduced support `S⊆J0`. Theorem A forces `K_SS>=0`; Theorem B puts its `eta` in the PSD kernel cone generated by `V_S`. The flat-active reduction writes its debit as `y^T M_S y>0`, hence `M_S!=0`.
- Conversely, if some support has `K_SS>=0` and `M_S!=0`, copositivity of `M_S` gives `y>=0` with positive debit. `eta=W_Sy` is a zero of `K` and zero-loaded, so the corresponding completed-square tangent is bi-critical, has zero endpoint energy, and positive debit. T-P5-210 then gives the exact beyond-endpoint negative-energy perturbation.

QED.

This closes T-P5-213 Boundary C at the mathematical decision layer.

---

## 9. Exact rational implementation

For rational source matrices, every branch can remain exact rational:

1. compute `g=Tz` and `J0={g_i=0}` exactly;
2. test `E=N^TPN`; if nonzero, use T-P5-213 pure-active witness;
3. otherwise enumerate nonempty supports `S⊆J0`;
4. test ordinary PSD of rational `K_SS` by the existing principal-minor/LDL machinery;
5. skip non-PSD supports — they cannot be the true support of a copositive zero;
6. for PSD singular supports, enumerate a complete rational generator family of `ker(K_SS)∩R_+^S` using T-P5-212 support descent;
7. zero-extend to `W_S` and form `M_S=W_S^T G W_S`;
8. `M_S!=0` is enough for a positive-debit witness under the inherited common-zero copositivity semantics;
9. if every surviving `M_S=0`, no second-order witness exists on the complete endpoint zero set.

No eigenvectors, pseudoinverses, square roots, nonlinear root search, or generic semialgebraic optimizer are logically required.

The worst-case support count is exponential. This theorem is about exact decidability/closure, not complexity optimality. In practice one should enumerate only subsets of `J0` and prune by PSD/minor failures.

---

## 10. Regression A — a copositive zero need not be a global kernel vector

Take

`K=[[1,-1,1],[-1,1,1],[1,1,0]]`.

For `x,y,z>=0`,

`[x,y,z]^T K [x,y,z]=(x-y)^2+2z(x+y)>=0`,

so `K` is copositive.

It is not PSD: its eigenvalues are

`2, sqrt(2), -sqrt(2)`

(and `det K=-4`).

Take

`eta=(1,1,0)`.

Then

`eta^T K eta=0`,

but

`Keta=(0,0,2) !=0`.

Its true support is `S={1,2}`, and

`K_SS=[[1,-1],[-1,1]]>=0`,

with kernel generated by `(1,1)`.

Thus the supportwise PSD theorem is exact while a global `ker(K)` search would miss this zero entirely.

---

## 11. Regression B — different zero supports cannot be freely conically mixed

Take

`K=[[0,1],[1,0]]`.

For `x,y>=0`,

`(x,y)^T K(x,y)=2xy>=0`,

so `K` is copositive and indefinite.

Both rays

`e1`, `e2`

are exact zeros. Their singleton principal blocks are `[0]`, hence PSD.

But

`(e1+e2)^T K(e1+e2)=2>0`.

Therefore `Z_+(K)` is the union of the two coordinate rays, not their conic hull.

A checker that concatenates `e1,e2` into one global generator matrix `V=[e1,e2]` and then allows arbitrary `Vy`, `y>=0`, creates false zero directions. Support branches must remain separate unless a larger principal PSD block proves that the combination itself stays in a zero cone.

---

## 12. Regression C — copositivity is essential for the support-PSD upgrade

Take

`K=diag(1,-1)`, `xi=(1,1)>0`.

Then

`xi^T K xi=0`,

but `K` is indefinite and not copositive. The strict-support principal block is not PSD.

Thus the implication

`strict-positive zero => principal PSD`

is a consequence of **copositivity plus two-sided feasible perturbations on the true support**. It must not be applied to an arbitrary symmetric quadratic that merely happens to vanish at one positive vector.

---

## 13. Failure/status semantics

The following are not mathematical FAIL states:

- a particular support has `K_SS` non-PSD: skip that support; a zero may live on a smaller/different support;
- a support's kernel cone is empty except zero: skip it;
- one `M_S` is zero: that support supplies no positive debit, but another support may;
- the producer supplies an incomplete support/generator list: return `INCOMPLETE_ZERO_SUPPORT_PACKET`, not `NO_WITNESS`;
- inherited copositivity/common-zero/range hypotheses are missing: return `T214_GATE_NOT_APPLICABLE`.

A genuine local no-witness conclusion requires exhaustion of all nonempty `S⊆J0` together with complete generator packets for every surviving PSD support, plus `E=0` and `M_S=0` for all of them.

---

## 14. Minimal formal theorem statements

Suggested theorem leaves:

1. `copositive_strictZero_supportPrincipal_psd`
   - `K` symmetric copositive, `xi>0`, `xi^T K xi=0` -> `K xi=0` and `K>=0` on that support.

2. `copositive_zero_complementarity`
   - `eta>=0`, `eta^TKeta=0` -> `Keta>=0` and `eta_i(Keta)_i=0`.

3. `copositive_zeroSet_eq_union_psdPrincipalKernelCones`
   - finite supportwise union theorem.

4. `commonZero_bicritical_support_subset_zeroLoad`
   - `g>=0`, `eta>=0`, `g^Teta=0` -> `supp(eta)⊆{i:g_i=0}`.

5. `flatActive_supportPullback_copositive`
   - under `E=0`, each supportwise `M_S=W_S^TGW_S` is copositive.

6. `copositiveSchur_secondOrderWitness_iff_activeOrSupportNonzero`
   - with complete packets, witness iff `E!=0` or some supportwise `M_S!=0`.

7. `copositive_zeroSet_not_conic`
   - the explicit `[[0,1],[1,0]]` regression can be kept as a test theorem/example preventing invalid global-generator refactors.

---

## 15. Boundaries deliberately left open

### Boundary A — support explosion

The theorem is finite but worst-case exponential in `|J0|`. Finding a canonical maximal-support or clique-style pruning rule is a separate optimization problem, not needed for correctness.

### Boundary B — incomplete PSD/kernel packets

A missing support or missing extreme ray can falsely erase a valid witness. Completeness remains an explicit trusted premise until separately certified.

### Boundary C — endpoint mixed-cone nonnegativity not established

Without inherited copositivity of `K`, Theorem A is false (Regression C). Do not use a sampled/nonnegative-at-one-point surrogate.

### Boundary D — actual source/coverage/runtime/formal verification

No same-key source, selector/tube coverage, interval/Float64 sign semantics, Lean/kernel validation, 封不觉 verification, admission, registry, or P5/P8/M4 parent closure is upgraded here.

---

## 16. Recommended handoff

The next producer/checker should replace the old `K not PSD -> generic fallback` rule by:

`E!=0 -> pure-active T-P5-213 witness`

else

`J0 zero-load filter -> finite support loop -> ordinary PSD principal test -> T-P5-212 kernel generators -> M_S!=0 test`.

The first worthwhile optimization child is now sharply isolated: derive a graph/clique or maximal-support pruning rule from the sign/zero pattern of a copositive `K`, while preserving the warning that zero rays from different supports cannot be conically mixed without a larger PSD principal certificate.
