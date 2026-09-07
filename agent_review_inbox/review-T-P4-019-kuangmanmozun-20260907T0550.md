# Review Result — T-P4-019

- task_id: `T-P4-019`
- review_id: `T-P4-019-kuangmanmozun-20260907T0550`
- reviewer: 狂蛮魔尊
- source_agent: 狂蛮魔尊
- status: `pending`
- depends_on: `T-P4-007`, `T-P4-014`, `T-P4-016`, `T-P4-017`
- scope: sharp inequality closure for a genuinely additive execution bias in one P4 Schur channel, with an explicitly available independent constant positive slack; corrected block-4 specialization uses canonical generalized-force `kc=1/20`.

## 1. Problem isolated from the execution-layer ledger

`T-P4-007` shows that the real source-facing residual contains terms such as the centered IEEE/model errors and the solve defect.  Some of these may fail to vanish with the cross-coordinate and therefore cannot honestly be forced into a bound of the form `|r| <= beta |y|`.

The remaining question is precise: suppose the same-coordinate part has already been compressed to `a y`, but there is a genuinely additive execution error `b`, `|b| <= B`.  Can unused Schur curvature absorb `b`?

Consider

`Q(x,y) = p x^2 + 2 x (a y + b) + d y^2 + s`,

where `s` is **not invented slack**: it must be a genuinely independent nonnegative constant reserve already present in the target certificate (or a separately proved uniform positive lower bound of another reserve).  Put

`Delta := p d - a^2`.

Assume `p>0` and `Delta>0`.

## 2. Exact division-free identity

The key identity is

`p Delta Q`
`= Delta (p x + a y + b)^2`
`  + (Delta y - a b)^2`
`  + p (Delta s - d b^2)`.

Proof: first complete the `x` square,

`p Q = (p x + a y + b)^2 + Delta y^2 - 2 a b y - b^2 + p s`.

Multiply by `Delta` and use

`Delta^2 y^2 - 2 a b Delta y + a^2 b^2 = (Delta y-a b)^2`.

The leftover coefficient of `b^2` is

`-Delta b^2-a^2 b^2 = -(Delta+a^2)b^2 = -p d b^2`,

which yields the displayed identity.

This form is suitable for Lean because it avoids square roots and division in the forward theorem.

## 3. Sharp uniform additive-bias budget

If `B>=0`, `|b|<=B`, and

`d B^2 <= Delta s`,

then `Q(x,y)>=0` for every `x,y` and every admissible `b`.

Indeed `Delta>0`, `p>0`, and the identity above reduces the claim to nonnegativity of two squares plus

`Delta s-d b^2 >= Delta s-d B^2 >= 0`.

Because `p>0` and `Delta>0` imply `d>0`, no separate positivity assumption on `d` is mathematically necessary.

### Sharpness

The budget is also necessary for uniform closure over `|b|<=B`.

When `Delta s < d B^2` and `B>0`, choose

`b=B`,
`y=a B / Delta`,
`x=-(a y+B)/p`.

Then the first two square terms in the identity vanish and

`Q = s - d B^2/Delta < 0`.

For the degenerate case `B=0`, failure of `Delta s>=0` means `s<0`; then `b=x=y=0` already gives `Q=s<0`.

Hence, under `p>0`, `Delta>0`, `B>=0`, the exact uniform criterion is

**`Delta s >= d B^2`.**

No choice of Young parameter can improve this criterion.

## 4. Important obstruction: unused curvature is not constant slack

Set `s=0`.  The sharp condition becomes

`d B^2 <= 0`.

Since `d>0`, this forces `B=0`.

Therefore **a nonzero truly additive source/IEEE/controller/solve bias cannot be absorbed merely because `Delta=pd-a^2` is positive**.  The Schur curvature only controls state-dependent directions.  To absorb a nonvanishing constant bias one must exhibit an actual independent positive constant reserve `s>0` (or prove that the alleged additive error in fact vanishes/has relative structure).

This gives a counterexample-guided classification rule for `T-P4-007`:

- if a remainder vanishes with `y`, charge it to the shared same-coordinate `beta` budget;
- if it vanishes with another controlled state direction, charge it through the transverse/dual budget of `T-P4-014/016`;
- if it is genuinely additive, it needs a real constant reserve and must satisfy the theorem here;
- if no such reserve exists, any nonzero uniform additive envelope is a closure obstruction rather than a usable Schur budget.

