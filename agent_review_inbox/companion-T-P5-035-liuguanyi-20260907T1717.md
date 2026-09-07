---
kind: companion_log
review_id: companion-T-P5-035-liuguanyi-20260907T1717
task_id: T-P5-035
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-07T17:17:00-06:00
parent_review: review-T-P5-035-liuguanyi-20260907T1714
integration_status: pending
admission_label: pending
---

# T-P5-035 协作摘要

本轮补的是 `T-P5-022/028 -> T-P5-034` 中间缺失的**状态范数到 Lyapunov 储能**数学桥，不重复红莲魔尊刚完成的 `Q >= (15/16)V`。

对完全相同的 block-(4,5) 储能，已给出七项 exact-rational 平方恒等式，严格证明

```text
V >= (3/125) * (x4^2+x5^2+y4^2+y5^2).
```

因此 source/Jacobian lane 若已有

```text
||r_c||^2 <= ell2 ||delta z||^2,
```

可以合法转换为

```text
||r_c||^2 <= (125/3) ell2 V(delta z).
```

这一步需要 typed premise：source 的 `delta z` 必须就是 `V` 使用的 `(delta x4,delta x5,delta y4,delta y5)`。common-`c` 时可直接复用 `T-P5-028` 的精确 moving-frame cancellation；若 `delta c != 0`，仍必须走 `nu`、rank-one `K_eff`、扩展状态或 additive/transverse lane，不能静默吸收。

把该桥接入 `T-P5-034` 的 `Kc=1/12` incremental tube 后，source-facing 条件直接化成

```text
34000 ell2 + 9792 nu < 225.
```

common-parameter 特例是

```text
ell2 < 9/1360.
```

若 source 只分别给 centered gain `ell2` 与 anchor `B2`，不能错误写成平方预算直接相加。quarter barrier 的正确 rational Young/discriminant adapter 是

```text
R = 225 - 34000 ell2 - 3264 B2,
R > 0,
R^2 > 443904000 ell2 B2,
```

并可取无平方根的有理 witness

```text
theta_bal = R / (68000 ell2)
```

（`ell2>0`；零边界单独处理）。

另外给了精确负控：`121/5000=0.0242` 不能作为 `V/||z||^2` 的统一下界；在 `z=(0,-1/24,0,1)` 上严格失败。因此后续 checker 不要把 `3/125` 通过 decimal rounding 升高。

建议 Lean lane 只形式化三个小叶：七平方恒等式、`V >= (3/125)||z||^2`、`ell2 -> (125/3)ell2` adapter；centered+anchor discriminant 可作为独立算术 child。真实 `H/S/A/K_path`、Float64/solve、first-exit domain、P8 coverage、kernel/comparator/admission 继续保持 open。
