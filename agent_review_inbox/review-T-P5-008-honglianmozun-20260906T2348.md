---
kind: review_result
review_id: review-T-P5-008-honglianmozun-20260906T2348
task_id: T-P5-008
source_agent: 红莲魔尊
claimed_at: 2026-09-06T23:39:33-06:00
created_at: 2026-09-06T23:48:00-06:00
inspected_commit: 0c71758e08d074be82ff3679faed6641ae357e06
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_storage_renormalized_energy_ledger_and_source_bind_remaining_terms
---

# T-P5-008 — deployed force-error split: two apparent biases are storage terms, one FD term is cubic power, and only controller/solve remain genuine bias candidates

## Scope

This review follows the coordinator's explicit P5 dispatch after `T-P5-005`.
The question is not whether the generic `DHPowerBinding.forceError` can imply a
velocity-relative bound—it cannot—but what the **actual deployed structure**
allows us to remove from that residual before attempting any small-gain bound.

Inspected repository objects:

- `examples/routeb_dh_power_binding/DHPowerBinding.lean`
  - blob `5e440147a2428262d1beea31ccb56c27d2818b07`;
  - exact abstract split
    `mass + controller + C + G + solveResidual`.
- `examples/routeb_dh_power_binding/FDForceBudget.lean`
  - blob `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36`;
  - current force-level FD envelope has positive additive offsets in channels
    1--4, but those offsets are enclosure slack rather than evidence that the
    actual error is nonzero at equilibrium.
- `examples/routeb_source_binding_audit/REPORT.md`
  - blob `8bc5cd5444473396caa13af107428f0350cca742`;
  - records the deployed source structure
    `M(q)=M_DH(q)+10^-6 I`, central FD `C/G` with `h=10^-5`, and acceleration
    solve from `tau-Cdq-Gq`.
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`
  - blob `e8e544007588e06fbac12638c7f71976fc094db9`;
  - proves the generic exact cubic Christoffel power identity.
- `examples/routeb_source_binding_audit/snapshots/current_exact/PotentialSlice.lean`
  - blob `2f7c009bc3d150544a257e43a5a84eeccd40a294`;
  - freezes the 17-row real cosine potential. Every frequency component is in
    `{-1,0,1}`.
- `examples/routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv`
  - blob `d7840a9c2e9c0485bcd78f209af7143e4e3ed303`;
  - mass modes contain coordinate frequencies of magnitude 2 as well as 1,
    so the mass/C finite-difference error does not reduce to one universal
    scalar multiplier.

No claim is made here that the frozen Fourier objects are already physically
identified with deployed DH. `B45-1/B45-2/B45-4` remain source-binding
obligations. The conclusions below separate algebra that is exact once those
bindings are supplied from facts already visible in the frozen objects.

## 1. Start from the exact `forceError` ledger

The current Lean interface writes, channelwise,

```text
e = e_M + e_tau + e_C + e_G + e_solve,
```

with

```text
e_M     = (Ma-Mi) a,
e_tau   = tauI-tauA,
e_C     = cA-cI,
e_G     = gA-gI,
e_solve = Mi a -(tauI-cI-gI).
```

The deployed source text gives the specific implemented mass

```text
Mi(q) = Ma(q) + epsilon I,
epsilon = 10^-6,
```

if `Ma` is taken to be the unregularized DH mass and the source-binding theorem
identifies the two constructions. Therefore

```text
e_M = -epsilon a.                                  (1)
```

A force-level residual treatment would try to bound `epsilon |a|` by velocity,
which is generally impossible. But in the energy identity this is the wrong
place to charge the term.

## 2. The `10^-6 I` mass regularizer is exactly removable by changing kinetic storage

Let

```text
T(q,v)         = 1/2 v^T Ma(q) v,
T_epsilon(q,v) = 1/2 v^T Mi(q) v
                = T(q,v) + epsilon/2 * ||v||^2.
```

Along any differentiable trajectory with `v'=a`,

```text
d/dt [epsilon/2 * ||v||^2] = epsilon <v,a>.        (2)
```

The mass-error power from (1) is

```text
<v,e_M> = -epsilon <v,a>.                          (3)
```

Hence (2) and (3) cancel **exactly**.

This is not a smallness argument and does not require `a` to be proportional to
`v`. The correct P5 architecture should therefore use the implemented
regularized kinetic energy, rather than paying the regularizer as an additive
force residual.

A second exact fact is useful: because `epsilon I` is constant in `q`, every
central difference satisfies

