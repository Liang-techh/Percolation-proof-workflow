---
kind: companion_log
review_id: review-T-P5-268-concave-quadratic-parameter-clamp-liuguanyi-20260910T1808Z
task_id: T-P5-268-CONCAVE-QUADRATIC-PARAMETER-CLAMP
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T18:10:00Z
review_commit: bcebee5554c3a98dbe3a716407a21586f6367839
status: pending
admission_label: pending
---

# 柳冠一协作交接：T-P5-268

- 当前完成：承接红莲魔尊 T-P5-267 留下的 concave-quadratic parameter seam，证明了一参数二次凹族的精确 clamp 定理。关键改进是把原先建议的 `A2>0` 放宽到 `A2>=0`：使用 LEFT→RIGHT→INTERIOR 的确定性分支后，零曲率的 affine/constant 情形不会产生除零漏洞；真正进入 INTERIOR 时，`g_a>0>g_b` 会自动推出 `A2>0`。
- 数学核心：定义 `p=K-A=C-A1*s+A2*s^2`、`g_a=A1-2aA2`、`g_b=A1-2bA2`、`E_a=p(a)`、`E_b=p(b)`、`F=4A2*C-A1^2`。LEFT 检查 `E_a>=0`，RIGHT 检查 `E_b>=0`，INTERIOR 检查 `F>=0`。三个分支都有完全无除法恒等式，且 `F=4A2E_a-g_a^2=4A2E_b-g_b^2` 精确保证 clamp seam 的兼容。
- 新 bridge：区间约束 `h=(s-a)(b-s)>=0` 下可以显式给出 lossless S-lemma multiplier：LEFT 为 `-g_a/(b-a)`，RIGHT 为 `g_b/(b-a)`，INTERIOR 为 `0`。因此 clamp optimizer 与一约束 S-lemma 在此结构下是显式等价，而不是两个独立 sufficient condition。
- exact dispatcher：先用 T-P5-266 决定 `A2>=0`，再对 `g_a,g_b,E_a,E_b,F` 的 squarefree product 做一元 Sturm 根隔离；每个 open sign cell 只需一个有理采样点决定分支和 debit 符号。内部根点由 `m(q)=min_s p(q,s)` 的连续性闭合，不需要浮点代数根。真实 box failure 总能导出有理 `(q,s)` counterexample；但若 `[0,R]×[a,b]` 只是 source outer box，该 counterexample 不能自动升级成物理 FAIL。
- 严格余量：要证明 `p>=eta`，分支只需替换为 `E_a>=eta`、`E_b>=eta`、`F>=4A2*eta`，可直接接后续 coefficient-error budget。
- 仍未闭合：actual P5 `A0/A1/A2` source identity、same-key `q/s`、真实 parameter fiber、state realizability、coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry。
- 建议下一步：不要继续造一般 bivariate optimizer。优先处理 source 真正给出 `s∈[a(q),b(q)]` 时的 moving quadratic fiber，证明端点代入、端点顺序与 denominator-sign transport 何时仍保持一元 fraction-free clamp；若只拿固定 outer box，PASS 可消费，FAIL 保持 inconclusive。
