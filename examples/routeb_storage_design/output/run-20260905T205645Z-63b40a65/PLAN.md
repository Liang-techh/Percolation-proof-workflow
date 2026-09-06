# Prospective single candidate calculation

Scope: revision46, full12 radius 3/20, w(0)=0, w(t)=ct, c^2<=3,
T=1, actual J=int delta'Ldelta<=1. Own only this new directory.

Read source signed-gap run-20260905T203532Z-b2dcff09 and its exact
reference.json, the signed_gap_lean README, and affine_multiplier DERIVATION.
No trajectory, sweep, solver, dependency install, browser, broad regression,
Lean build, registry edit, or writes outside this directory.

One exact rational calculation is planned, before its execution:

1. Construct Pbar using S=K+H0, the full M0,D,G,A14 and beta=8/5:
   Pqq=beta*S/2, Pqv=S, Pvv=D+beta*M0/2,
   Pqw=-beta*G/2, Pqc=G, Pvw=-G; other ramp blocks zero.
   Vbar=Y'Pbar Y-beta*Sgap. Verify the coefficient identities for
   g=-M0*a0 and d=-2a0'M0*a0-v'Wv-beta*c*G'q+beta*v'eta,
   W=beta*D-2S. The intended selection is sigma=1/64,
   P=sigma*Pbar, k=-beta*sigma=-1/40, fixed Z=I.
2. Give a rational full-initial-ball upper storage bound via one matrix
   row-sum bound and the original single ramp parameter; import the signed
   source initial bound without re-running its enclosure audit.
3. Evaluate ONE predeclared endpoint test state q2=2,v2=2, all other
   coordinates zero, w=c=0, against all 97 published final-cell supports.
   Check the restricted M22 and potential Fourier coefficients exactly.
   Use a rational Taylor enclosure of cos(2), not floating trigonometry.
   A low storage value here obstructs a uniform endpoint certificate on
   that outer set; it is NOT evidence that this state is actually reachable.
4. Compute the antisymmetric coefficient obstruction for trying the more
   direct but potentially nonintegrable condition g=-L*a0.

Do not search over endpoint states or storage coefficients if a check fails.
Save the failed result honestly. A checked source identity or test-state
enclosure never passes the full-horizon certificate gate.

The constant candidate's scalar dissipation gate and the all-prefix endpoint
conditions will be derived in DERIVATION.md. Their uniform verification is
not part of this one small calculation.
