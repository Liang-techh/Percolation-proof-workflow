# Line 9 source-level non-identification

**OPEN_UNCOMPILED.** Read-only source trace on 2026-09-07. Only this new review is written; no source/registry changes, Lean execution, solver or regression. This is a source-level obstruction, not a physical infeasibility result.

**Finding:** `A_up` has a candidate formula in the actual upstream producer, but no complete source/manifest binding uniquely supplies line 9's `b_base`, `ell`, target or P4 front/offset/scale/nominal. The missing data are not recoverable merely by locating similarly named formulas.

## Actual dependency chain

All paths below are under `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

`routeB_analytic_mass_full_cs_polynomial.csv` → `routeB_compact_composed_interval_probe.py` → `routeB_compact_composed_interval_partition_bounds.csv` → `routeB_compact_external_budget_ledger.py` → external ledger physical line 9.

- Probe lines 20–46 load the mass polynomial and environment-selected regularizer/gamma. Lines 115–120 define `B_up`. It does not import a controller, storage certificate or target.
- Ledger lines 47–75 group by eta, maximize the selected port coefficient over resolved cells, require one external candidate gamma, and apply theta. Line 9 is the eta=5.6/theta=1 aggregate over 321 resolved cells, not a state row. Its regularizer is copied from the first resolved row; the generator does not check a controller/storage/manifest identity across the group.
- The two ledger scripts' `b_base`/`l_base` occurrences are interface descriptions, not loaded polynomial definitions. Their inputs and output schema carry no storage/controller digest, scalar target or complete instance key.

## Field trace, without splicing

| Requested field | Located source candidate | Same-instance verdict |
|---|---|---|
| `A_up` | Actual probe lines 115–120 and combined-Schur interface lines 10,117 specify `(1402217/12000000)*a4² + (200739/4000000)*a5²` | Matrix formula identified in the producer; acceleration functions, their source/domain embedding and the consumer binding are absent from line 9 |
| `ell=||l_base||` | `routeB_compact_direct_descriptor_structure.jl:78–86`: `lBase_i=IVAL_i*fB_i-M0BB_i*aB_i` | Separate script; controller branch is selected by environment at lines 24–28 and is not recorded by the external ledger |
| `b_base` | Combined-Schur interface lines 7,121–127 use it as a free interface term | No defining expression or unique import in the producer chain. `Dbase` in the descriptor script is a different expression; there is no supplied equality `b_base=Dbase` |
| prescribed target | None in producer chain/output schema | Missing. `candidate_margin` is a computed coefficient difference, not a requested margin floor |
| front | No P4 remainder test-vector binding | Cannot identify the BODY6/front vector with `a_B` by position or name |
| offset | No P4 scalar offset or uniform offset floor | Missing |
| scale / gain | theta=1 and external gamma=0.2 are present | They are Young parameter and external budget coefficient; neither identifies alpha/beta/front scale/gainCap. No sf is recorded |
| nominal | Separate descriptor script constructs `Dcore_correct`, `Dbase`, etc. | No equality to the P4 nominal scalar; no lower-direction normalization proof |

The descriptor script explicitly says its affine storage template is **not certificate values** (lines 161–162) and its fixed positive placeholders are **not a gain claim** (185–186). Thus its `V`, `sres=5`, and `betaB` cannot fill the missing slots automatically.

## Concrete source-level ambiguity

The descriptor script shares the mass but allows `ROUTEB_CONTROLLER_BRANCH=fourier` or `dh`. From `routeB_factorized_descriptor_model.jl:193–194` and descriptor lines 26–27, joint-4 damping is respectively `1/5+3/10=1/2` or `1/2+3/10=4/5`. Applying the actual `lBase` formula gives

`lBase_DH,1 - lBase_Fourier,1 = -(3/10)*dq4`.

The second residual component has the same damping in these two branches. At the formal-variable specialization `q=0, aB=0, w=0, dq4=1, dq5=0`, the squared residual norms are respectively `1/4` and `16/25`. This is an exact formula specialization, not an asserted descriptor-feasible physical state.

The external mass-only producer has no input selecting either residual branch. Consequently its same coefficient row cannot uniquely determine `ell`. This is a structural information loss, even before trying to choose storage or target. No constants from either branch were imported into line 9.

## Exact inequality still required

For theta=1, the source consumer description requires one same-domain proof of

`target + 2*ell(x)^2 + charge*A_up(x) <= b_base(x)`, with `target>0`,

plus a binding/comparison from that expression to the intended scalar source margin. For the **printed-decimal model only**, `charge=15698624457194343/10^17`; interval/Float64-to-exact reification remains separate. The previous sidecar `NEW_P4_032_ActualRowMissingBase.lean` already gives the exact allocation equivalence and the same-coefficients/different-base counterexample. No additional unbound source numbers are needed for that obstruction.

Minimal repair: one consumer packet must identify the selected controller branch, storage polynomial and exact coefficient digests, domain/state embedding, acceleration/residual definitions, scalar target, and the P4 object/normalization equalities. Its allocation proof must consume this row's charge with its validated numerical interpretation. A mass/eta match alone cannot replace this packet.

## Provenance and search boundary

| File | Live SHA-256 |
|---|---|
| external ledger CSV | `a00383cb7ff547979028047c4489d7a4328d60b582b808efb65b19c2bba3c2c6` |
| external ledger Python | `c36fe1f3c6b62bad7121458481b63f58dac130f251d413c68ed1a4f9430e7da9` |
| partition bounds CSV | `4cc46e20d2a2917005243ecaedbf5042ed7a7d53ff4f71395a9728b1e3ffecbc` |
| composed interval probe Python | `ab6a4e34ecb391247eef796496f57b28407587b366c360f4e0ad441fedd04ba6` |
| direct descriptor structure Julia | `2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c` |
| factorized descriptor model Julia | `c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427` |
| analytic mass polynomial CSV | `1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451` |

The external directory's TOML/JSON search found no references to these live hashes and no matching line-9 consumer manifest. The workflow workspace's TOML/JSON/YAML search found no external-ledger name/hash or partition-hash reference. This is a bounded search, not a claim about every possible external repository or future manifest. Live hashes freeze inspected files; they do not prove that the existing CSV was generated by the currently inspected source revision.
