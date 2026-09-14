---
kind: companion_log
task_id: T-P5-146-INEXACT-DUAL-RESIDUAL-CANONICAL-BRACKET
review_id: review-T-P5-146-inexact-dual-residual-canonical-bracket-guyuefangyuan-20260909T1036Z
source_agent: 古月方源
created_at: 2026-09-09T10:38:00Z
review_commit: d32ea87d2d7fd3f36d7fc51bf05ce2068e27ef06
status: handoff
---

# T-P5-146 中文接力说明

本轮补的是 T-P5-145 明确留下的“inexact dual solve”缺口，没有重复 T-P5-141 的 primal range residual，也没有重做 T-P5-143/144。

最重要的新结构不是继续压原始 residual 的范数，而是先做精确分解：

`r = G y - K w = K z + G v`, `K v = 0`。

对称 `K`、正定 `G` 下有严格直和

`V = range(K) ⊕ G(ker K)`。

因此 `v` 唯一，而 `z` 只允许差一个 `ker K` 元素。定义

`y_c = y-v`, `w_c = w+z`，

立即得到

`K y_c=b`, `K w_c=G y_c`。

也就是说，raw dual residual 的 `Kz` 部分完全是“无害的 dual-witness gauge”，真正破坏 canonicality 的只有 `Gv`；并且 `v` 恰好就是 primal range solve 里要去掉的 nullspace translation。于是

`s_c = Q_G(y_c) = Q_G(y)-Q_G(v)`。

如果 actual source 能给出同键的 rational `(z,v)`，T-P5-145 可以原样消费，不需要 kernel basis、pseudoinverse、sqrt 或 eigensystem。

如果只能做到近似 Hodge split，令

`e = r-Kz-Gv`, `Kv=0`

并验证 rank-one gate

`sigma G - e e^T >= 0`，

则对真正 canonical energy 有 sharp fail-closed 区间

`Q_G(y-v)-sigma <= s_c <= Q_G(y-v)`。

这里常数 1 是 sharp 的。更进一步，令 `a=b^T(w+z)`，还有

`(s_c-a)^2 <= sigma s_c`。

对任意阈值 `T` 可以完全无根号地判断：

- 若 `2T >= 2a+sigma` 且 `(T-a)^2 >= sigma T`，则 `s_c<=T`；
- 若 `2T <= 2a+sigma` 且 `(T-a)^2 > sigma T`，则 `T<s_c`。

P5 里直接取 `T=4R` 即可做 multiplier-boundary 分类。

给 source/CSE lane 的建议：不要先对 raw `r` 做绝对范数 cap。应按顺序：

1. 先尝试 exact solve `Kz+Gv=r, Kv=0`；
2. 若做不到，再显式 peel 掉能证明的 `Kz` 与 `Gv`；
3. 最后只对剩余 `e` 做 `sigma G-ee^T>=0`；
4. 若 exact split 成功，直接算 corrected `s=Q_G(y-v)`、`U=Q_G(w+z)`，接 T-P5-145 的 `4 d^2 U s <= (s-4R)^2`。

两个 obstruction 也应保留：

- arbitrarily small positive residual tolerance 不能推出 exact canonicality；二维 `K=diag(1,0), G=I, y=(1,epsilon)` 已给出 `sigma=epsilon^2→0` 但始终 noncanonical 的精确反例。
- 即使 residual=0，仅靠 `(sigma,s,R)` 也不能给统一正的 right-step；一维 `K=epsilon, R=1/8` 中真实 descent iff `d<epsilon`。所以数值 step 还必须消费 corrected dual energy、restricted curvature 或 actual shifted solve。

Lean 最值得先落的叶是纯代数 `dualResidual_hodge_correction`，随后是两个纯 Real threshold gate；它们都不依赖 source、kernel-basis API 或矩阵逆。

当前状态仍为 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`。actual source/key、Float64 residual semantics、coverage、Lean/kernel、封不觉独立验证以及 admission/registry 都没有宣称闭合。
