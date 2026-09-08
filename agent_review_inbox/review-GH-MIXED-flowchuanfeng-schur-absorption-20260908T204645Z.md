---
kind: review_result
task_id: GH-MIXED-flowchuanfeng-schur-absorption
review_id: review-GH-MIXED-flowchuanfeng-schur-absorption-20260908T204645Z
source_agent: Codex-schur-source-obstruction
created_at: 2026-09-08T20:46:45Z
inspected_commit: 0046469d6c31918d50991fe27f36cd1c84c749bf
status: EXACT_UNIFORM_MISSING_WITNESS_OBSTRUCTION
integration_status: pending
admission_label: pending
exact_rational_check: pass
actual_source_binding_proven: false
runtime_verified: false
lean_run: false
state_registry_mutated: false
formal_certificate_allowed: false
P5_closed: false
---

# Schur/PMI：同配置零 port 接口的全方向负 margin 上界

## 1. 新增结论与边界

历史 lane 已有单次 debit、signed-defect 双 gate 和 opposite-base 的抽象结论。
本轮不重复这些一般不等式，而在其实际引用的 block456 source/configuration 上，
把旧的单加速度方向 obstruction 加强为**全部非零 a_C 的统一有理界**：

```text
q=v=w=0, reduced port r_C=0, lT=lBase=-K*a_C
P_direct = beta_C-lT' K^-1 lT <= -(1/256)*||a_C||².
```

对 a_C≠0，实际还有严格小于。因此旧直接9式接口加任意好的 port cap，均不能
独自产生该 slice 的非负 direct target；任何有限 lambda>1 的 Young 分配也不能。

与此同时，在同一理想解析质量配置下，完整原点方程 M_mu(0)*a=0 只允许 a=0。
这精确说明需要补交的不是新 Young 参数，而是同源完整 force/acceleration graph
以及 a_C 的实际投影身份。测试族不是机器人可达状态；也不是整个 factorized ideal
或部署 FD/Float64 模型的反例。

本轮只新增本 immutable review；没有改 state、registry、shared files、旧 review、
P5 cone-index 或源文件。没有运行 Lean/Lake、Julia、producer、solver、采样或全回归。
仅做文本/hash 阅读及两个针对同一原点矩阵的 Fraction stdin 检查；未新增 checker 文件。

## 2. 同一 configuration，明确不混用 DH runtime 或 CSV Mref

E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。
W = `C:/Users/z5242/Desktop/重构版/工作流`。

固定配置为下列现有 include chain 的**精确有理 symbolic/analytic interpretation**：

| source path/行号 | 冻结含义 |
|---|---|
| E/routeB_compact_block456_residual_schur_interface_audit.jl:11,15–36 | include结构源；lambda=2；beta_a=1/100；beta_qv=1/10；beta_w=1/20；H=inv(M0CC456Q)；direct与Young target分开 |
| E/routeB_compact_block456_descriptor_structure_audit.jl:12,16–22,44–76 | C=(4,5,6)，D=(1,2,3)；mu=1/1000000只加一次；原点CS；M0CC、DeltaMDC、lBase、nominal/port/total三组三式 |
| E/routeB_factorized_descriptor_model.jl:188–200 | 从analytic mass/C/G CSV读精确分数；固定本文件自己的controller；g0为同一G的原点值 |
| 同文件:253–263,281–284 | 另定义完整六维force/descriptor结构，不等于block456的nominal port约束 |
| E/routeB_compact_block456_descriptor_structure_audit.jl:145–148 | all_eq456组装的是link/remote/port/total等式，不凭此获得实际加速度身份 |

尤其本 include chain 的 Kd=[4,5,3,1,2,3]/5，Bfr=[1,2/5,7/20,3/10,1/4,1/5]。
它们不是 dhport_lib.jl 的整组 damping 常量。本轮没有将其改成 DH branch，也没有
因原点速度为0使 damping 项消失，就宣称两个完整模型相同。

这里 K 是 analytic mass 原点加一次精确 mu 后的3×3主块，不是实际 Float64
`routeB_Mq_M0.csv` 对角读取，不是 M_CC(q)，也不是 B_up^-1。
所有 L/Q/cross term 均使用同一 H=K^-1。

## 3. 从实际 mass CSV 重构的精确矩阵与全方向界

对 E/routeB_analytic_mass_full_cs_polynomial.csv：令全部 sine=0、cosine=1，
保留 sine 指数全0的项并按(row,col)精确求和，再在六个对角加1/1000000。
C×C原点项来自物理行269、271、272、289、296、297；非零 sine 项自动消失。

得到

```text
K = [350003/3000000       0               1/60
            0       200739/4000000          0
           1/60          0          50003/3000000].
```

取 kappa=1/256。令 A=K-(1/100+1/256)I，其精确值为

```text
A = [1233137/12000000       0                1/60
              0       72557/2000000            0
             1/60          0            33137/12000000].
```

对任意 x∈R³，下面不是方向探针，而是系数级恒等式：

```text
x'Ax = (1233137/12000000)*(x1+(200000/1233137)*x3)^2
     + (72557/2000000)*x2^2
     + (287486923/4932548000000)*x3^2.
```

三个系数均严格正，线性换元可逆；故 A正定，特别地
`a_C'K*a_C >= (1/100+1/256)*||a_C||²`。
Fraction 重构逐项核对了此 R^T diag(d) R 恒等式；另核对leading minors：

```text
1233137/12000000
89472721309/24000000000000
20859188672111/96000000000000000000
```