```text
D_h,k (Ma + epsilon I) = D_h,k Ma.                 (4)
```

So moving the regularizer into kinetic storage creates no new Christoffel/FD
term.

### Lean-friendly derivative-level form

Before formalizing full calculus, the algebraic seam can be stated as:

```lean
-- eM = -eps*a and dExtra = eps * dot v a cancel in power.
theorem regularizer_power_cancel
    (eps : ℝ) (v a : Fin 6 -> ℝ) :
    (∑ i, (-eps * a i) * v i) + eps * (∑ i, v i * a i) = 0
```

Then a storage theorem can identify the second summand with the derivative of
`eps/2 * sum_i v_i^2`.

## 3. The frozen cosine potential makes the gravity central difference exactly conservative

The current frozen potential has the form

```text
U(q) = sum_r A_r cos(nu_r · q),
```

and every coordinate of every `nu_r` is `-1`, `0`, or `1`.
Let

```text
h = 1/100000,
sigma = sin(h)/h.
```

For one cosine mode and coordinate `k`,

```text
D_h,k cos(nu·q)
 = [cos(nu·q + nu_k h)-cos(nu·q-nu_k h)]/(2h)
 = -sin(nu·q) * sin(nu_k h)/h.
```

If `nu_k=0`, both the exact derivative and central difference are zero. If
`nu_k=±1`,

```text
sin(nu_k h) = nu_k sin(h),
```

so

```text
D_h,k cos(nu·q) = sigma * d/dq_k cos(nu·q).
```

By linearity over the 17 frozen rows,

```text
G_FD(q) = sigma * G_exact(q).                       (5)
```

Therefore

```text
e_G = G_exact-G_FD = (1-sigma) G_exact
    = grad[(1-sigma) U].                            (6)
```

Thus, **conditional on the still-open physical potential source binding**, the
FD gravity discrepancy is not a genuine dissipative bias either. It is exactly
removed by replacing the potential part of storage `U` with

```text
sigma U.
```

Indeed, if the old energy derivative contains `<G_exact,v>` and then pays
`<(G_exact-G_FD),v>` as a residual, subtracting `(1-sigma)U` from storage
cancels precisely that residual power.

This is much stronger than using the positive-offset force envelope in
`FDForceBudget.lean`.

### Equilibrium consequence

At `q=0`, every frozen cosine mode has zero exact derivative, hence both
`G_exact(0)=0` and `G_FD(0)=0`. So the positive channel offsets in the current
FD envelope must **not** be interpreted as proof of a physical nonzero gravity
bias at equilibrium. They are only conservative global enclosure constants.

### Important boundary

The repository explicitly says the frozen Fourier potential is not yet proven
to be the deployed DH potential. Equation (5) is therefore an exact theorem
about the frozen 17-row object and a **candidate physical theorem after B45-2**,
not current true-DH admission evidence.

## 4. After storage renormalization, the exact power ledger is much smaller

Let the original storage be the one used in the current mechanical/controller
energy identity. Define the structurally adapted storage

```text
E_tilde
  = E
  + epsilon/2 * ||v||^2
  - (1-sigma) U
  = [regularized kinetic] + [sigma * physical potential]
    + [existing controller/storage terms].          (7)
```

Under the two explicit semantic premises

```text
Mi = Ma + epsilon I,
gI = sigma gA,
```

and the ordinary derivative identities for kinetic/potential energy, the
current five-term force-error ledger reduces to

```text
E_tilde_dot
 = supply(v,w)
   + <e_tau,v>
   + <e_C,v>
   + <e_solve,v>.                                  (8)
```

The mass regularizer and gravity-FD error disappear from the residual budget.
This is the highest-value structural simplification found in this pass.

A source-independent algebraic theorem can avoid calculus by defining

```text
dE_tilde := dE + epsilon<v,a> -(1-sigma)<gA,v>
```

and proving from `implemented_energy_identity` plus
`Mi=Ma+epsilon I`, `gI=sigma gA` that (8) follows.

Recommended theorem signature:

```lean
theorem storage_renormalized_force_ledger
    (eps sigma : ℝ)
    (Ma Mi : Mat) (v a tauA tauI cA cI gA gI : Vec)
    (hMi : ∀ i j, Mi i j = Ma i j + (if i=j then eps else 0))
    (hgI : ∀ i, gI i = sigma * gA i) :
    -- original force-error power + the two storage derivative corrections
    -- equals controller mismatch + C mismatch + solve residual power
```

