kind: review_result
task_id: GH-MATH-P3-FD-REMAINDER
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-08T15:07:00Z
inspected_commit: 141e4005b5d31421c416fcd0399010224b5c0ebf
claim_file: agent_review_inbox/claim-GH-MATH-P3-FD-REMAINDER-honglianmozun-20260908T1453Z.md
claim_commit: f87a28c39cd52439b1023f67ab714271b35cc358
target: NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean
status: pending mathematical child
admission_label: pending

# Scope

This review supplies the minimal mathematics contract requested by the queue for a centered finite-difference derivative remainder: the exact C3/step/full-shifted-region hypotheses, the sharp `1/6` remainder constant, a uniform-cell/variable-step form, and a linear residual-budget handoff. It also preserves the required `x^3` sharpness/counterexample and records the precise failure boundaries.

This review does **not** claim the deployed evaluator has been source-bound to this theorem, does not claim Float64/libm/rounding correctness, and does not claim that the queue-level target filename has been located at a canonical source path or compiled at the inspected commit.

# 1. Pointwise centered-FD remainder

For `h > 0`, define

`D_h f(x) := (f(x+h) - f(x-h)) / (2h)`.

Assume:

1. `[x-h,x+h]` lies in a region `J` on which `f` is `C^3`;
2. `M >= 0`;
3. `|f'''(t)| <= M` for every `t in [x-h,x+h]`.

Then

`|D_h f(x) - f'(x)| <= M h^2 / 6`.

A division-free raw-defect form is cleaner for a trusted checker. Define

`delta_h f(x) := f(x+h) - f(x-h) - 2h f'(x)`.

Then

`3 |delta_h f(x)| <= M h^3`.

Equivalently, after squaring nonnegative quantities,

`9 (delta_h f(x))^2 <= M^2 h^6`.

The normalized squared form is

`36 (D_h f(x) - f'(x))^2 <= M^2 h^4`.

## Proof

Taylor expansion with third-order remainder gives

`f(x+h) = f(x) + h f'(x) + (h^2/2) f''(x) + R_+`,

`f(x-h) = f(x) - h f'(x) + (h^2/2) f''(x) + R_-`,

with

`|R_+| <= M h^3/6`,

`|R_-| <= M h^3/6`.

Subtracting cancels both the zeroth-order and second-order terms exactly:

`delta_h f(x) = R_+ - R_-`.

Hence

`|delta_h f(x)| <= |R_+| + |R_-| <= M h^3/3`,

which is exactly

`3 |delta_h f(x)| <= M h^3`.

Since `2h>0`, dividing by `2h` yields

`|D_h f(x)-f'(x)| <= M h^2/6`.

This cancellation is the structural reason the centered stencil is second order.

# 2. Uniform shifted-region theorem

Let the base state cell be `X=[a,b]`, and let `h_max>0`. Define the full shifted source region

`X_shift := [a-h_max, b+h_max]`.

Assume `f` is `C^3` on `X_shift` and

`|f'''(t)| <= M`

for every `t in X_shift`, with `M>=0`.

Then for every `x in X` and every step satisfying

`0 < h <= h_max`,

the entire stencil `[x-h,x+h]` lies in `X_shift`, and therefore

`|D_h f(x)-f'(x)| <= M h^2/6 <= M h_max^2/6`.

This remains valid for a state-dependent step `h=h(x)` provided the source contract proves pointwise

`0 < h(x) <= h_max`.

Thus the minimal uniform packet is not merely `(C3 on X, h_max)`. It is:

- positive step;
- full shifted-region containment;
- uniform third-derivative bound on that shifted region.

A slightly more abstract sufficient hypothesis is that `f''` is Lipschitz with constant `L2` on the full shifted region. The same proof gives `L2 h^2/6`. The requested source-facing contract can stay with `C^3` and `M=sup |f'''|`, which supplies such a Lipschitz constant.

# 3. Sharpness and the required x^3 witness

Take

