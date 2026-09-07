# H_acc source theorem seam: pending / OPEN_H_ACC

本次把 source theorem 的最小接口收敛为六项条件：source idealization、
scalar evaluator、array lowering、occurrence aliases、body identity、ordered fold。
真实 `NEW_INTAKE.json` 的 export、mapping、updates、runtime、interval 仍为空。
没有生成 DAG、DH/m/I_val 数值表、H_acc 常数、运行观测或形式证明。
`NEW_SEAM_REPORT.json` 是对实际本地字节的只读定位审查，不是 Julia export。

仅新增本目录 `NEW_SEAM_*` 文件；不修改 intake、schema、checker、已有 NEW_*、
state、registry 或共享脚本。新脚本调用已有 `NEW_source_intake.inspect`，不安装
新 admission 规则。本文中的条件化数学推导没有经过 Lean/Lake 验证。

## 1. Source binding 与最小 span

目标 snapshot 是
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`，
raw-byte SHA256 为
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`。
定位只对这个 snapshot 成立，不声明部署中的 Julia 文件/方法相同。

现有 span 是 **1-based inclusive lines**，digest 包含原始换行字节。
新 report 补充 **0-based half-open raw UTF-8 byte offsets** 和 fragment digest，
定位行内表达式。byte column 也从 0 开始，不能当作 Unicode 字符列。
这属于独立 sidecar；不能往 closed v1 intake 的 span 对象添加这些字段。

| 对象 | 最小 source occurrence | 必需语义，而非 span/hash 所能证明 |
|---|---|---|
| DH / m / I_val | 6–11 / 12 / 13 | decimal→有理数、pi→精确实数；坐标与 literal-expression 的绑定 |
| q、角度、trig、A | 37 / 37 / 38 / 39 | 输入 joint 绑定；九种 scalar op 的正确 lowering |
| Tc[0]、Tc[f>0] | 32 / 40 | identity；push 前父 frame 与矩阵乘法 |
| o[0]、o[f>0] | 33 / 41 | initial zero；push 后 frame 的第四列 |
| z[j] | 36 | push 前 `Tc[end]`，即 frame j−1；34 只初始化后会被覆盖 |
| COM[b] | 50 | 前后 origin 的 midpoint |
| Ri[b] | 51 | `Tc[ii+1]` 的左上 3×3 block，即 frame b |
| Ii[b] | 52 | `(I_val[b]/3) I3`，不能丢掉除以 3 |
| Jv / Jw active | 55 / 56，控制 54 | j≤b；cross / z 的列复制 |
| Jv / Jw inactive | 53，控制 54 | j>b 的初始零保留，不能声称执行了 55/56 |
| S0 | 48 | 6×6 zero allocation 的 ideal-real 含义 |
| translation / rotation / B / Sb | 58 的各自 fragment | 两项、两项之和、以及 M 更新必须分开 |
| final | 58 body 6，loop end 59 | alias S6，程序点在 60 之前 |

第 58 行的四个 selector 已按真实字节分别定位：

```julia
m[ii] .* (Jv' * Jv)
Jw' * (Ri * Ii * Ri') * Jw
m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw
M += m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw
```

前两段不相交，均包含于 B，B 包含于 update。同一行 hash 无法辨别这四个角色。
行 60 完全不进入 export/root/occurrence span；return value、减去 regularizer、
`regularization=0` 的返回值均不能代替该程序点的观测。

行 35、40 的顺序，47 的调用连接，以及 49、54、59 的循环控制是 theorem 所需的
source context。它们不必被伪装成算术 DAG 节点。一次静态 line-58 occurrence
有六个 body 实例；实例键至少是 `(source hash, site, body, row, column)`。
仅复制同一个 span 六次不证明执行了六次。

