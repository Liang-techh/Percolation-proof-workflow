---
kind: companion_log
review_id: review-T-P5-269-moving-quadratic-fiber-fraction-free-clamp-guyuefangyuan-20260910T1830Z
task_id: T-P5-269-MOVING-QUADRATIC-FIBER-FRACTION-FREE-CLAMP
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T18:32:00Z
review_commit: 5334199bdb2c7b093239ffb72ffd4c759294323c
status: pending
admission_label: pending
---

# 古月方源协作交接：T-P5-269

- 当前完成：承接柳冠一 T-P5-268 留下的 moving-fiber seam，证明当真实参数纤维端点是有理函数 `a=Na/Da`、`b=Nb/Db` 时，在分母定向为正且端点顺序成立的径向 cell 上，整个二次参数 clamp 仍可无损压回一元 `Q[q]` 符号问题，不需要把 `(q,s)` 当作一般二维 box。
- 数学核心：定义 `L=Nb*Da-Na*Db`、`Ga=Da*A1-2*Na*A2`、`Gb=Db*A1-2*Nb*A2`、`Ea=Da^2*C-Na*Da*A1+Na^2*A2`、`Eb=Db^2*C-Nb*Db*A1+Nb^2*A2`、`F=4*A2*C-A1^2`。在 `Da,Db,L>0`、`A2>=0` 下，LEFT 只检 `Ga<=0,Ea>=0`，RIGHT 检 `Ga>0,Gb>=0,Eb>=0`，INTERIOR 检 `Ga>0>Gb,F>=0`；所有 gate 都是一元有理系数多项式。
- 新的 fraction-free 证书：令 `x=Da*s-Na>=0`、`y=Nb-Db*s>=0`，则 LEFT 有 `L*Da^2*p=(-Ga)*Da*x*y+L*Ea+(L*A2-Ga*Db)*x^2`，RIGHT 有 `L*Db^2*p=Gb*Db*x*y+L*Eb+(L*A2+Gb*Da)*y^2`，INTERIOR 仍是 `4*A2*p=(2*A2*s-A1)^2+F`。这三张恒等式可直接作为 Lean 的 `ring_nf` 叶，不需要在证明主体中处理有理函数除法。
- seam 兼容：`Da^2*F=4*A2*Ea-Ga^2`、`Db^2*F=4*A2*Eb-Gb^2`，所以 branch switch 可精确 gluing。严格余量 `eta` 只需改成 `Ea-eta*Da^2`、`Eb-eta*Db^2`、`F-4*eta*A2`，可直接接 T-P5-265/266 的 Bernstein/Sturm radial checker。
- 端点退化：`L=0` 不是 FAIL，而是 moving fiber 缩成 singleton；直接检查 endpoint debit。`L<0` 若端点被声明为 lower/upper，则是 source geometry/typing obstruction；只有 source 明确允许 unordered pair 时才能按 sign cell 交换端点。
- 关键 soundness 警告：分母符号绝不能省略。给出了 exact false-PASS regression：`a=1/(q-1), b=0, A=s, K=-1/2, q∈[0,1/2]`。若直接拿负分母形成 `Ga` 会错误选择 LEFT 并通过；把 `a=(-1)/(1-q)` 定向到正分母后会正确进入 RIGHT 并发现 FAIL。
- source fidelity regression：`A=s-q,K=0,s∈[0,q]` 在真实 moving fiber 上精确安全，但若粗化成固定 `[0,1]`，`(q,s)=(0,1)` 会产生伪 counterexample。实际 source 若能给 moving endpoint，就应优先消费本轮 theorem，而不是回退 outer box。
- algebraic 边界：一般代数端点仍可 pointwise clamp，但不能用 resultant/norm 的符号替代选定物理根的符号；`z=sqrt(2)`、`H=z-3<0` 而 `Res(z^2-2,z-3)=7>0` 已锁死该错误 shortcut。若 actual endpoint 是 algebraic，下一位数学 Agent 应做 Thom/isolation selected-root sign transport，而不是盲目平方或取 norm。
- 仍未闭合：actual P5 source endpoint reification、same-key `q/s`、denominator/order proof、state realizability、cell/tube/trajectory/FD-halo coverage、Float64/interval、Lean/kernel、封不觉验证、admission/registry。
- 协作建议：先看真实 source endpoint 类型。若是 rational，直接按本轮 `L/Ga/Gb/Ea/Eb/F` packet 做 exact 一元闭合；若是 algebraic，再开独立 selected-root/Thom child。不要因为 fixed outer box FAIL 就宣称真实 source FAIL。

备注：共享 `collaboration_board.md` 当前 GitHub contents 接口只有整文件替换，没有原子 append；多 Agent 并发时直接覆盖存在丢失他人留言的风险。本条中文协作建议因此先固化在 immutable companion，等待协调层安全汇总。