`f(t)=t^3`.

Then

`D_h f(x) = ((x+h)^3-(x-h)^3)/(2h) = 3x^2+h^2`,

while

`f'(x)=3x^2`.

Therefore

`D_h f(x)-f'(x)=h^2`.

Since `f'''(t)=6`, the theorem gives

`M h^2/6 = 6 h^2/6 = h^2`.

Equality is attained. In raw form,

`delta_h f(x)=2h^3`

and

`M h^3/3 = 6h^3/3 = 2h^3`.

Hence the constant `1/6` is sharp over the class controlled only by a uniform bound on `|f'''|`.

# 4. Why pointwise C2 data are insufficient

Fix a center `x0` and consider

`f_A(t) := A (t-x0)^3`.

For every real `A`, all functions in this family have exactly the same 2-jet at the center:

`f_A(x0)=0`,

`f_A'(x0)=0`,

`f_A''(x0)=0`.

But their centered-FD error is

`D_h f_A(x0)-f_A'(x0) = A h^2`.

For fixed `h>0`, its magnitude is arbitrarily large as `|A|` grows. Therefore **no finite centered-FD remainder budget can be inferred from the pointwise C2 jet at the center alone**. A full-stencil third-derivative bound, or an equivalent full-stencil Lipschitz bound on the second derivative, carries genuinely necessary information.

This is stronger than merely saying a C3 proof is convenient: the missing information cannot be reconstructed from center-point C2 data.

# 5. Why the shifted region is necessary

A third-derivative bound only on the base cell `X` does not control a centered stencil that exits `X`. If `x+h` or `x-h` lies outside the region on which the bound is certified, a smooth extension can be modified outside `X` while preserving all values/derivatives on `X`, yet changing the off-cell stencil value and hence the finite difference.

Therefore the theorem must fail closed unless the complete stencil lies inside the region carrying the C3/Lipschitz-`f''` certificate. This is an information boundary, not a proof artifact.

# 6. Linear residual-budget handoff

Suppose a downstream residual component has already been source-typed in the form

`r_exact_i(x) = sum_j a_ij(x) f'_ij(x)`

and the finite-difference version uses the **same coefficients at the same state**:

`r_FD_i(x) = sum_j a_ij(x) D_{h_j} f_ij(x)`.

Assume for every term `j`:

`|a_ij(x)| <= A_ij`,

`|f'''_ij(t)| <= M_ij` on the complete shifted stencil for that term,

and `0 < h_j` (with any required uniform upper bounds supplied by the shifted-region packet).

Define

`e_i := r_FD_i-r_exact_i`.

Applying the scalar theorem term by term gives

`|e_i| <= B_i`,

where

`B_i := sum_j A_ij M_ij h_j^2 / 6`.

Equivalently, with

`C_i := sum_j A_ij M_ij h_j^2`,

a division-free consumer can use

`6 |e_i| <= C_i`,

or the squared form

`36 e_i^2 <= C_i^2`.

For a common step `h`, this reduces to

`|e_i| <= (h^2/6) sum_j A_ij M_ij`.

For a vector residual, the componentwise packet is

`e_i in [-B_i,B_i]`.

If a scalar Euclidean budget is truly required downstream, one may further derive

`||e||_2^2 <= sum_i B_i^2`.

However, the componentwise enclosure should be retained when possible because later Lyapunov consumers may exploit signed/correlated structure more efficiently than a prematurely scalarized norm bound.

## Type boundary

This aggregation theorem is valid only after source binding proves that the actual consumer is the stated linear combination with the same coefficients and the same differentiated primitives. It does **not** authorize replacing a nonlinear evaluator, a differently normalized residual, or a coefficient that is itself finite-differenced by this formula. Those require their own chain-rule/Lipschitz/structural bridge.

Therefore this review establishes the mathematical residual-budget interface, not the deployed evaluator binding.

# 7. Failure boundaries / exact obstructions

The theorem must not be applied under any of the following silent weakenings:

- `h=0`: the normalized centered finite difference is undefined.
- stencil leaves the C3-certified region: no bound follows from base-cell data alone.
- only pointwise values of `f,f',f''` are certified at the center: the `A(t-x0)^3` family gives arbitrarily large error with identical center 2-jet.
- sampled/empirical values of `f'''` are used as though they were a rigorous supremum on the whole stencil.
- the deployed stencil is asymmetric, clipped, one-sided, or otherwise differs from `(f(x+h)-f(x-h))/(2h)`.
- the residual consumer is nonlinear or uses coefficients different from those in the exact residual identity.

# 8. Candidate theorem statements for formalization

The mathematical API can be split into the following children:

1. `central_fd_raw_defect_le_of_third_deriv_bound`
   - hypotheses: `0<h`, `0<=M`, full-stencil C3, `|f'''|<=M` on the stencil;
   - conclusion: `3*|f(x+h)-f(x-h)-2*h*f'(x)| <= M*h^3`.

2. `central_fd_error_le_sixth_third_deriv`
   - same hypotheses;
   - conclusion: `|D_h f(x)-f'(x)| <= M*h^2/6`.

3. `central_fd_error_uniform_on_shifted_interval`
   - hypotheses: base cell, `h_max>0`, C3 and third-derivative bound on `[a-h_max,b+h_max]`;
   - conclusion uniform over `x in [a,b]` and `0<h<=h_max`.

4. `central_fd_error_variable_step_on_shifted_interval`
   - same packet with `h=h(x)` and `0<h(x)<=h_max`.

5. `central_fd_linear_residual_budget`
   - consumes componentwise coefficient bounds and scalar FD remainder bounds;
   - conclusion `6|e_i| <= sum_j A_ij M_ij h_j^2`.

6. `central_fd_x_cube_sharp`
   - exact equality regression for `f(t)=t^3`.

7. `central_fd_pointwise_c2_insufficient`
   - obstruction family `f_A(t)=A(t-x0)^3`.

For a checker-oriented Lean route, the raw-defect lemma is preferable as the core: prove two Taylor remainder inequalities, use exact centered cancellation, triangle inequality, then ordered-ring arithmetic. Normalized forms can be descendants that divide only after `0<h` is available. The `x^3` regression should reduce to ring normalization.

# 9. Dependencies and remaining obligations

Dependencies used here are only the queue assignment and standard one-variable Taylor remainder mathematics. No source-level evaluator identity was assumed beyond the explicitly conditional residual formula in Section 6.

At inspected commit `141e4005b5d31421c416fcd0399010224b5c0ebf`, connector searches/root fetch did not establish a canonical repository path for the queue-level target `NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean`. Consequently no Lean build or executable checker is claimed in this review.

The narrow remaining source-side obligation is:

1. expose the actual canonical central-FD call site / theorem scaffold;
2. prove the deployed stencil is exactly symmetric central FD with positive step;
3. prove every shifted evaluation lies in the region carrying the uniform C3 (or Lipschitz-`f''`) bound;
4. source-bind the actual residual expression to the linear combination consumed in Section 6, or provide a different structural bridge if it is nonlinear.

Only after those bindings exist may the resulting `B_i` be passed as a certified evaluator/residual error budget to downstream Lyapunov energy closure.

# 10. Evidence / checker status

Read this round before claim/work:

- `agent_review_inbox/README.md`
- `agent_review_inbox/task_queue.md`
- `agent_review_inbox/collaboration_board.md`
- recent inbox/commit state

Inspected repository head before claim: `141e4005b5d31421c416fcd0399010224b5c0ebf`.

Claim commit: `f87a28c39cd52439b1023f67ab714271b35cc358`.

Executable checker / Lean compilation for the queue-level target: **not run / not claimed**, because the canonical target source path was not established by the repository connector at the inspected commit. The result here is a mathematics contract and exact obstruction package, deliberately separated from evaluator/source/provenance/admission work.
