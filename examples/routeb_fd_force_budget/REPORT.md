# Conditional exact FD force-error budget

For the specified six damping and disturbance coefficients, the existing exact Fourier data give

\[
\sum_{i=1}^6 \frac{e_i^2}{2D_i}\le R(V_{cap})
\le \frac{3103V_{cap}^2+152V_{cap}+4}{10^{21}},
\qquad e=C_{analytic}-C_{fd}+G_{analytic}-G_{fd},
\]

provided **all six** velocities satisfy
`(9401/2000000) ||v||² ≤ V ≤ Vcap`, with `Vcap ≥ 0`, and FD denotes the exact-real centered difference of the exported Fourier model at `h=1/100000`. Here C denotes the six-vector of quadratic Coriolis forces, not a matrix. This is an exact rational conditional computation, not a Float64 execution enclosure or a new Lean certificate. The main task owns the Lean energy composition.

The unrounded value is `R(1) = 6488721350704815125680143589 / 1991694478098124800000000000000000000000000000`, approximately `3.257889913367e-18`. Consequently the supplied Lean inequality has the conditional specialization

\[
P+e\cdot v\le \frac{631227}{1086800}w^2+R(V_{cap}).
\]

The additive defect remains at `w=0`; subtracting it from a coefficient of `w²` is not homogeneous absorption.

## Coefficient derivation and source checks

Read-only source directory: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

`routeB_fourier_rational_probe.py:110` constructs the mass and potential from exact Gaussian-rational Fourier arithmetic. Its DH offsets/twists are exact multiples of pi/2, its lengths, masses, gravity `981/100`, and inertias are exact decimal rationals. Each COM is the midpoint of successive origins; joint axes are taken before the current transform. The translational contribution is `m_i Jv_iᵀJv_i`; the rotational contribution is `(I_val_i/3) Jw_iᵀJw_i`, without an additional mass factor. This uses exact rotation orthogonality to simplify Julia's `Ri Ii Riᵀ`. The Fourier mass is unregularized; the intended port mass adds `10^-6 I`.

`routeB_analytic_fourier_dynamics_probe.py:53` derives each derivative remainder using

\[
|\nu-\sin(\nu h)/h|\le |\nu|^3h^2/6,\qquad
\epsilon_{ij,k}=\frac{h^2}{6}\sum_\nu
(|\Re a_{ij,\nu}|+|\Im a_{ij,\nu}|)|\nu_k|^3.
\]

The potential coefficients give the corresponding `β_i` by the same formula. This bounds the difference operator applied to the **mass**, not a difference operator applied to the already assembled analytic Christoffel tensor. The script reconstructs all 216 mass-derivative bounds and six gravity bounds from the input coefficient CSVs, checks equality against `routeB_fourier_fd_error_bounds.csv`, and checks the CSV polynomials against the small exact source constructor. It does not run any target script's `main()`. It also checks conjugate symmetry and mass symmetry.

With `A_ijk = (ε_ij,k + ε_ik,j + ε_jk,i)/2 ≥ 0`, Julia's Christoffel convention (`dhport_lib.jl:73`) implies

\[
|e_i|\le\sum_{j,k}A_{ijk}|v_jv_k|+\beta_i.
\]

The previous audit discarded the component structure by summing all A entries. Recomputed `Σ_ijk A_ijk = 12390647/192000000000000000` agrees exactly with its ledger; `Σ_i β_i²/D_i = 90362741420079/12646400000000000000000000000000000` also agrees. Its `csum*r³ + gravity_constant` is a different, unsquared energy remainder allocation and is not the budget required here.

For arbitrary component caps `|v_j| ≤ r_j`, use the directly available bound
`Σ_i (Σ_jk A_ijk r_j r_k + β_i)²/(2D_i)`. For a uniform cap r, define `α_i=Σ_jk A_ijk`, giving `Rbox(r)=Σ_i(α_i r²+β_i)²/(2D_i)`. All α values and all 216 A values are in the generated CSVs. For example, the separately assumed six-component cap `r=15` gives `Rbox(15) ≈ 2.238860912197e-17`.

