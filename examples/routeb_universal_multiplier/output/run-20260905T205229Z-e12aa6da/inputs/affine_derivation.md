# Affine residual multipliers recover valid signed dissipation candidates

The physical objective and all initial/input sets remain unchanged. This leaf
improves the mathematical certificate class proposed in SIGNED_WORK.md; it
does not supply a uniform state-cell certificate or prove J<=1.

## Why the homogeneous multiplier can lose a valid certificate

Let M,L be symmetric, M delta=r, and Vdot=d+2 g' delta. The desired local
inequality is delta'Ldelta+Vdot<=b. The previous homogeneous multiplier
2(Z delta)'(M delta-r) gives the sufficient block PSD condition

    Hhom = [b-d, -(g+Z'r)'; -(g+Z'r), Z'M+MZ-L] >=0.

This is VALID but not complete: every such matrix requires b-d>=0, even
when a negative 2g'delta makes the actual dissipation inequality true.
Increasing Z or changing its sparsity cannot repair a negative top-left
entry. This is a restriction introduced by the certificate, not a physical
necessity and not a counterexample to M4.

## The affine condition and exact cancellation

Allow the multiplier vector z+Z delta. Its symmetric block matrix is

    Haff = [ b-d-2z'r,             -(g+Z'r-Mz)' ;
             -(g+Z'r-Mz),           Z'M+MZ-L     ].

For any delta, exact expansion gives

    [1;delta]' Haff [1;delta]
       = b-d-2g'delta-delta'Ldelta
         +2(z+Z delta)'(M delta-r).

Thus Haff>=0 and the actual residual equality imply the requested inequality.
Neither a sign on storage V nor a contraction factor is assumed. The six
acceleration components do not need separate box bounds. Matrix PSD remains
a premise to be proved uniformly on the source/time cells, not a numerical
solver status that can be promoted to a theorem.

The companion routeb_signed_gap_lean/ResidualMultiplier.lean implements the
finite-vector expansion and its implication. Its compiler receipts, not
this derivation alone, determine formal proof status.

## Pointwise completeness when an exact inverse is available

For a fixed symmetric invertible M and positive definite L, let

    Z=M^-1 L,  z=M^-1 g,  delta=M^-1 r,
    margin=b-d-2g'delta-delta'Ldelta.

Then

    Haff = [margin+delta'Ldelta, -delta'L; -Ldelta, L]
         = [1, -delta'; 0, I] diag(margin,L) [1, 0; -delta, I].

Consequently Haff>=0 exactly when margin>=0. This is a constructive
pointwise result. A state-dependent inverse is NOT silently replaced by a
constant rational matrix, and no uniform rational multiplier of a prescribed
degree is thereby guaranteed to exist.

For a finite, source-informed ansatz use the checked rational R=M0^-1 and
set Z=R L, z=R g, dM=M0-M. The matrix entries reduce to

    top    = b-d-2g'Rr,
    cross  = -(L R r+dM R g),
    bottom = L-L R dM-dM R L.

The audit verifies all 43 entry identities as exact polynomial coefficients
in 21 independent symmetric dM entries and all six entries of g and r.
This keeps correlations between storage derivative, source residual and
mass variation. It is not an independent norm bound on each term. Bottom
positivity and the full block PSD must still be proved on actual source cells.

The stable alternative Z=I has bottom 2M-L>=L under the existing M>=L
premise. Choosing z=R g then gives cross=-(r+dM R g), top unchanged. It is
a valid alternative when the frozen-inverse bottom cannot be bounded positive,
but the complete signed Schur expression must be evaluated before norms.

## Exact source-instantiated witness inside the original initial ball

The audit independently reads the source mass and potential Fourier CSVs,
adds the original mu=1/1000000, and recomputes all Christoffel contributions
at q=0, v=(e4+e5)/20, w=0, eta=0. It obtains

    ||(q,v)||^2=1/200 <9/400,
    C=(21/10000000)e1, G=0,
    a0=-M0^-1 Dv, a=M0^-1(-Dv-C), delta=-M0^-1 C.

Let E=delta'Ldelta>0 and choose the LOCAL storage derivative data
g=-Ldelta, d=E, b=E/2. These are an admissible algebraic storage jet for
testing the certificate class, NOT a supplied global Lyapunov/storage function.
Then E+d+2g'delta=0<b. Every homogeneous matrix has top-left -E/2<0, so
none can certify this valid local signed inequality. The affine choices above
give Haff congruent to diag(E/2,L), strictly positive. Exact rational matrix
entries and the congruence are retained in the result.

The witness is a single exact source point, not a simulated trajectory or
an all-initial-data result. There is no claim that J was bounded by this
choice of a storage jet, nor that the physical system violates any target.

## Evidence and next obligation

`output/run-20260905T202634Z-e39dc9a3` completed with AUDIT_EXIT_CODE=0.
All inputs and the executed scripts were copied and hashed before execution.
SymPy performs exact rational polynomial coefficient checks; no floating
spectra, sampling, numerical solver or trajectory integration was used.

Next: construct compatible global/time-dependent storage P,k and affine
multipliers z,Z; prove the resulting source block PSD on covered cells and
all-prefix endpoint/supply bounds. Combine with the signed gap derivative,
gravity twist floor, actual eta bound, and formal first-hit theorem. Until
then formal_certificate_allowed=false, and no registry admission is justified.
