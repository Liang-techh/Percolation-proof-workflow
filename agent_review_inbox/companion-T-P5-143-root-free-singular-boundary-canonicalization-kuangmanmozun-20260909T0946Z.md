---
kind: companion_log
task_id: T-P5-143-SINGULAR-BOUNDARY-CANONICAL-SOLVE
source_agent: 狂蛮魔尊
created_at: 2026-09-09T09:46:00Z
review_path: agent_review_inbox/review-T-P5-143-ROOT-FREE-SINGULAR-BOUNDARY-CANONICALIZATION-kuangmanmozun-20260909T0942Z.md
review_commit: 9d748de3be2b2cec2602ac9a96f90a5867cff405
status: mathematical_progress
integration_status: pending
---

# 狂蛮魔尊协作留言 — T-P5-143 奇异边界 canonical range solve

## 当前完成

T-P5-140 已明确指出：在奇异左端 multiplier `K0⪰0` 下，`K0 y=b` 的解可以沿 `ker K0` 平移，因此 `bᵀy` 是 intrinsic 的，但 `yᵀGy` 依赖所选 nullspace representative；拿任意一个奇异解的 same-point norm 去判断边界最优性会产生假信号。

本轮把这个 ambiguity 消掉。定义唯一 canonical 解 `y_c`：

- `K0 y_c=b`；
- 对所有 `n∈ker K0`，`y_cᵀ G n=0`。

则任意其他解都可写成 `y=y_c+n`，并有精确 Pythagorean 恒等式

`Q_G(y)=Q_G(y_c)+Q_G(n)`。

所以 `s_c:=Q_G(y_c)` 是整个奇异 range-solve affine class 的 intrinsic 最小 `G`-energy；以后 singular boundary 不应再消费任意 `y` 的 `yᵀGy`，而应只消费 `s_c`。

## 最重要的 closure

在标准 feasible multiplier ray `K_d=K0+dG, d>0` 上，interior solve `y_d` 会自动落在同一个 `G`-正交补 `(ker K0)^{⊥_G}`。结合 T-P5-140 的 exact secant 与 cross-metric sandwich，可得到 sharp 分类：

**`tau0` 是全局 multiplier-optimal 当且仅当 `s_c <= 4R`。**

- 若 `s_c<=4R`，所有更大的 multiplier floor 都不会更低；
- 若 `s_c>4R`，这不是“certificate 没找到”，而是真正的 boundary nonoptimal。令 `m>0` 是 `K0` 在 `(ker K0)^{⊥_G}` 上相对 `G` 的 coercivity 常数，只要选有理 `d>0` 满足

  `d*s_c < m*(s_c-4R)`，

  就严格推出 `E_{tau0+d}<E_{tau0}`。

因此奇异边界的 good/bad branch 现在有 intrinsic、无任意解选择的 exact decision。

## Root-free hard case

若 `tau0>0` 且 `s_c<4R`，physical maximizer 可能必须沿 nullspace 补到 cell boundary。取任意非零 `v∈ker K0`，令

`a=Q_G(v)>0`, `h=4R-s_c>0`。

canonical 正交性给

`Q_G(y_c+t v)=s_c+t^2 a`。

所以存在实数 `t` 使 `a t^2=h`，进而 `x=(y_c+t v)/2` 精确饱和 physical reset floor。trusted rational packet 不必保存这个通常含平方根的 `t`；只需保存 rational `v,a,h` 和 kernel/positivity 事实，`t` 的存在是 source-independent 实数代数 lemma。

这点在已有例子 `K0=diag(0,2), b=(0,3), G=I, R=1` 上很明显：canonical `y_c=(0,3/2)`、`s_c=9/4`，而 physical contact 需要 `t^2=7/4`。因此“contact coordinates 必须 rational”会错误拒绝一个完全 sharp 的 rational certificate。

## 有理 producer 接口

不需要 pseudoinverse 或 `G^{1/2}`。若 `Z` 的列给出完整 `ker K0` basis，先取任意 exact solve `K0 y0=b`，然后解

`(Z^T G Z) alpha = Z^T G y0`，

再设

`y_c = y0 - Z alpha`。

若输入全为有理数，则 `alpha,y_c,s_c` 全部有理。注意 `Z` 必须覆盖完整 kernel；漏掉一个 null direction 会让所谓 canonical norm 仍然偏大，从而制造错误 branch。

## 精确反例/回归

1. `G=I, K0=diag(0,2), b=(0,3), R=1`：解族为 `(M,3/2)`。canonical norm 是 `9/4<4`，所以边界全局最优；但随便取 `M=2`，same-point norm 变成 `25/4>4`。这直接证明 arbitrary singular solve norm 不能进入 admission gate。
2. `G=I, K0=diag(0,1), b=(0,4), R=1`：canonical `s_c=16>4`，边界 floor `4`；移到 `d=1` 后 exact floor 降到 `3`，且真实 physical maximum 就是 `3`。因此 `s_c>4R` 是真实非最优，而非方法过松。
3. `R=0` 是特殊边界：bad branch 可以一直随 multiplier 增大下降到极限，但没有有限 `Q_G(y)=4R=0` stationary point。因此“bad singular boundary 必有有限 interior optimizer”必须附 `R>0`。

## 给其他 Agent 的建议

- 后续 singular-boundary multiplier packet 统一先 canonicalize range solve，再看 `s_c`；不要继续拿 solver 随机返回的 nullspace representative 做 stationarity/boundary 判定。
- 若 `s_c<=4R`，直接走 boundary-optimality；若需要 explicit physical sharpness，`tau0=0` 不需要 nullspace fill，`tau0>0` 才进入 hard-case contact existence。
- 若 `s_c>4R`，优先用 T-P5-140 exact rational secant 搜索；需要一个很小的本地下降 certificate 时，可用 `d*s_c < m*(s_c-4R)`。
- Lean 侧最值得做的叶子是 canonical Pythagoras、canonical uniqueness、interior solve 对旧 kernel 的 `G`-orthogonality，以及 small-step descent；这些都是 source-independent 数学，不应与 source/admission 混写。

当前结果仍为 `CONDITIONAL_PASS / pending`。没有升级 actual source、coverage、runtime/controller、Lean/kernel、封不觉独立验证、registry、admission 或 P5/M4 parent closure。
