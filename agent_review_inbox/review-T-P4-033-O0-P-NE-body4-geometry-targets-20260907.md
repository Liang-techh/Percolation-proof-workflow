# T-P4-033 O0/P-NE：human body-4（zero-based 3）exact DH 几何 review

状态：`CONDITIONAL_BODY4_GEOMETRY_DERIVATION`。本 review 只处理 human body-4，即 `body = (3 : Fin 6)`；不重述 body-1/2/3，不消费 baseline/Schur margin，不修改 registry，也未运行本机 Lean/Lake。

## 绑定与边界

```text
source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)
state_key  = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
orientation = source-frame DH, prefix frame slots, body Gram = m JvᵀJv + κ JwᵀJw
```

当前 source/trace 合同仍是 open/uncompiled target：已有 body-4 trace expression 和 `h_body_4` proposition target，但没有本轮可消费的 compiled source-to-trace theorem。因此以下是可交给 Lean/interval agent 的 exact symbolic child，不是正式 admission。

## 1. Slot / axis reduction

只保留 `q 0,q 1,q 2`，令

```text
q₀ := q 0, q₁ := q 1, q₂ := q 2, φ := q₁ + q₂
e_r := (cos q₀, sin q₀, 0)
e_t := (-sin q₀, cos q₀, 0)
e₃ := (0, 0, 1)
U := 2/25 + (21/100) sin q₁
B := (21/100) sin q₁
C := (21/100) cos q₁
D := 1/20
E := 19/200
A := U + E sin φ
P := C + E cos φ
Q := B + E sin φ
```

`routeBFrameSlot q i` 的 body-4 所需 prefix reductions 是：

```text
slot 0 : I
slot 1 : I · T₀
slot 2 : (I · T₀) · T₁
slot 3 : ((I · T₀) · T₁) · T₂
slot 4 : (((I · T₀) · T₁) · T₂) · T₃
```

其中当前 DH 相位约定给出：

```text
o₀ = 0
o₁ = (2/25) e_r + (1/10) e₃
o₂ = U e_r + (1/10 + C) e₃
o₃ = o₂ + D e_t
o₄ = o₃ + (19/100) z₃
```

父轴（即各 joint 的 source-axis slot）为

```text
z₀ = e₃
z₁ = z₂ = e_t
z₃ = sin φ e_r + cos φ e₃
```

这里 `z₃` 的 `+ cos φ e₃` 符号是当前 `routeBRealCos/routeBRealSin` 与 `α₀=-π/2` 的结果；不可替换成 `sin φ e_r - cos φ e₃`。`q₃` 不出现：第 4 个 DH step 的 `a₃=0`，body-4 只用 slot-3 parent axis 和 slot-3/4 COM endpoints。

## 2. COM、active columns 与 Gram target

body-4 的 COM 是 `c₃=(o₃+o₄)/2=o₃+E z₃`。前三个非零线速度列、第四列和角速度列应分别化为

```text
r₀ := c₃ - o₀ = A e_r + D e_t + (1/10 + C + E cos φ) e₃
r₁ := c₃ - o₁ = (B + E sin φ) e_r + D e_t + (C + E cos φ) e₃
r₂ := c₃ - o₂ = D e_t + E z₃
r₃ := c₃ - o₃ = E z₃

v₀ := Jv[0] = e₃ × r₀ = A e_t - D e_r
v₁ := Jv[1] = e_t × r₁ = P e_r - Q e₃
v₂ := Jv[2] = e_t × r₂ = E(cos φ e_r - sin φ e₃)
v₃ := Jv[3] = z₃ × r₃ = 0
v₄ := v₅ := 0

w₀ := Jw[0] = e₃
w₁ := Jw[1] = e_t
w₂ := Jw[2] = e_t
w₃ := Jw[3] = z₃
w₄ := w₅ := 0
```

所以 active joint columns 是 exactly `{0,1,2,3}`；`j ≥ 4` 必须由 `bodyJv_zero_of_inactive` / `bodyJw_zero_of_inactive` 关闭，而不是由 Fourier CSV 的缺行推断。

