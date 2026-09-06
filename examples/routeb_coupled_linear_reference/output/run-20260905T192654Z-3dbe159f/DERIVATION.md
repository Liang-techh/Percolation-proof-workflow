# Exact coupled six-axis reference

This sidecar constructs coefficient data for the main task's explicit nominal
balance premise. It does not prove physical-DH or Float64 identification, run
a trajectory/eigenvalue screen, or assume stability of the full nominal model.
Actual run status and immutable evidence are recorded in ATTEMPT_HISTORY.md.

## Definition and conventions

For the full Gaussian-rational mass Fourier ledger,
`M0_ij=sum_nu a_ij,nu+mu*delta_ij`, with mu=1/1000000. All conjugates are counted
exactly once as CSV rows, and imaginary sums vanish. The potential ledger has
17 real, conjugate-symmetric rows. Its exact gradient at zero vanishes and
`H0_ij=-sum_nu a_nu nu_i nu_j`. No finite-difference Hessian is substituted.

From the Julia source's intended real parameters:

```
K=diag(1,4/5,7/10,3/5,1/2,2/5),
D=diag(13/10,11/10,19/20,4/5,13/20,1/2),
G=(1,1/2,3/10,1/5,1/10,1/20),
R=Mref_BB=diag(350003/3000000,200739/4000000).
```

D uses Kd+b_fr. G uses the exact divide-then-multiply interpretation of
`gw_coef .* I_val`, not gw_coef alone. The reference acceleration is

```
a0=-M0^-1 (K+H0)q-M0^-1 Dv+M0^-1 Gw.
```

For x=(q1,...,q6,v1,...,v6),

```
x'=A12*x+B12*w,
A12=[0 I; -M0^-1(K+H0) -M0^-1 D],
B12=[0; M0^-1 G].
```

The JSON saves all rational entries of M0,H0,M0^-1,A12,B12, the three
acceleration maps, the stiffness matrix, and a positive-pivot LDL factorization
of M0. Both inverse products are checked entrywise, as is the complete 6x13
coefficient identity `M0*a0=-(K+H0)q-Dv+Gw`. These are polynomial coefficient
identities for all real q,v,w, not evaluation at sample points.

## Actual two-row reference residual; retained remote correlations

Let B=(4,5), D_remote=(1,2,3,6). Define the residual (not the historical port)

```
e0=R*a0_B+K_B*q_B+D_B*v_B-G_B*w.
```

It is a 2x13 exact map in (q,v,w), saved separately as a 2x12 state matrix and
a two-entry input vector as well. Because R=M0_BB, the nominal balance implies
the particularly compact identity

```
e0=-M0_BD*a0_Dremote-H0_B*q,
M0_BD=[7/60, 0, 0, 1/60;
       -21/80000, 41827/800000, 8189/160000, 0].
```

Writing c=20601/400000, the potential Hessian block rows are
`H0_4*=0`, `H0_5*=(0,-c,-c,0,-c,0)`. Thus equivalently

```
e0_4=-(7/60)a0_1-(1/60)a0_6,
e0_5=(21/80000)a0_1-(41827/800000)a0_2-(8189/160000)a0_3
       +c(q2+q3+q5).
```

Both compact expressions are audited against the complete 2x13 residual map.
Remote accelerations here mean the same coupled nominal a0, not independent
inputs or a projected two-axis solve. No q2/q3 cancellation, sign correlation,
or velocity coupling is discarded. Exact supports and nonzero cross terms
are exported, including the factorized PSD instantaneous cost matrix
`E' diag(5/8,10/13) E` for e0=E(q,v,w). Its off-diagonal coefficient is twice
the corresponding Gram entry. This is not an integrated residual-cost bound.

## Relation to earlier linear_direction.py

The earlier script constructs precisely the same intended exact-real M0,H0,
K,D,G, then converts to NumPy floats and calls floating linear solves. This
audit compares the saved rational M0/H0 fields in its linear_output/result.json
when available; it never executes that script. It separately reconstructs the
same 14-state augmentation (x,w,c), with w'=c,c'=0, and its 2x14 residual map.
The c column of that instantaneous residual is zero. All these new maps are
rational, whereas the old matrix exponentials, quadrature and adversarial
direction were unenclosed numerical results. None of those numerical results
is promoted to a bound here.

## Stability and source boundary

The exact stiffness quadratic form at the coordinate vector e2 is negative.
This is not inconsistent with M0 positive definite or D positive definite.
Indeed the symmetric pencil lambda² M0+lambda D+(K+H0) has a negative smallest
eigenvalue at zero and is positive definite for sufficiently large positive
lambda; continuity forces a singular pencil at some lambda>0. Hence the
associated full nominal first-order system has a positive real growth mode.
No eigenvalue computation is needed or performed. Do not reuse the stable
decoupled momentum-filter assumption for this coupled model.

The reference is an analytic Fourier linearization at (q,v,w)=0: dM terms
multiply the zero equilibrium acceleration, and analytic C is quadratic in v.
The Julia source actually evaluates centered-FD C/G in Float64 and solves with
backslash. Thus this is not claimed to be its exact numerical Jacobian. FD
truncation, represented parameters, mass/trig arithmetic and solve errors stay
in the main task's source/implementation seam. The main separately handles
`r=(M0-M)a0+H0q-G-C+eta` and the coupled resolvent reduction; neither is duplicated
or assumed discharged by this coefficient audit.

## Reproduction and evidence

Run `python -B examples/routeb_coupled_linear_reference/verify.py` from the
workspace. Every run creates a new directory, snapshots this sidecar and all
source inputs, records their SHA256 hashes, then opens the terminal log before
executing the saved audit. The parent waits synchronously and appends the exit
code before closing the log. Failed attempts, if any, remain intact.
Only files below this new directory are written. No Lean compilation, broad
regression, trajectory, Taylor flow, target modification or registry/state
write is part of this leaf.