`NEW_SEAM_source.py` 在 v1 检查之后报告 occurrence 是否覆盖表中必要行。
例如，v1 可以接受 z span=34 或 active Jw span=53（落在宽 role anchor 内），
但这些位置不包含最终 mapped entry 的赋值。新审查把它列为 pending seam gap，
不将原本合法的 v1 candidate 改判 rejected；包含必要行的宽 span 仍可保留。
同一行内表达式和 scalar 节点之间的正确性仍需独立 witness。

## 2. E_star scalar DAG 的精确语义接口

令 G 是通过现有结构检查的有限、拓扑排序 DAG。固定同一个 q∈ℝ⁶，定义 νq(n)：

| op | Real 解释 |
|---|---|
| input(j) | q[j] |
| rat(p,d) | p/d，canonical integers，d>0 |
| pi | 数学常数 π |
| neg(a) | −νq(a) |
| add(a,b) | νq(a)+νq(b) |
| mul(a,b) | νq(a)νq(b) |
| div_nat(a,d) | νq(a)/d，d 为正自然数 |
| sin(a), cos(a) | 实函数 sin(νq(a)), cos(νq(a)) |

这是声明的 denotation，不是 Python/Julia Float64 evaluator。每个参数引用更早的
节点，归纳可定义唯一 νq；除数恒正，所有 op 在实数域上有定义。形式实现仍为空。
节点共享意味着在同一 G、同一 q 下共享 νq 值。`semantic_role` 字符串和 source hash
不参与 νq 的计算，因此也不能证明某个任意合法 rational 就是源码中的 m[b]。

必须另有 source correspondence：每个被根/array 使用的 scalar 子图，在给定
source site、动态实例和 typed coordinate 下等于所声称的 source idealization。
应覆盖所有相关中间运算；未使用节点也不能作为补齐语义覆盖的替代品。
目前 v1 没有 DH/m/I_val 的逐项 literal binding 表，也没有 matrix reduction、
transpose、broadcast 或 cross 的 lowering witness。下一份真实 exporter 产物至少
需要把这些绑定与 graph digest 关联；现有封闭字段容不下的部分需独立、经审查的
proof sidecar，不能直接扩充 v1 或靠 role 标签补足。

source idealization 把 source decimal tokens 解释为有理数，把 pi 解释为 π；
`Matrix{Float64}(I,...)` / `zeros` 在这一层的目标是实数 identity / zero。
这不宣称实际 Julia 构造和运算没有舍入。`0.5 .* x` 可在实数域证明等于 x/2，
但不要求 exporter 用虚构的 `div_nat` 节点替换源码乘法；真实 lowering 应保留
自己的表达式，并提供等价理由。`I_val/3` 必须保留其除法语义。

source binding 还需固定参数/global 的意义与生命周期；Julia `DH,m,I_val` 是
可变数据，snapshot 文本本身不能保证运行时没被修改。实际 Julia dispatch、
多参数 `*`、矩阵核的结合方式、FMA/trig 都留给 source/runtime refinement。
下面的实数乘法展开是明确的目标，不是从源码文本猜出的机器执行树。

## 3. Ri / Jw / z occurrence aliases

令 N_X(c) 是 array_mapping 中 X 的 coordinate c 引用的 node ID，
X̂(c)=νq(N_X(c))。人类 frame f=0..6 对应 Julia `Tc[f+1]`；
人类 o[f] 对应 Julia `o[:,f+1]`。必须保持：

```text
N_z(j,k)     = N_Tc(j-1,k,3)          j=1..6, k=1..3
N_o(f,k)     = N_Tc(f,k,4)            f=1..6
N_Ri(b,k,l)  = N_Tc(b,k,l)            b=1..6, k,l=1..3
N_Jw(b,k,j)  = N_z(j,k)               j<=b
Jv̂(b,k,j) = Jŵ(b,k,j) = 0          j>b, explicit rat zero nodes
```

现有 checker 已检查这些 node ID 等式和 explicit zeros。给定 νq，node identity
立即推出 value equality；这个小 congruence 步骤无需添加 `add(x,0)` 或 alias op。
例如 z[1,k] 的值可由定义在 32 的 identity node 提供，其 occurrence 在 36；
Jw 的 occurrence 在 56，同一个 scalar 定义不需要再搬到 56。

