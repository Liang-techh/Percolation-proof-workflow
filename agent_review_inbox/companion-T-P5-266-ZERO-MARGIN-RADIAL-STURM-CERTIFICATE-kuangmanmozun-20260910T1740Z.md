---
kind: companion_log
review_id: companion-T-P5-266-zero-margin-radial-sturm-certificate-kuangmanmozun-20260910T1740Z
task_id: T-P5-266-ZERO-MARGIN-RADIAL-STURM-CERTIFICATE
source_agent: 狂蛮魔尊
created_at: 2026-09-10T17:40:00Z
inspected_commit: f027ff66827c872da510b17df3467d44d7c2459f
result_review: review-T-P5-266-zero-margin-radial-sturm-certificate-kuangmanmozun-20260910T1737Z
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# 狂蛮魔尊 companion — T-P5-266

本轮接住 T-P5-265 明确保留的 **zero-margin radial fallback**，没有重复做 Bernstein strict-margin 证明，也没有转去 provenance / receipt / admission。

## 数学推进

对任意非零 `p in Q[q]` 做 squarefree multiplicity decomposition

`p = c * product_j f_j^j`

并定义

`E = product_j f_j^(floor(j/2))`,

`O = product_{j odd} f_j`。

于是精确得到

`p = c E^2 O`。

因此真正能改变符号的只有 `O` 的根，也就是 `p` 的奇重根。把区间两个端点处的 `O` 因子精确除掉后，对 `O_int` 做 Sturm root count，得到开区间内奇重根个数 `N_odd`。

核心必要充分条件是：对 `a<b`，`p!=0`，

`p>=0 on [a,b]`

当且仅当

1. `N_odd=0`；
2. 任取一个内部有理非根 `r`，有 `p(r)>0`。

这个 `r` 不需要搜索 oracle：若 `d=deg p`，固定取

`r_k=a+(b-a)k/(d+2)`, `k=1,...,d+1`，

至少一个点不是根，因为 degree `d` 的非零多项式不可能有 `d+1` 个不同根。取第一个非零值即可决定整体符号。

这补上了 T-P5-265 在接触零点时不完备的部分：**Bernstein 用作 strict-margin fast path，squarefree-parity + Sturm 用作 zero-margin complete fallback。**

## 精确 FAIL 路由

- `N_odd=0` 且固定非根 sample 为负：sample 本身就是 rational negative witness。
- `N_odd>0`：用 Sturm 把某个内部奇重根隔离到只有一个 `rad(p)` 根的 rational interval `(l,u)`；奇重性迫使 `p(l),p(u)` 异号，所以必有一个 rational endpoint 是负 witness。

因此这个 fallback 不只是 `CERTIFICATE_NOT_FOUND`，而是对 univariate rational polynomial interval nonnegativity 的完整 exact decision packet。

## 已钉死的错误路线

1. “存在内部 real root 就 FAIL”错误：`(q-1/2)^2>=0`，内部根为偶重。
2. “闭区间里存在奇重根就 FAIL”错误：`q>=0` on `[0,1]`，`0` 是端点简单根。
3. “没有内部奇重根就 PASS”错误：`-(q-1/2)^2` 没有奇重根但整体为负。
4. “只看端点”错误：`(q-1/4)(q-3/4)` 在 `0,1` 都为 `3/16>0`，但中点为 `-1/16`；Sturm 计数精确给出两个内部奇根。
5. “固定看中点作为 sign anchor”错误：正例 `(q-1/2)^2` 的中点恰好为零；应使用有限 `d+1` grid 找到非根。

## 形式化建议

最小 theorem packet 可拆成：

- `oddKernel_factorization`：`p=cE^2O`；
- `noInteriorOddRoot_of_nonneg`；
- `nonnegOn_interval_iff_oddSturm_zero_and_positive_anchor`；
- `finiteGrid_anchor_exists`；
- `oddInteriorRoot_gives_rational_negative_witness`。

Sturm 链若要整数序列化，只允许对每项做**正数**缩放；随意乘 `-1` 会改变 sign variation，不能为了统一 leading coefficient 而静默翻符号。

## 边界与下一步

本轮仍是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。没有声称 actual P5 polynomial、`Q/R`、source chart、coverage、Float64、Lean/kernel、封不觉验证、registry/admission 或 parent closure。

下一条真正值得数学槽继续推进的 seam 已从“零余量一元符号判定”移走：应检查 actual signed homogeneous allocation 是否真的能同源压成单变量 rational `A(q)`。若还有额外 cell parameter，则应直接进入结构化二变量 certificate，而不是继续堆一元 lemma。
