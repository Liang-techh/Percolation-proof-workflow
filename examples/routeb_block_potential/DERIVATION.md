# Block potential: exact factorization and the moving-remote obstruction

The proposed block-centered potential is **not nonnegative uniformly over remote configurations**, even arbitrarily close to the block origin. Its q5 gradient at that origin is `-(20601/400000) sin(q2+q3)`. This is a linear obstruction, despite a uniformly positive block Hessian after adding the actual proportional gains. Subtracting the block-origin tangent term gives a uniformly positive quadratic block storage as an algebraic function; its dependence on moving remote coordinates must still be included in any derivative argument.

## Exact factorization

Write `s=q2+q3`, `x=q4`, `y=q5`, and

\[
c=\frac{20601}{400000}.
\]

The full 17-row Fourier potential is exactly

\[
U(q)=\frac{10791}{4000}
+\frac{762237}{200000}\cos q_2
+\frac{242307}{200000}\cos s
+c\bigl(\cos s\cos y-\sin s\cos x\sin y\bigr).
\]

There is no q1 or q6 dependence. Each CSV row is included once, including both conjugates. The four `(±s,±y)` rows produce `c cos(s)cos(y)`; the eight `(±s,±x,±y)` rows with their signed coefficients produce `-c sin(s)cos(x)sin(y)`. The remaining five rows give the constant and the two remote cosines. All imaginary coefficients vanish. `audit.py` expands these products in Gaussian-rational Fourier arithmetic and checks equality of every frequency and coefficient, not sampled trigonometric values. It also checks the source rows and actual Kp against the successful imported `PotentialSlice.lean` snapshot.

At the block origin,
`U(qD,0)=10791/4000+(762237/200000)cos(q2)+(2526075/2000000)cos(s)`.
Consequently, for the actual `Kp4=3/5`, `Kp5=1/2`, the requested function is

\[
F(s,x,y)=c\{\cos s(\cos y-1)-\sin s\cos x\sin y\}
+\frac3{10}x^2+\frac14y^2.
\]

This subtraction fixes qD only within the definition of the two evaluations. It imposes no frozen-remote trajectory assumption.

## Block gradient and explicit negative configuration

Exact differentiation gives

\[
U_x=c\sin s\sin x\sin y,\qquad
U_y=-c\{\cos s\sin y+\sin s\cos x\cos y\}.
\]

Thus `∂4 U(qD,0)=0`, `∂5 U(qD,0)=-c sin(s)`, and
`∇_B F(s,0,0)=(0,-c sin(s))`. For `sin(s)≠0`, a lower bound `F≥λ(x²+y²)` on a whole neighborhood of the block origin is impossible for any finite λ: the nonzero linear term dominates all quadratic terms on one side of the origin.

In particular, choose `q2=pi/2`, `q3=0`, `x=0`, so

\[
F(\pi/2,0,t)=-c\sin t+\tfrac14t^2.
\]

Taylor's theorem implies `sin(t)≥t-t³/6≥t/2` for `0≤t≤1`. Therefore for `0<t<2c`, F is negative. At the explicit choice `t=1/100`,

\[
F(\pi/2,0,1/100)\le-\frac{18601}{80000000}<0.
\]

No decimal evaluation of pi or sin enters this witness. Restricting remote angles to `sin(s)=0` would remove the linear term but would change the requested global domain; it is not used here.

## Exact Hessian and uniform entry bounds

The block Hessian of U is

\[
H_B=c\begin{pmatrix}
\sin s\cos x\sin y & \sin s\sin x\cos y\\
\sin s\sin x\cos y & -\cos s\cos y+\sin s\cos x\sin y
\end{pmatrix}.
\]

In particular, `H_B(s,0,0)=diag(0,-c cos(s))`. The script verifies all first and second derivative Fourier coefficients against these formulas by exact differentiation of the original coefficient dictionary.