这里的 alias 是 **scalar denotation / node identity**，不是 Julia heap alias
声明。slice、列赋值即使产生 copy，也可以在对应程序点有同样的 scalar 值。
source theorem 仍需说明 z 在 push 前读取父 frame、Ri 读取 frame b、Jw 的 loop
只写 active prefix，以及相关数组不会在读取前后被意外改写。node ID 等式不能
独自证明这些时间与索引事实。

## 4. B=translation+rotation 的最小 semantic seam

先把下列数组公式作为未解决的 source/array refinement 前提，全部在 ℝ 上：

```text
T0 = I4; Tb = T(b-1) Ab                         b=1..6
o0 = 0; ob[k] = Tb[k,4]
zj[k] = T(j-1)[k,3]
pb = (o(b-1) + ob)/2
Rb[k,l] = Tb[k,l]                              k,l=1..3
Ib[k,l] = (I_val[b]/3) delta(k,l)
vb[:,j] = zj cross (pb - o(j-1)), wb[:,j] = zj  j<=b
vb[:,j] = wb[:,j] = 0                          j>b
```

Ab 的各项必须按 line 39 绑定 line 37 的角度/DH 和 line 38 的 trig，
不能只证明某个矩阵看起来像 DH。cross 的 component 必须分别是
`z2*d3-z3*d2, z3*d1-z1*d3, z1*d2-z2*d1`，其中 d=pb−o(j−1)。
这些等式尚未由现有 intake checker 检查。

对每个 body b 和全部 r,c=1..6，取 k,l,h∈1..3，明确以下有限实数和：

```text
L_b[r,c] = m[b] * sum_k (v_b[k,r] * v_b[k,c])
P_b[k,l] = sum_h (R_b[k,h] * I_b[h,l])
Q_b[k,l] = sum_h (P_b[k,h] * R_b[l,h])
U_b[r,l] = sum_k (w_b[k,r] * Q_b[k,l])
W_b[r,c] = sum_l (U_b[r,l] * w_b[l,c])
B_target_b[r,c] = L_b[r,c] + W_b[r,c]
```

P,Q 是 3×3，U 是 6×3，W 是 6×6。因为取值在 ℝ，adjoint 的目标是 transpose；
这里特别保留 `R_b[l,h]` 的转置索引。于是 W 的矩阵目标为
`(w_bᵀ ((R_b I_b) R_bᵀ)) w_b`，即源码未化简的 rotational term。
每个 sum 是数学上的有限和；具体 DAG reduction tree 要靠展开/结合律证明与其
相等，不能从这个公式反推一个已执行的 Julia reduction。

最小 body theorem 只需要两个真正的 semantic 假设：

```text
νq(N_translation(b,r,c)) = L_b[r,c]
νq(N_rotation(b,r,c)) = W_b[r,c]
```

再用 checker 已要求的
`G[N_B(b,r,c)] = add(N_translation(b,r,c), N_rotation(b,r,c))`
和 evaluator 的 add equation，一次代入即得
`νq(N_B(b,r,c)) = B_target_b[r,c]`。
216 个 coordinate 都需要；共享节点不允许省略零项或另一个三角。
translation/rotation 必须先具有上述含义，顶层 add 本身不能补出这些前提。
不借用 R 的正交性把 RIRᵀ 化掉，也不把 B 换成已经化简的惯量表达式。

## 5. S_b=S_(b−1)+B_b 的条件化归纳

定义 A0[r,c]=0，Ab[r,c]=A(b−1)[r,c]+B_target_b[r,c]。
目标 `M_NE^0(q)[r,c]` 是 A6；若项目中另有独立定义的 `M_NE^0`，
还必须证明其与这里的 unsimplified target 相同，不能仅重命名便声称 theorem。

