# Signed alternative after the two norm bootstraps remain unclosed

The supplied exact prefix audit was inspected directly. Its nominal-force
envelope is 1.928686371..., and its strict conditional analytic prefix reaches
33/64 with J<=21783090379/10^11. The fixed J=1 envelope is 778.636480259....
These are upper bounds from a sufficient envelope, not lower bounds on actual J.

The main agent subsequently reports preconditioned values: conditional prefix
9/16 with J<=.131405996245, full-horizon J=0 envelope 1.86868 and J=1 envelope
777.3176. Those latest figures are user-provided here, not independently rerun.
They establish progress in the envelope calculation, not closure. No further
norm experiments are part of this study.

The main preconditioner is algebraically correct. If L=T^T W T,
S=T*M0^-1, dM=M0-M, B=S*dM, then

    ||T*delta||_W <= ||S*r||_W + epsilon*||T*delta||_W,
    epsilon^2 <= trace(W*B*Q*B^T)  [as an operator-norm upper bound],

where r=r0+eta and Q=L^-1. More precisely, taking epsilon to be the square
root of that trace gives a sufficient upper bound for the required induced
operator norm. The denominator 1-epsilon requires epsilon<1. Failure of this
test does not imply the physical inverse is singular. REPORT equations (6)-(7)
give a noncontractive approximate-solve alternative; they alone need not close
the budget, as the main agent's latest cap illustrates.

## Exact signed work identity: the full Coriolis work cancels

The following is a mathematical identity under analytic Euler-Lagrange source
semantics. Its use in a successful finite-horizon certificate remains future
work; this leaf does not claim a new independent full-six-axis Coriolis CSV
audit or an FD/Float64 identification proof.

Let dM=M0-M(q), h=H0*q-grad U, and define the explicit potential remainder

    R(q)=U(q)-U(0)-(1/2)*q^T H0 q
        =A*Psi(q2)+B*Psi(s)+Cg*Psi(s+y)+Cg*p(s,x,y),
    Psi(z)=z^2/2+cos(z)-1,
    p(s,x,y)=sin(s)*(1-cos(x))*sin(y).

A,B,Cg and s,x,y are exactly those in REPORT equation (1). Psi>=0 globally;
R itself is not nonnegative, as the audited radial witness demonstrates.
Define the **signed** energy difference

    Sgap(q,v)=(1/2)*v^T dM(q) v - R(q).                 (S1)

Then, along the actual dynamics, with eta counted exactly once,

    d/dt Sgap = v^T M0*delta - v^T eta.                (S2)

Proof with all cancellations visible:

    v^T C = (1/2)*v^T dot M v,
    d/dt[(1/2)*v^T dM v] = v^T dM a - v^T C,
    dot R = -v^T h,
    dot Sgap = v^T[dM a+h-C]
             = v^T[r0+dM*delta]
             = v^T M0*delta-v^T eta.

Thus this preserves the *entire* mass/Coriolis work cancellation rather than
signing separate C components. It also preserves the gravity twist term that
cannot belong to a PSD radial sector. Equivalently Sgap=E_nominal-E_actual,
where the two energies use the same q,v and the actual controller stiffness K.

The exact integrated constraint is

    integral_0^T v^T M0*delta
      = Sgap(T)-Sgap(0)+integral_0^T v^T eta.           (S3)

For a differentiable scalar multiplier k(t),

    integral k*v^T M0*delta
      = [k*Sgap]_0^T - integral k'*Sgap + integral k*v^T eta. (S4)

Equations (S3)-(S4) are the signed information that a free L2 correction input
and independent absolute-force boxes discard. Sgap must remain signed. They
do not bound integral delta^T L delta by themselves: bounding a work integral
is insufficient to bound an acceleration-square integral.

## A concrete finite signed certificate to investigate next

Use the existing 14-state augmentation Y=(q,v,w,c), w'=c, c'=0, and the exact
reference matrix A14, with Bdelta inserting delta into the six velocity rows.
Select a symmetric differentiable rational matrix P(t) and scalar k(t), and
use the nonlinear storage

    V(t,Y)=Y^T P(t)Y+k(t)*Sgap(q,v).

Equation (S2) gives the exact derivative

    dot V=d+2*g^T delta,
    d=Y^T(P'+A14^T P+P A14)Y+k'*Sgap-k*v^T eta,
    g=Bdelta^T P Y+(k/2)*M0*v.                        (S5)

This introduces the signed source energy without differentiating the source
inverse or adding componentwise Coriolis bounds to the storage derivative.
The following **7x7 matrix inequality** is a sufficient pointwise certificate.
For a rational 6x6 multiplier Z and scalar supply b(t), require on each proved
state/source cell

    [ b-d,              -(g+Z^T*r)^T ;
     -(g+Z^T*r),   Z^T*M+M*Z-L       ] >= 0,          (S6)

where r=r0+eta. This is an explicit condition involving the full source M and
the complete signed residual. The six acceleration coordinates do not need
independent box bounds: for any delta satisfying M*delta=r, evaluating the
quadratic form in (1,delta) cancels the multiplier term and yields

    delta^T L delta + dot V <= b(t).                  (S7)

Indeed the quadratic form is
b-d-2*g^T delta-delta^T L delta+2*delta^T Z^T(M*delta-r).
This proof does not require a contraction factor or replacing delta by a norm
ball. It is a signed dissipation certificate, not a claim that suitable P,k,Z
have already been found. The off-diagonal combination g+Z^T*r must be formed
before interval bounding; splitting it would discard the desired cancellation.

To close J<=1, one would still need V(0,Y0)<=v0 for the entire original
full12 ball and c^2<=3, V(1,Y)>=vT on the final enclosure, and

    v0-vT+integral_0^1 b(t) dt <= 1.                  (S8)

Prefix continuation/domain arguments and all eta bounds remain necessary.
V need not be positive globally: the stated lower endpoint bound is what the
integrated certificate uses. Neither Sgap nor R is silently made positive.

The source-specific established result in this leaf is the gravity algebra
and its rigorous local obstruction, with an immutable exact audit receipt.
Applying (S2)-(S8) to obtain an admissible full-ball certificate, and achieving
enough combined mass/Coriolis cancellation in that certificate, are future work.