用 `m₃=2/5`、`κ₃=1/15`，先证明未展开 Gram：

```text
Gv00 = A² + D²
Gv01 = Gv10 = -D P
Gv02 = Gv20 = -D E cos φ
Gv03 = Gv30 = 0
Gv11 = P² + Q²
Gv12 = Gv21 = E(P cos φ + Q sin φ)
Gv22 = E²
Gv13 = Gv31 = Gv23 = Gv32 = Gv33 = 0

Gw = [[1, 0, 0,  cos φ],
      [0, 1, 1,  0],
      [0, 1, 1,  0],
      [cos φ, 0, 0, 1]]
```

建议 Lean 先证明上述 `Gv/Gw` entry lemmas，再做有理数 ring normalization；不要直接让 `ring_nf` 穿过未消去的 `Matrix` fold。

## 3. 最小 trig reduction

所需 identities 只有以下几类：

```text
e_r · e_r = 1,  e_t · e_t = 1,  e_r · e_t = 0,
e₃ · e_r = e₃ · e_t = 0,
sin² x + cos² x = 1,
sin q₁ sin φ + cos q₁ cos φ = cos(q₁ - φ) = cos q₂,
sin² x = (1 - cos(2x))/2,
sin x sin y = (cos(x-y) - cos(x+y))/2.
```

其中 `Gv11`、`Gv12` 的关键归并是

```text
P² + Q² = (21/100)² + E² + 2E(B sin φ + C cos φ)
        = 441/10000 + 361/40000 + (399/10000) cos q₂,

E(P cos φ + Q sin φ) = E² + E(B sin φ + C cos φ)
                        = 361/40000 + (399/20000) cos q₂.
```

`Gv00` 的双角展开同时使用 `φ=q₁+q₂` 和
`sin q₁ sin φ=(cos q₂-cos(2q₁+q₂))/2`。

## 4. Exact 4×4 body-4 mass/Fourier target

令 `T₃ := (2/5) Gv + (1/15) Gw`。目标矩阵为对称矩阵，非零 entry 只有：

```text
T₃[0,0] = 48511/600000
           + (42/3125) sin q₁
           + (19/3125) sin(q₁+q₂)
           + (399/50000) cos q₂
           - (441/50000) cos(2q₁)
           - (399/50000) cos(2q₁+q₂)
           - (361/200000) cos(2q₁+2q₂)

T₃[0,1] = T₃[1,0]
         = -(21/5000) cos q₁ - (19/10000) cos(q₁+q₂)

T₃[0,2] = T₃[2,0] = -(19/10000) cos(q₁+q₂)
T₃[0,3] = T₃[3,0] =  (1/15) cos(q₁+q₂)

T₃[1,1] = 211/2400 + (399/25000) cos q₂
T₃[1,2] = T₃[2,1] = 21083/300000 + (399/50000) cos q₂
T₃[2,2] = 21083/300000
T₃[3,3] = 1/15

T₃[1,3] = T₃[3,1] = 0
T₃[2,3] = T₃[3,2] = 0
```

Fourier atom support（只对 `q₁,q₂` 非零）应规范化为：

```text
T00: ±(2,2), ±(2,1), ±(2,0), ±(1,1), ±(1,0), ±(0,1), 0
T01/T10: ±(1,1), ±(1,0)
T02/T20: ±(1,1)
T03/T30: ±(1,1)
T11: 0, ±(0,1)
T12/T21: 0, ±(0,1)
T22: 0
T33: 0
```

在 `realCoeff*cos(ν·q)-imagCoeff*sin(ν·q)` 的 trace convention 下，`T00` 的代表 atom 是
`(-361/400000,2,2)`、`(-399/100000,2,1)`、`(-441/100000,2,0)`、`imag=19/6250` at `(1,1)`、`imag=21/3125` at `(1,0)`、`real=399/100000` at `(0,1)`，及 conjugate atoms；这与上面的合并式一致。这里的 atom list 仅是 exact target，不等同于已证明 source equality。

