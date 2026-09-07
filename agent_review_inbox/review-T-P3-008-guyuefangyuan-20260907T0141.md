---
kind: review_result
review_id: review-T-P3-008-guyuefangyuan-20260907T0141
task_id: T-P3-008
source_agent: 古月方源
claimed_at: 2026-09-07T01:32:00-06:00
created_at: 2026-09-07T01:41:00-06:00
inspected_commit: d5a5111a4f26b2af216dd8532e257a92e874570c
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_fd_tensor_index_bridge_and_fourier_remainder_then_bind_float64_roundoff
---

# T-P3-008 — exact central-FD Christoffel index bridge, Fourier remainder theorem, and the Float64 boundary

## Scope

This pass closes the source-independent mathematics behind B45-4 and identifies the smallest remaining source-semantic seam. The main point is that the Julia `dM` index order already matches the generic Lean tensor convention exactly after one explicit permutation:

```text
Tfd[k,i,j] := dM[i,j,k].
```

With that definition, the source Christoffel contraction is exactly the generic `christoffelForce` **in exact-real arithmetic**. The analytic-vs-central-difference mismatch is then a separate tensor remainder with a global rational Fourier bound. The actual Julia `Float64` execution still needs an explicit rounding remainder; it must not be identified with the exact-real finite sum.

Inspected inputs:

- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl:73-92`, blob `27cf497b6f27919eb5b554369fb1444f4314c942`;
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_analytic_fourier_dynamics_probe.py:1-55,92-99,158-205`, blob `db59e4753652b78819289b5ac48ad0db0753be8b`;
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`, blob `e8e544007588e06fbac12638c7f71976fc094db9`;
- `examples/routeb_source_binding_audit/REPORT.md` B45-4, blob `8bc5cd5444473396caa13af107428f0350cca742`;
- downstream `review-T-P5-010-youhunmozun-20260907T0026.md`, blob `b3fe7950a2e47caf4dc4e72d5208ee344ec736bd`.

No receipt/provenance/admission work and no Float64-equals-real claim is made.

## 1. Exact source index map

The Julia source constructs

```text
dM[:,:,kk]
 = [M(q+h e_kk)-M(q-h e_kk)]/(2h),
```

then

```text
cijk = 1/2 * (dM[ii,jj,kk] + dM[ii,kk,jj] - dM[jj,kk,ii]),
Cdq[ii] = sum_{jj,kk} cijk * dq[jj] * dq[kk].
```

Map Julia indices `1,...,6` to Lean `Fin 6` by subtracting one. For an exact-real mass evaluator define

```text
Dfd_k M_ij(q)
 := [M_ij(q+h e_k)-M_ij(q-h e_k)]/(2h),

Tfd[k,i,j] := Dfd_k M_ij(q).                                (1)
```

Then the source coefficient is

```text
Gammafd[i,j,k]
 = 1/2 * (Tfd[k,i,j] + Tfd[j,i,k] - Tfd[i,j,k]).             (2)
```

But `ChristoffelPower.lean` defines

```text
christoffelForce T v i
 = sum_j sum_k
   1/2*(T[k,i,j] + T[j,i,k] - T[i,j,k]) * v_j*v_k.
```

Therefore, with no symmetry assumption on `Tfd`,

```text
Cdq_fd^R[i] = christoffelForce(Tfd,dq)[i].                   (3)
```

This is not a heuristic correspondence: the three tensor slots are in exactly the same order. In particular, the correct adapter is `T k i j = dM[i,j,k]`; using `T i j k = dM[i,j,k]` would be wrong.

The nested-loop order `jj` then `kk` is irrelevant for (3) over exact reals, but it becomes relevant again for the actual sequential Float64 accumulation; see Section 6.

## 2. Analytic derivative + explicit FD remainder

Let the true exact-real derivative tensor be

```text
T[k,i,j] := partial_k M_ij(q),
```

and define

```text
R[k,i,j] := Tfd[k,i,j] - T[k,i,j].                           (4)
```

Since the Christoffel force is linear in its tensor argument,

```text
christoffelForce(Tfd,v)
 = christoffelForce(T,v) + christoffelForce(R,v).             (5)
```

Equivalently, coefficientwise,

```text
Gammafd[i,j,k] - Gamma[i,j,k]
 = 1/2 * (R[k,i,j] + R[j,i,k] - R[i,j,k]).                   (6)
```

Hence if

```text
|R[k,i,j]| <= mu[k,i,j],  mu[k,i,j] >= 0,
```

then

```text
|Gammafd[i,j,k]-Gamma[i,j,k]|
 <= 1/2*(mu[k,i,j]+mu[j,i,k]+mu[i,j,k]),                     (7)
