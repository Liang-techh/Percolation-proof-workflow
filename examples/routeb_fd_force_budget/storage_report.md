# Exact obstruction to the unshifted storage

For the actual `Kp=(1,4/5,7/10,3/5,1/2,2/5)`, **W is negative arbitrarily close to q=0**. Both the proposed global quadratic lower matrix H and the actual Hessian of W at zero have exact inertia `(4 positive, 2 negative, 0 zero)`. This rules out `W≥0` and any positive quadratic lower bound for the unshifted storage on a full neighborhood of zero. It does not rule out coercivity at infinity: W is coercive, and an explicit constant shift makes it globally positive with a scalar quadratic lower bound.

## Exact coefficient calculation

The read-only inputs are `routeB_fourier_potential_rational.csv` and `dhport_lib.jl` in `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`. The potential contains 17 Gaussian-rational rows, all with zero imaginary part, and exact equality between conjugate coefficients. The nonconstant rows comprise 12 positive and 4 negative coefficients. The constant cancels from `U(q)-U(0)`.

Every original row is counted once, including both members of each conjugate pair; there is no additional factor of two. Thus

\[
W(q)=\tfrac12\sum_i Kp_i q_i^2+
\sum_{\nu\ne0}a_\nu(\cos(\nu\cdot q)-1).
\]

For positive a, `cos x-1≥-x²/2`; for negative a, `a(cos x-1)≥0`. Therefore

\[
W(q)\ge\tfrac12 q^T Hq,\qquad
H=\operatorname{diag}(Kp)-\sum_{a_\nu>0,\nu\ne0}a_\nu\nu\nu^T.
\]

In contrast, the actual Hessian is
`J=∇²W(0)=diag(Kp)-Σ_{ν≠0}a_ν ννᵀ`, with both signs retained. The script computes the complete rational matrices and exact factorizations `H=L_H D_H L_Hᵀ`, `J=L_J D_J L_Jᵀ`, verifies reconstruction entry by entry, and stores them in `storage_results.json`. Both pivot sign sequences are `+,-,-,+,+,+`.

An especially simple rational witness is `e₂=(0,1,0,0,0,0)`:

| quadratic form | exact value |
|---|---|
| `e₂ᵀ H e₂` | `-3439979/800000` |
| `e₂ᵀ J e₂` | `-1709689/400000` |
| `e₁ᵀ H e₁ = e₁ᵀ J e₁` | `1` |

The first row alone would only obstruct this lower-bound method. The second row obstructs nonnegativity of W itself: W is analytic, `W(0)=0`, `∇W(0)=0`, and its second derivative along e₂ is strictly negative. The following explicit analytic estimate removes any reliance on a numerical Hessian or an unspecified small-neighborhood radius.

## A rigorous negative neighborhood witness

All nonconstant frequencies have `|ν₂|=1`. Their signed coefficient sum is
`A=2029689/400000`, so exactly

\[
W(te_2)=A(\cos t-1)+\tfrac25t^2.
\]

Taylor's theorem with the fourth derivative bounded by one gives
`cos t-1≤-t²/2+t⁴/24`. Hence, for every real `|t|≤1`,

\[
W(te_2)\le\left(\tfrac25-\tfrac{11}{24}A\right)t^2
=-\frac{6162193}{3200000}t^2.
\]

This is strictly negative whenever `0<|t|≤1`. At the explicit rational configuration `q=e₂/10`, retaining the fourth-order term gives

\[
W(e_2/10)\le-\frac{683199037}{32000000000}<0.
\]

These statements concern the exact-real Fourier/DH model. Binary parameter conversion and Float64 trigonometric execution are not enclosed here. If a lifted representation is used, its c/s coordinates must represent these same real angles; independent circle variables do not change this configuration-space conclusion.

## Consequences and alternatives preserving the controller

For `E(q,v)=½vᵀM*(q)v+W(q)`, the implication
`E≥(9401/2000000)||v||²` is false: set v=0 and take the negative configurations above. Thus the previous FD-force calculation remains a valid **conditional** result, but this unshifted E does not establish its kinetic premise. Likewise, no inequality `p45≤κE` with κ>0 can hold globally: at `q=te₂,v=0`, p45=0 while κE<0. A smaller full neighborhood of zero cannot fix either problem.

One valid global alternative is a constant shift. Since `cos x-1≥-2` and the negative-coefficient contributions remain nonnegative, define

\[
B=2\sum_{a_\nu>0,\nu\ne0}a_\nu
=\frac{4079979}{400000}.
\]

Then the actual positive Kp gives the scalar certificate

\[
W(q)+B\ge\tfrac12\sum_iKp_iq_i^2\ge\tfrac15\|q\|^2.
\]

This also proves `W(q)→+∞` as `||q||→∞`, despite its negative values near zero. Using the previously checked exact-real regularized mass lower bound,

\[
E+B\ge\frac{9401}{2000000}\|v\|^2+\tfrac15\|q\|^2,
\qquad
p45\le\frac{1600000}{9401}(E+B).
\]

The shift leaves the dynamics and energy derivative unchanged. If the available tube is `E≤Ecap`, use **`Vcap=Ecap+B`** in the existing FD-force budget, and shift the initial storage value by B as well. This supplies a rigorous interface, not a completed tube or terminal certificate. The global comparison is coarse: even at the origin it returns the upper bound `16319916/9401` for p45. Moreover, a negligible shift cannot work: evaluating the negative estimate at t=1 shows that any constant C making `W+C≥0` globally must satisfy `C≥6162193/3200000`. Sharpening the constant shift or directly bounding `p45-κE` using the full Fourier potential could improve the terminal comparison without altering the controller; that optimization is not performed here.

A second, restricted alternative is available on `q1=q2=q3=q6=0`. The principal (4,5) block of H is exactly
`diag(459399/800000,338197/800000)`. Subtracting `(2/5)I` gives positive pivots `139399/800000,18197/800000`; hence
`W≥(q4²+q5²)/5` on that configuration slice. This does not cover a full neighborhood or prove a trajectory stays on the slice. A block-only initial set is insufficient; the coupled original dynamics would require a separate invariant-slice or remote-coordinate estimate. No gain changes, altered equilibrium target, or unsupported extension from p45 to all coordinates is used.

## Reproduction and scope

Run from the workspace:

```powershell
python -B examples/routeb_fd_force_budget/storage_check.py
```

The standard-library script writes only `storage_results.json`; this report and the script also use the requested `storage_` prefix. Exact matrix reconstruction, witness inequalities, conjugate accounting, and shifted/slice constants passed. SHA-256 checks confirmed that both source inputs and every existing non-storage output were unchanged. No existing script was rerun, and no broad tests, Lean work, solver, or runtime infrastructure was added.
