# T-P5-029：非负 gain increment 的固定 N-slack 更新

日期：2026-09-07。**未编译的 source-independent Lean proof skeleton**。
本轮仅新增 `NEW_KPATH_INTERFACE_SPNIncrement.lean` 和本 review；未运行 Lean/Lake，
未重做/运行 K_path checker，未实例化 concrete K/source/kappa/gamma，未改 state、registry、共享脚本或旧文件。

依据：`agent_review_inbox/review-T-P5-029-kuangmanmozun-20260907T1152.md`，
SHA-256 `882b697850faca81e17946842d3f1ef5a794fb9257ea91365d0a3af7f7cc10c2`。
直接复用既有 `NEW_KPATH_INTERFACE_Core` 的 `SPNWitness`、`ConeGapBinding`、
`liftSPN`/`direct_envelope`，没有依赖前几轮未编译的 rational/Fin adapter。

## 最小更新链

本文件的 A/B 是**锥上的绝对值映射**，不是 source residual 的力归一化 A：

```text
A_C : 4×4, B_C : 2×4, E : 2×4，均逐项非负；
|chart(c,u)| = A_C u， |L chart(c,u)| = B_C u，u≥0；
M_C(E) = B_Cᵀ E A_C； C_C(E) = (M_C(E)+M_C(E)ᵀ)/2。
```

`rawCorrection`/`correction` 显式展开有限和，不使用谱 API。
`correction_nonnegative` 的证明脚本逐项累加非负乘积，得到 **C 逐项非负**。
`correction_quad` 给出对所有实数 u 的纯代数身份
`uᵀCu=(B_Cu)ᵀE(A_Cu)`。

需要区分定义域：实际绝对值 envelope 增量等于这条二次型，只在 `u≥0` 且
提供了 `state_abs/channel_abs` 时由 `correction_envelope` 连接。
不能将锥上的绝对值身份推广到任意带符号 u。

`updatedGap` 直接构造 canonical 新 gap `H_new=H_old−C`，保留同一 Q 和 mu，
并用 envelope 对 gain 的加法性证明它绑定 `K+E`。若要识别另一个独立导出的 H_new
矩阵，必须另给矩阵等式；二次型相同本身不能排除不同的反对称部分。

对旧证书 `H_old=S+N`，`chargeN` 只接受显式逐项前提 `C[i,j]≤N[i,j]`，返回

```text
H_old−C = S+(N−C)， N−C逐项非负。
```

返回结构中的 S 和 PSD 证明直接使用 `old.S`、`old.psd`；`chargeN_same_S` 是 rfl。
不需要重新生成旧 S 的 LDL/PSD witness。`fixed_slack_iff` 说明 `C≤N` 恰好是
这种**固定 S、仅扣 N**方式保持 N 非负的充要条件，不是一般 SPN 可行性的必要条件。

`updatedRepresentatives` 对原有 18 个代表分别扣减 N；`updated_direct_envelope`
调用现有 consumer。`AbsoluteConeMaps.a_flip/b_flip` 与旧 H 的 flip 身份保证新 H
也反号不变，因此现有 witness lifting 保留全部 36 个标签。没有按相等矩阵去重。
“保留旧 S”指这 18 份输入证书，未断言另行导出的任意 36 份分解也与之相同。

## Rank-one 结构

全部参数保持符号化。`rankOneGain` 在另外提供 `kappa≥0,gamma≥0` 后包装
`E[a,k]=kappa[a]*gamma[k]`。候选定理给出：

```text
alpha=B_Cᵀkappa， beta=A_Cᵀgamma；
B_CᵀEA_C=alpha betaᵀ；
C[i,j]=(alpha[i] beta[j]+beta[i] alpha[j])/2；
uᵀCu=(alpha·u)(beta·u)。
```

`alpha_beta_nonnegative` 单独证明两向量逐项非负。`rankOne_charge_iff`、
`chargeRankOne` 消费无除法的逐项条件
`alpha[i] beta[j]+beta[i] alpha[j]≤2*N[i,j]`，零 slack 条目也无需构造比值。
纯代数 rank-one 扣减 lemma 不需要参数符号；作为“非负 gain increment”使用时，
必须通过 `rankOneGain` 提供非负证明，不可省略物理增量契约。

## 不可推出的矩阵序与 pending boundary

逐项非负不蕴含 PSD。例如符号参数 t>0 下，矩阵 `[[0,t],[t,0]]` 逐项非负，
但在 `(1,−1)` 上二次型是 `−2t`。因此本文件不从 E≥0 推出 C PSD 或 H 的
全空间 Loewner 单调性；C 的功率非负仅在相应非负正交象限上使用。

新增局部类型 `ReuseAttempt Hnew` 只有 `pending reason` 或携带真正
`SPNWitness Hnew` 的 `witness` 分支。它不是自动执行的 checker，也不是 registry 状态：

- 缺少映射/旧证书/扣减证明，保持 `missingBinding/missingOldWitness/missingSlackProof`。
- 若有确切条目证明 C>N，只能记 `fixedNSlackInsufficient`，不能记 non-copositive、
  small-gain failure 或 source 反例。未取得扣减证明也不能自动说已有反例条目。
- 编译尚未完成，保持 `buildNotVerified` 边界；当前整个 artifact 属于此情况。

固定 N 不够不排除其他分解：抽象地取 `S=sI,N=0,C=cI` 且 `0<c<s`，
固定 N 条件失败，而改用 `(s−c)I+0` 仍可获得 PSD/SPN 分解。这只是矩阵层面的
符号示例，不是 concrete K/source 数值。重搜或分摊 PSD slack 是之后的独立工作。

## 精确剩余前提与验证状态

仍须提供：实际旧 K 的 gap/Q 身份及 18 份 SPN witness；A_C/B_C 的非负性、
正交象限绝对值身份和反号身份；真实增量 E≥0（rank-one 时包括真实 kappa/gamma
绑定）；每个代表全部 16 项 C≤N 的精确证明。消费实际 residual 还须另给同域
`ComponentBinding`，不是由旧 K 的 residual bound 自动覆盖增大的实际残差。

只有上述条件成立，才能将更新后的 envelope 用于进一步的 pointwise power consumer。
源路径、参数不匹配、Float64/additive bias、coverage/P8/continuation 均未闭合。

本轮只核对源码接口；所有证明脚本及末尾 `#print axioms` 均未执行。
尚需在授权环境编译并检查公理，且须使 inherited `P5FeasibleConeSPN` 指向
`examples/routeb_p5_feasible_cone_spn_lean/` 的通用 sidecar，避免导入本目录同名旧 proof attempt。
不声称 kernel PASS、LEAN_VERIFIED、source closure 或 registry eligibility。

新 Lean artifact SHA-256：
`2e7c2bdaab7653bd15d253ca9d8729a412788dfff144e41d7626fb6014418e56`。