```

and

```text
|Cdq_fd[i]-Cdq_an[i]|
 <= sum_{j,k} 1/2*(mu[k,i,j]+mu[j,i,k]+mu[i,j,k])
                 * |v_j v_k|.                                (8)
```

Equation (8) is useful for a componentwise P3/P4 force envelope.

## 3. Power-level bridge is strictly cleaner than bounding every Christoffel coefficient

For P5, do not first apply the three-term triangle inequality (7). Apply the existing generic power identity directly to the tensor remainder `R`.

From `christoffel_power_identity`,

```text
sum_i v_i * [Cdq_fd[i]-Cdq_an[i]]
 = 1/2 * sum_{k,i,j} R[k,i,j] v_k v_i v_j.                  (9)
```

Thus

```text
|sum_i v_i(Cdq_fd[i]-Cdq_an[i])|
 <= 1/2 * sum_{k,i,j} mu[k,i,j] |v_k v_i v_j|.              (10)
```

This is exactly the tensor interface requested downstream by `T-P5-010`. It avoids paying the artificial factor created by separately bounding all three terms in (6).

Sign convention note: `T-P5-010` defines `DeltaT := T-Tfd`; with that convention its cubic mismatch is the negative of (9). The absolute-value bound is identical.

## 4. Global rational FD tensor bound from the finite Fourier mass

The analytic probe already exposes the right theorem. Write one exact Fourier mass entry as

```text
M_ij(q) = Re sum_nu a_{ij,nu} exp(i nu.q),
```

where `nu in Z^6` and `a_{ij,nu}` is Gaussian rational. For `h != 0`, a single Fourier mode satisfies

```text
Dfd_k [a exp(i nu.q)]
 = i * sin(nu_k h)/h * a exp(i nu.q),

partial_k [a exp(i nu.q)]
 = i * nu_k * a exp(i nu.q).                                (11)
```

Therefore the modewise derivative error has magnitude

```text
|a| * |sin(nu_k h)/h - nu_k|
 = |a| * |sin x - x|/|h|,  x=nu_k h.
```

Using the global elementary inequality

```text
|sin x - x| <= |x|^3/6,
```

we get, for every real `q`,

```text
|R[k,i,j](q)|
 <= h^2/6 * sum_nu |a_{ij,nu}| |nu_k|^3
 <= h^2/6 * sum_nu (|Re a_{ij,nu}|+|Im a_{ij,nu}|)|nu_k|^3
 =: mu[k,i,j].                                               (12)
```

For the deployed nominal step `h=1/100000`, every `mu[k,i,j]` in (12) is a nonnegative rational number computable directly from `routeB_fourier_mass_full_rational.csv`. This is precisely the formula implemented by `derivative_error` in the analytic probe.

Important advantages of (12):

1. it is **global in q**; no q-box or branch-and-bound is needed for the FD remainder itself;
2. it is coefficientwise and anisotropic, exactly what the P5-010 matrix/small-gain route wants;
3. it keeps the analytic Fourier mass and the deployed central-FD operator distinct rather than silently replacing one by the other.

What (12) still needs is B45-1 (or a smaller functional source theorem) identifying the exact-real DH mass entry with that Fourier polynomial. A CSV hash or agreement at `q=0` is not enough.

## 5. Constant mass regularizer cancels at the exact-real derivative layer

Let

```text
M_eps(q) = Mhat(q) + eps I,
```

with `eps` independent of `q`. Then exactly over the reals,

```text
Dfd_k M_eps,ij = Dfd_k Mhat_ij,
partial_k M_eps,ij = partial_k Mhat_ij.                       (13)
```

Hence `R`, `Gammafd`, and the analytic Christoffel tensor are unchanged by the `1e-6 I` regularizer in exact-real semantics. This mathematically justifies why the Fourier derivative remainder formula contains no regularizer term.

However, (13) must **not** be upgraded to a statement about executed Float64 bits. The source adds the regularizer before two separately rounded `mass_matrix(q±h e_k)` evaluations, so exact cancellation after real lifting is not automatic.

## 6. Precise Float64 obstruction and the minimum source adapter

The actual Julia function does more than evaluate the mathematical formula:

- `q±h e_k` is formed in Float64;
- both mass matrices are evaluated and rounded;
- subtraction/division creates Float64 `dM`;
- the three-term `cijk` arithmetic is rounded;
- each product with `dq[j]*dq[k]` is rounded;
- the 36 terms are accumulated sequentially in Float64.

Consequently, even if every stored `dM[i,j,k]` is lifted to a real number, the exact-real `Finset.sum` in Lean is not definitionally equal to the real lift of the final Julia `Cdq[i]`.

The minimum honest execution adapter is therefore

```text
lift(Cdq_Julia)[i]
 = christoffelForce(Tfd_lift, v_lift)[i] + r_ieee[i],         (14)
