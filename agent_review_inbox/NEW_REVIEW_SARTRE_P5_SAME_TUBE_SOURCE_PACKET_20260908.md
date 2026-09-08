---
task_id: SARTRE-P5-SAME-TUBE-SOURCE-PACKET
state_revision_observed: 826
status: NO_CONSUMABLE_SAME_TUBE_SOURCE_PACKET_FOUND
integration_status: pending
admission: pending
source_binding_proven: false
---

# P5 same-tube source packet — 字段级 obstruction

结论：在本次定向检查的现有 artifacts 中，没有找到能同时实例化 P5-090/091/093
的真实 Route-B 同 tube source packet。存在可继续使用的 exact analytic slab 与
同 slab descriptor bound，但缺的不是优化常数，而是源向量场/metric/导数/残差的
同域语义绑定。也不能用它直接消费 P5-092 的 Euler-chord 接口。
本轮未构造 synthetic packet，未用 Float64 数据作为证据，未运行 Lean/Lake、
生成器、数值或全回归；仅新增本 review。

## 1. 当前入口

读取 state.json 时 revision=826。按 nodes 的 name 检索，P5.sparse_disjunctive_sos、
P5.componentwise_relative_decay、M4.block45_full_certificate 等仍 open。
本轮不从 state 的数学子节点数量或某个 compiled algebra leaf 推导 source closure。
最新已定位 P5 review 为 T-P5-093（base-flow Lie defect），结合 090/091/092 的
source-facing packet 条款作消费检查。093 自身是 CONDITIONAL_PASS、pending，
且明确 deployed same-tube binding、coverage 与 kernel receipt 未完成。

所检查的共享消费链是：

`same source/tube + F,DF,W,Wt,DW -> C0 -> P5-090`

`same source/tube + b,Db -> Sb=DW[b]+Db^T W+WDb -> P5-093`

`same source/tube + additional e=r+d -> P5-091`

不得把 Db*xi 同时装入 Sb 和 additional e。P5-091 本身保持 nominal base path，
只有经093的 base-flow 修正后才可用于实际受扰 base flow。

## 2. 最接近的 exact artifact pair：同 slab 有接点，但不足消费

