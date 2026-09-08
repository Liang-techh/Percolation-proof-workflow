# Raw Vfull_DH: uniform initial-envelope obstruction

Status pending; exact rational computation plus a paper uniform inequality,
not Lean verification, Julia execution or runtime/source admission.

We FIX the pinned ideal-real analytic Vfull_DH expression (original Kp_DH,
positive-sign analytic g0 compensation, one declared mass regularizer, no
cross term, no additive shift) and the block-only initial ball X0. We do not
select or redefine the active consumer's V. Configuration/source hashes and
all exact arithmetic are recorded in NEW_RESULT.json.

## Function-level proof on every initial state

Embed x into q,v with only joints4/5 free, all other coordinates zero, and
c_j=cos(q_j), s_j=sin(q_j). The ball constraint is
q4^2+q5^2+v4^2+v5^2<=r^2 for the existing r=3/20.

Reading the actual Ugrav_DH value polynomial and substituting q2=q3=0 gives
U(q)=A0+A+B*cos(q5), where A0,A,B are its pinned source coefficients. This is
a value-level polynomial substitution, not an origin or derivative argument.
Since B>0 and cos(t)>=1-t^2/2 for real t,

    U(q)>=A0+A+B*(1-r^2/2) =: L_U.

The trigonometric inequality follows from 1-cos(t)=2*sin(t/2)^2 and
|sin(s)|<=|s|. No sampled trig values or interval-library heuristics are used.

The source imports exact rational mass polynomials. The script restricts their
entries to this initial configuration: terms with sin(q1),sin(q2),sin(q3),
sin(q6) vanish, the corresponding cos factors become one, and duplicate
remaining q4/q5 monomials are combined exactly. It adds the source regularizer
ONCE to the two diagonal entries. On physical c/s values, each remaining
monomial has absolute value at most one; coefficient absolute sums therefore
bound every entry. Maximum row/column absolute sums yield a uniform Euclidean
operator bound m. Hence, without assuming symmetry or positive definiteness,

    (1/2)*v_B^T M_BB(q)*v_B >= -m*||v_B||^2/2 >= -m*r^2/2.

This intentionally conservative lower bound avoids relying on a separate
unverified mass-coercivity certificate. All cross-block kinetic terms vanish
because the corresponding velocities are identically zero on X0, not because
the matrix is approximated or Schur-reduced.

The analytic g0 entries are calculated exactly from the pinned gravity CSV
using the SAME all-cos-one/all-sin-zero substitution as the imported source.
Their decoded rational values are zero. This is not a claim about FD/runtime
G0. The proof also retains the general safe term
g0_B dot q_B >= -r*(|g0_4|+|g0_5|), so the positive source sign is not dropped.
The Kp_DH quadratic is nonnegative from its explicit positive source entries.

Combining these pointwise inequalities for EVERY x in X0 gives

    Vfull_DH(embed(x)) >= L_U-m*r^2/2-r*(|g0_4|+|g0_5|)
                       = 32462895903/6400000000
                       > 492033745203/25600000000000
                       = recorded initial_storage_upper.

The exact strict gap is 129359549866797/25600000000000. These are newly
computed rational envelope outputs of this isolated audit, not solver,
runtime or formal constants admitted to the workflow. The source scalar is
only the comparison target; CSV continuity supplies none of the inequalities.

Thus the requested upper inequality is incompatible with this fixed raw
ideal-expression target on the WHOLE initial ball, not merely at one point.
No centered-bound shortcut, Hessian envelope or origin equality is used.

## What this does and does not close

This closes the paper/rational obstruction for the stated ideal analytic
source expression: the old scalar cannot be its uniform initial upper bound.
It does not prove the active V equals that expression, or that Float64 dhport
evaluates it exactly. To assert the same result about an active runtime object,
its value-level source/configuration and error-refinement witnesses remain
required. We do not relabel that object, change its threshold, or replace it
with another storage. No Vshift selection audit is repeated.

## Reproduction and checks

Run from workspace root:

    python -B examples/routeb_active_v_function_envelope/NEW_envelope.py

The script reads seven pinned external inputs, uses only integer/Fraction
arithmetic and CSV parsing, prints JSON, and writes nothing. Exit zero means
its arithmetic assertions passed, not source admission. Hash drift raises an
error instead of accepting changed inputs. NEW_RESULT.json stores the printed
result; runtime observations remain null and admission flags false.

The interpretation of source syntax and the real trigonometric/norm lemmas
are explained here; the Python script is not a Julia interpreter or a formal
proof checker. No local Lean/Lake, Julia, source producer, full regression or
state/registry mutation occurred. Existing artifacts remain untouched.
