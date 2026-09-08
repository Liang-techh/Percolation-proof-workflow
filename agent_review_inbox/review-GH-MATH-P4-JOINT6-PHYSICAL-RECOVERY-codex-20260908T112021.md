---
kind: review_result
review_id: review-GH-MATH-P4-JOINT6-PHYSICAL-RECOVERY-codex-20260908T112021
task_id: GH-MATH-P4-JOINT6-PHYSICAL-RECOVERY
source_agent: codex-principal-physical-recovery-interface
created_at: 2026-09-08T11:20:21-06:00
integration_status: pending
admission_label: pending
proof_status: PAPER_EXACT_CONTRACT_AND_RATIONAL_POINT_CHECKS
source_binding_proven: false
actual_physical_rows_recovered: false
runtime_executed: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: supply same-domain actual physical row and defect witnesses, then bind the complete numerator/determinant and observable; do not treat isolated rational tests as actual source evidence
---

# Joint6 physical recovery：principal exact contract 与隔离有理检查

## 1. 本次实际交付

新增 `examples/routeb_joint6_physical_recovery/NEW_principal_contract.py` 与本 review。
Python 仅依赖标准库，接收显式 Fraction tuple，检查完整 physical-row 前提、signed
adjugate identity 与正分母 packet gate；不读取 source、不执行 solver、不写输出文件。
它不是实际 source/checker admission adapter，也不伪造域量词或认证 metadata。

普通与 `-O` 模式 self-test 均 exit 0，八个负控全部拒绝。全部都是合成有理点，
不是 DH/Float64/物理可达状态，不能代替下文普遍实数推导或 Lean kernel 检查。
没有运行本机 Lean/Lake、Julia、rank/Young 审计或全回归。
没有修改 state、registry、既有 K_path/source、shared adapter 或任何旧文件。

## 2. 固定 principal route 的 exact contract

对同一个 full-state x∈Omega，B=(4,5)、E=(1,2,3)、physical joint6：

```text
A=[[a,b],[b,c]]=(M_A)_BB,
u=ahat_B, h=(M_A)_B6, v=ahat6,
p=(F_A)_B-(M_A)_BE*ahat_E,
A u+h v=p+z_B.                                        (P)
```

M_A 包含一次选定 regularizer，F_A 是同 configuration 的 corrected force chart。
前提 (P) 是 actual physical rows4/5，不是两个 X-preconditioned rows 或 nominal descriptor。
它允许非零 z_B；p 已包含全部 E acceleration，h v 保留 joint6。
不需要 row6、d≠0、A invertibility、T 的 SPD 或 Schur elimination。

完整 RHS 为 `f=p+z_B-hv`，故 `Au=f`。
固定 observable covector nu=(nu1,nu2)，定义

```text
D=ac-b²,
N=nu1*(c*f1-b*f2)+nu2*(a*f2-b*f1).
```

直接相消得到

```text
c*f1-b*f2=D*u1,
a*f2-b*f1=D*u2,
N=D*(nu1*u1+nu2*u2).                                 (I)
```

这是不要求 D 非零的多项式恒等式。下一层 bound 才需要对同一个域给

```text
delta>0, delta<=D, |N|<=R, R<=delta*A_cap.
```

由 delta*|nu^T u|<=D*|nu^T u|=|N|<=R<=delta*A_cap，得
`|nu^T u|<=A_cap`。不能把零/负 D 输入现有 positive-denominator gate。
若想处理 |D| 下界，需要另一个明确接口，不在此代码里偷偷放宽。

同源输入的完整性体现在

```text
N = nu^T adj(A)p + nu^T adj(A)z_B - (nu^T adj(A)h)*v.
```

忽略 defect 或 joint6 coupling 会直接改变 N，不只是放松估计。
先对整个 signed N 形成 enclosure 才保留 cancellation；分别绝对包住各项可作为
有证明的保守 fallback，但不能声称与完整 signed bound 等价。

## 3. 从 actual residual 到 (P)：必须保留 solve/model

针对同次运行返回的 ahat，实际 assembled M_R/F_R 与 analytic chart 的关系应为

```text
e_solve=M_R*ahat-F_R,
e_model=(M_A-M_R)*ahat+(F_R-F_A),
z=e_solve+e_model=M_A*ahat-F_A,
z_B=P_B*z.
```