The theorem should be kept abstract from the numerical `eps=10^-6` and
`sigma=sin(10^-5)/(10^-5)` specialization.

## 5. The C finite-difference mismatch is cubic power, not additive bias

Let

```text
T_kij   = partial_k Ma_ij,
T^h_kij = D_h,k Ma_ij.
```

Build `C(T)` and `C(T^h)` by the same Christoffel contraction. The already
formalized generic Christoffel power identity gives, exactly,

```text
<v, C(T)v - C(T^h)v>
 = 1/2 * sum_{i,j,k} (T_kij-T^h_kij) v_i v_j v_k.  (9)
```

Hence the FD-C mismatch power vanishes to third order in velocity. In
particular it is exactly zero at `v=0` even before any smallness estimate.

This means it belongs naturally in the **relative/local dissipative lane**, not
in an additive equilibrium-bias lane.

If a same-domain derivative-error tensor bound

```text
|T_kij-T^h_kij| <= mu_kij
```

is available, then

```text
|<e_C,v>|
 <= 1/2 * sum_{i,j,k} mu_kij |v_i v_j v_k|.        (10)
```

A box or energy sublevel bound can turn (10) into

```text
|<e_C,v>| <= kappa_C * A(v),
```

which is exactly the relative-power input needed by the P5 strict-decay lane.
No componentwise `|e_C,i| <= rho_i |v_i|` theorem is required.

### Why no single gravity-style scalar exists for mass FD

The frozen mass Fourier CSV contains frequencies of magnitude `2` as well as
`1`. For a Fourier frequency `n` in one coordinate,

```text
exact derivative multiplier = n,
central-FD multiplier        = sin(n h)/h,
error multiplier             = n - sin(n h)/h.     (11)
```

Since the ratio depends on `|n|`, the mass derivative cannot in general be
obtained from the analytic derivative by one global scalar `sigma`.

However the source has only small integer frequencies in the frozen expansion,
and the generic inequality

```text
|x-sin x| <= |x|^3/6
```

gives, for `|n|<=2` and `h=10^-5`,

```text
|n - sin(nh)/h| <= |n|^3 h^2/6 <= 4 h^2/3.        (12)
```

Thus a purely exact-rational coefficient summation over the frozen mass rows
can produce a very small global `mu_kij`; the missing step is the B45-1/B45-4
source identification, not a new energy identity.

## 6. What remains a genuine additive-bias candidate

After (7)--(9), only two classes remain structurally capable of producing a
nonzero force error independent of velocity/configuration vanishing:

### A. Controller/parameter mismatch `e_tau = tauI-tauA`

If the deployed controller is proven definitionally equal to the analytic
controller with the same constants, this term is zero. If constants,
feed-forward values, saturation, or Float64 evaluation differ, it may contain
an affine or constant part. The current abstract interface does not decide
this.

A useful source theorem should split

```text
e_tau(q,v,w) = Lq q + Lv v + Lw w + b_tau,
```

or prove `b_tau=0` directly at the designated equilibrium.

### B. Runtime linear-solve residual `e_solve`

`DHPowerBinding` deliberately defines

```text
e_solve = Mi a -(tauI-cI-gI)
```

because a Float64 backslash result is not an exact real solve. This term is
zero under an exact-real solve premise. For the deployed runtime it needs an
independent residual theorem.

At the equilibrium it also vanishes if the source proves both

```text
rhs = tauI-cI-gI = 0,
a = 0,
```

but neither fact follows from the generic interface. Therefore `e_solve` should
remain in the **bias/runtime lane** until a typed zero-equilibrium or relative
runtime theorem is supplied.

## 7. Precise classification table

| source term | force-level appearance | energy classification | equilibrium status from current structure |
|---|---|---|---|
| `+10^-6 I` mass regularizer | `-epsilon a` | **exact storage term** via `+epsilon/2 ||v||^2` | no bias needs to be charged after storage change |
| central-FD C | `C_exact-C_FD` | **cubic power**, eq. (9); local relative/absorbable candidate | zero whenever `v=0` |
| central-FD G | `G_exact-G_FD` | for frozen 17-row potential, **exact conservative storage term** `(1-sigma)U` | frozen Fourier object gives zero at `q=0`; physical claim awaits B45-2 |
| controller mismatch | `tauI-tauA` | relative/affine/bias depending source theorem | OPEN |
| solve residual | `Mi a-(tauI-cI-gI)` | runtime bias/relative term | OPEN; zero only under explicit RHS/solve equilibrium contract |