A state-dependent reserve `H(z)` only helps with a fixed additive `B>0` if one has a **uniform positive floor** `H(z)>=s0>0` on the certified domain.  If `H` can vanish, then at its zero set the same no-slack obstruction returns.

## 5. Corrected canonical block-4 rational specialization

Use the corrected source-facing block-4 constants from `T-P4-017`:

`p4 = 3/5`,
`d4 = 116667666666667 / 10^15`,
`p4*d4 = 350003000000001 / 5000000000000000`.

### 5.1 After spending same-coordinate budget up to total `a=1/4`

Then

`Delta4 = p4*d4 - (1/4)^2`
`       = 37503000000001 / 5000000000000000`.

The sharp additive-bias condition is therefore exactly

**`37503000000001 * s >= 583338333333335 * B^2`.**

Equivalently, the constant reserve costs a factor

`d4/Delta4 = 583338333333335 / 37503000000001 ~= 15.5544445333`.

Thus once the same-coordinate envelope has been enlarged to `1/4`, additive bias is expensive.

### 5.2 Before spending the extra same-coordinate budget: canonical `kc` alone

For the canonical generalized-force `kc`, `a=1/20`.  Then

`Delta4,kc = p4*d4-(1/20)^2`
`          = 337503000000001 / 5000000000000000`.

The sharp additive-bias condition becomes

**`337503000000001 * s >= 583338333333335 * B^2`.**

Here

`d4/Delta4,kc ~= 1.7283945130`.

This quantifies the tradeoff already suggested by `T-P4-014/016`: spending same-coordinate curvature reduces the amount of a genuine independent reserve available to tolerate additive execution error.  A source lane that can prove smaller relative envelopes should not automatically consume the full `1/4` allowance if an additive execution term later needs protection.

## 6. Suggested minimal Lean decomposition

```lean
theorem additive_bias_square_identity
    (p d a x y b s : ℝ) :
    p * (p*d-a^2) * (p*x^2 + 2*x*(a*y+b) + d*y^2 + s)
      = (p*d-a^2) * (p*x+a*y+b)^2
        + ((p*d-a^2)*y-a*b)^2
        + p * ((p*d-a^2)*s-d*b^2) := by
  ring
```

Forward consumer:

```lean
theorem additive_bias_schur
    (p d a B s x y b : ℝ)
    (hp : 0 < p)
    (hDelta : 0 < p*d-a^2)
    (hB : 0 <= B)
    (hb : |b| <= B)
    (hbudget : d*B^2 <= (p*d-a^2)*s) :
    0 <= p*x^2 + 2*x*(a*y+b) + d*y^2 + s := by
  -- use square identity; derive 0<d from hp,hDelta; square_le_square from hb
```

Sharpness can be represented either with the explicit division witness above, or with a division-free witness hypothesis:

```lean
-- Let Delta = p*d-a^2.
-- If b=B, Delta*y=a*B, and p*x=-(a*y+B),
-- then the two square terms vanish.
```

For portability, a separate exact-rational corollary should instantiate block 4 twice: `a=1/20` and `a=1/4`.  No new P4 architecture is needed.

## 7. Failure branches / boundaries

1. This theorem does **not** prove that the real source has a constant slack `s`; it only gives the exact consumer if such a reserve is separately present.
2. One may not add a positive constant to the certificate merely to satisfy the budget.  If the original target quadratic has no such term, set `s=0`, and the result becomes an impossibility theorem for nonzero additive `B`.
3. The theorem does not replace `T-P4-012` remote-mass transfer, `T-P4-016` aggregate transverse budgeting, or source semantic binding.
4. Runtime errors that actually depend on state should preferably be classified before taking a coarse global `B`; a relative/transverse enclosure can close without a constant floor and is therefore structurally superior.
5. This review makes no admission/provenance/source-authentication claim and does not change P4/M4 status.

## 8. Recommended next step

Ask the source/IEEE lane to classify each term in the `T-P4-007` execution ledger (`DeltaM`, `DeltaC`, centered `DeltaG`, `delta_ctrl`, solve defect) as same-coordinate relative, transverse/state-relative, or genuinely additive.  For any genuinely additive aggregate envelope `B`, either exhibit a real uniform reserve `s` and check the exact rational budget here, or record the no-slack obstruction.  Formalization only needs the square identity, forward sharp consumer, and the two block-4 rational corollaries.

**Result:** a nonzero additive execution bias has a precise sharp consumer only when an independent constant reserve exists; positive Schur curvature by itself is not such a reserve.  Status remains `pending`;待封不觉独立验证 / 待梁智炜收割与最终整合。
