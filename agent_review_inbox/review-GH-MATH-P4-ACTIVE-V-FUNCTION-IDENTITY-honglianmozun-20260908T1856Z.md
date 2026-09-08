---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY-honglianmozun-20260908T1856Z
created_at: 2026-09-08T18:56:00Z
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY
source_agent: 红莲魔尊
agent: 红莲魔尊
claim_commit: 8db1006308600abfd1c962607e0881df0f102f4f
inspected_commit: 88d8ca97d6af89733d40f62b7ddd70496488e99f
integration_status: pending
admission_label: pending
status: BLOCKED_ACTUAL_SELECTOR_MISSING_FUNCTION_LEVEL_IDENTITY_AND_GAUGE_OBSTRUCTION_PROVED
proof_status: exact_function_algebra_and_integrability_obstruction; actual_runtime_binding_missing
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
threshold_mutation: false
state_mutation: false
requested_action: bind one concrete active-V producer and the initial_storage_upper consumer to the same function/convention; do not infer the scalar from P_active positivity alone
---

# GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY — 红莲魔尊

## 1. Bounded outcome

The accessible repository evidence does **not** select an actual active scalar
function.  In particular, the current convention artifact explicitly records

```text
runtime_observation      = null
source_binding_proven    = false
active_function_selected = null
```

while the same artifact records the numerical consumer token

```text
initial_storage_upper = 492033745203/25600000000000
active_threshold      = 1.
```

Therefore this task cannot honestly return `V_active = ...` as an actual
runtime/source identity from the GitHub checkout inspected here.  The external
DH source root named by the predecessor review is not present as a repository
file, and the committed convention artifact deliberately did not import or
execute that producer.  This is now a **field-level selector obstruction**, not
an ambiguity to resolve by choosing the most favorable normalization.

What can be closed mathematically is the exact function/gauge contract that the
missing source witness must satisfy, and the centered candidate's explicit
function identity on the fixed X0.

## 2. The explicit scalar candidate already justified at function level

On the fixed block-only initial set X0 used by the predecessor, write

```text
a = 2029689/400000,
c = 205029/40000.
```

The source-algebra review gives the explicit centered scalar

```text
F(q,v) = W(q,v) - a
       = (1/2) v_B^T M_BB(q) v_B
         + B (cos(q5)-1)
         + (3/10) q4^2 + (1/4) q5^2.             (1)
```

Thus, at the mechanical anchor q_B=v_B=0,

```text
F(0,0)=0,
W(0,0)=a,
Z(0,0)=a+c=4079979/400000,
```

where `Z=W+c` is the source storage-shift convention in the fixed analytic
g0=0 configuration.  Constant shifts imply

```text
dF = dW = dZ,                 Hess F = Hess W = Hess Z,              (2)
```

wherever these functions are twice differentiable.  Hence **derivative/Hessian
data cannot distinguish W, F, and Z**.  Their initial-value and barrier
contracts are nevertheless different.

The already established all-X0 value estimate is

```text
F <= 27/4000 < 492033745203/25600000000000,                           (3)
```

whereas raw W and source-shifted Z have uniform lower bounds above 1 on the
same fixed ideal configuration.  Equation (3) is therefore a valid candidate
initial theorem for the explicitly named function F; it is not evidence that
the actual consumer uses F.

For the cross-term branch, on this same X0 the previously reduced expression is

```text
T-a = F + eps q_B^T M_BB(q) v_B,   eps=1/1000,                       (4)
```

with the separate absolute cross allowance already recorded upstream.  This is
a different function and cannot be silently identified with F either.

## 3. Gauge-fixing theorem: P_active does not determine V_active

This is the exact mathematical reason the source selector is indispensable.
Let H be any constant symmetric matrix.  Every scalar of the form

```text
V_{ell,c}(x) = (1/2)(x-x*)^T H (x-x*) + ell^T(x-x*) + c             (5)
```

has

```text
Hess V_{ell,c} = H.                                                   (6)
```

Thus even a proved positive-definite `P_active=H` leaves both a linear gauge
`ell` and an additive gauge `c` undetermined.  If a separately source-bound
vector field satisfies

```text
Pvec(x)=H(x-x*)+ell = grad V(x),                                     (7)
```

then (7) fixes `ell` but still leaves the additive constant `c` free.  One
scalar anchor value, e.g. `V(x*)=c`, is still necessary before a numerical
`initial_storage_upper` or barrier threshold can be attached to V.

In the special centered convention

```text
Pvec(x)=H(x-x*),   V(x*)=0,                                          (8)
```

the unique scalar in the quadratic family is

```text
V(x)=(1/2)(x-x*)^T H(x-x*).                                         (9)
```

This is the precise guard against the invalid inference

```text
P_active positive definite  ==>  the consumer's scalar Lyapunov function
                                 has been identified.
```

Positive definiteness supplies coercivity only **after** the scalar/function
binding and normalization have been fixed.

