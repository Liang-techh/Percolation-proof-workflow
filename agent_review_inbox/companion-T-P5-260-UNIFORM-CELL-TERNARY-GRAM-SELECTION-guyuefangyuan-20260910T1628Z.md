---
kind: companion_log
task_id: T-P5-260-UNIFORM-CELL-TERNARY-GRAM-SELECTION
source_agent: 古月方源
created_at: 2026-09-10T16:28:00Z
review_path: agent_review_inbox/review-T-P5-260-UNIFORM-CELL-TERNARY-GRAM-SELECTION-guyuefangyuan-20260910T1624Z.md
admission_label: pending
---

# T-P5-260 companion — 古月方源

本轮承接柳冠一 T-P5-259 明确保留的 cell-dependent ternary Gram selector seam，没有转做 provenance、receipt、admission 或重复验证。

最关键的新结论是：若 15 个 ternary-quartic 系数对 source 参数在凸多面体上是 affine，则整个连续 cell 的非负性 **精确等价于有限个顶点 quartic 非负**。每个顶点可以使用不同的六维 Gram gauge；对任意内部点，把顶点 gauge 按同一凸组合插值，Gram 矩阵就是顶点 PSD Gram 的凸组合。因此“找不到一个 constant gauge”绝不能判 physical FAIL。

若 cell 是 simplex，上述顶点 gauge 自动给出全局 affine selector；若是一般 polytope，可在任意给定 triangulation 上得到连续 piecewise-affine selector。若 source box 的系数是 multi-affine，则角点 barycentric 权重直接给出一个全局 multi-affine selector，而且角点检查仍然 lossless。

我加入了 exact regression：`p_s=(1-s)(x²-y²)²+4s x²y²+z⁴` 在 `[0,1]` 上始终非负，但 `s=0` 的 binary restriction 强制 Gram cross gauge `t1=-2`，`s=1` 强制 `t1=0`，所以不存在 constant gauge；然而 `t1(s)=-2(1-s)` 是显式 affine PSD selector。

对一般 rational-polynomial 参数依赖，本轮给出 Bernstein-Gram hierarchy：把 parameter polynomial 精确写成 Bernstein control quartics；若每个 control quartic 有 PSD Gram，则其 Bernstein 凸组合给出全局 rational polynomial Gram selector。更强的是，在 ternary quartic **uniformly strict positive** 分支，degree elevation 的 control forms 一致逼近网格点 quartic；利用紧致性正 margin 与 T-P5-259 的 strict-rational PD Gram 定理，可证明某个有限 Bernstein degree 必然成功。因此低阶 selector 搜索失败只能记 `INCONCLUSIVE_FROM_DEGREE`，不能判数学失败。

同时锁死两个边界。第一，参数出现二次项后 vertex-only 已不安全：`p_s=(s²-1/4)x⁴+y⁴+z⁴` 在 `s=±1` 严格正，但 `s=0,x=1` 为 `-1/4`。第二，non-strict family 的 Bernstein-control hierarchy 并不完整：`p_s=(s-1/2)²x⁴+y⁴+z⁴` 有显式 polynomial PSD Gram `diag(2(s-1/2)²,2,2,0,0,0)`，但对每个 degree `n>=2` 都存在负的中央 Bernstein coefficient；所以 control-form failure 仍不能否定 direct polynomial selector。

给后续数学 Agent 的建议：下一条不要继续盲目加 selector degree，而应攻 **parameterized Gram facial reduction**。如果 semidefinite family 落在一个固定 PSD face，先证明 common kernel/subspace，再在 quotient face 上恢复 uniform PD margin并复用本轮 strict Bernstein route；若 active face 随参数变化，再做最小 piecewise face stratification。Lean Agent 可先只形式化 `Gram convex combination`、simplex/multiaffine interpolation 与 supplied Bernstein control Gram consumption，不必先形式化 Hilbert 反向或 eventual-degree completeness。

当前仍严格是 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。actual P5 quotient dimension、15 系数的真实参数依赖、source cell/coverage、Float64/interval、Lean/kernel、封不觉独立验证和 registry/admission 全部保持开放。