The sharper energy result uses `b_i=max_j Σ_k A_ijk`. Since each A_i is symmetric,
`Σ_jk A_ijk |v_jv_k| ≤ Σ_j (Σ_k A_ijk)v_j² ≤ b_i ||v||²`, by `2|v_jv_k|≤v_j²+v_k²`. Thus `|e_i|≤a_i Vcap+β_i`, where `a_i=(2000000/9401)b_i`:

| i | D_i | disturbance G_i | a_i | β_i |
|---|---|---|---|---|
| 1 | 13/10 | 1 | 257371/150416000000000 | 0 |
| 2 | 11/10 | 1/2 | 257371/150416000000000 | 68343/800000000000000 |
| 3 | 19/20 | 3/10 | 109951/150416000000000 | 21909/1000000000000000 |
| 4 | 4/5 | 1/5 | 173713/300832000000000 | 6867/8000000000000000 |
| 5 | 13/20 | 1/10 | 520451/1353744000000000 | 6867/4000000000000000 |
| 6 | 1/2 | 1/20 | 1/4834800000 | 0 |

The exact polynomial `R(Vcap)=Σ_i(a_i Vcap+β_i)²/(2D_i)` has coefficients:

| power of Vcap | exact coefficient | approximate display |
|---|---|---|
| 2 | 98881705013075533/31867111649569996800000000000000000 | 3.102939045761e-18 |
| 1 | 4234629090421/27973836800000000000000000000000 | 1.513782010204e-19 |
| 0 | 90362741420079/25292800000000000000000000000000000 | 3.572666585751e-21 |

`dhport_lib.jl:14` supplies D=`Kd+b_fr`. Its disturbance force is `(gw_coef .* I_val)w`, whose intended exact-real coefficient is the G vector in the table; using `gw_coef` alone would give the wrong force. Recalculation gives `Σ_i G_i²/(2D_i)=631227/1086800`. G does not enter R because the supplied theorem already budgets its contribution.

## Exact premises and the velocity-domain limitation

The Fourier remainder holds for every real `q∈R⁶`; there is no local q box restriction. For lifted coordinates, require `c_k=cos(q_k), s_k=sin(q_k)` and hence `c_k²+s_k²=1`, for all six k. FD shifted evaluations must represent the same q with exact shifts `q±h e_k` (equivalently, exact circle rotations by ±h). Independent circle points at q and at its FD samples do not encode a difference quotient. Circle equations alone do not identify lifted c/s with a separately used q. Smoothness is automatic for these finite Fourier polynomials; no flowpipe or trajectory regularity is established by the arithmetic audit.

The kinetic lower coefficient is supported structurally: let `u_j=z_j v_j` for exact unit DH axes, and `ω_i=Σ_{j≤i}u_j`. For the scalar prefix matrix `T_ij=1_{j≤i}`, the script independently verifies positive exact LDL pivots of `Tᵀ diag(I_val/3)T - (47/5000)I`. Applying this inequality to each Cartesian component of u proves rotational mass ≥ `(47/5000)||v||²`. Adding positive semidefinite translation and the exact regularizer gives `M*≥(9401/1000000)I`. Therefore a storage `V=½vᵀM*v+W(q)` with `W≥0` has the required kinetic lower bound. For other storage definitions, including cross terms or a potential shifted below zero, that lower bound must be established separately. A mass lower bound alone does not prove it for an arbitrary V. No assertion that an actual trajectory satisfies `V≤Vcap` is made here.

`p45=(3/2)(q4²+q5²)+(4/5)(v4²+v5²)≤η` only gives `v4²,v5²≤5η/4`. In particular η=27/10 and 28/5 justify caps 2 and 8/3 for v4,v5 only. The old audit's use of those caps for all six components requires an additional full-velocity bound or a proved invariant slice with all remote velocities zero. A block-only initial condition does not prove such an invariant slice in the coupled dynamics. The generated numerical cases labeled `all_six_component_cap_*_conditional` explicitly assume those full caps; no inference from p45 is used.

## Missing Float64 and force-balance terms

