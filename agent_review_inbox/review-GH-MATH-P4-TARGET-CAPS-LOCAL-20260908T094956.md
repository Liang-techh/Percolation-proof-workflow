---
kind: review_result
review_id: review-GH-MATH-P4-TARGET-CAPS-LOCAL-20260908T094956
task_id: GH-MATH-P4-TARGET-CAPS
source_agent: codex-local
created_at: 2026-09-08T09:49:56-06:00
inspected_commit: a370eff67b6d694a7387525a3a53ea94c85bd582
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCaps.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean
  - examples/routeb_block456_beta_design_research/NEW_BETA_DESIGN_check.py
integration_status: pending
admission_label: pending
proof_status: READ_ONLY_MATHEMATICAL_REVIEW
kernel_verified: false
final_integration: false
registry_promoted: false
formal_certificate_allowed: false
requested_action: Supply same-source domain, acceleration remainder and block456 correction/metric witnesses before using the local bank for A_upper or port caps.
---

# TARGET-CAPS：local remainder 不能直接覆盖真实 DH target

结论：在本轮检查的接口中未找到闭合 witness。存在确定的域包含反例；此外还有
analytic/central-FD/Float64 源区分、remainder/总加速度区分，以及 block456 修正变量
与物理加速度区分。该结论不是“物理路径必然越界”或“不可能存在证书”。

本轮只读源码与 JSON 元数据，并做下述纸面精确推导；没有运行 Python producer/
checker、Julia、Lean/Lake、采样或全回归。只新增本 review，不修改 state/registry。

## 1. 当前外部源与 bank 的实际含义