Therefore the current positive-offset `FDForceBudget.envelope` should remain a
safe fallback enclosure, but it is too coarse to decide which physical terms
are true equilibrium biases.

## 8. New Lyapunov architecture suggested by the deployed implementation

The natural candidate is no longer the original storage plus a five-term
force residual. It is

```text
V_tilde
 = 1/2 v^T (M(q)+10^-6 I) v
   + sigma U(q)
   + U_controller(q),

sigma = sin(10^-5)/(10^-5),                         (13)
```

with derivative ledger

```text
V_tilde_dot
 = nominal supply
   + P_C_FD_error(v,q)
   + <e_tau,v>
   + <e_solve,v>,                                  (14)
```

where `P_C_FD_error` is cubic in `v` by (9).

This candidate is mathematically better aligned with the deployed source:

- the regularized mass is treated as the mass defining kinetic storage;
- the special cosine-frequency structure makes the current gravity central
  difference exactly a scaled gradient of the frozen potential;
- only the genuinely nonconservative/runtime pieces are left as residuals.

### Coercivity warning

Equation (13) is only a derivative-architecture improvement. It is **not yet a
Lyapunov certificate**. The repository already contains a separate storage
nonnegativity obstruction for the current potential/proportional-energy slice.
The modified coefficient `sigma` must receive its own positivity/coercivity
analysis; no positivity claim is made here.

## 9. Smallest next theorem chain

The shortest mathematically meaningful continuation is now:

```text
P5-A  regularizer_storage_cancel
      Mi=Ma+epsilon I
      => mass error disappears from energy ledger

P5-B  cosine_central_fd_gradient_scaling
      all potential frequencies in {-1,0,1}
      => G_FD = sigma G_exact

P5-C  gravity_storage_rescale
      P5-B + source potential binding
      => gravity FD error disappears after U -> sigma U

P5-D  christoffel_fd_power_error
      => exact cubic identity (9)

P5-E  tensor-error-to-damping absorption
      same-domain bound on T-T^h + velocity domain
      => |P_C_FD_error| <= kappa_C A(v)

P5-F  controller/solve split
      prove either relative gain or explicit bias for the only two remaining
      runtime/source terms.
```

This is strictly shorter than trying to prove a five-term componentwise
`|forceError_i| <= rho_i |v_i|` bound.

## 10. Formalization handoff

Highest-value source-independent Lean children:

```lean
theorem regularizer_power_cancel ...

theorem force_ledger_after_mass_gravity_storage_shift
    -- assumptions Mi=Ma+eps I and gI=sigma*gA
    -- conclusion: corrected force-error power contains only tau/C/solve

theorem christoffel_difference_power
    (T Th : Fin 6 -> Fin 6 -> Fin 6 -> ℝ) (v : Fin 6 -> ℝ) :
    dot v (C T v - C Th v)
      = (1/2) * sum_i,j,k ((T-Th) k i j) * v i*v j*v k
```

Then a separate Fourier-calculus child should prove

```text
all |nu_k| <= 1 for the 17 potential rows
  -> centralDiffGradient h U = (sin h/h) * grad U.
```

Do not fuse that theorem with physical DH source binding.

## Remaining blockers

- B45-1: deployed DH mass = frozen/evaluated Fourier mass + `10^-6 I`;
- B45-2: deployed potential = frozen 17-row Fourier potential;
- B45-4: source `Cdq` = central-FD Christoffel contraction with the documented
  indexing;
- source theorem for controller equality/mismatch;
- runtime solve residual bound and equilibrium zero condition;
- positivity/coercivity of the modified storage (13);
- same-domain velocity/domain bounds to absorb the cubic C-FD power;
- P8 flowpipe/domain coverage and final M4 integration.

## Conclusion

The deployed source structure is materially better than the generic
`forceError` obstruction suggests. Two terms that look like additive residuals
at force level are exact storage corrections, and the C-FD term is cubic in
velocity power:

```text
five-term forceError
  -- change storage -->
controller mismatch + cubic C_FD power + solve residual.
```

The physically meaningful next question is therefore no longer “can every
force error be bounded by `rho |v|`?” It is “can the cubic FD-C power be
absorbed on the covered velocity domain, and do controller/solve have a genuine
zero-equilibrium or small-gain theorem?”

No registry/admission promotion is requested. Formalization belongs to the
Lean agents, independent gate review to 封不觉, and final integration to 梁智炜.
