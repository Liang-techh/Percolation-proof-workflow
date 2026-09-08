# review_result — GH-MATH-P5-CERTIFICATE-KPATH-NEXT

- agent: 狂蛮魔尊
- source_agent: 狂蛮魔尊
- coordinator: 梁智炜
- status: `CONDITIONAL_PASS / ACTUAL_SOURCE_BOUND_PENDING`
- mathematical_scope: 18 representative SPN certificates -> one certificate-indexed rational `K_path` admissible region; exact obstruction if actual source-bound `K_path` is absent.
- non_scope: no provenance/admission/receipt/re-audit; no Lean/kernel claim; no P8/ODE/registry/P5 closure.

## 0. Executive result

There is a clean finite-dimensional closure already latent in the 18 representative certificates: **do not collapse the certificates to one scalar norm and do not require one re-factorized common SPN table.** Keep the representative index and intersect the 18 certificate capacities.

For the existing rational toy packet, this gives a 72-halfspace polytope (18 representatives × 4 PSD-dominance rows) for the nonnegative gain increment `E`. Along the all-ones gain ray the exact common sufficient capacity is

```text
t_cap = 32553 / 4000000.
```

Since the toy baseline is `K0[a,j]=1/1000`, the corresponding common componentwise box cap is

```text
K_box = 1/1000 + t_cap = 36553 / 4000000
```

for all eight `(force row,state slot)` entries: any nonnegative `K_path` with every entry `<= K_box` can be consumed by the toy 18-certificate family through envelope monotonicity.

**However this is not a concrete physical `K_path` bound.** The packet itself is explicitly `scope=source-independent-unbound`, `source_binding=false`, `concrete_K_path_bound=false`. The comparison review also says there is no concrete input JSON binding actual `A/Hjac/Scoord/K_path`. Therefore the directed task closes mathematically but remains source-bound pending. The minimal missing object is one canonical rational, source-bound eight-entry `K_path` (or direct same-domain component binding) with exact comparison to the certificate capacity.

## 1. Inspected fixed artifacts

The mathematical conclusion below uses only the following already-existing source-independent artifacts.

- `NEW_KPATH_INTERFACE_REVIEW.md`, blob `36...?` not used as provenance; semantic point only: actual source gain `K` is consumed through componentwise `K <= G`, and the larger certified gain `G` gives the power envelope.
- `NEW_KPATH_INTERFACE_Comparison_REVIEW.md`, blob `6e740f024cce54cdb73bac19201474fabcf8071a`: no concrete `K_path` values are supplied; exact comparison is eight rational inequalities.
- `NEW_KPATH_PACKET_ObstructionAndCapacity20260908.md`, blob `9b293f149e69d71335b809faa0a0f0eb8b24f018`: fixed-`N` increment is obstructed, while PSD slack yields 18×4 rational capacity inequalities.
- `NEW_KPATH_PACKET_PSDCapacity20260908.py`, blob `a4154d9e29dc5d59436acbff3788599239192e8f`: constructs the rational capacity rows and the all-ones ray minimum.
- `NEW_KPATH_PACKET_PSDCapacityWitness20260908.json`, blob `433ec889e8ab4a1516684a21ed7ae6385ba9428f`: reports `t_cap=32553/4000000`, active cone `[2,4]`, active row `2`, but explicitly leaves `source_binding=false` and `concrete_K_path_bound=false`.
- `NEW_KPATH_PACKET_UpdatedToySPN20260908.json`, blob `b39a3217f31cc64e875e11f7d030efaf07b32897`: an 18-certificate source-independent toy family at `K=1/500` in every slot.

No statement below upgrades these artifacts to source authentication or admission.

## 2. Certificate-indexed capacity theorem

Fix a representative set `R` (here `|R|=18`). For each representative `r`, suppose the existing gap certificate has

```text
H_r(K0) = S_r + N_r,
S_r >= 0  (PSD),
N_r >= 0  entrywise.
```

Assume source/exporter gives a rational coercivity reserve `delta_r >= 0` such that

```text
S_r - delta_r I >= 0.
```

For a nonnegative gain increment `E >= 0`, let the chart-induced gap loss be

```text
C_r(E) = sym(B_r^T E A_r),
```

where `A_r,B_r` are the nonnegative absolute chart maps. In the present packet every entry of `C_r(E)` is nonnegative and depends linearly on the eight entries of `E`.

If, for every representative `r` and every matrix row `i`,

```text
sum_j C_r(E)[i,j] <= delta_r,                    (CAP-r-i)
```

then

```text
delta_r I - C_r(E) >= 0
```

because it is symmetric, has nonpositive off-diagonals, and is weakly diagonally dominant with nonnegative diagonal. Therefore

```text
S_r - C_r(E)
 = (S_r - delta_r I) + (delta_r I - C_r(E))
 >= 0,
```

and hence

```text
H_r(K0+E) = (S_r-C_r(E)) + N_r
```

is again an SPN witness on that representative cone.

Thus the unified admissible increment region is the rational polytope

```text
P_cap := { E >= 0 : (CAP-r-i) for all r in R and i=0,1,2,3 }.
```

For 18 representatives this is exactly 72 rational linear inequalities, plus the eight nonnegativity inequalities. This is the correct **certificate-indexed `K_path` bound**: each certificate keeps its own capacity row, while the physical gain must lie in their intersection.

### Formalizable theorem statement

```text
theorem indexed_spn_capacity
  (hbase  : forall r, H r K0 = S r + N r)
  (hS     : forall r, PSD (S r - delta r * I))
  (hN     : forall r, EntrywiseNonnegative (N r))
  (hC     : forall r E, C r E = sym (transpose (B r) * E * A r))
  (hE     : EntrywiseNonnegative E)
  (hrows  : forall r i, rowSum (C r E) i <= delta r)
  : forall r, SPNWitness (H r (K0+E)).
```

