---
kind: review_result
review_id: review-GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-SOURCE-BINDING-20260908T152743Z
task_id: GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-SOURCE-BINDING
source_agent: codex-q6-ray-source-runtime-contract
created_at: 2026-09-08T15:27:43Z
integration_status: pending
status: EXACT_REAL_PREMISES_IDENTIFIED_RUNTIME_RELATIVE_ERROR_OPEN
admission_label: pending
proof_status: conditional_source_semantics_and_error_decomposition_only
lean_compile_status: not_run
julia_execution: false
beta_audit_repeated: false
full_regression: false
registry_eligible: false
formal_certificate_allowed: false
source_binding_proven: false
runtime_error_bound_proven: false
physical_ode_impossibility_proven: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-GRAPH-EXCLUSION-20260908T152042Z.md
predecessor_sha256: 4bf6b2529bbce744f884945f7d8074fb64c0754cf71b5bd909ae71c7c5d3a4be
requested_action: prove exact-real source premises or supply a separately authenticated runtime projected relative-error witness; do not promote conditional exclusion to admission
---

# q6-ray source/runtime contract: exact cancellations and the remaining error

This review consumes the predecessor's conditional graph-exclusion theorem;
it does not repeat its beta, mass-table inverse or target-sign calculation.
Only this new inbox file is written. Validation consists of reading the actual
DH source and comparing source/review hashes, with mathematical derivation.
No Julia, Lean, numeric ray evaluation, full regression or state/registry action ran.

The key source consequence is local and exact: for q_s=s e6, v=w=0, both the
analytic ideal-real force and the ideal-real **central-FD** force equal
`-(2/5)s e6`. FD truncation error need not be bounded to obtain this particular
force difference. Float64 execution does not inherit the identity automatically;
paired gravity evaluation, RHS assembly and solve residual require distinct
bindings. Source text and hashes do not establish those runtime premises.

## 1. Pinned source and precise semantics

The current `dhport_lib.jl` files in both directories

```text
C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/
C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_final/
```

have identical raw-byte SHA256
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.
All line references below refer to these bytes.

Keep three interpretations separate:

1. **Exact-real source:** source decimals are rational, pi/trig and arithmetic
   are real, array indexing has the displayed order, and a solve means a proved
   matrix equation. The source coefficient kappa_star is 2/5.
2. **Exact-real FD source:** the same definitions, but derivatives are the
   central-difference formulas evaluated in exact arithmetic at one fixed h≠0.
   It is a separate definition from analytic differentiation.
3. **Runtime:** decoded loaded globals, rounded stencil inputs, Float64 kernels,
   computed matrix/RHS and returned solve. These require actual artifact/method
   bindings and residual witnesses. No loaded bits or runtime outputs are supplied.

An optional unrounded model of loaded constants can reuse the geometric argument
if final DH a6=0, alpha6=0, positive masses/inertias and nonzero loaded Kp6 are
proved. Its coefficient is kappa_loaded, not silently 2/5. The source defaults
mu=1e-6 and h=1e-5 are not proof that a caller selected them: both are overridable
keywords and the globals are mutable. Pin the chosen values and same-call lifetime.

## 2. Source-derived independence, and what it does not mean

| Quantity | Source spans | Exact-real conclusion |
|---|---|---|
| final DH translation | 11, 37–41 | Last column of A6 is (0,0,d6,1); it does not depend on q6 |
| origins / midpoint COM | 32–41, 50, 67 | Every origin and midpoint is unchanged by adding s e6 to q |
| potential U | 63–70 | U(q+s e6)=U(q) for all relevant q,s |
| analytic gravity | derivative of U | G(q+s e6)=G(q); G6(q)=0, with differentiability |
| regularized mass | 48–60 | M_mu(q+s e6)=M_mu(q) in the exact-real source model |
| C/FD contraction | 77–92 | At v=0, C_h(q,v)v=0, irrespective of q6 mass invariance |
| controller | 14–17, 104–109 | It is **not** independent of q6: on the ray the surviving torque increment is −Kp6*s*e6 |

For mass invariance, origins and parent axes do not involve q6, so Jv/Jw are
unchanged. Only the sixth body rotation can depend on q6, and its inertia at
line 52 is isotropic: R6*(Ival6/3)I*R6^T=(Ival6/3)I under exact orthogonality.
The constant diagonal regularizer is also unchanged. This argument does not
assert bitwise invariance of computed Float64 M: rounded products need not obey
R6*R6^T=I exactly.

For analytic Coriolis or its exact-FD version, mass invariance implies invariance
under q6 shifts at **fixed velocity**. It does not make every coefficient with
index 6 zero, nor remove terms involving nonzero velocity6; other derivatives
of M_i6 can contribute. The ray theorem only needs the weaker zero-velocity
contraction, visible directly in `cijk*dq[j]*dq[kk]` at line 89.

No mass-invariance or full Coriolis-equivalence theorem is needed for the minimal
exclusion proof. It needs same-source D-block injectivity, force cancellation,
and the graph equation. Proving more would unnecessarily enlarge this seam.

