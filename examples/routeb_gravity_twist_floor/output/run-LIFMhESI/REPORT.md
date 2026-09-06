# Global gravity twist floor for signed storage

The concrete all-real theorem is compiled successfully in `GravityTwistFloor.lean`:

```text
forall u s x y : Real,
  R(u,s,x,y) >= -x^4/40,

R = A Psi(u) + B Psi(s) + C Psi(s+y)
    + C sin(s)(1-cos(x))sin(y),
Psi(z) = z^2/2 + cos(z) - 1,
A = 762237/200000, B = 242307/200000, C = 20601/400000.
```

All four coordinates are independent real numbers. There is no joint domain,
small-angle restriction, positivity assumption on R, or trigonometric premise.
No Taylor theorem, custom axiom, `sorry`, or `admit` is used. Only this new
directory was written. No dependency rebuild or broad test was performed.

## Proof and exact constants

The final proof uses the user's quarter-angle argument. Put t=z/4. The
double-angle identities and sin^2(t)+cos^2(t)=1 give

```text
Psi(z) = 8t^2 - 8 sin^2(t) cos^2(t)
       >= 8 sin^2(t)(1-cos^2(t)) = 8 sin^4(t).
```

The inequality uses Mathlib's `Real.sin_sq_le_sq`. Twice applying
`sin^2(2t) <= 4 sin^2(t)` gives `sin^4(z) <= 256 sin^4(t)`.
Thus `psi_ge_sin_fourth` proves `sin^4(z)/32 <= Psi(z)` globally.
`psi_nonneg` also follows directly from Mathlib's
`Real.one_sub_sq_div_two_le_cos`.

For a=|sin(s)|, b=|sin(s+y)| and rho=1-cos(x)>=0, the subtraction identity

```text
sin(y) = sin(s+y)cos(s) - cos(s+y)sin(s)
```

gives `sin(s)sin(y) >= -(2a^2+b^2/4)`. The Lean proof uses signed squares
directly, avoiding absolute-value case splits. The remaining lower bound is
certified by the exact completion of squares

```text
B a^4/32 + C b^4/32 - C rho(2a^2+b^2/4)
 = (B/32)(a^2 - 32C rho/B)^2
   + (C/32)(b^2 - 4rho)^2 - K rho^2,
K = 32 C^2/B + C/2 = 18932319/197600000,
1/10 - K = 827681/197600000 > 0.
```

`gravity_floor_exact_rho` retains the stronger `R >= -K rho^2` result.
`gravity_floor_rho` weakens this to `R >= -rho^2/10`.
Finally `0 <= rho <= x^2/2` gives the requested global quartic floor.
The coefficient value and margin are independently checked by `norm_num`
in `exact_constant_value` and `exact_constant_margin`.

## Source identity binding: separate from the Lean inequality

The source inspected is `../routeb_J_strategy/REPORT.md`, section 1, together
with `../routeb_J_strategy/SIGNED_WORK.md`, equation (S1). They state

```text
u=q2, s=q2+q3, x=q4, y=q5,
U(q)=10791/4000+A cos(u)+B cos(s)+C cos(s+y)
     +C sin(s)(1-cos(x))sin(y),
R(q)=U(q)-U(0)-(1/2)q^T H0 q.
```

The twist has zero Hessian at the origin. Consequently the cosine sectors
give `q^T H0 q = -A u^2 - B s^2 - C(s+y)^2`, producing exactly the R
definition above. The substitution into the independent-coordinate theorem
therefore gives `R(q) >= -q4^4/40` once those source identities are bound.

The existing Python algebra audit checks the Fourier coefficient identity
and Hessian/reference correspondence. Its existing receipt at
`../routeb_J_strategy/output/run-20260905T201432Z-5c2562b5/receipt.json`
was inspected and reports exit 0 and unchanged inputs. It was not rerun here.
This leaf does not formalize that external CSV identity, prove physical DH
identification, or discharge represented-parameter, FD, solve, or rounding
defects. The two source documents are copied and hashed in every compile run.
The unconditional Lean theorem is about the explicit real-valued R definition;
application to the physical model retains these separate binding obligations.

## Relevance and sign for the J storage

Writing `kinetic=(1/2)v^T(M0-M(q))v`, equation (S1) uses
`Sgap=kinetic-R`. The compiled `signed_gap_upper` gives

```text
Sgap <= kinetic + q4^4/40.
```

This is an upper bound on Sgap. For a negative storage multiplier k it gives
`k*Sgap >= k*(kinetic+q4^4/40)`, which can supply the gravity part of a lower
endpoint bound for `Y^T P Y+k*Sgap`. For positive k this floor alone does not
give that lower endpoint bound. R and Sgap remain signed. No J<=1 closure,
dissipation matrix certificate, kinetic estimate, or trajectory result is
claimed by this lemma.

## Compilation and retained failures

Run from the workspace in PowerShell:

```powershell
wsl -e bash examples/routeb_gravity_twist_floor/verify.sh
```

The runner invokes the explicit Lean 4.33.1 binary with warnings as errors
and uses only existing package oleans from `/home/z5242/sos_lean`.
Mathlib is pinned to commit `0df444a360eaa60ab8c11dca51a86af692955474`.
No `lake build`, cache download, or project-wide testing is invoked.
Before each compilation, the runner creates a unique run directory, copies
the Lean source, runner, source documents and cache manifests, hashes those
inputs, and opens `terminal.log`. It compiles the copied source and verifies
snapshot hashes afterwards. Previous runs are never overwritten.

| Run | Result |
| --- | --- |
| `output/run-bUZVPiqE` | Exit 1: real-valued definitions needed noncomputable marking; initial half-angle proof retained. |
| `output/run-dh7oXqQH` | Exit 1: missing closing `end` for the noncomputable section; quarter-angle proof retained. |
| `output/run-blLCv1In` | Exit 0: final quarter-angle proof, exact rho floor, quartic floor and signed-gap corollary. |

The successful source is byte-identical to the delivered Lean file. Its
`#print axioms` output for the global Psi lemma, exact rho floor, quartic
floor and signed-gap corollary contains only
`[propext, Classical.choice, Quot.sound]`. These are standard Lean/Mathlib
foundational axioms; no custom mathematical or trigonometric axiom occurs.
The successful output olean SHA256 is
`4bb403566b3b9b56a2816956c006c2e7126c07cca272e272124463264925ba27`.
This report was added after that successful compilation; it is not claimed
to have been part of that earlier snapshot.