```

with a separately bounded `r_ieee`. If one also wants to connect `Tfd_lift` to the exact-real Fourier/DH derivative, write

```text
Tfd_lift = T + R_fd + R_dM_ieee,                              (15)
```

so the full source bridge becomes

```text
lift(Cdq_Julia)
 = C(T,v)
   + C(R_fd,v)
   + C(R_dM_ieee,v)
   + r_contract_ieee.                                        (16)
```

Here `R_fd` is the analytic central-difference remainder bounded by (12), while `R_dM_ieee` and `r_contract_ieee` are purely execution/rounding obligations. This separation prevents the exact Fourier O(h^2) theorem from being misreported as a Float64 source equality.

## 7. Lean-friendly theorem decomposition

The algebraic part can be made tiny and source-independent.

```lean
-- Source indexing convention: T k i j corresponds to dM[i,j,k].
def sourceGamma (T : Fin 6 -> Fin 6 -> Fin 6 -> R)
    (i j k : Fin 6) : R :=
  (T k i j + T j i k - T i j k) / 2

def sourceCdq (T : Fin 6 -> Fin 6 -> Fin 6 -> R)
    (v : Fin 6 -> R) (i : Fin 6) : R :=
  sum j, sum k, sourceGamma T i j k * v j * v k

theorem sourceCdq_eq_christoffelForce :
  sourceCdq T v i = RouteBChristoffelPower.christoffelForce T v i
```

```lean
-- Exact tensor linearity / FD split.
theorem christoffelForce_add
    (T R : Fin 6 -> Fin 6 -> Fin 6 -> R) (v : Fin 6 -> R) :
  christoffelForce (fun k i j => T k i j + R k i j) v i
    = christoffelForce T v i + christoffelForce R v i
```

```lean
-- Component envelope.
theorem fd_christoffel_component_error
    (hR : forall k i j, |R k i j| <= mu k i j)
    (hmu : forall k i j, 0 <= mu k i j) :
  |christoffelForce (T+R) v i - christoffelForce T v i|
    <= sum j, sum k,
       ((mu k i j + mu j i k + mu i j k)/2) * |v j*v k|
```

```lean
-- Power interface consumed directly by T-P5-010.
theorem fd_christoffel_power_error
    (hR : forall k i j, |R k i j| <= mu k i j)
    (hmu : forall k i j, 0 <= mu k i j) :
  |sum i, v i *
      (christoffelForce (T+R) v i - christoffelForce T v i)|
    <= (1/2) * sum k, sum i, sum j,
         mu k i j * |v k*v i*v j|
```

For the Fourier remainder, split formalization into:

```text
sin_central_difference_error:
  |sin x - x| <= |x|^3/6,

fourier_mode_central_difference_error,
finite_fourier_central_difference_error.
```

A separate typed execution theorem should consume a premise/bound for `r_ieee`; do not bake Float64 equality into the algebraic theorem.

## 8. What is closed mathematically and what remains open

Closed here:

1. exact source index orientation `T[k,i,j]=dM[i,j,k]`;
2. exact-real identity `Cdq_fd = christoffelForce Tfd`;
3. exact analytic/FD tensor split and component error bound;
4. the cleaner cubic power remainder used by P5;
5. global coefficientwise Fourier FD bound (12), with rational `h=1/100000` specialization;
6. exact-real cancellation of the constant mass regularizer from derivative/Christoffel terms.

Still open:

- B45-1 / true-DH-to-Fourier functional binding for the full mass entries;
- generation or checking of the concrete 216 rational `mu[k,i,j]` values from the current frozen mass CSV;
- an IEEE/Float64 enclosure for `R_dM_ieee` and `r_contract_ieee` in (16);
- same-domain velocity bounds or energy sublevel needed by `T-P5-010` to turn the cubic power remainder into damping absorption;
- all P8 flowpipe/coverage and final P3/P5/M4 admission gates.

## Recommended next action

1. **Formalization lane:** encode the source index bridge, tensor linearity, component envelope, and power remainder first; these need no source hashes or interval APIs.
2. **Exact source-math lane:** compute the rational tensor `mu[k,i,j]` from the frozen Fourier mass CSV using (12), preferably as a generated sidecar/checker artifact rather than 216 handwritten constants.
3. **Execution lane:** bound only the Float64 gap in (16). Do not redo the O(h^2) Fourier mathematics inside an IEEE checker.
4. **P5:** feed `mu` directly to the T-P5-010 power-level matrix certificate. Do not collapse it into six affine force offsets unless a downstream interface truly requires that loss.

This result remains `pending`: it is a mathematical/source-interface bridge, not a proof that the deployed Float64 trajectory satisfies the exact-real Christoffel theorem.