外部只读根：
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/`。

- `half_active_vanis2_domain_probe.json`：RATIONAL_FIRST_NONLINEAR_SLAB，formal=false。
  scope 是 imported analytic model、full initial radius 3/20、measurable |w|<=2、
  first slab only；角半径 (9/20,19/50,37/100,19/50,37/100,9/20)，速度半径3，step=1/512。
- `half_active_vanis2_bound_probe.json`：COMBINED_POLYNOMIAL_DESCRIPTOR_BOUND，formal=false。
  domains[0].slab 明确指向上述 domain 文件；含 preconditioned gravity/coriolis/mass/
  defect、acceleration_remainder_abs、coefficient_abs、velocity_radii。
  因而不是“完全没有同域接点”，但这些字段只够候选 acceleration/descriptor bound。
- source_hashes 声明 analytic mass/gravity/coriolis CSV 身份；不是 F、DF、W、DW、Db
  的 typed function equality，且这里不把声明哈希升级为已认证 provenance。

一个容易误消费的字段是 domain 的 `contraction_matrix`。已读取对应
exact_checks/check_initial_analytic_slab.py 行34–47：它逐 entry 上界
`abs(I-X*M)`，并检查加权 C*w<=kappa*w、kappa<1。
这是质量线性方程的 preconditioned inverse/Neumann guard，
不是 P5-090 的 `C0=DF^T W+W DF-(Wt-DW[F])`，kappa 也不是 differential contraction rate。
同名“contraction”不能消除类型差异；本轮没有重跑 checker。

## 3. 字段级 obstruction 与多个消费者

| 共享字段 | 现有证据/缺口 | 不能消费的接口 |
|---|---|---|
| source_id + full state convention | analytic CSV 哈希和旧 B=(4,5)/D=(1,2,3,6) ledger 存在；缺统一 exact F、controller/input/regularizer 与 state-map 身份 | 全部 |
| tube_id, time interval, initial set, input law | 首 slab box 有值；没有统一已认证 tube inclusion/continuation；|w|<=2 不自动绑定 w=ct、c²<=3、完整[0,1] | 090/091/093 invariance；092 chord |
| xdot=-F+b, A=DxF | descriptor acceleration 绝对界不提供完整12D/14D exact field derivative | 090/093 |
| W(t,x), symmetry/PSD, Wt,DW | 所查 slab/descriptor payload 不含已绑定 moving metric 或 material derivative；不能以 X、weights、mass interval 替代 | 090/091/093 |
| C0>=2mu W | 未找到同 tube 的 signed quadratic lower witness；Neumann C 不是它 | 090/091/093 |
| b, Db, DW[b], Sb | 未找到实际 residual 到 base perturbation 的函数等式与导数 witness；幅值界不能推出 Db 或 Sb | 093 |
| additional e=r+d, signed relative power, QW(d) | acceleration_remainder_abs 是状态方程/descriptor 量，不是变分残差；缺从实际 variational equation 导出的类型/维数/metric 转换 | 091，093混合分支 |
| chart T,J,G,DG 与 Je_z=e_x | 未找到同 source/tube 的真实 chart packet；不能拿任意常值/identity chart 作 synthetic 填充 | 090 chart、091 transport |
| Euler endpoint, frozen g, whole chord, D²V[zeta,zeta] | first slab step 不证明真实 Euler endpoint，也不提供 frozen-chord signed curvature；真流 slab 与数值 chord 非同一对象 | 092 |

状态 storage `y^T W(t,y)y` 和 variational storage `xi^T W(t,x)xi` 不能混同。
即使共用 W/material derivative，也必须分别声明对象和导数。普通 residual ledger
里的 rho_C/rho_G 等不是093的 rho（Lie-defect rate），也不是091的 relative operator。

## 4. 其他实际检查与不允许的拼接

- GAK exporter manifest：admissible_numeric_receipts=[]、cell_id=null、numeric_receipt=null；
  缺 q_box/dq_box/w_box/M_q/inverse_guard/Cdq/Gq/a/f/l_true/l_true_square_bounds/
  kappa/h_lo/h_hi，以及 coefficient_version、keyed receipt、rounding。
  其语义记录指向 Float64/central FD/solve，故本轮排除为正向 witness，而非消费其值。
- GBC residual ledger 是 OPEN_FAIL_CLOSED_SCHEMA_ONLY。它正确要求 full q,dq,t,w,c,
  aB,aD,a,MBD_aD 和 exactly-once remainder，但 bound 为空；这是 schema，不是实例。
- EF flowpipe parent receipt：numeric_receipt.present=false、initial/steps/continuation/
  terminal=false。没有公共 tube coverage 可从这里借入。
- dynamic_descriptor_l2_chain_v3.json 自称 PARTIAL_DYNAMIC_DESCRIPTOR_SINGLETON_CHAIN、
  formal=false，记录 end_time=183/512，stop.reason=guard_or_endpoint_domain_exit。
  domain_bank 是多个 half_domain 与 vanis2 配对域；这不是完整[0,1]认证 tube，
  也没有自动提供上述 W/Db/variational fields。时间值仅转述 artifact，未重验 chain。
- 原 block45 目标采用 full12D 初始球与 w=ct；14D lift 还含 w,c。不能把 block-only
  ledger、6D mass preconditioner、12D状态 storage、14D input lift 和变分空间无映射拼接。
- exact analytic first slab 的 measurable-input scope 不自动提供 P5-092 所需的
  time/state C² storage 与 chord coverage；不能把样本、端点或 flow 二阶导数顶替它。

## 5. 下一最小 witness：同一真实 cell 的 exact jet packet

最小有区分力的下一步不是调 mu/rho/K，而是选定现有真实 analytic slab（例如上述
vanis2）并交一份不可变 keyed packet，先明确它只声称 analytic-model 局部结果：

1. 精确 source/controller/input/state-map 身份及该 cell 的完整 time/state/input 域，
   并证明相关轨迹/导数评价点确在该域；没有证明前只能给条件点态 consumer。
2. 从同一 source 输出 exact F、DF、W、Wt、DW，并绑定函数/导数等式与 regularity；
   先生成 signed C0 和其 quadratic lower witness。这一份共同底座可喂090、091、093。
3. 若有真实 base residual，输出 b、Db 的 source identity，组装 Sb 后给 signed
   quadratic upper witness；再从实际 variational equation 定义 additional e，
   明确不重复计 Db*xi，输出 r/d 的同 metric 功率/平方界。
4. 只有这些字段齐全后，才检查既有 mu-rho-sigma 和 Ebar/Vstar 消费门槛。
   此处没有挑选或优化任何新常数，也不假定 b/e=0。

若要同步消费092，还必须另给实际 frozen Euler map、whole chord inclusion 与同一
storage 的 directional Hessian enclosure；不能从090/091/093连续时间结果推来。
若要升级为 deployed Route-B 而非 analytic model，还需实际 source refinement；
本轮明确不以 Float64 输出替代它。

## 6. 当前读取的字节身份

| 文件 | SHA-256 |
|---|---|
| T-P5-093 review | F8F0380C6512D2F9095ACADD81A2252CD484621EC83B4B32C6CC9395A45F72F5 |
| GAK manifest | E5572411033A2BB131CBB9966E1FF6DFD1894EF3F1A040D168FAC75D4B7685C1 |
| GBC ledger | C799F4F544BF0FF15F5DC5B62D056D204C839431B54C14516C50FA00F912616C |
| EF parent receipt | B816B56E4B8A838D6064A5E1D4DA004869F0CB9C7FA14FBE0C6E0390AF3579A6 |
| vanis2 domain | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| vanis2 bound | 961DE57FAAF70CB25D646C6B02116D6C1B4DA766CF0F8E982D7B58F56883E9D6 |

搜索限于当前 state、最新相关 reviews、source/residual/flowpipe ledger 与上述
exact analytic 产物；不是全机不存在证明。哈希只标识所读字节，不是认证 theorem。
没有修改 StateStore、registry 或旧文件；source/admission 均 pending。