外部根 R 为
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`。
以下路径相对 R，不与另一个 robot_final 副本混同。

`robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json:2-4`
标记 formal=false，scope 为 analytic CSV、相同对称域、|w|≤2、非 flowpipe。
它的 domains 引用五个 slab；从当前 slab 读取的精确参数为：

| slab | 每个角半径 r | 每个速度半径 s | step |
|---|---|---|---|
| initial_analytic_slab_v1.json | 4/25 | 3/10 | 1/256 |
| expanded_analytic_slab_v1.json | 1/5 | 3/5 | 1/256 |
| adaptive_domain_0_v1.json | 1/4 | 9/10 | 1/256 |
| adaptive_domain_1_v1.json | 3/10 | 6/5 | 1/256 |
| adaptive_domain_2_v1.json | 7/20 | 3/2 | 1/256 |

slab scope 为 full initial Euclidean ball radius 3/20、measurable |w|≤2、first slab
only。五个嵌套空间盒不是五个已连接的时间步，更不是 [0,1] 的路径覆盖。

`exact_checks/combined_descriptor_remainder.py:33-90`（位于 robot_formal_v1）
读取线性矩阵 A、M0、解析质量/重力/Coriolis CSV，按各盒角/速度/w cap 计算
预条件化缺陷 b，给出 D=(I-C)^(-1)b。实际代码按 ars+vc+[2] 收缩质量缺陷。
`affine_initial_endpoint.py:27-46` 单独保留 a1=|A|caps，再将 D 注入加速度余项。
所以拟证明的是 |a_analytic-A(q,v,w)|≤D，而不是 |a_analytic|≤D。

`check_combined_descriptor_remainder.py:26-86` 重构多项式区间并检查 b+CD≤D；
其文本不独自提供收缩与物理源同一性。收缩约束在另一个
`check_initial_analytic_slab.py:38-47`：正 weights、0≤kappa<1、C weights≤kappa weights。
这些都未在本轮执行，也没有把 JSON 中数值当作已证的全称不等式。

## 2. 四种域必须分开

令 E={ (3/2)Σq_j²+(4/5)Σv_j²≤28/5 }，求和均为全部六坐标。

- E ⇒ q_j²≤56/15<4、v_j²≤7<9，因此 |q_j|≤2、|v_j|≤3。
  再给 w²≤3，可得目标粗 cap |q|≤5/2、|v|≤15、|w|≤2。
  这是合法的条件包含；并未证明真实 target 或轨迹在 E 内。
- `routeB_dense_Mq/routeB_certificate_manifest.toml:25` 的 p 只含 q4,q5,dq4,dq5，
  不是 E。精确点 q1=3、dq1=16、其余零满足 p45=0，却违反两项粗 cap。
  这是集合不包含反例，不声称它是从初始球可达的状态。
- V≤1 本身不能推出任何指定 full-state coercivity。若 V 只依赖 block45，
  在任意 V≤1 的 block 切片上远端坐标可任意延伸。若显式另给
  (1/5)Σq²≤V、(9401/2000000)Σv²≤V，则 q²≤5<25/4、
  v²≤2000000/9401<225，才可推出粗 q/v cap。扰动仍需独立前提。
  当前 TargetCaps.lean 恰将这些作为参数；它是未编译条件接口，不是 V 的源绑定。
- 每个 bank 盒 B_i 本身确实包含于粗 cap 域；但反向不成立，E⊂∪B_i 也不成立。
  精确点 q1=1、v=0、其他 q=0、w=0 在 E 内（p_full=3/2），却因 1>7/20
  在全部五个盒外。即便再交 p45 target，该反例仍保留。

对非零中心盒必须用 |center_j|+radius_j≤cap_j，不能只检查半径。
对 path coverage 还需 ∀初值∈初始球、∀允许输入、∀t∈[0,1]，路径状态属于某个
已绑定盒。初始球确实在第一盒内，但这不是流不变性；端点包含也不证明步内包含。
manifest:3-5 的 coverage_completed=true 同时明确 trajectory_monte_carlo_only 与
global_box_coverage=false，不能用第一个布尔值覆盖后两个限定。

## 3. Analytic remainder 如何才可能变成同源 acceleration cap

设 z=(q,v,w)，在某个已覆盖盒内有 |z_k|≤c_k，并证明同源
a_analytic=A z+e、|e_j|≤D_j。则可合法定义

```text
L_j = Σ_k |A_jk| c_k + D_j,
|a_analytic,j| ≤ L_j.
```

精确反例说明不能丢掉线性项：标量 a=z=1、A=1、e=0、D=0 满足零余项界，
但 |a|≤D 为假。这只是对错误推理的反例，不是当前 DH 取值诊断。

`routeB_dense_Mq/dhport_lib.jl:73-111` 实际用 M(q±h e_k)、U(q±h e_k)
central differences 构造 C_h/G_h，再执行 Float64 线性求解。解析 CSV 的导数
不是自动等于这些差分。若先证明 exact-real 相同 M 与
|rhs_FD-rhs_analytic|₂≤ε、M≽μI、μ>0，则
|a_FD-a_analytic|₂≤ε/μ，故每坐标可加 ε/μ。
不同质量矩阵需要额外 perturbation 项；Float64/libm/求解舍入还需独立 seam。

FD 需要源恒等式及误差界覆盖整条 q+s e_k，|s|≤h（并含 G_h(0) 的 stencil）。
小盒边界上的外移点不在原盒；E 同样不对 stencil 封闭：取 q=0，
v=(2,1,1,1,0,0)，则 p_full=28/5；任意非零角位移 δe1 使其增加 (3/2)δ²。
可改用扩大源域，但不能声称仍在原 E。E 的 |q|≤2 与 h≤1/2 可以推出
扩大 stencil 位于 |q|≤5/2；这依旧不能把小盒 remainder 向外延拓。

## 4. block456 的 Aup 与 port 不是 block45 consumer 的字段

`routeB_compact_block456_residual_schur_interface_audit.jl:15-35` 定义

```text
Bup = (133374,50185,33335)/1000000,
Aup456 = Σ_{k=1..3} Bup_k aC_k²,
W = M0CC456^(-1),
port quadratic 使用 rC' W rC，lBase 使用 lBase' W lBase。
```

这不是 NEW_P4_032_DescriptorPUpper.lean 中的双通道 metric，也不是任意叫作
A_upper 的 ||lBase||² 上界。若同源物理 aC=(a4,a5,a6) 已绑定且有上述 L，
可得到 Aup456≤Σ Bup_k L_{k+3}²。Bup 的“upper”性质及 rho²=589578/1000000
对哪些盒、哪些 metric 成立，仍需覆盖与算子界 witness；代码注释的 resolved
ledger/upward diagnostic 不代替它。

`routeB_compact_block456_descriptor_structure_audit.jl:43-70` 给出的是

```text
MDD vD + (MDC-M0DC) aC = 0,
rC = MCD vD,
lBase = diag(IVAL_C) fC - M0CC aC.
```

因此 vD 是修正变量，不能直接设为物理 aD。物理 D 行应为
MDD aD+MDC aC=rhsD。若要满足上式，一个候选定义是
vD=aD-MDD^(-1)(rhsD-M0DC aC)，而不是 vD=aD。
前者与真实 residual/total 的 source embedding 还必须核对，尤其 fC 是 nominal
force field，不能自动替换实际 C_h/G_h 的受控力。

源接线成立、MDD≽μ_D I、同盒算子界 ||MCD||≤H_CD、||ΔMDC||≤H_Δ 时，才有

```text
||rC||₂ ≤ (H_CD H_Δ / μ_D) ||aC||₂,
rC' W rC ≤ ω (H_CD H_Δ / μ_D)² Σ L_C²,
```

其中 W≼ωI 必须单独证明。没有匹配 metric 的 witness，Euclidean port cap
不能原样填入 W-metric。对 lBase，可先逐坐标用
F_i≥|IVAL_i fC_i|、T_i=F_i+Σ_j |M0CC_ij|L_Cj，得 ||lBase||²≤ΣT_i²，
或 lBase'W lBase≤ωΣT_i²。这是可执行的证明义务清单，不是当前得到的数值 cap。

若只保留粗 q/v/w cap 而忘记 descriptor graph，则在 q=v=w=0、aC=(n,0,0)
上 Aup456=(133374/1000000)n² 无界；M0CC 可逆时 lBase=-M0CC aC 也无界。
这个自由变量反例不能宣称为物理 DH 反例；其用途正是说明 graph witness 不可省略。

## 5. 最小关闭清单与证据身份

需要：真实 target 定义与空间/路径 cover；每盒 analytic 源与收缩/remainder
证明；完整线性项；FD 与数值 seam（按主张级别）；physical acceleration 与
block456 修正变量/source embedding；同盒同 metric 的 port/lBase 上界。
已有 P4 双通道 Lean 候选只能说明条件接口的形状，不能移植常数后自动关闭三通道。

当前只获得文件快照。以下 SHA-256 相对外部 R：

```text
robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json
68596f1557aa709d86bc8711ed7985552684dffe7fde290abf03b511f6bd9805
robot_formal_v1/exact_checks/combined_descriptor_remainder.py
babaebf0cd5e7f0cf3a68c116d24e0f67dfea547ee906846a2f4da5633c4fb5f
robot_formal_v1/exact_checks/check_combined_descriptor_remainder.py
5f16afadaa1291da81c37e8bab98bd396b6f07e853436e3ce11e9aa0d53c3d0a
routeB_dense_Mq/dhport_lib.jl
aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
routeB_dense_Mq/routeB_certificate_manifest.toml
d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495
routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl
9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79
routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl
3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98
```

没有核验 JSON 内全部 source_hashes，也没有声称其生成程序与历史输出完全同步。
工作流 HEAD 不是外部源仓库的 commit；上列字节绑定不冒充 provenance admission。
