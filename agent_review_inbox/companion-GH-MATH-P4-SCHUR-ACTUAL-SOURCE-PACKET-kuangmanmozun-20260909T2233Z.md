# 狂蛮魔尊 companion — GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET

本轮优先处理梁智炜此前明确点名、且我方 claim 仍停留在 `CLAIMED` 的 Schur actual-source packet，没有转去做 audit / receipt / admission，也没有抢占 T-P5-190/191 等其他数学 Agent 的 lane。

正式结果已写入：

`review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET-kuangmanmozun-20260909T2232Z.md`

## 本轮结论

这个任务现在可以结束为“数学 packet 规格已闭合，但 actual source 仍被精确阻塞”，不应继续无限保持 CLAIMED。

现有仓库已经有 exact rational 的 block-(4,5,6) metric 候选、三维 rank-deficient observation obstruction，以及古月方源给出的最优相关第三标量

`w6 = 350003*d6 - 50000*d4`。

若同一个 source/configuration/domain key 能直接给出

`d4^2 <= U4, d5^2 <= U5, w6^2 <= Uw`

并证明同源的 `H=M0_CC^-1`，则可直接用 exact rational completed-square 计算 `D=d^T H d` 的 sharp cap，不需要浮点逆、谱分解或平方根。

当前真正缺失的仍是 actual same-key source packet：仓库里 joint-6 的 rational residual bridge 自己也明确停在 principal compact branch 的具体 `N_a,D_a` source CSE 未出现，因此不能把一个 source-independent joint6 theorem 偷换成 actual `d6/w6` 见证。

## 本轮新增的数学 fallback

除了相关坐标 `w6` 路线，本轮补了一个 producer-facing 的精确备选：如果 source lane 只能给同源的 rational absolute raw boxes

`|d4|<=a4, |d5|<=a5, |d6|<=a6`，

则 block456 energy 在这个独立对称 box 上的**精确最大值**为

`D_raw = h11*a4^2 + h22*a5^2 + h33*a6^2 + 2*|h13|*a4*a6`，

其中 `h13<0`。这个 bound 是 sharp 的，因为在 box corner 取 `d4,d6` 反号就达到等号。于是如果 producer 做不出 `w6`，也不必重新开复杂 Schur 推导；只要 raw absolute caps 是 rational，就仍然能得到完全 rational 的 exact cap。

若 producer 只有 squared caps `d4^2<=U4,d5^2<=U5,d6^2<=U6`，没有 rational absolute radius，则 sharp raw-box 公式一般会出现 `sqrt(U4*U6)`。为保持 trusted checker 全有理，可固定任意 rational `eta>0`，用

`2|d4*d6| <= eta*d4^2 + eta^{-1}*d6^2`

得到 rational Young fallback。这个分支是 sufficient/nonsharp，不能冒充 `w6` transformed sharp cap。

## 最小 downstream 选择

后续 source/CSE lane 有三条合法路：

1. **优先**：同源 `d4,d5,w6` quadratic caps；这是 sharp rational route。
2. **备选**：同源 rational raw absolute boxes `a4,a5,a6`；本轮给出 exact sharp raw-box maximum。
3. **再备选**：只有 squared caps 时固定 rational `eta`，走 Young rational cap。

任何只给 rows 4/5、只给 `u,s`、只给另一个同尺寸 SPD/metric、或只给 source-independent joint6 residual theorem 的 packet，都不能关闭三维 `D`。

本轮没有升级 source binding、coverage、Float64/interval、Lean/kernel、封不觉验证、admission、registry 或 P4/M4 parent closure。正式 review commit 为 `6103f963db923e9008696e1dd3a462c4bddcdc37`。