均严格正。这是一个明确有理安全界，不声称1/256是最优常数。
源旁的 origin_beta_audit 已报告 beta_a I-K 负定；本轮没有只复述该布尔值，
而是独立从 mass CSV 得到上述统一余量和可检查的补平方。

## 4. Exact missing-witness obstruction：完整保留 single debit

在q=v=w=0、真实原点CS，结构源给DeltaMDC=0和fC=0。任取a_C，令v_D=0、r_C=0，
lT=lBase=-K*a_C。于是nominal_eq456、port_eq456、total_eq456三组三式全部成立。
此处只声称这9个直接等式；没有核验每个factorized auxiliary/理想流形约束。

同一H下，Q=r_C'Hr_C=0、cross=<lBase,r_C>_H=0、
L=lBase'HlBase=a_C'K*a_C、beta_C=(1/100)||a_C||²。因此

```text
P_direct = beta_C-L <= -(1/256)||a_C||².
```

这是实际source固定beta模板上的结论，不是通过自由改变beta造出的opposite-base例子。
即使抽象defect扩展给出最有利的d=0、signed debits u=s=D=0，这个nominal base deficit
仍存在；这里并未认证实际FD/controller/solve defect为0。

对任意lambda>1、任意合法cap W>=Q=0，正确单次Young扣账精确等于

```text
P_Young = beta_C-lambda*W-lambda/(lambda-1)*L
        = P_direct-L/(lambda-1)-lambda*W
        <= P_direct.
```

所以对a_C≠0，所有有限lambda>1及所有合法W均不可能给出P_Young>=0。
把cap改善到W=0，或令lambda趋于无穷，只能使supremum趋近仍为负的P_direct。
此结论不要求旧global rho²/B_up是否真的构成source cap；给理想cap也不足。

若继续沿用SchurPMIBinding的特定接线E=E_A、Q=port square、margin=P_direct，
则对a_C≠0，E_A=a_C'B_up*a_C>0而P_direct<0，`E_A-Q<=P_direct`必失败。
更一般地，任何E>=0都不能在此测试点与该负margin构成该binding。
这不是说任意另定义的physical margin都为负；结论只针对所列source direct target。

relative coefficient的strict slack不会给出缺失binding。signed-debit信息用于保留
真实cross term，不能凭空生成base；重复扣Q/B只会更保守，漏掉base loss则不健全。

## 5. 同模型完整graph排除测试族：最小下一跳

在相同q=v=w=0和controller配置，源rhs定义给g0-G=0、C(v,v)=0，因此完整rhs=0。
本轮从同一CSV重构的完整6×6 M_mu(0) 精确对称，六个LDL pivot严格正，并逐项通过
M=L diag(d) L^T重构。因此完整理想方程

```text
M_mu(0)*a_full=0, a_C=(a_full4,a_full5,a_full6)
```

唯一给a_full=0。这将上述所有a_C≠0测试点排除于该完整理想graph之外。
故不能将本obstruction推广为机器人不稳定、reachable counterexample，或在加入
完整source图之后仍不可能证明目标的结论。

下一跳应交一个同配置的窄binding，而不是再搜Young参数：

1. a_C是同一次完整六维source acceleration的4/5/6投影；不能是自由PMI变量。
2. 把remote nominal-subtracted v_D与actual a_D的reference关系明确绑定，并连同
   retained C force rows/完整six-row force balance使用；不能只交port三式。
3. 若声称exact analytic graph，给同质量/regularizer/rhs的等式；若是数值source，
   显式保留force/solve defects及其same-H signed debit，不把Float64反斜杠当精确方程。
4. 完成上述接线后，在真实source-domain上重新判断direct margin floor；本原点排除
   不证明其他状态的positivity，也不提供full-domain/P8 coverage。

Source source-identity、域覆盖、runtime refinement 与后续统一margin仍PENDING。
这里没有建议静默删除actual状态，也没有修改beta、source target或registry。

## 6. 哈希、验证范围与历史材料

| 路径 | SHA-256 |
|---|---|
| E/routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| E/routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| E/routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| E/routeB_compact_block456_residual_schur_interface_audit.jl | 3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98 |
| E/routeB_compact_block456_direct_target_origin_beta_audit.jl | ed69ec4af06d69e00e980c68a3b861a086c7e42396b2b4ef3daac0f6c42c241a |
| E/routeB_compact_block456_direct_target_origin_beta_audit.csv | d6260d4a02b1fb32074bd036296c96929b614b6baa2fa4398bd78026d7bf174a |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean | f18f9fb180aeafaad0dc3cd5149894d03ee111db5c45abfb86caa927df4050e3 |
| W/agent_review_inbox/review-GH-MIXED-flowchuanfeng-schur-absorption-liuchuanafeng-20260907T1823.md | 3d87c8d84afd6ae4a44bf2b80d7b3a06d3f167a61871e2bfa5beef0216a2a5c2 |
| W/agent_review_inbox/review-GH-MIXED-flowchuanfeng-schur-absorption-takeover-codex-20260908T101432.md | 565f536cf93ea26b3125cc46418cd6c1593e236538a1c3f129cbb37a550a37de |
| W/agent_review_inbox/review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-20260908T105720.md | 4a7b5d054f53bef37d920d70682b3769d97ab19076622a0bdd5a0a4c19fe476f |

历史signed gates/source-binding reviews仅用来避免重复数学与定位缺口；没有继承任何
旧Lean编译或source-admission状态。本轮精确检查是原点矩阵系数/LDL检查，不是有限
方向测试，也不是全模型回归。未生成compile receipt、source packet或P5 closure。
