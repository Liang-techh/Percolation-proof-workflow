# T-P4-033 O1 next — exact port identity / Schur action

范围严格限定为 exact-real 的有限维线性代数与 Schur 消元；本审阅不改 canonical candidate、state 或 registry，也不做大回归。

## 结论

纯线性代数部分没有 obstruction。最小可证明链应拆为：

1. `eliminate_D`：由 D-block 方程和左逆消去 `v`；
2. `schur_port_action`：把消去式左乘 `M_BD`，得到端口作用式；
3. `routeB_port_identity`：再接上 `h_B : r_B - M_BD.mulVec v = 0` 并展开 `R_port`。

这三个命题的临时 probe 已在当前 pinned Mathlib 源树下定向编译通过（Lean exit code 0，无 `sorry`/`axiom`）；该 probe 已删除，不能替代 canonical candidate 的正式 compile/admission receipt。

## 可直接交给 Lean agent 的最小接口

```lean
import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic.Linarith

set_option autoImplicit false
open scoped Matrix

abbrev DVec (d : Nat) := Fin d → ℝ
abbrev BVec (b : Nat) := Fin b → ℝ

def R_port {d b : Nat}
    (M_BD : Matrix (Fin b) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ) :
    Matrix (Fin b) (Fin b) ℝ :=
  -(M_BD * M_DD_inv * DeltaM_DB)

lemma eliminate_D {d b : Nat}
    (M_DD : Matrix (Fin d) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ)
    (v : DVec d) (a_B : BVec b)
    (h_inv_left : M_DD_inv * M_DD = (1 : Matrix (Fin d) (Fin d) ℝ))
    (h_D : M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0) :
    v = -(M_DD_inv.mulVec (DeltaM_DB.mulVec a_B)) := by
  have hD_left := congrArg
    (fun x : DVec d => M_DD_inv *ᵥ x) h_D
  have hsolve :
      v + M_DD_inv *ᵥ (DeltaM_DB *ᵥ a_B) = 0 := by
    simpa only [Matrix.mulVec_add, Matrix.mulVec_zero,
      Matrix.mulVec_mulVec, h_inv_left, Matrix.one_mulVec] using hD_left
  funext i
  have hi := congrFun hsolve i
  change v i + (M_DD_inv *ᵥ (DeltaM_DB *ᵥ a_B)) i = 0 at hi
  change v i = -(M_DD_inv *ᵥ (DeltaM_DB *ᵥ a_B)) i
  linarith

lemma schur_port_action {d b : Nat}
    (M_DD : Matrix (Fin d) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ)
    (M_BD : Matrix (Fin b) (Fin d) ℝ)
    (v : DVec d) (a_B : BVec b)
    (h_inv_left : M_DD_inv * M_DD = (1 : Matrix (Fin d) (Fin d) ℝ))
    (h_D : M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0) :
    M_BD.mulVec v =
      -((M_BD * M_DD_inv * DeltaM_DB).mulVec a_B) := by
  have hv := eliminate_D M_DD M_DD_inv DeltaM_DB v a_B h_inv_left h_D
  have h := congrArg (fun x : DVec d => M_BD *ᵥ x) hv
  funext i
  have hi := congrFun h i
  change (M_BD *ᵥ v) i =
    (M_BD *ᵥ (-(M_DD_inv *ᵥ (DeltaM_DB *ᵥ a_B)))) i at hi
  simpa only [Matrix.mulVec_neg, Matrix.mulVec_mulVec,
    Matrix.mul_assoc] using hi

theorem routeB_port_identity {d b : Nat}
    (M_DD : Matrix (Fin d) (Fin d) ℝ)
    (M_DD_inv : Matrix (Fin d) (Fin d) ℝ)
    (DeltaM_DB : Matrix (Fin d) (Fin b) ℝ)
    (M_BD : Matrix (Fin b) (Fin d) ℝ)
    (v : DVec d) (a_B r_B : BVec b)
    (h_inv_left : M_DD_inv * M_DD = (1 : Matrix (Fin d) (Fin d) ℝ))
    (h_D : M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0)
    (h_B : r_B - M_BD.mulVec v = 0) :
    (R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B = r_B := by
  have hremote := schur_port_action M_DD M_DD_inv DeltaM_DB M_BD
    v a_B h_inv_left h_D
  have hresidual : r_B = M_BD *ᵥ v := by
    funext i
    have hi := congrFun h_B i
    change r_B i - (M_BD *ᵥ v) i = 0 at hi
    linarith
  calc
    (R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B =
        -((M_BD * M_DD_inv * DeltaM_DB) *ᵥ a_B) := by
      rw [R_port, Matrix.neg_mulVec]
    _ = M_BD *ᵥ v := hremote.symm
    _ = r_B := hresidual.symm
```