The exact model's potential coefficients are all real conjugate pairs, so `U(-q)=U(q)`. Hence both `Ganalytic(0)` and the exact centered `Gfd(0)` are exactly zero. Thus Julia's `G0v` compensation (`dhport_lib.jl:102`) creates no additional exact-real constant bias in this particular model. Its Float64 evaluation still needs an enclosure.

For a precise runtime interface, define `M*=M_Fourier+10^-6 I`, `Cfd*,Gfd*` as its ideal exact-real FD forces, and let hats denote computed Julia values at the same interpreted q,v,w. Define

\[
\Delta M=\widehat M-M^*,\quad
\delta C=\widehat C-C_{fd}^*,\quad
\delta G=\widehat G-G_{fd}^*,\quad
\delta\tau=\widehat\tau-(-K_pq-Dv+Gw),\quad
r_s=\widehat M\widehat a-\widehat b,
\]

where `bhat` is the actual rounded vector passed to the mass solver, and `δb=bhat-(tauhat-Chat-Ghat)` records its final subtraction rounding. Then, as an exact identity between interpreted floating values,

\[
M^*\widehat a=-K_pq-Dv+Gw-C_{analytic}-G_{analytic}
+ e + \underbrace{\delta\tau-\delta C-\delta G+\delta b+r_s-\Delta M\widehat a}_{\xi}.
\]

This identifies the missing quantities without assuming any is zero:

- `δC,δG`: binary parameter conversion (lengths, mass, inertia, 9.81, pi/2), trigonometric evaluation, FK products, COM/Jacobian formation, nonexact rotation orthogonality, potential/mass sums, perturbed sample arguments `fl(q±h)`, subtraction/division in FD, and Christoffel/velocity accumulation. With exact arguments and denominator, sample mass errors E⁺,E⁻ contribute at most `(E⁺+E⁻)/(2h)` to a derivative; the ledger contains none of this cancellation amplification. Binary `hhat` requires the `hhat²/h²` adjustment to truncation plus argument and denominator errors. These terms must be decomposed consistently to avoid counting parameter effects twice.
- `δtau`: computed `G0v`, rounded D additions, rounded Kp, the `gw_coef` divide-then-multiply path, and torque arithmetic. In particular parameter perturbations include `-ΔKp q-ΔD v+ΔG w`. A uniform additive runtime budget then needs q and w caps, or a separate revised supply bound for w-dependent errors; the exact FD bound's global q domain does not supply such caps.
- `ΔM ahat`: parameter/rounding error of the evaluated mass and its regularizer, multiplied by acceleration. Matching the exact regularizer cancels it from ideal derivatives, but does not bound its floating evaluation error. Comparing an unregularized storage mass with the regularized port instead adds the explicit `-10^-6 ahat` mass-mismatch term. A component estimate needs `Σ_j |ΔM_ij||ahat_j|`, so acceleration or validated force/inverse bounds are needed.
- `δb,r_s`: final force-vector assembly rounding and the residual of the actual mass solve. The backslash expression named `exact_ddq` is a Float64 solve; the FD ledger does not certify its residual or inverse. Time integration/state representation defects, if the claimed object is a numerical trajectory, require a further validated ODE connection.

If validated component bounds `|ξ_i|≤ζ_i` become available, the compatible total force budget is `Σ_i(a_i Vcap+β_i+ζ_i)²/(2D_i)`. Adding a separate squared runtime-error budget without cross terms is not justified. No numerical ζ, mass perturbation, solver residual, or parameter enclosure has been supplied by this ledger.

## Reproduction

From `C:/Users/z5242/Desktop/重构版/工作流`, run:

```powershell
python -B examples/routeb_fd_force_budget/recompute.py
```

`--source` accepts another directory containing the same input filenames. The script uses only the Python standard library, reads the target, and writes `results.json`, `component_bounds.csv`, and `christoffel_bounds.csv` beside itself. Results include exact fractions and source SHA-256 values. The run checked the constructor/CSV match, all 222 derivative records, both historical scalar totals, the actual controller vectors, and the six positive exact prefix LDL pivots. No regressions, browser, solver runs, Lean changes, or infrastructure rebuilds were performed.
