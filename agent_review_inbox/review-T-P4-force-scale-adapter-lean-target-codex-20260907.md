---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# T-P4 force-scale adapter：q4/q5 exact algebra 与 Lean target

## 结论（本轮新增、可独立关闭的 child）

`P4.force_scale_adapter_q45` 的最小数学 child 可以独立定义为：对
`q = (q4,q5) ∈ ℝ × ℝ`，把 normalized PMI force descriptor
`(q5/20,q4/20)` 左乘 block scale `diag(1/5,1/10)`。其 exact result 是

\[
 \operatorname{diag}(1/5,1/10)(q_5/20,q_4/20)
   =(q_5/100,q_4/200).
\]

该 child 不需要 DH、`M_BD`、动力学域、Float64 语义或任何数值假设。它只需要
`q4,q5 : ℝ` 及 exact rational arithmetic，因此适合作为一个单独的无假设坐标
adapter theorem。它仍然不是 deployed `tau` 的等价定理（见下文的明确边界）。

## Canonical source anchors

本 review 使用的 canonical source 快照为：

- deployed source：`C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\robot_final\dhport_lib.jl`
  - SHA-256：`AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`
  - `exact_ddq` 的 `tau` 组合在 lines 102–109：`tau = -Kp .* q - (Kd+b_fr).*dq + G0v + (gw_coef .* I_val).*w`，没有显式 `q5/q4` 交叉 torque term。
- lifted source：`C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_fourier_lifted_descriptor_model.jl`
  - SHA-256：`0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D`
  - lines 153–154：`Ival[4]=1/5`、`Ival[5]=1/10`；
  - lines 160–166：nominal rows contain `+ Q(1,20)*q[5]` in row 4 and `+ Q(1,20)*q[4]` in row 5, while the corresponding force expressions multiply by `Ival[4]` and `Ival[5]`.
- workflow contract：`docs/routeb-p4-kc-force-contract.md`，其中 normalized descriptor 与 force-coordinate descriptor 已分开记录为
  `rho_kc^f=(q5/20,q4/20)` 与 `rho_kc^F=(q5/100,q4/200)`。

上述 source anchors 只说明 adapter 的输入系数和组合来源；它们不构成对 Julia
执行语义、DH 完整 coefficient coverage 或 deployed `tau` 等价性的证明。

## 最小 Lean interface

当前 sidecar `examples/routeb_b45_5_residual_decomposition_lean/ResidualDecomposition.lean`
已经采用了合适的最小类型：

```lean
abbrev Vec2 := ℝ × ℝ

def rhoKcNormalized (q : Vec2) : Vec2 :=
  (q.2 / 20, q.1 / 20)

def forceScaleKc (q : Vec2) : Vec2 :=
  ((1 / 5 : ℝ) * (rhoKcNormalized q).1,
   (1 / 10 : ℝ) * (rhoKcNormalized q).2)

def rhoKc (q : Vec2) : Vec2 :=
  (q.2 / 100, q.1 / 200)
```

最小 exact theorem target 是：

```lean
theorem forceScaleKc_eq_rhoKc (q : Vec2) :
    forceScaleKc q = rhoKc q := by
  rcases q with ⟨q4, q5⟩
  apply Prod.ext <;>
    dsimp [forceScaleKc, rhoKcNormalized, rhoKc] <;>
    ring
```

这个 proof 的关键是先 `rcases` 固定 pair order，再用 `Prod.ext` 分解两个
坐标，最后由 `ring` 处理 `ℝ` 上的有理常数。这里 `.1=q4`、`.2=q5`，所以
结果的第一分量确实是 `q5/100`，第二分量确实是 `q4/200`；不应在后续泛化到
`Fin 2 → ℝ` 时默默改成 zero-based 或未声明的排列。

若需要更直接的 source-literal bridge，可增加以下同样无假设的 theorem，而不
引入矩阵库：

```lean
def liftedKcForce (q : Vec2) : Vec2 :=
  ((1 / 5 : ℝ) * (1 / 20 : ℝ) * q.2,
   (1 / 10 : ℝ) * (1 / 20 : ℝ) * q.1)

theorem liftedKcForce_eq_rhoKc (q : Vec2) :
    liftedKcForce q = rhoKc q := by
  rcases q with ⟨q4, q5⟩
  apply Prod.ext <;>
    dsimp [liftedKcForce, rhoKc] <;>
    ring
```

