# K_path packet：固定 N 障碍与 PSD-slack 构造

数学草稿，未运行 Lean/checker，未实例化实际 source。所有坐标固定
z=(x4,x5,y4,y5)，L=[[1,0,1,0],[0,1,0,1]]，K 为 2×4 非负 gain。
这里 μ 是 small-gain envelope 系数，不与别处 mass regularizer 混同。

## 1. 当前 toy 固定 N 路线实际没有正增量容量

源码 check_exact.py:212–225 的 fixture 固定 K0[a,j]=1/1000、μ=1/2。
每个代表 N 只有 N01=N10=1/10000，其余全零；S=H(K0)−N。
这不是 actual K_path，也不是已绑定的 physical certificate。

考虑任何逐项 E≥0，使 Knew=K0+E，且 μ/Q/chart 全不变。
pp×pp 代表的 T=I，A_abs=I，B_abs=L。
gap 降低量 C(E)=sym(Lᵀ E)。固定 S、只从 N 扣减的策略需要 C≤N 逐项。

其四个对角条件直接给出
E00=E11=E02=E13=0（每项非负，而 Njj=0）。
再看 N03=N12=0：
C03=(E03+E10)/2≤0，C12=(E12+E01)/2≤0，
故余下 E03=E10=E12=E01=0。
因此仅 pp×pp 一张证书就迫使 **E=0**。

这是当前 toy 分解的固定-N 更新机制的精确障碍，不是 H 不共正、
实际 K 超界或 P5 不可能的证明。旧 SPNIncrement 的一般接口并无错误；
它的 C≤N 前提在此 fixture 对任何非零 E≥0 都无法满足。

## 2. 可行的最小替代：消耗 PSD slack 而非只扣 N

对每个代表 r，提供可核验的 δ_r>0 与 S_r ⪰ δ_r I。
若原 S_r=R_rᵀdiag(d_r)R_r，R_r 可逆且 d_r 所有项严格正，
可用完全有理的保守下界

δ_r = min_i d_ri / Σij (R_r⁻¹)_ij²。

因为 ‖u‖²≤‖R_r⁻¹‖F²‖R_r u‖²，得到该 coercivity；
R/d identity、逆矩阵 identity 和正性仍须对实际 18 表精确检查。
一般奇异 SPN 并不满足这些条件，不可强制正 δ。

定义 A_r≥0、B_r≥0 为固定 chart 上的 abs-state/abs-channel 映射，
C_r(E)=sym(B_rᵀ E A_r)，E≥0。
若对每个代表和每一行 i 都有 Σj C_r(E)ij≤δ_r，则
δ_r I−C_r(E) 对称对角占优且对角非负，从而 PSD。
于是 Snew_r=S_r−C_r(E) PSD，Nnew_r=N_r≥0，
H(K0+E,r)=Snew_r+Nnew_r。

这形成 18×4 个线性有理不等式定义的 **gain 增量容量多面体**。
保持 18 标签及 flip identities，不按矩阵值相等去重；实际新 S 的 proof/witness
需要由上述 PSD dominance 构造或重新 exact factor，不是只改 JSON 数字。

给定非负方向 D，令 c_ri=Σj C_r(D)ij。
E=tD 时可取 0≤t≤min_{c_ri>0} δ_r/c_ri；c_ri=0 不产生约束。
若所有 δ_r>0，任一固定有限 D 都有足够小的 t>0 可行，说明固定-N 的 E=0 障碍
不等于全部 SPN 方法没有增量容量。本轮未计算具体 δ/t 或生成新证书。

## 3. 更小的无需增量路线

若实际 K_path≤K0 逐项，已有 K0 证书可通过 envelope monotonicity 直接消费；
无需把 H(K_path) 与 H(K0) 当同一矩阵，也无需改证书。
若有分量超过 K0，令 E=(K_path−K0)_+，G=K0+E；
满足上述容量条件就能建立 K_path≤G 和 G 的 18 SPN witnesses。
这只在 μ/Q/chart/force normalization 完全相同时成立。

## 4. 所得结论与不能填补的缺口

数学目标只到 |(Lz)ᵀrc|≤μQ(z)，且前提为同域真实 centered residual
|rc_a|≤Σj K_path[a,j]|z_j|。
还需 PathBinding、真实 source/chart/state identity、same-Q gap identity、
完整 18 rational certificates、consumer/import identity 与准入 receipts。
如 z(x)=0 而 rc(x)≠0，任何有限 homogeneous gain 都不可能成立；
必须拆出 additive bias 或修正 centering，而不是调大 K。

μ<1 与 Q 正定仍不单独给 trajectory closure；需要 Vdot 真实等式/不等式、
bias budget、域包含、ODE continuation 等其他义务。