这里 `Matrix.mul_assoc` 只处理括号，不改变因子顺序；必须保留 `M_BD * M_DD_inv * DeltaM_DB`，不可交换或转置任一因子。

## 维度与 true-DH block-(4,5) 分界

令 `B = {4,5}`、`D = {1,2,3,6}`（Lean 的 `Fin 6` 索引为 `Bidx = ![3,4]`、`Didx = ![0,1,2,5]`）。则：

```text
M_DD       : D×D
M_DD_inv   : D×D
DeltaM_DB  : D×B
M_BD       : B×D
R_port     : B×B
```

直接用行/列投影定义：

```lean
def blockExtract {ι κ : Type}
    (A : Matrix (Fin 6) (Fin 6) ℝ)
    (rows : ι → Fin 6) (cols : κ → Fin 6) :
    Matrix ι κ ℝ := fun i j => A (rows i) (cols j)

def Bidx : Fin 2 → Fin 6 := ![3, 4]
def Didx : Fin 4 → Fin 6 := ![0, 1, 2, 5]
def M_BD45 (M : Matrix (Fin 6) (Fin 6) ℝ) := blockExtract M Bidx Didx
def M_DD45 (M : Matrix (Fin 6) (Fin 6) ℝ) := blockExtract M Didx Didx
def M_DB45 (M : Matrix (Fin 6) (Fin 6) ℝ) := blockExtract M Didx Bidx
def DeltaM_DB45 (M M0 : Matrix (Fin 6) (Fin 6) ℝ) :=
  M_DB45 M - M_DB45 M0
```

然后 adapter 只需把 `M_DD45 M`、`DeltaM_DB45 M M0`、`M_BD45 M` 代入 `routeB_port_identity`。它只证明“给定已投影的 `h_inv_left`, `h_D`, `h_B` 后结论成立”，不证明这些 premises 来自完整 true-DH 方程。尤其不能把 `M_BD` 默认为转置；若要使用对称性，须另给 exact-real 对称性 lemma。

## 系数归一化边界

核心 Schur lemma 不应引入 `k_c`、`I_B` 或 `M0_BB`。它只处理 `DeltaM_DB = M_DB - M0_DB` 与 `r_B` 的同一坐标/单位约定。若 `r_B` 是 force-side residual，source adapter 才负责 force 归一化（当前约定的 cross term 为 `(q5/100, q4/200)`）；不能把 acceleration-side 的 `I_B = diag(1/5,1/10)` 混入核心 identity，也不能将 `k_c` 吸收到 `R_port` 后再宣称同一恒等式。

## 明确剩余 obstruction 与所需 receipt

1. Canonical candidate 当前仍是 `REPAIR_PATCHED__PENDING_LEAN_COMPILE`：需补 `Mathlib.Data.Real.Basic`、`open scoped Matrix`，并采用上述坐标级 `change` 与 `hresidual.symm` 修复。临时 probe 的 exit 0 不是 canonical verification。
2. State 给的是 `det(M_DD) ≠ 0`，而最小 Lean lemma 需要显式 `h_inv_left`。需要一份 pinned Mathlib 下的 exact adapter/receipt，把非奇异性转成同一 `M_DD_inv` 的 `M_DD_inv * M_DD = 1`；在此之前不把 determinant claim 当作 lemma premise 已被绑定。
3. 需要 true-DH block extraction receipt：完整 `6×6` 矩阵、`Bidx/Didx`、行列方向、`M0` 绑定及 hash，证明使用的四个 projected blocks 与 source formula 是同一对象。
4. 需要 exact-real projected balance receipt，分别给出本定理所需的 `h_D` 与 `h_B`；现有 scalar bridge 不能替代完整矩阵 projected premises。
5. 需要同一 `(mu,q)` 下 `M_DD` 与 inverse witness 的 receipt；不能用另一个 regularization、另一个 q box 或数值逆近似代替。
6. 正式 admission 仍需 pinned Lean compile exit 0、zero-sorry/allowed-axioms、statement comparator 与 candidate hash receipts。完成前保持 `P4.true_dh_exact_real_coefficient_identity` open，禁止 registry promotion。

以上是 O1 exact port identity 的数学最小闭环；其余 source/controller 绑定问题属于 adapter 层，不在本次 Schur identity 证明内。
