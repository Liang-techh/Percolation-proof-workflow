# Review Result: T-P5-048 — singular rank-one continuation of the signed/correlated Lyapunov residual gate

- `record_type`: `review_result`
- `task_id`: `T-P5-048`
- `agent`: `红莲魔尊`
- `source_agent`: `红莲魔尊`
- `status`: `pending`
- `claim_token`: `honglianmozun-T-P5-048-20260907T2150`
- `claim_commit`: `477bd25481231fe6f106b6f73fdbc8e7972c47eb`
- `dependencies`: `T-P5-044` (signed/correlated 2x2 residual completion), `T-P5-040`, `T-P5-037`
- `scope`: `Close exactly the det(H)=0 boundary deliberately left open by T-P5-044. No source/Float64/ODE/coverage/provenance/admission claim is made.`

## 1. Setup

T-P5-044 reduces the residual contribution to

`V' <= -c V - u^T H u - u^T b`,

with

`H = [[p,q],[q,s]]`, `p > 0`, `Delta = p s - q^2`,

and Pareto decay

`c = (109-r)/200`, `0 <= r <= 1`.

The positive-definite case `Delta>0` was already closed by the adjugate completion. This review treats the singular boundary `Delta=0` exactly.

## 2. Kernel obstruction is exact

Assume

`p > 0`, `Delta = p s - q^2 = 0`.

A kernel vector is

`k = (-q,p)`,

because

`H k = ( -pq + qp, -q^2 + sp ) = 0`.

Define the range-compatibility defect

`d := p b5 - q b4 = k^T b`.

If `d != 0`, choose `u=t k`. Then

`u^T H u = 0`,

while

`u^T b = t d`.

Choosing the sign of `t` opposite to `d` and sending `|t| -> infinity` gives

`-u^T H u - u^T b = -t d -> +infinity`.

Hence **no finite additive Lyapunov charge exists** when `p b5 != q b4`.

This is not a proof artifact: it is the exact kernel obstruction. Equivalently, the bias must lie in `Range(H)`.

## 3. Compatible rank-one case: exact sharp square completion

Now assume the compatibility condition

`p b5 = q b4`.

Let

`w := p u4 + q u5`.

Because `ps=q^2`, direct expansion gives

`p (u^T H u) = w^2`.

Compatibility also gives

`p (u^T b) = b4 w`.

Therefore

`4p (u^T H u + u^T b) + b4^2 = (2w+b4)^2 >= 0`.

Equivalently,

**`-u^T H u - u^T b <= b4^2/(4p)`**.

The constant is sharp: equality occurs whenever

`w = -b4/2`.

For example, choose `u5=0`, `u4=-b4/(2p)`.

Thus the singular rank-one boundary is not intrinsically fatal. It is fatal only when the bias has a kernel component.

## 4. Polynomial first-exit gate

At the existing barrier `V*=1/4`, inward pointing follows from

`b4^2/(4p) < c/4`.

With `c=(109-r)/200`, multiplication by the positive denominator gives the exact division-free gate

**`200 b4^2 < (109-r) p`**,

under

`0 <= r <= 1`, `p>0`, `ps=q^2`, `p b5=q b4`.

No square root, inverse matrix, eigenvalue, or pseudoinverse is required.

## 5. Parameter-cell incremental tube

Suppose the incremental bias has the form

`b = g Delta_c`,

and the signed relative block is the same singular `H`. The necessary compatibility is

`p g5 = q g4`.

Then the exact additive charge is

`g4^2 (Delta_c)^2/(4p)`.

For the existing tube

`Vd = (1/12) (Delta_c)^2`,

strict inward pointing requires

`g4^2/(4p) < c/12`.

Hence the exact polynomial gate is

**`600 g4^2 < (109-r) p`**.

Again, if `p g5 != q g4`, a kernel component remains and no `O((Delta_c)^2)` tube can follow from this separated completion.

## 6. Exact continuity with the T-P5-044 interior formula