No square root, eigenvalue, matrix inverse, or floating tolerance is required in the trusted consumer once `delta_r` and the rational row coefficients are supplied.

## 3. Uniform ray / box corollary and exact toy number

For a common nonnegative direction `D`, define

```text
c_{r,i}(D) := sum_j C_r(D)[i,j].
```

Then `E=tD` is certified whenever

```text
0 <= t,
forall r,i with c_{r,i}>0:  t * c_{r,i} <= delta_r.
```

Hence the largest scalar allowed by this *specific row-dominance capacity proof* is

```text
t_* = min_{r,i:c_{r,i}>0} delta_r / c_{r,i}.
```

A division-free checker does not need to evaluate the ratios: a candidate rational `t` is accepted iff all cross-multiplied inequalities

```text
t * c_{r,i} <= delta_r
```

hold.

In the existing toy packet `D` is the 2×4 all-ones matrix. The generated witness reports

```text
t_* = 32553/4000000,
active representative cone = [2,4],
active matrix row = 2.
```

The baseline is `K0=1/1000` in all eight slots, so the ray endpoint has

```text
K0 + t_* D = 36553/4000000
```

in all eight slots.

Now use the already-formalized envelope monotonicity: if the actual nonnegative gain satisfies

```text
K_path[a,j] <= 36553/4000000     for all 8 slots,
```

then `K_path <= K0+t_*D` componentwise, so the endpoint certificates' power envelope also consumes `K_path`. Therefore `36553/4000000` is a valid **toy common box cap** derived from all 18 representative capacities.

The checked toy file chooses the much smaller `t=1/1000`, giving `K=1/500`; that is an interior witness, not the capacity endpoint.

## 4. What is sharp, and what is not

The `min` over representative capacities is forced for a global 18-representative consumer. Replacing it by `max` is unsound: with two representatives having admissible ray caps `1` and `2`, choosing `t=2` leaves the first representative uncertified. Global coverage therefore uses the minimum.

Likewise, for fixed certificate-indexed componentwise caps `G_r`, define the meet

```text
G_meet[a,j] := min_r G_r[a,j].
```

Then

```text
K_path <= G_r for every r
iff
K_path <= G_meet.
```

So `G_meet` is the largest common componentwise matrix inferable from those fixed per-representative caps. A componentwise maximum or a single Frobenius/operator norm cannot replace this statement without a separate comparison theorem.

But **`t_*` is not claimed to be the true maximal SPN/copositive gain**. It is sharp only for the stated 72-row sufficient construction using the supplied `delta_r`. For `t>t_*`, the active row `[2,4], row 2` violates this particular diagonal-dominance capacity gate. Correct status is

```text
NOT_CERTIFIED_BY_INDEXED_CAPACITY_GATE
```

not mathematical `FAIL`. A true failure would require, for example, an explicit nonnegative cone vector with negative gap quadratic form, or a real source point violating the homogeneous gain envelope.

## 5. Why 18 representatives are enough only under the right symmetry

The 36→18 compression is legitimate only when the cone predicate transported to the flip is explicitly even / flip-invariant. For the intended power envelope this is natural when:

- `Q(-z)=Q(z)`;
- the residual gain bound uses `|z|` and a sign-independent nonnegative `K_path`;
- the representative certificate is assigned identically to its global-sign flip.

If the source gain or predicate is orientation-dependent, 18 tests cannot be silently reused for all 36 orientations. In that case the capacity index set must be expanded or a flip identity must be proved first.

## 6. Minimal actual-source obstruction

The repository currently has enough source-independent mathematics to define and even populate a toy certificate-capacity polytope, but it does **not** contain the one object needed to turn this into a physical `K_path` conclusion:

```text
ACTUAL_KPATH_PACKET :=
  coordinates/order = (r4/r5) x (x4,x5,y4,y5),
  exact rational A/Hjac/Scoord or a direct same-domain ComponentBinding,
  exact recomputed K_path[2][4],
  same source/domain/path identity,
  same Q, mu, chart and force normalization as the 18 certificates,
  exact eight-slot comparison against a certified G (or against P_cap),
  stable data digest / source identity.
```

The comparison review explicitly says no concrete input JSON exists. The capacity witness explicitly says `source_binding=false`, `source_coverage_verified=false`, `concrete_K_path_bound=false`. Therefore substituting the toy `1/500`, the endpoint `36553/4000000`, or any sampled/Float64 estimate for the missing physical `K_path` would be an invalid source upgrade.

A second exact obstruction must also be checked at source level: if some certified-domain point has `z=0` but `rc != 0`, then no finite homogeneous `K_path` can exist at all. That case must split an additive bias or repair centering rather than enlarge the gain cap.

## 7. Recommended child lemmas / next handoff

Minimal math/formalization leaves:

```text
indexed_capacity_row_psd
indexed_spn_capacity
indexed_ray_capacity_cleared
representative_gain_meet
indexed_capacity_not_fail_of_gate_miss
```

The next source lane should not search for new SPN tables first. It should export the actual 8-entry rational `K_path` packet and test either:

1. direct box comparison `K_path <= 36553/4000000` only if the toy Q/mu/chart are truly the same physical packet; or preferably
2. the full 72-inequality capacity polytope, which can admit anisotropic gains substantially larger than the uniform box in some slots.

If neither same-source identification nor exact `K_path` can be produced, this task remains `ACTUAL_SOURCE_BOUND_PENDING` with the obstruction above; that is not a P5 mathematical impossibility statement.