Each entry has the global bound `|H_B,ij|≤c`. For the yy entry, this follows from Cauchy-Schwarz and
`cos²(y)+cos²(x)sin²(y)≤1`; adding absolute Fourier coefficients would lose this improvement. The xx and xy bounds follow directly from the trigonometric factors. All three entry bounds can attain c in magnitude.

There is also a sharper operator estimate than the row-sum bound `2c`. For a unit vector `(u,v)`, put `r=v²`, `a=sin(s)`, `b=cos(s)`. Then

\[
\frac{(u,v)H_B(u,v)^T}{c}
=a\{\cos x\sin y+2uv\sin x\cos y\}-b v^2\cos y.
\]

Applying Cauchy-Schwarz first in `(a,b)` and then in `(cos x,sin x)` gives

\[
\left|\frac{(u,v)H_B(u,v)^T}{c}\right|^2
\le\sin^2y+(4r-3r^2)\cos^2y
\le\frac43,
\]

because `4/3-(4r-3r²)=3(r-2/3)²`. Since H_B is real symmetric,

\[
\|H_B\|_2\le\frac{2c}{\sqrt3}
\le\frac76c=\boxed{\frac{48069}{800000}}=:L.
\]

The irrational bound is sharp: set `x=pi/2`, `y=0`, choose `sin(s)=sqrt(2/3)`, `cos(s)=-1/sqrt(3)`, and `(u,v)=(1/sqrt(3),sqrt(2/3))`. The quadratic form equals `2c/sqrt(3)`. The rational relaxation is certified by `(7/6)²≥4/3`. These analytic inequalities and the sharpness argument are documented mathematics, not claimed Lean theorems in this leaf.

## What remains viable on the original domain

Adding the block proportional gains yields

\[
\nabla_B^2 F=\operatorname{diag}(3/5,1/2)+H_B
\succeq\mu I,\qquad \mu=\frac{351931}{800000}>0.
\]

Uniform strong convexity does not place the minimum at the block origin when `sin(s)≠0`. The exact usable affine-quadratic lower bound, obtained by integrating the Hessian along the block segment, is

\[
F(s,x,y)\ge-c\sin(s)y+\frac{351931}{1600000}(x^2+y^2).
\]

For the tangent-subtracted function
`T(s,x,y)=F(s,x,y)+c sin(s)y`, the same argument supplies the uniform two-sided comparison

\[
\frac{351931}{1600000}(x^2+y^2)
\le T(s,x,y)
\le\frac{528069}{1600000}(x^2+y^2).
\]

This is a possible algebraic block-storage replacement with the original gains and arbitrary real remote configurations. It neither shrinks the domain nor changes the controller. It does change the storage function: treating the added tangent term as constant along the trajectory would be invalid when s moves. Descriptor/port composition, remote-rate terms, kinetic coupling, flowpipe inclusion, and terminal closure remain with the main task. The small scalar offsets in `audit_results.json` are merely consequences of the displayed affine-quadratic inequality, not a composed energy certificate.

## Evidence and scope

Actual Lean result: **PASS**, `LEAN_COMPILE_EXIT_CODE=0` and `VERIFY_EXIT_CODE=0`, in `output/run-RDCanfXw/verify.log`. The three identities `potential_factor`, `centered_block_identity`, and `remote_pi_half_slice` depend only on `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` appears. This compile does not formalize the derivative/operator-bound analysis above.

The source CSV SHA-256 is
`4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c`.
`audit_results.json` includes the controller and imported Lean-source hashes, exact derivative dictionaries, bounds, and witness arithmetic. All calculations concern the exact Fourier model; physical DH identification and Float64 enclosure remain separate.

Run `python -B examples/routeb_block_potential/audit.py` for the small exact coefficient audit. `verify.sh` imports the successful cached `PotentialSlice` and `StorageObstruction` outputs using Lean 4.33.1 and the existing pinned mathlib, with no downloads or dependency rebuilds. The Lean file addresses only the exact factorization, centered-block identity, and remote pi/2 slice. Actual compile status and axioms are recorded in its own `output/run-*/verify.log`. No target or other sidecar is edited.