## 4. State-dependent integrability guard

If the active block is a state-dependent matrix field `P(x)`, positivity is
even less sufficient.  Suppose a proposed gradient is

```text
g_i(x)=sum_k P_ik(x) (x_k-x*_k).                                    (10)
```

A necessary local condition for a C2 scalar V with `grad V=g` is the closed
one-form condition

```text
partial_j g_i = partial_i g_j    for all i,j.                        (11)
```

If P is symmetric, (11) reduces to

```text
sum_k [partial_j P_ik - partial_i P_jk] (x_k-x*_k) = 0.              (12)
```

On a simply connected/star-shaped domain, the standard closed-one-form
hypothesis makes (11) sufficient as well, and then one may define V by a path
integral; for the radial path,

```text
V(x)-V(x*) = integral_0^1 g(x*+t(x-x*)) dot (x-x*) dt.               (13)
```

If instead one claims **Hess V=P(x)** directly, the derivative tensor of P must
satisfy the mixed-partial compatibility

```text
partial_k P_ij = partial_i P_kj                                      (14)
```

(together with symmetry of P), equivalently the third derivative tensor must
have the required permutation symmetry.  SPD of P does not imply (14).

### Exact SPD path-dependence counterexample

Let, on `|eps*y|<1`,

```text
P(x,y) = [[1, eps*y],
          [eps*y, 1]].                                                (15)
```

P is symmetric positive definite there.  With `x*=0`, the proposed field
`g=P(x,y)*(x,y)` is

```text
g1 = x + eps*y^2,
g2 = eps*x*y + y.                                                     (16)
```

But

```text
partial_y g1 = 2 eps y,
partial_x g2 = eps y,                                                 (17)
```

so the one-form is not closed for `eps*y != 0` and no scalar V has this g as
its gradient on such a neighborhood.

The obstruction is visible as literal path dependence.  From (0,0) to (a,b),
integrating g first along x then y gives

```text
I_xy = a^2/2 + b^2/2 + eps*a*b^2/2,
```

whereas y then x gives

```text
I_yx = a^2/2 + b^2/2 + eps*a*b^2.
```

Hence

```text
I_yx-I_xy = eps*a*b^2/2,                                             (18)
```

which is generically nonzero despite pointwise SPD.  This is the exact failure
mode the active-V source binding must rule out if P_active is state dependent.

A simpler Hessian-only obstruction is `P(x,y)=diag(1+y,1)` on `|y|<1/2`:
P is SPD, but `partial_y P_11=1` while `partial_x P_21=0`, contradicting (14).

## 5. Derivative identity for the explicit centered mechanical candidate

For (1), along a differentiable path `(q_B(t),v_B(t))`, the function-level
chain rule is

```text
dF/dt
 = v_B^T M_BB(q) dot(v_B)
   + (1/2) v_B^T [d/dt M_BB(q)] v_B
   - B sin(q5) dot(q5)
   + (3/5) q4 dot(q4)
   + (1/2) q5 dot(q5).                                                (19)
```

If the actual mechanical source additionally binds `dot(q_B)=v_B`, (19)
becomes the usual kinetic-plus-potential power identity.  Crucially, the
constant gauges a and c disappear from (19), exactly as in (2); therefore an
Edot/P_active proof cannot retroactively decide whether the scalar consumer is
W, F, or Z.

## 6. Exact smallest remaining source witness

To close the assigned task rather than merely the mathematics, the runtime or
source owner must provide one same-configuration packet containing all of:

1. `active_V_source`: exact file/function/expression that computes the scalar
   consumed by the barrier, with state embedding and configuration key;
2. `normalization`: an explicit equality fixing its additive gauge, preferably
   a named anchor value such as `V(x*)=0`, `=a`, or `=a+c`;
3. `initial_storage_upper_source`: the exact producer/consumer of
   `492033745203/25600000000000`, with evidence that this token bounds the same
   scalar function, not merely another constant-shift convention;
4. `P_active/Pvec bridge`: if the quadratic block is used, an equality showing
   `Pvec=grad V` and/or `P_active=Hess V` on the required domain, including the
   factor-of-two convention;
5. if P_active is state dependent, either the actual scalar V itself or a
   checked closed-one-form/mixed-partial condition sufficient for path
   independence.

A hash of an external file without its accessible function identity is not
sufficient to fix items 1-4.  Conversely, once items 1-3 are present, the
constant-shift ambiguity is removed and the already-proved X0 bound can be
attached only to the matching convention.

## 7. Admission boundary

This review proves a function-level/gauge theorem and a sharp integrability
obstruction.  It does **not** select F merely because F satisfies the recorded
upper bound, does not modify threshold 1, and does not claim that raw W or Z is
the actual runtime storage.  The current accessible evidence explicitly leaves
`active_function_selected=null`, so `GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY`
remains pending on the concrete source/runtime selector and same-function
`initial_storage_upper` binding.
