---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# B45-5 sourceBlockForce binding：最小 state witness / source contract

本轮不重复 force-scale literal comparator。目标只限于为 Lean adapter 的两条
具体 premise 固定 source 对象：

```text
sourceBlockForce = expectedSourceForce q v w t
sourceBlockForce = sourceDescriptorRhs t
```

## 1. 可审计的 source object contract

对 deployed `arm_MCG` 的每个运行点 `s=(q,dq,w)`，固定 block index

```text
B = [4,5]       D = [1,2,3,6]
q_B = q[B]      v_B = dq[B]
c_B = Cdq[B]   g_B = Gq[B]   g0_B = G0[B]
rhs = tau - Cdq - Gq
sourceBlockForce_s := rhs[B]
a := Mq \ rhs
massBB_s(x) := Mq[B,B] x
remote_s := Mq[B,D] a[D]
sourceDescriptorRhs_s := massBB_s(a[B]) + remote_s
```

这一定义选择实际 `Mq(q)` 的 B/B 与 B/D block；不得用旧的 nominal
`M0_BB` 代替 `Mq[B,B]` 来声称 deployed descriptor binding。对于 Lean
`DescriptorResidualTerms`，实例化为

```text
t.coriolis = c_B
t.gravity = g_B
t.gravityAtZero = g0_B
t.accelerationB = a[B]
t.massBB = massBB_s
t.remoteMassAcceleration = remote_s
```

则两个目标分别对应：

```text
(E1) rhs[B] = sourceForce(q_B, v_B, w, c_B, g_B, g0_B)
(E2) rhs[B] = Mq[B,B] a[B] + Mq[B,D] a[D]
```

`E1` 是 deployed controller/C/G/G0 到 exact-real adapter 的 source contract；
`E2` 是 full six-row descriptor equation 的 B-row projection。二者必须针对
同一个 `s` 和同一个 `a`，不能拿 PMI nominal `f` 或 `M0_BB` 的 residual
定义替代。

## 2. 当前可审计的 zero-state witness

现有 `robot_final/routeB_descriptor_residual_interface.csv` 的 sample 1
记录：

```text
q4=q5=dq4=dq5=w=0
a4=a5=0
descriptor_eq_inf=0
linking_eq_inf=0
```

对应 source script `routeB_descriptor_residual_interface.jl` 的运行结构为：

- lines 30–31：`G0 = arm_MCG(zeros(6), zeros(6))[3]`；
- lines 41–45：同一 `arm_MCG` 产生 `Mq,Cdq,Gq`，随后定义
  `rhs = tau-Cdq-Gq`、`a = Mq \ rhs`、`dyn_err = Mq*a-rhs`；
- lines 48–55：`l` 使用 B block acceleration，并以独立标量 M0 entries
  重算 linking map；
- lines 72–74：输出 B-state、`a4,a5` 与 residual fields。

在如下 source contract 下，sample 1 给出一个最小 concrete instance：

```text
q=dq=0, w=0
Cdq=0
Gq=G0                         (same deterministic zero-state call)
tau=G0                        (deployed exact_ddq controller expression)
sourceBlockForce=rhs[B]=0
a=Mq \ 0=0
massBB_s(a[B]) + remote_s=0
```

因此 zero-state 的 `(E1,E2)` 可审计地收敛到 `(0,0)=(0,0)`，但这是一个
state-specific witness/contract，不是所有状态的 source theorem，也不含
Float64-to-`ℝ` kernel proof。

## 3. 已有 runtime evidence 的精确范围

本轮重新运行了已有独立 metadata checker，输出：

```text
DESCRIPTOR_INTERFACE_METADATA_OK
```

绑定输入为：

| artifact | SHA-256 |
|---|---|
| `dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| `routeB_descriptor_residual_interface.jl` | `d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24` |
| `routeB_descriptor_residual_interface.csv` | `ed10d0335debacd670a26871cad9ce51fc871cb86f6ae956125aeae3dee00e24` |
| `verify_descriptor_interface.py` | `47e1c02ea4addd64eb8c11f3dbbdf7b414288a55e8aa625494c365fc9b3fcbb0` |
| `routeB_Mq_M0.csv` | `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40` |

The saved 16-state artifact reports `max descriptor_eq_inf = 2.220446049250313e-16`
and `max linking_eq_inf = 0.0`, with `mass_regularizer=1e-6` and
`coriolis_gravity_fd_step=1e-5`. This is runtime regression evidence for the
full `Mq*a=rhs` calculation and the M0 linking-map index check. It is not a
fresh Julia run in this worker and it does not itself export the B-row fields
needed to instantiate `(E1,E2)` in Lean.

## 4. Remaining minimum repair for a general-state receipt

To close general-state source binding, one fresh run must export, per state and
with the same source/hash manifest:

```text
q_B,v_B,w,
Cdq_B,Gq_B,G0_B,tau_B,rhs_B,
a_B,a_D,
Mq_BB,Mq_BD,
rhs_B - sourceForce(q_B,v_B,w,Cdq_B,Gq_B,G0_B),
rhs_B - (Mq_BB*a_B + Mq_BD*a_D)
```

The receipt must record the block order `B=[4,5]`, `D=[1,2,3,6]`, regularizer,
finite-difference step, source hashes, state seed/points, and both componentwise
residual vectors. A pass would be a **runtime/source-binding receipt** only;
the Float64-to-exact-real bridge remains a separate Lean premise.

## Disposition

- zero-state `(E1,E2)` witness: `AUDITABLE_STATE_CONTRACT_PASS`;
- 16-state full descriptor regression: `RECORDED_RUNTIME_REGRESSION`, not fresh
  in this worker;
- general `sourceBlockForce = expectedSourceForce`: `OPEN_PENDING_B_ROW_EXPORT_AND_FLOAT64_BRIDGE`;
- general `sourceBlockForce = sourceDescriptorRhs`: `OPEN_PENDING_ACTUAL_MQ_BB_BD_EXPORT`;
- deployed `tau` equivalence: `NOT CLAIMED`;
- registry/state mutation: `false`.