设 Z 为 initial_zero root，Nb 和 Ns 分别为 body 与 accumulator roots。
existing checker 提供以下**候选图语法条件**：

```text
G[Z] = rat(0,1)
G[Ns(b,r,c)] = add(Z, Nb(b,r,c))                b=1
G[Ns(b,r,c)] = add(Ns(b-1,r,c), Nb(b,r,c))      b=2..6
N_final(r,c) = Ns(6,r,c)
```

在 evaluator 和 body theorem 成立的前提下：基例 νq(Z)=0=A0；
归纳假设 νq(Ns(b−1,r,c))=A(b−1)[r,c]，由 literal add 和 body equality 得
νq(Ns(b,r,c))=A(b−1)[r,c]+B_target_b[r,c]=Ab[r,c]。
b=1 用 Z 替代前驱；到 b=6 再用 final node identity，得到
`νq(N_final(r,c)) = M_NE^0(q)[r,c]`。逐项等式推出 6×6 矩阵等式。

36-slot 顺序是 `6*(c−1)+(r−1)`；body block 的 slot 再加 `36*(b−1)`。
source_updates 的 before/body_roots/after 必须分别绑定这些根：body 1 的 before
重复 Z，后续 before 等于前一 after。它们是冗余 source occurrence 绑定；
source loop theorem 仍需证明 line 48、49、58、59 的程序状态满足这条递推。
`M += ...` 在此以 M 的 successive values 建模，不声明是原位 element update。

这个条件化 argument 对 ideal-real q 有意义；当前运行输入契约只是 finite
binary64 qhat 且 Decode(qhat)∈Q1000。若将 H_acc 扩展到全部 real inputs，
仍须独立处理 RN64 input conversion 和 expanded cover。
`E_star=M_NE^0` 不涉及 E_loaded、J_acc 的数值误差：

```text
J_acc - M_NE^0 = (J_acc - E_loaded) + (E_loaded - E_star)
                + (E_star - M_NE^0)
```

只有真实 source/evaluator/body/fold theorem 才能消去末项；interval 表格不能消去它。

## 6. 下一份真实输入与本次验证

下一步是接收有 provenance 的真实 source export，包含原 v1 中的 scalar DAG、
dense array mapping 和六个 source updates。随后把上面六项 witness 绑定到
source hash、canonical graph hash、occurrence mapping/update digest、target
definition、semantic environment 与实际验证过的 proof dependencies。
本次 `required_witnesses` 全部 artifact=null / verified=false，没有可接受
theorem-success flag 的路径；即使所有 candidate checks 通过，退出码仍为 3。

可从仓库根目录运行（只输出，不写文件）：

```powershell
python -B examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_source.py
exit $LASTEXITCODE
```

```powershell
python -B -m unittest discover -s examples/routeb_o0_h_acc_source_refinement -p NEW_SEAM_test_source.py -v
exit $LASTEXITCODE
```

测试只使用真实 snapshot、空 intake 和内存中的畸形输入/定位记录；不构建假 DAG、
假 loaded constants 或假 Julia observations。源码定位、byte slicing、active/inactive
occurrence 区分、pending/rejected 边界及 duplicate-key 拒绝是开发检查，
不构成 H_acc_expr、H_acc_round 或 source binding 的证明。

本次实际验证：9 项定向测试全部通过；CLI 用 `exit $LASTEXITCODE` 保留原生
退出码，得到 pending / 3。保存的 report 经严格 JSON parser 重新读取后与 live
audit 对象完全一致，含 27 个实际源码 fragment。目录内 12 个原有文件的 SHA256
均与工作前一致，tracked diff 为空。其他目录出现了并发新增文件，本次未触碰；
本次写入仅为 `NEW_SEAM_source.py`、`NEW_SEAM_test_source.py`、
`NEW_SEAM_REPORT.json`、`NEW_SEAM_REVIEW.md`。未运行 Julia、Lean 或 Lake。
