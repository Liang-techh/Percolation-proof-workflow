# A fixed multiplier and a concrete nonnegative storage family

This is a mathematical reduction of the original full12 initial ball, whole
ramp family and T=1 RouteB block45 goal. It is not a completed certificate.
The existing conditional prefix reaches 9/16; nothing here extends that
verified analytic prefix by itself. The FD/Float64 source binding is still open.

## 1. Fix Z=I without a contraction assumption

Write M delta=r, where eta is included in r once, L>0, and M>=L.
For Vdot=d+2g'delta, the affine residual multiplier z+delta gives

    H = [ b-d-2z'r, -(g+r-Mz)'; -(g+r-Mz), 2M-L ].

H>=0 implies delta'Ldelta+Vdot<=b. Its bottom block D=2M-L satisfies
D-L=2(M-L)>=0 globally on the source mass-bound domain. No epsilon or
statewise bottom-block search is needed. Moreover this fixed-Z class is
pointwise lossless: solve Mz=g-r+Ldelta. Then

    quad H(s,v) = (b-d-2g'delta-delta'Ldelta)s^2
                  +(v-s delta)'D(v-s delta).

This construction uses the actual inverse M^-1; it does not license treating
the frozen inverse M0^-1 as the actual one.

## 2. A rational frozen-center sufficient scalar gate

Let R=M0^-1, Q=L^-1, dM=M0-M and use

    h=Rr,
    z=Rg+(RLR-R)r,
    e=dM(2h+z),
    mhat=b-d-2g'h-h'Lh-2(z+h)'dM h.

Recenter the affine matrix at h, not at the unknown actual delta. Exactly,

    quad H(s,v) = mhat*s^2 - 2s e'(v-sh) + (v-sh)'D(v-sh).

For y=v-sh its square completion is

    y'(D-L)y + (y-sQe)'L(y-sQe) + s^2(mhat-e'Qe).

Consequently the single sufficient condition is

    b >= d+2g'h+h'Lh+2(z+h)'dM h+e'Qe.

The signed mixed term is not replaced by separate absolute values. The gate
is exact when M=M0. For fixed source state it is convex quadratic in the
storage-gradient coefficients. The original affine matrix is affine in
those coefficients when Z=I. A uniform source-domain bound is still needed.

The exact audit checks 49 recentering entries, one symbolic metric square
completion and 49 pointwise-lossless entries, with 21 independent symmetric
mass-defect entries. It also checks the actual rational M0 inverse and L/Q.
These are coefficient identities, not interval or kernel source proofs.
The companion Lean module proves finite-vector versions independently.

## 3. Actual-energy storage cancels g identically

The already compiled literal Fourier remainder theorem gives
Rpot(q)>=-q4^4/40. The original output domain

    Pout=3/2(q4^2+q5^2)+4/5(v4^2+v5^2)<=28/5

implies q4^2<=56/15. Set

    W0 = v'M0v/2-Sgap+(7/75)q4^2
       = v'M(q)v/2+Rpot+(7/75)q4^2.

W0>=0 on this domain and M>=0, since
q4^2(7/75-q4^2/40)>=0. This does not assume global positivity of Rpot.

For tau=1-t and nonnegative a_j,p_ji,c_j, j>=1, use

    f(t)=sum a_j tau^j,
    p_i(t)=sum p_ji tau^j,
    h_c(t)=sum c_j tau^j,
    V=f W0+sum p_i q_i^2+h_c c^2.

V>=0 on every covered prefix and V(1)=0. In Y'P(t)Y+kSgap form,

    k=-f, Pvv=f M0/2,
    Pqq=diag(p_i)+(7f/75)E44, Pcc=h_c,
    all other blocks zero.

Thus g=Bdelta'PY+(k/2)M0v=0 exactly. The signed-gap derivative cancels
the actual acceleration defect in the derivative of nominal kinetic energy:

    W0dot=-v'(K+H0)q-v'Dv+v'G w+(14/75)q4v4+v'eta.

Vdot=f'W0+f W0dot+sum(p_i' q_i^2+2p_i q_i v_i)+h_c' c^2.
It is linear in all storage coefficients. With g=0, the frozen scalar source
cost h'Lh+2(z+h)'dM h+e'Qe is independent of these coefficients. Therefore
finite collocation of Vdot+cost<=0 is an LP, without a conic solver. An LP
solution only proposes coefficients; it does not cover unsampled states.
The c^2 storage term matters: ramp input can generate positive J from x0=0.

## 4. Preserve the full initial ball and strict prefix logic

The exact reference M0 has every absolute row sum below one, so a concrete
rational diagonal-dominance proof can establish M0<=I. Under the separately
audited initial Sgap>=-3/10000 and ||(q,v)||^2<=9/400,
W0(0)<=231/20000. Do not charge every coordinate the full ball radius.

More sharply let A=sum a_j, Pi=sum p_ji, Hc=sum c_j and choose beta with

    beta>=A/2,
    beta>=Pi+(7A/75)*[i=4] for each i.

Then the shared initial ball and c^2<=3 give

    V(0)<=9 beta/400+3 A/10000+3 Hc.

If this upper bound is strictly below one and the uniform dissipation gate
holds on pre-exit prefixes, integration and V>=0 give J<1 there. The earlier
direct-output gain bridge then gives strict Pout<28/5, closing that output
exit condition by continuity. It is NOT valid to assume the output domain
for the entire trajectory before this continuation argument. Other joint
domains, existence/regularity, eta and the source/comparator bindings remain
separate obligations. No full-horizon theorem or registry admission is claimed.

## 5. Necessary local gate before more nonlinear coefficient fitting

For analytic eta=0 semantics, scale (q,v,c) together toward zero at fixed t,
keeping w=tc. The source has M(0)=M0, gradU(0)=0 and HessU(0)=H0.
Then r=O(||(q,v,c)||^2), so the residual energy cost is fourth order, while
W0 has quadratic part v'M0v/2+(7/75)q4^2. A zero-supply candidate must
therefore have a nonpositive quadratic derivative at the origin. With
S=K+H0 and E44 the fourth-coordinate projector, its 13-dimensional block is

    Aqq = diag(p')+(7f'/75)E44,
    Avv = f'M0/2-fD,
    Aqv = diag(p)-fS/2+(7f/75)E44,
    Avc = (ft/2)G,
    Acc = h_c',  Aqc=0.

The remaining blocks are transposes. A(t)<=0 is a necessary local condition
for uniform zero-supply dissipation on a source neighborhood. It is not a
sufficient bound for nonlinear terms, nor is the all-time matrix condition
proved by this note. This Taylor-order interpretation remains a source-level
derivation, separate from the completed fixed-multiplier algebra receipt.

This gate explains two exact candidate failures found by the storage-design
leaf: a mixed q2/v2 direction at an allowed initial state, and a ramp-driven
small-velocity point missed by zero-state ramp tests. Repairing only a few
sampled residuals does not enforce this whole quadratic condition. Positive
supply is an alternative, but its integral must fit the remaining budget.
