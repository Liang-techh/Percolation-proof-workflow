# Final pinned compilation receipt

Successful run: `output/run-76aeLbcO`.
Complete compiler stdout/stderr: `output/run-76aeLbcO/terminal.log`.
Start/end UTC: 2026-09-05T21:00:25Z / 2026-09-05T21:01:25Z.
UniversalMultiplier_COMPILE_EXIT_CODE=0; VERIFY_EXIT_CODE=0.
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6.
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474.
Options: -DwarningAsError=true; explicit snapshot root and olean output.
Only UniversalMultiplier.lean was compiled; dependencies were cached only.

| File in successful run | SHA256 |
| --- | --- |
| UniversalMultiplier.lean | 001d38906138439bd733c7d49195e50f7cfdedd9017f6e3770d13d9e664ccce5 |
| UniversalMultiplier.olean | 5cee29a13ccb9c3c41f1692dcf86f468e043d0b82bdebd241c6c3303d08e7c8e |
| terminal.log | 2f0c5258ef8b3d1c65e152503c2af86c02460dd9050449eb9f337f731092edf0 |
| before_run.sha256 | dc7e7aaa5a8fbb71ae446c6c467724eae22f6f813459302c3f87f40202f69012 |

Post-compilation read-only checks confirmed the delivered source matches
the successful run, the complete pre-run manifest passes sha256sum -c,
and the live revision-46 state file matches its read-only input snapshot.
The new Lean source contains no sorry, admit, or custom axiom declaration.
All 21 printed theorem axiom reports contain only propext, Classical.choice,
Quot.sound. The earlier failed snapshots are retained and are not proof
receipts. See ATTEMPT_HISTORY.md for all four attempts.

The full original `routeb_signed_gap_lean/output/run-iH9FGdAL` was copied
into each attempt before compilation, including its finite-vector source,
oleans, transitive local cache, snapshots, manifest, and receipt log.
The runner checks the original SignedGap and ResidualMultiplier olean
hashes against their published final receipt before loading them.

## Handoff declarations

All are in namespace `RouteBUniversalMultiplier` and reuse the actual
`RouteBSignedGap` finite sums and affine matrix.

- `bottom_identity`, `D_dominates_L`, `D_positive`,
  `finite_quadratic_coercivity`, `global_coercivity`: Z=I, D=2M-L>=L;
  quantitative and strict positivity transfer from L with the explicit
  actual source mass-order premise.
- `optimal_matrix`, `finite_vector_congruence`: derive the actual block
  entries and the identity for every finite vector (s,v), including s=0.
  The congruence identity is never an assumed premise.
- `psd_iff_margin`, `affine7x7_lossless`: full quadratic nonnegativity iff
  the signed margin is nonnegative under D>=0 and the actual two vector
  equations M delta=r, M z=g-r+L delta.
- `optimalZ_balance`, `CONSTRUCTIVELOSSLESS`: explicit formula
  z=R g-delta+R L delta, with R a right inverse of the actual M. This
  inverse premise is exposed, never inferred for a frozen nominal R.
- `recenter_block`, `affine_center_identity`: derive the actual finite
  change of center for arbitrary h, without assuming M h=r.
- `frozen_center_error`, `frozen_center_margin`: derive ec=dM(2h+z) and
  mhat=b-d-2g'h-h'Lh-2(z+h)'dM h from M0h=r and M0z=g+Lh-r.
- `centered_dual_sos`, `centered_dual_bound`: exact finite completion
  quad K(s,y)=quad(D-L)y+quad L(y-sQec)+s^2(mhat-ec'Qec), followed by
  the all-vector inequality using L(Qec)=ec and D>=L>=0.
- `affine_centered_dual_bound`, `frozen_affine_dual_bound`: complete
  affine matrix nonnegativity from the single signed scalar source
  condition, using the derived recentering. No inverse premise on actual
  M, epsilon, contraction hypothesis, or extra D-positivity test.

For the centered result, Q is required to solve the L dual equation;
the frozen handoff uses the explicit right-inverse property for L.
No symmetry of Q or inverse of M is silently assumed.

## Source and ownership boundary

All writes were under examples/routeb_universal_multiplier_lean/.
No registry or live state writes, broad tests, source coefficient audits,
dependency builds/downloads, or new numerical runs were performed.

The frozen rational ansatz h=Rr, z=Rg+(RLR-R)r, R=M0^-1 remains the main
task's source-coefficient audit. This leaf exposes its two M0 equations
and derives their consequences. At dM=0 the correction ec vanishes and
mhat is the exact margin. Away from M0, the frozen z is NOT asserted to
satisfy the actual optimality equation and h is NOT asserted to equal
the actual correction delta.

The physical source binding of M(q)>=L, L positivity/inverse, the uniform
scalar source condition, and the storage/budget/trajectory obligations
remain explicit external obligations. No full-horizon J<=1 or registry
admission is claimed by these conditional compiled theorems.