赋值 z:=M_A*ahat-F_A 可使行等式成为恒等式，但不提供 z 的有效 bound 或实际
source refinement，也不能借恒等式反过来制造一个小 numerator。
runtime scalar/constants、FD/G0、RHS assembly 与模型误差必须统一 convention。
代码的 `check_defect_split` 只核对输入 tuple 的和，不认证这些 tuple 是真实误差。

physical row6 是 z6；preconditioned row6 是 y6=(Xz)6，混合全部 residual；
lift 第六行仅在 actual lift identity 成立时给 ahat6=eta_acc,3。
三者不互换，任何一项都不单独给 ahat6=0 或 physical row6=0。

若从 preconditioned measurements 恢复 z_B，另需同一个 actual y=Xz 的合法 dual
identity/weighted 值与误差。这里只消费其可能的输出 z_B，不重做 rank。
即使恢复成立，M_BE*ahat_E 与 M_B6*ahat6 仍必须留在 p/f 内。

metric 是可选上游 defect/numerator enclosure 工具，不是 (I) 的前提。
若用某个 H-budget，它必须控制本处 z_B 或相应实际 map，不能使用 nominal port-only
budget 代替。observable nu 固定还需真实物理量、坐标/时间单位及导数身份；
代码的 nu^T u 只是代数线性观测，不创建 trajectory semantics。

## 4. 新 Python 接口与边界

`PrincipalPoint` 保存 (a,b,c,u,h,v,p,z,nu)，所有值强制为 Fraction，拒绝 Float64
或隐式 decimal conversion。f、D、N 由同一个 tuple 计算，避免 caller 用另一矩阵
的 determinant/numerator 字段冒充当前对象。

- `check_rows`：检查 Au+hv=p+z_B；不因定义 f 就免掉此前提。
- `check_identity`：先检查 rows，再检查 (I)。
- `check_positive_packet`：检查 delta/R/cap 的正分母 gate 和单点结论；
  即使通过，source_bound、runtime_verified、cell_coverage_verified、registry_eligible
  均显式 false。
- `check_defect_split`：核对显式 solve+model tuple；无源解释/范围推断。

它没有遍历或认证一个 cell，没有解 actual ODE，没有解析 source hashes 并假装其
具有语义权威。实数/超越 source 值将来需要 typed theorem 或有效 interval binding，
不得把 round 后的 Fraction tuple 当作 exact source point。

## 5. 定向检查结果

正例取 A=[[2,1],[1,3]]，u=(1,-2)，h=(3,-1)，v=2，
p=(11/2,-25/4)，z_B=(1/2,-3/4)，nu=(2,-1)。
完整 f=(0,-5)，D=5，N=20，nu^T u=4；delta=5、R=20、cap=4 恰好通过。
solve=(1/4,-1/2)、model=(1/4,-1/4) 的和等于 z_B。

负控拒绝：丢 joint6 coupling、丢 physical defect、漏 model defect、错误 determinant
floor、低估 numerator radius、cap 太小、singular matrix 的正分母 gate、float input。
另一个 singular tuple 通过不带正分母 gate 的 identity 检查，说明代码没有把
恒等式有效性与可除性混为一谈。所有检查使用显式异常，不依赖可被 -O 删除的 assert。

复现（stdout only，无 bytecode）：

```powershell
python -B examples/routeb_joint6_physical_recovery/NEW_principal_contract.py --self-test
python -B -O examples/routeb_joint6_physical_recovery/NEW_principal_contract.py --self-test
```

## 6. 当前 source 能否实例化

本轮刷新两个核心外部 payload 的 hashes，均未变：

- force_balance_bridge_dh_v1.json：
  `3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107`；
- physical_acceleration_bridge_v1.json：
  `01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede`。

消费刚完成的 `review-GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT-capture-spec-codex-20260908T111359.md`：
它是未执行 capture specification，不是 target mu/h 的 actual receipt。
已有 centered bridge 仍只给部分 preconditioned expression；physical bridge 仍是
nominal coordinate transform。相关 actual/substitution/defect 缺口沿用已审查版本，
本轮没有对全仓库重新作不存在搜索。

最短 obstruction：**没有同配置 actual ahat/z_B witness 及其完整 signed numerator
包络，因此不能把 source 值填入 (P) 并认证 positive-denominator packet。**
还须交实际行/weighted recovery、同域 det(A) 正下界、完整 N 上界与固定 observable。
旧 port cap、origin determinant、mu=0 sanity、synthetic tuple 或已编译泛型定理都不能替代。

结论：数学接口与隔离有限检查已交付，source 实例化仍 pending。
没有 VERIFIED、physical/source admission、K_path/P4/P5 closure 或 registry 修改。
