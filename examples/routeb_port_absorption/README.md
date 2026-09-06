# Fixed-nu finite-vector port absorption

This isolated Lean leaf proves a conditional algebraic implication for arbitrary
finite real vectors, including `Fin 2`. It does not import the robot model or
assert an interval enclosure, model identity, or SOS feasibility.

**Compilation passed** on 2026-09-05 using the pinned environment below.
See [VERIFICATION.md](VERIFICATION.md) for the real successful compile log and
all three retained failed attempts.

## Contract and sharpness

`sqNorm v = sum_i (v i)^2` is the Euclidean squared length. Using this explicit
sum avoids accidentally using the sup norm of Lean's function space.
`dot h r = sum_i h i * r i`. `rhoSq` is the source parameter `rho^2`, so an
application with a radius `rho` supplies `rho ^ 2` as this argument.

The definitions are exactly

```text
full = Dbase + sRes * sqNorm r + dot h r
phi  = Dbase - nu * rhoSq * AB - sqNorm h / (4 * (sRes + nu))
```

The proof exposes the exact identity

```text
full = phi
     + (sRes + nu) * sum_i (r_i + h_i/(2*(sRes + nu)))^2
     + nu * (rhoSq * AB - sqNorm r).
```

`conditional_absorption_bound` proves `phi <= full` from `nu >= 0`,
`sRes + nu > 0`, and the port premise `sqNorm r <= rhoSq * AB`.
`conditional_absorption` additionally takes `phi >= 0` and concludes `full >= 0`.
No separate nonnegativity assumptions on `sRes`, `rhoSq`, or `AB` are needed.

`quadratic_completion`, `quadratic_lower_bound`, and `quadratic_minimizer`
prove the exact completion, lower bound, and attainment at `r_i = -h_i/(2*a)`
for the positive quadratic coefficient `a`. Thus the factor `1/(4*a)` is sharp
for the unconstrained quadratic. `fixed_nu_certificate_iff` proves that
`phi >= 0` is equivalent to nonnegativity of
`full - nu*(rhoSq*AB - sqNorm r)` for **all** vectors `r`.
The minimizing vector need not satisfy the port constraint. No necessity
claim for constrained positivity, or existence of a suitable multiplier, is made.

`conditional_absorption_nu1_sres5` specializes the source constants to the
denominator `24`, while retaining both the port and scalar positivity premises.

## Read-only source audit

Source root: `../../../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.
The corrected report location is in this directory, not `robot_final`.

- `P5_COMPACT_ROBUST_PMI_STRUCTURE.md`: the displayed Phi formula and open obligations.
- `routeB_compact_robust_pmi_structure.jl`, lines 14-31: `NU=1`, `SRES=5`,
  `RHO2_56=469442/10000000`, the upper metric energy, and both negative Phi terms.
- `routeB_compact_direct_descriptor_structure.jl`, lines 187-200: `sres=5`,
  `Dbase`, `hvec[i]=rt[i]+2*sres*lBase[i]`, and
  `Dsplit=Dbase+sum(hvec[i]*rExpr[i])+sres*sum(rExpr[i]^2)`.
  This confirms the **positive** linear port term and the single residual charge.
  These are inspected Julia expressions, not a Lean model identification theorem.

SHA-256 of the inspected files, in the same order:

```text
6f5639bf5e0537325f243248b8ce65ef435399464e1d001eb89b5910c26b87c1
dce4beb11d882004e620e706f43c1d41deb7b121033b79ae3aa731c3c226f6d3
2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c
```

## Remaining premises

An application must still prove, on its chosen descriptor-compatible domain:

1. The actual port satisfies `sqNorm r <= rhoSq * AB`, including the justified
   metric upper bound and independently checked outward rational interval bounds.
2. The actual `phi` is nonnegative on that domain, together with the multiplier
   and denominator sign conditions.
3. The actual corrected dissipation equals `full`, with the stated `Dbase`, `h`,
   and residual accounting. Trajectory/domain membership is also needed to use
   these pointwise premises along a flowpipe.

The current report explicitly says the acceleration domain generator is missing
and Phi is unbounded below along free acceleration directions. This leaf does
not remove that obstruction. The explicit descriptor-compatible acceleration
bound/domain gate belongs to the main task. No current SOS feasibility or
robot-level certificate is claimed.

## Direct cached compilation

From PowerShell at the workspace root:

```powershell
wsl -d Ubuntu -- bash '/mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_port_absorption/verify.sh'
```

The script follows `../routeb_christoffel_power/verify.sh`: the direct Lean
4.33.1 binary, cached package libraries under `/home/z5242/sos_lean`, and Mathlib
commit `0df444a360eaa60ab8c11dca51a86af692955474`. It invokes no Lake builds,
downloads, broad tests, or solvers. Warnings are errors.

Each invocation creates a new `output/run-*` directory containing the exact
source/script snapshots, `compile.log`, and `verify.log`. The latter records
version, pin, hashes, and the compiler/verification exit codes. Successful runs
also contain the compiled `.olean`. Failed runs are retained. Every theorem
prints its axiom dependencies; standard Lean foundations may appear, but no
source-specific axiom or admitted proof is introduced.