## 3. Central-FD gravity cancellation needs stencil invariance

For exact arithmetic and a fixed h≠0, define

```text
G_h,j(q) = (U(q+h e_j)-U(q-h e_j))/(2h).
```

The q6 translation invariance from section 2 gives, for every j=1..6,

```text
U(s e6 + h e_j) = U(h e_j),
U(s e6 - h e_j) = U(-h e_j),
therefore G_h(s e6)=G_h(0), and G_h,6(q)=0.
```

This is exact at any such h; it is not a claim that G_h=grad U globally. Merely
showing U(s e6)=U(0) on the ray would be insufficient: U(q)=q1*q6 is constant on
that ray but has a varying transverse derivative. A minimal local source premise
may state the two displayed stencil equalities for each j instead of proving
global q6 invariance. The source validity domain must contain the stencils,
not only the original ray points.

`exact_ddq` forwards the same h and mu to the current-state and zero-state
`arm_MCG` calls (104–107). At v=w=0, exact source force is consequently

```text
R_h(s)= -Kp6*s*e6 + G_h(0) - G_h(s e6) - C_h(s e6,0)*0
      = -(2/5)s e6.
```

The source `mgl` array at line 18 is not used by `exact_ddq`. In particular,
the nominal 3/100 q6 restoring term is not a physical gravity term here.
The prior review's factorized-versus-runtime damping mismatch also remains
irrelevant at v=0 but cannot be ignored for an off-ray force theorem.

## 4. Minimal exact graph premises

Let C=(4,5,6), D=(1,2,3), s≠0, kappa≠0. A theorem consumer can take only:

```text
sameState: q=s e6, v=0, w=0, aC=alpha_C,
forceIdentity: R(q,0,0)=-kappa*s*e6,
graphIdentity: M_mu(q)*alpha=R(q,0,0),
remoteInjective: kernel(M_mu(q)_DD)={0}.
```

Then aC=0 forces alpha_D=0 from the D rows, contradicting the sixth row.
For the displayed exact-real source kappa=2/5. This proof does not require a
matrix inverse expansion, beta, a particular mass table, or an ODE path witness.

Source producers for those fields are:

- coordinate/global/call binding and the paired-stencil/zero-velocity/controller
  equalities above for `forceIdentity`;
- a genuine exact solve or a separately defined exact graph for `graphIdentity`;
- positive regularization and a bound to the exact mass expression for injectivity.

The raw source mass expression itself supplies a useful coercivity route:

```text
z^T M_mu(q) z = sum_b [m_b ||Jv_b z||^2
                    +(Ival_b/3)||R_b^T Jw_b z||^2] + mu||z||^2
              >= mu||z||^2,   mu>0.
```

This route does not even need R_b orthogonal: positive scalar inertia and the
same real matrix multiplication/transpose suffice. It applies to the exact mass
expression, not automatically to a rounded assembled matrix. Restrict z to D
to obtain the required kernel condition. mu=0 needs a different witness.

To connect to compact auxiliaries, retain the predecessor's reference-action
binding for vD456; it is not alpha_D or velocity_D. To use the graph along a
trajectory, additionally prove qdot=v, vdot=alpha, path-domain membership and
the desired existence/continuation properties. The four algebraic fields alone
make no reachability or physical ODE impossibility claim.

## 5. Runtime error ledger: force, solve and mass are separate

Use exact real decodings of finite machine outputs, at qhat=s e6, vhat=what=0.
Let Mhat, bhat, alphahat be the actual assembled matrix, RHS and returned solve.
Do not replace the actual RHS with a recomputed nominal one. Define

```text
delta_b = bhat - (-kappa_star*s*e6),
r_solve = Mhat*alphahat - bhat.
```

One exact decomposition of the first term is

```text
delta_b = -(kappa_loaded-kappa_star)*s*e6
          + (Ghat_0-Ghat_s) - Chat_s + epsilon_assembly.
```

Here `epsilon_assembly` is defined against real arithmetic on the decoded
loaded gain, recorded G/Chat and input values. It includes the actual broadcast,
products, additions/subtractions and their rounding; no nonexistent intermediate
array is assumed to have been exported. Chat_s is the computed Coriolis-vector
output, not the analytic coefficient tensor.

For runtime, zero velocity implies decoded Chat_s=0 only after all computed
coefficients/products are shown finite and the floating operations are bound.
For example an infinite/NaN coefficient times zero is not justified by the
real polynomial identity. Nonzero h alone does not establish finite dM or 1/h.

Two sound choices of matrix chart must be kept distinct:

| Chart | Exact decoded equation | Additional obligation |
|---|---|---|
| computed Mhat | Mhat alphahat=−kappa_star*s*e6+delta_b+r_solve | Prove Mhat_DD injective/invertible |
| ideal source M_star | M_star alphahat=−kappa_star*s*e6+e_star, where e_star=delta_b+r_solve−(Mhat−M_star)alphahat | Bound mass error as well as RHS and solve residual |

