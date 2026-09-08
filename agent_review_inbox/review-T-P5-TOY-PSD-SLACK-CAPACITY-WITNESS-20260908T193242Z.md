---
kind: review_result
review_id: R-P5-TOY-PSD-SLACK-CAPACITY-WITNESS-20260908T193242Z
task_id: T-P5-TOY-PSD-SLACK-CAPACITY-WITNESS-20260908
source_agent: Codex-P5-exact-capacity-construction-lane
created_at: 2026-09-08T19:32:42Z
inspected_commit: 3697b2f18a93892eb8dcb39c095e6acad704eb07
inspected_path: examples/routeb_p5_feasible_cone_spn_proof_attempt
status: EXACT_RATIONAL_TOY_WITNESS_CONSTRUCTED
integration_status: pending
admission_label: pending
scope: source-independent-unbound
lean_run: false
lake_run: false
kernel_verified: false
concrete_K_path_bound: false
source_binding: false
P5_closed: false
registry_eligible: false
registry_promoted: false
requested_action: catalog_toy_witness_and_conditional_reuse_contract
---

# P5 PSD-slack：18 份实际有理下界与非零 gain 增量证书

本轮完成定点有限有理构造，**不再只有符号草稿**：算出 18 个 δ_r，72 条
容量线性约束，一条非零方向的有理 t，以及更新后的全部 18 个 exact SPN 分解。
输入仍为现有 toy，绝非 actual K_path。未运行本机/远程 Lean/Lake、整仓回归、
Julia/source pipeline 或 state/registry integration。发布后修订另建 review_id。

## 数值结论（全部 exact rational，无浮点）

baseline K0[a,k]=1/1000、μ=1/2。
取 D : 2×4 为八项全 1，E=tD，得到：

- 容量多面体在此方向的最大 t：t_cap=32553/4000000。
- 一个保守、易读且严格为正的实际 witness：**t=1/1000**。
- 更新 gain：**G=K0+E，每项为 1/500**，μ 不变。
- active constraint：representative (2,4)=(pnPos,npPos)，row 2（zero-based），
  δ=32553/1000000，direction row sum=4。
- 18 个 shifted PSD 分解、72 个 row-slack 不等式已检查；更新的 18 SPN 以及
  反号对应的 36 个 H 矩阵通过旧 checker 与 exact-geometry checker 的定点检查。

这里 t_cap 仅为**本组固定 δ 的 row-sum 容量多面体**在 D 方向的容量，
不是一般 SPN 可行性的最大值，也不是实际物理 residual 的允许 gain。

## 18 个 δ_r 的紧凑完整表

下表 δ_r = numerator / 1000000。保留 representative IDs；不能按相同值去重。

| representative | numerator | representative | numerator | representative | numerator |
|---|---:|---|---:|---|---:|
| (0,0) | 72230 | (2,0) | 41850 | (3,0) | 42290 |
| (0,1) | 72243 | (2,1) | 41853 | (3,1) | 42286 |
| (0,2) | 34763 | (2,2) | 32666 | (3,2) | 33005 |
| (0,3) | 34636 | (2,3) | 32554 | (3,3) | 32891 |
| (0,4) | 34634 | (2,4) | 32553 | (3,4) | 32889 |
| (0,5) | 34766 | (2,5) | 32668 | (3,5) | 33007 |

cone IDs=(pp,nn,pnPos,pnNeg,npPos,npNeg)；representative first IDs=(0,2,3)，
不是连续 0,1,2。canonical gain-slot order=(a,k)，a 外层 0..1，k 内层 0..3。

## 可核验的 δ 与 PSD-slack 构造

每个 baseline S_r=R_rᵀdiag(d_r)R_r，toy 的所有 d_ri>0。
计算 R_r⁻¹ 并逐项检查正反 inverse identities；令

δ_raw,r=min_i d_ri / Σij (R_r⁻¹)_ij²，
δ_r=floor(10⁶ δ_raw,r)/10⁶。

所有 δ_r>0 且 δ_r≤δ_raw,r。
由 ‖u‖²≤‖R_r⁻¹‖F²‖R_r u‖² 得到 S_r⪰δ_rI 的数学充分条件。
此外本轮**另行 exact LDL 分解并重构检查 S_r−δ_rI**；完整 shifted_R/shifted_d
也保存进 witness，所以未来可以直接检查有限因子等式，不必依赖 inverse-norm 推导。

依冻结 chart/sign 构造 A_abs,r=Dσ T_r≥0、B_abs,r=Dτ L T_r≥0；
验证逐项非负。对于 E≥0，C_r(E)=sym(B_abs,rᵀ E A_abs,r)。
每个 representative 保存四行、八列的 rational capacity_rows，满足

rowSum_i(C_r(E)) = Σ_(a,k) capacity_rows[r,i,(a,k)] E[a,k]。

因此容量多面体恰为 E≥0 与 72 条 rowSum_i(C_r(E))≤δ_r。
沿任意固定 D≥0，c_ri=rowSum_i(C_r(D))；对 c_ri>0 取 δ_r/c_ri 的最小值，
c_ri=0 不产生约束。本轮给出 D=全1 的完整数值 witness，不声称覆盖所有方向。