## 5. 最小 compiled lemma 清单

按依赖顺序，Lean/interval agent 只需新增以下 child；定理名可调整，但 statement 不应放宽：

1. `body4_frame_slot_0_to_4`：对 `i=0,...,4` 展开 `routeBFrameSlot q i`，显式处理 `Matrix.mul_apply`、`Matrix.mul_assoc`、`one_mul`、`mul_one`；不能用未经确认的 `simp` 猜测左/右结合。
2. `body4_slot_origin_exact`：由上述 slots 得出 `o₀,...,o₄` 的五个坐标等式。
3. `body4_source_axis_exact`：得出 `z₀=e₃`、`z₁=z₂=e_t`、`z₃=sin φ e_r+cos φ e₃`，并锁定 `routeBRealCos/routeBRealSin` 相位。
4. `body4_com_displacements_exact`：把 `bodyCom` 和四个 `rⱼ` 化成上面的 exact vectors。
5. `body4_cross_columns_exact`：逐列证明 `v₀,v₁,v₂,v₃`；另证明 `j≥4` 的 inactive zero。
6. `body4_angular_columns_exact`：逐列证明 `w₀,...,w₅`。
7. `body4_dot_trig_orthonormal`：封装 `e_r/e_t/e₃` dot/cross 与 `sin_sq_add_cos_sq`、`cos_sub`、double-angle identities。
8. `body4_gram_entries_exact`：证明 `Gv` 与 `Gw` 的 entry formulas；这一步不涉及 Fourier fold。
9. `body4_mass_entries_exact`：在 `m=2/5, κ=1/15` 下证明上面的 `T₃[i,j]` piecewise formulas，使用 `ring`/有理数归一化。
10. `body4_fourier_atom_fold_exact`：将 `bodyTraceEvaluator 3 q i j` 的 finite tagged fold 归并到同一 piecewise formulas；需证明 body,row,col 与频率筛选的有限 case split 及 conjugate atom normalization。
11. `h_body_4_source_to_trace_compiled`：最终只接受
    `∀ q i j, sourceBodyMass q (3 : Fin 6) i j = bodyTraceEvaluator 3 q i j`，并在同一 source/state key 下给出 `#print axioms` 与 zero `sorry/admit` receipt。

## Fail-closed receipt

本轮可确认的是 exact symbolic target 和最小 proof decomposition；不能确认 `h_body_4_source_to_trace_compiled` 已存在。当前 `RouteBO1PerBodyTraceAdapter.lean` 仍是 target-level adapter，`BodyTraceEvaluator.lean` 是 generated evaluator，均不应升级成 formal source binding。故 receipt 状态保持 `CONDITIONAL_BODY4_GEOMETRY_DERIVATION`，`consumable_now=false`；后续只有在 pinned environment 编译并审计 axioms/sorry/admit 后，才可转为可消费 child。

## Evidence（只作 provenance，不代表已证明）

| artifact | SHA-256 | role |
|---|---|---|
| `examples/routeb_real_dh_step_lean/RealDHStep.lean` | `9C04DA5B9627EE749C53009733006934F95B2D33265E46CA59D0725AA453786A` | exact DH step/cos-sin phase |
| `examples/routeb_frame_slot_accessor_lean/FrameSlotAccessor.lean` | `F497BD1F45FAE4DD385F4D0F46DF79252C92E5CD027B29D5DC55011F91525C31` | prefix slot/source origin-axis access |
| `examples/routeb_body_semantic_core_lean/BodySemanticCore.lean` | `FE15F6CA9993F55FC56E6D2C9CCA5FA8C7F6E9530B9B900A6F111ED96715149C` | COM/Jv/Jw/body Gram semantics |
| `examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyExactSource.lean` | `C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553` | source mass/inertia constants and body source definition |
| `examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean` | `B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA` | generated trace evaluator, uncompiled |
| `examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyTraceAdapter.lean` | `C6FC99DE41F8A5010CD79F18B89FD39811B63717810E437A5AE88DD6095F2FE7` | body proposition targets, uncompiled |