Do not charge the mass difference again in the computed-matrix chart. In the
ideal chart the mass term has the displayed minus sign. Neither chart makes a
nonzero residual into an exact source-graph equality for alphahat.

An optional sufficient numerical-matrix injectivity witness is a proved ideal
D-block lower bound lambda_D>0 together with
`||sym(Mhat_DD−M_star_DD)||_2 < lambda_D`. Then the symmetric part of Mhat_DD
is positive definite, implying injectivity even if Mhat is slightly nonsymmetric.
The textual +mu diagonal alone does not supply this floating-point inequality.
Likewise, assumed backward stability of a library solve is not a measured or
verified residual bound: supply a sound enclosure of r_solve or a justified
kernel-specific error theorem for the selected method and data.

## 6. The precise relative-error condition

Choose one of the two matrix charts A above, its matching aggregate e, and a
proved inverse for A_DD. Put K=A_CD A_DD^-1. If returned alphahat_C were zero,
eliminating the D rows would force

```text
0 = -kappa_star*s*e3 + e_C - K e_D.
```

A sufficient exclusion witness is therefore

```text
abs((e_C-K e_D)_3) <= gamma*abs(s),   gamma < abs(kappa_star).
```

This pays for the projected remote error, not just the sixth force component.
A more conservative modular bound is
`||e_C||_2 + ||K||_2*||e_D||_2 <= gamma*abs(s)`.
These inequalities are **required evidence**, not bounds obtained in this review.
Replacing kappa_star by a proved nonzero kappa_loaded is possible for a
loaded-constant theorem; it does not identify that theorem with the rational-source
one. For s=0 the strict relative exclusion is inapplicable by design.

A fixed absolute bound E yields only `abs(s)>E/abs(kappa_star)`. It cannot close
the whole punctured neighborhood. Underflow is one reason not to assume such
a uniform runtime statement: under round-to-nearest with gradual underflow,
if eta is the smallest positive subnormal and 0<kappa_loaded<1/2, the product
kappa_loaded*eta rounds to zero. If paired gravity cancels and the remaining
RHS/solve also return zero, the nonzero input has zero returned acceleration.
This is a conditional machine-semantics obstruction, not an observed run or a
claim that this exact execution occurred. A runtime theorem must restrict its
input range or explicitly cover these cases and its actual rounding mode.

## 7. Why generic FD error estimates do not close this ray automatically

Choose h to be the same decoded nonzero step used by both runtime calls. Relative
to the exact source stencil q±h e_j, a computed gravity component can be written

```text
Ghat_h,j(q)-G_star_h,j(q)
  = (deltaP_plus(q,j)-deltaP_minus(q,j))/(2h) + epsilonFD_j(q).
```

deltaP includes rounded stencil formation, potential evaluation and any selected
constant-model difference; epsilonFD covers the subtraction/division relative
to that expression. In particular, a supplied absolute bound gives

```text
abs(Ghat_h,j-G_star_h,j)
 <= (Eplus+Eminus)/(2*abs(h)) + EFD.
```

Using this separately at q_s and 0 generally gives a constant bound on
`Ghat_0-Ghat_s`; it need not shrink with |s| and can lose the exact cancellation.
No analytic O(h^2) derivative estimate is needed for the exact-real ray identity,
so introducing one here would solve a stronger, different problem.

The useful runtime producer is a **paired** difference witness for Ghat_0−Ghat_s.
For example, proving equal decoded outputs for the corresponding potential
stencils plus identical step/arithmetic can yield exact cancellation. This needs
kernel-level independence/noninterference and finite-value assumptions: generic
matrix multiplication, signed zeros, trig calls and rounding must be accounted
for; a real identity is not a bitwise execution theorem. Alternatively supply a
direct interval bound that vanishes proportionally to |s| on the declared input
range. No such producer is present in the consumed receipt.

## 8. Next proof boundary and provenance

The existing `DescriptorTermsAdapter` pattern remains appropriate: separately
bind the same source force to its formula and to its mass/acceleration action.
For this task the type must be full six-state / block456, not its existing Vec2.
For exact-real use, prove the four fields in section 4 from source semantics.
For returned Float64 use, add actual input/global/method bindings, finite stencil
and matrix data, D-block injectivity, and the chart-consistent projected error
bound in section 6. Runtime artifacts must include actual matrix/RHS/solve
outputs and their binding, not reconstructed zero values.

The earlier graph-exclusion review hash was checked as
`4bf6b2529bbce744f884945f7d8074fb64c0754cf71b5bd909ae71c7c5d3a4be`.
The reusable `examples/routeb_b45_5_descriptor_terms_adapter_lean/DescriptorTermsAdapter.lean`
hash is `1455d987f899102e68346a7d8d074b8aa472d721151b6992d373f005a955750a`.
No earlier source, receipt or review was modified. The current task supplies
conditional interfaces and source reasoning only; no runtime relative bound,
formal source theorem, full-domain residual certificate or admission is asserted.