其中 `liftedKcForce_eq_rhoKc` 是 source literals (`1/20`, `1/5`, `1/10`) 到
目标 descriptor 的最短 bridge；`forceScaleKc_eq_rhoKc` 则是 normalized
descriptor API 的 compositional theorem。两者都不应被命名为 DH theorem。

## 可并列验收的 quadratic child

若继续关闭队列中同一 adapter 的 budget 子项，最小接口仍可保持 pair-based：

```lean
def rhoKcSq (q : Vec2) : ℝ :=
  (rhoKc q).1 ^ 2 + (rhoKc q).2 ^ 2

theorem rhoKc_sq_le_of_block_energy
    (q : Vec2)
    (hp : (3 / 2 : ℝ) * (q.1 ^ 2 + q.2 ^ 2) ≤ 28 / 5) :
    rhoKcSq q ≤ 7 / 18750 := by
  rcases q with ⟨q4, q5⟩
  dsimp [rhoKcSq, rhoKc]
  nlinarith [sq_nonneg q4, sq_nonneg q5]
```

这个 theorem 只证明给定 `hp` 后的 exact finite-dimensional arithmetic bound；
它不证明 `hp` 来自 deployed trajectory、DH model 或 full state coverage。
coordinate equality 与 quadratic budget 应保留为两个 receipt 条目，以免把
adapter 的代数正确性误报成 source/domain admission。

## Required source/runtime receipt

当前 sidecar 的旧 `FINAL_RECEIPT.md` 对应 earlier candidate hash，不能覆盖本轮
q45 extension。要关闭本 child，最小 receipt 应重新绑定当前
`ResidualDecomposition.lean` 内容，并至少记录：

1. 当前 Lean source SHA；
2. pinned Lean/Mathlib identity（此前环境记录为 Lean 4.33.1、commit
   `819816b2`，Mathlib commit `0df444...`，需以本次实际 worker 输出为准）；
3. compile exit code `0`；
4. theorem-check/verify exit code `0`；
5. `sorry`/`admit` 扫描为空；
6. `#print axioms forceScaleKc_eq_rhoKc`（及若加入的
   `liftedKcForce_eq_rhoKc`、`rhoKc_sq_le_of_block_energy`）仅出现标准逻辑
   axioms；
7. source restriction 明确列出 source hash 与 lines 153–166 的 coefficient
   anchors；
8. `registry promotion = false`，直到独立 receipt 被审核。

本轮没有运行 pinned Lean worker，因此状态是
`PENDING_PINNED_LEAN_RECOMPILE`，不是 `LEAN_VERIFIED`。本 review 也没有修改
主 state 或 registry。

## Deployed tau 非等价边界（必须保留）

即使上述 theorem 获得 Lean receipt，也只得到

\[
  \rho_{kc}^{F}(q)=\operatorname{diag}(1/5,1/10)\rho_{kc}^{f}(q).
\]

它不能推出以下任一命题：

- `tau` in `dhport_lib.jl` 已含有 `q5/100` 或 `q4/200` 的 torque component；
- `M_BD a_D`、`M_DD a_D` 或完整 DH force row 可由该 pair 唯一恢复；
- lifted nominal rows 与 deployed `exact_ddq` 的 `tau-Cdq-Gq` 在 B block 上相等；
- source-level Float64 运算已经被嵌入为 exact-real theorem；
- `forceScaleKc_eq_rhoKc` 可直接升级为 true-DH force descriptor theorem。

因此，若目标 contract 要求“deployed `tau` 本身等价于该 q45 force term”，在不
修改物理模型的前提下不能用这个 adapter theorem 填补缺口；必须另给一个显式
source contract，说明该项是 additive force residual / PMI descriptor，而不是
deployed torque law 的隐藏重写。当前最小可关闭 child 是上面的 exact adapter
identity（以及可选的 quadratic budget），而不是 tau equivalence。

## Review disposition

- `forceScaleKc_eq_rhoKc`：数学接口已足够小，Lean proof skeleton exact；等待本次
  source hash 绑定的 pinned compile/axiom receipt。
- `liftedKcForce_eq_rhoKc`：推荐作为 source-literal bridge；不引入新物理假设。
- `rhoKc_sq_le_of_block_energy`：可独立验收；其 `hp` 来源仍是外部 domain
  obligation。
- deployed `tau` equivalence：明确保留为 `OPEN / NON-EQUIVALENCE BOUNDARY`，不由
  本 review 关闭。