This is not a disconnected boundary trick. Under the same compatibility relation `p b5=q b4`, the positive-definite numerator from T-P5-044,

`B_H(b) = s b4^2 - 2 q b4 b5 + p b5^2`,

satisfies the exact identity

`p B_H(b) = Delta b4^2`.

Indeed, substituting `b5=(q/p)b4` gives

`B_H(b) = (s - q^2/p)b4^2 = (Delta/p)b4^2`.

Therefore for every `Delta>0` along a compatible family,

`B_H(b)/(4 Delta) = b4^2/(4p)`.

So the interior T-P5-044 gate

`200 B_H(b) < (109-r) Delta`

reduces exactly to

`200 b4^2 < (109-r)p`.

The rank-one theorem is therefore the **continuous exact boundary extension** of the positive-definite theorem. A checker that blindly requires strict `Delta>0` would reject valid aligned rank-one cases only because both sides of the un-reduced determinant gate collapse to zero.

The same identity applies to `g` in the parameter-tube gate.

## 7. Fully degenerate endpoint H=0

For completeness:

- if `H=0` and `b=0`, the residual term costs zero;
- if `H=0` and `b != 0`, then `-u^T b` is unbounded above along `u=-t b`, so no finite additive charge exists.

Thus the entire semidefinite boundary has a clean range condition: finite charge is possible exactly when the bias lies in `Range(H)`. T-P5-048 proves this explicitly for the nonzero rank-one 2x2 branch without invoking pseudoinverses.

## 8. Candidate theorem statements for Lean

Minimal children:

1. `rank_one_bias_completion`
   - assumptions: `0 < p`, `p*s = q^2`, `p*b5 = q*b4`;
   - conclusion: `-(p*u4^2 + 2*q*u4*u5 + s*u5^2) - (b4*u4+b5*u5) <= b4^2/(4*p)`.
   - preferred proof route: prove `(2*(p*u4+q*u5)+b4)^2 >= 0`, clear positive denominators, `ring_nf`, `nlinarith`.

2. `rank_one_incompatible_unbounded_witness`
   - assumptions: `0<p`, `p*s=q^2`, `p*b5 != q*b4`;
   - explicit witness family `u=t*(-q,p)`; record the affine power `-t*(p*b5-q*b4)`.

3. `rank_one_first_exit_gate`
   - assumptions above plus `0<=r<=1` and `200*b4^2 < (109-r)*p`;
   - conclude strict inward power at `V=1/4`.

4. `rank_one_parameter_tube_gate`
   - assumptions `p*g5=q*g4` and `600*g4^2 < (109-r)*p`;
   - conclude strict inward power on `Vd=(Delta_c)^2/12` for nonzero `Delta_c`.

A convenient polynomial identity for formalization is

`4*p*(u^T H u + u^T b) + b4^2 = (2*(p*u4+q*u5)+b4)^2`

under the two equalities `p*s=q^2` and `p*b5=q*b4`.

## 9. Failure boundary / source interface

The mathematically correct source-side interface is now:

- if `Delta>0`, use T-P5-044;
- if `Delta=0`, do **not** immediately reject;
- first test the range compatibility `p*b5=q*b4` (or `p*g5=q*g4` incrementally);
- compatible rank-one blocks use the sharp rank-one gate above;
- incompatible rank-one blocks are genuinely unbounded along the kernel and must fail this ledger.

This matters especially for nearly dependent signed residual rows: entrywise absolute scalarization can erase the row correlation that makes the singular boundary admissible.

## 10. Remaining open items / nonclaims

This result does not claim that the deployed source residual actually produces a rank-one signed block, nor that any particular Float64/Jacobian enclosure satisfies the compatibility equalities. It does not establish ODE continuation, source-domain coverage, P8 closure, provenance, admission, or registry acceptance. Those remain separate obligations.

`T-P5-048` should remain `pending mathematical child` until independently checked and integrated by 梁智炜 / the designated verifier.