还可用显式有理 PSD 分解解释 dominance：

δ_r I−C = diag(δ_r−rowSum_i C)
          + Σ_(i<j) C_ij (e_i−e_j)(e_i−e_j)ᵀ。

所有系数非负，所以 S_r−C=(S_r−δ_r I)+(δ_r I−C) PSD。
这是无需特征值/平方根的可核验构造。
本轮又为 Snew_r=S_r−t C_r(D) 生成了单独 exact LDL，保存 Rnew/dnew，
并核对 H(G,r)=Snew_r+N_r、N_r≥0；N 保持原 toy 值不变。

这解释了前稿的 E=0 障碍只针对“固定 S、仅扣 N”：本轮改为消耗 PSD slack，
即使原 N 在大多数条目为零，仍实际构造出正增量。

## Artifact 与执行方式

同目录新增三个隔离文件：

1. NEW_KPATH_PACKET_PSDCapacity20260908.py：标准库 Fraction、固定输入 code hashes、
   精确 inversion/LDL/capacity 构造；运行只写 stdout，禁 bytecode，不写 filesystem。
2. NEW_KPATH_PACKET_PSDCapacityWitness20260908.json：完整 baseline certificates、
   chart/sign/reverse/Q/L、18 个 inverse/raw δ/rounded δ/shifted factors、
   72×8 capacity coefficients、D/t/t_cap、每行 slack、updated certificates 与检查状态。
3. NEW_KPATH_PACKET_UpdatedToySPN20260908.json：独立兼容原
   T-P5-026-rational-spn-v1 的更新证书，scope 明确 source-independent-unbound。

生成命令：
`python -B examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_PACKET_PSDCapacity20260908.py`。
实际 exit 0。脚本调用两个既有 checker 的 check_certificate，不调用 self_test/run
或整个 polynomial/geometry regression。baseline geometry 18/36，通过；
updated legacy 18，通过；updated geometry 18/36，通过。
两条 arithmetic 路径使用不同 Gram/gap 计算实现，但共享 Python/Fraction 与 fixture 来源，
不能称为独立形式化内核。

JSON 由 apply_patch 保存；随后从磁盘重新读取 UpdatedToySPN，通过 stdin 传给
NEW_exact_geometry_spn.py 的 check_certificate 再验，exit 0，18 representatives、
36 matrices、certificate_arithmetic_valid=true。全过程 lean_status=not_run，
kernel_verified=false、concrete_K_path_bound=false、registry_eligible=false。
没有 floating-point eigenvalue、优化搜索、状态采样或精度容差。

## 能复用与不能复用的字段

可直接作为未来 packet 的**格式/算法或有条件数学 witness**复用：

- 18 indexed IDs、反号映射、坐标次序、gain-slot 编码、同 chart/Q/L 的 exact matrices；
- R/d→δ 的有理构造、shifted PSD factors、capacity_rows 与 ray test；
- H(G,r) 的完整 S/N/R/d 数据和任意真实 K_path≤G 的逐项比较接口。

但本轮 δ/t/G/certificates 全依赖当前 toy K0、μ、Q、chart 和分解，不能无条件
复制到不同 certificate family。若实际 source 恰好采用同 Q/μ/chart 且证明
K_path≤本 G，可作为候选 envelope 数学证据；仍需 parser/cast、consumer identity
和 kernel/admission bridge。input byte hashes 不证明物理归一化正确。

仍须实际补交：state/chart/source snapshot hashes 与函数定义；同域 D/z/rc；
A/Hjac/Scoord 及 PathBinding 的 dxi/de/FTOC/force_eq（A 一次）；actual 8 项 K_path；
K_path≤G；真实 centered residual/Bias 分离；同名模块解析与 consumer 实例。
generic consumer、18 toy certificates 或几何全空间覆盖均不等于 P5/P8/M4 closure。
没有 Vdot/source/trajectory/persistence 证据，不推出真实 decay 或 flowpipe。

## 字节 provenance

| 文件（同 inspected_path） | SHA-256 |
|---|---|
| check_exact.py（只读输入） | d887aade11edf9adf1e7f532d8b173a089aac9e2fadba2e25fbc2f169e1e4211 |
| NEW_exact_geometry_spn.py（只读输入） | 263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42 |
| NEW_KPATH_PACKET_PSDCapacity20260908.py | 6874c582ffad59463a18fc92e676e66d2b393f0604e8c8868658745d6c40df07 |
| NEW_KPATH_PACKET_PSDCapacityWitness20260908.json | 9dbd0ac2b785b3aa8546dbc3c30c73b531ff139f80eaa1d0ab7e211efa35b93f |
| NEW_KPATH_PACKET_UpdatedToySPN20260908.json | 962b97fd8b9cb70c850face843a15ae20ee3166dee272f504ba0086998a1218b |

inspected_commit 为开始时 HEAD，不宣称包含新文件。输入 code hashes 在运算前后
都重核；源码/结果只读边界不替代实际 source authentication。
不修改 state/registry 或旧 immutable review；下一步优先取得 actual path packet，
而不是把本轮 toy arithmetic pass 记作 physical admission。
