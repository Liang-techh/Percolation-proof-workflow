---
kind: review_result
review_id: NEW_REVIEW_P5_EXACT_DH_CELL_SOURCE_JET_CONTRACT_20260908
task_id: P5-EXACT-DH-SAME-CELL-SOURCE-JET
agent: Sartre
status: EXACT_JET_EXTRACTION_ONLY_PENDING
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# 可执行 exact DH cell jet：提取结果与最小条件 contract

本轮新增只读 Python 提取器：
`examples/routeb_p5_source_jet/NEW_EXACT_DH_CELL_JET_20260908.py`。
只用标准库 csv/Fraction 等，无 Float64、Julia、Lean、矩阵逆求值、随机数据或外部写入。
默认 stdout 给 compact receipt；`--emit` 同时给 exact coefficient tables。
本 review 是新增 immutable 记录；后续修正需另命名，不覆盖本文。

## 1. 必须先修正导数类型

用 alpha 表示 acceleration，h=(h_q,h_v,h_w) 表示微分方向，R 表示力 RHS。
原问法 `DF=M^-1(R-DM[a])` 不能原样作为 contract：R 必须是方向导数 DR[h]，
DM[h_q] 是矩阵，还必须右乘 alpha；完整 DF 也不只是 acceleration 的6行。

正确的同点接缝是：

```
M(q)*alpha(q,v,w) = R(q,v,w)
M(q)*Dalpha[h] = DR[h] - DM[h_q]*alpha
f=(v,alpha)  => Df[h]=(h_v,Dalpha[h])
```

仅在同 cell 的开邻域上 M 可逆且源函数可微时，才能写成
`Dalpha[h]=M^-1*(DR[h]-DM[h_q]*alpha)`。
P5 使用 xdot=-F+b；若另行绑定 nominal f=-F，才有 DF=-Df。
不能忘记负号、上方运动学6行或把 alpha 误当成任意状态方向。

实际 W=W(q) 时，沿真实流的项是 DW[v]，不是默认 DW[alpha]；
DW[alpha] 只是当 q-space 方向明确取 alpha 时的方向导数。
若 W=W(t,x)，须用 Wt+DW[f_actual]，不能静默删去时间/速度依赖。

## 2. 已执行的真实 source 提取

外部根 E：`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`。
提取器先检查六个输入 SHA，后核对 cell.source_hashes 与 M/C/G 文件一致。

| E下输入 | 锁定SHA-256 |
|---|---|
| routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv | 2760489CBA6DC2F2D25AC8F33FA5A25E430BB92040C022004D1EF949D3E09C5D |
| routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv | CDC587AFD26B2AB5498C5917E8C620E7C9AADA8B2F5B4128C88DF14E78B4E4BB |
| routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl | 0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |

实际从 DH regeneration 文件解析 Kp_DH/d_DH/GwI_DH 的 Q(...) 列表，拒绝不支持的
语法或非6维数据；不使用另一个 Fourier controller 的 damping。
从已有 polynomial CSV 构造 M 并按 imported model 加1/1000000对角 regularizer；
g0 按 c=1,s=0 得到。R 采用所读 source 的明确表达式
`-Kp*q-d*v+g0+GwI*w-Cvv-G`。
这段表达式是人工审阅后的受哈希约束转录；不是解析整个 Julia 程序的语义验证器。
没有冒充完整跨语言 import/source closure；source_binding_proven 始终 false。

变量排列为 q1..q6,v1..v6,w,c1,s1,..,c6,s6。
物理角度导数实现为
`d/dq_i = partial_q_i - s_i*partial_c_i + c_i*partial_s_i`，
避免将 c/s 独立偏导当成 q 导数。导出的键与数量：

- M[i,j]：36；DM[i,j,k]：216（k为六个物理角方向）。
- R[i]：6；DR[i,k]：78（q/v/w十三个方向）。
- 共336个 sparse polynomials，6372个非零有理项。

系数表的 canonical JSON SHA-256：
`c1cee2bc333ead4211842a086e68fae4f52fc95400c78e729935abba19dec139`。
每项编码 exponent tuple、numerator、denominator，无浮点近似；--emit 可直接输出。
这是真实源数据的 exact arithmetic extraction，不是 Da/W/b/e 的 witness。

## 3. 可执行检查的边界

运行命令（工作流根目录）：

```
python -B examples/routeb_p5_source_jet/NEW_EXACT_DH_CELL_JET_20260908.py E
```

实际运行时 E 替换为上面的完整外部根。最终脚本 SHA-256：
`3BD8AC1D468B6F73A5FF230F031CE3D38315B608C90AB0381762054BF0C5A6AE`。
显式读出的 Python exit code=2，为完整 packet 缺失的设计返回值。
外层 PowerShell命令可以退出0；不得把外层退出码当作 packet pass。
一次开发运行后增加了输出中的 conditional_contract 描述，再复跑相同提取，
coefficient digest 一致。不是独立数学验证、回归覆盖或 kernel 证明。

同 cell 目前只绑定到 vanis2 JSON 的字节与 M/C/G 来源；其 scope 为 imported analytic
model、初始球3/20、measurable |w|<=2、first slab，formal=false。
这不自动给导数邻域、实际输入时间律或全程覆盖，也不绑定 deployed FD dynamics。

## 4. 未找到的实际 witness 文件/字段

| 必需 witness | 当前对应实际文件 | 仍缺的字段/证明 |
|---|---|---|
| alpha及Dalpha | cell有 acceleration_radius；regeneration有 descriptor_DH | 没有 alpha 函数图、同域唯一可解性/可微性、Dalpha 满足微分descriptor 的 witness；半径不是函数 |
| W/Wt/DW | physical_rational_energy_metric.csv、block_local_storage_metric_audit.csv | 没有实际P5状态/variation carrier绑定。前者remote G_D，后者block比较；不能自动置Wt/DW=0 |
| b与Db | analytic C/G、FD error表、regeneration descriptor_delta | 缺指定 actual/nominal full vector fields 的函数差及其导数。gain delta或截断幅值不等于b/Db |
| e | descriptor_residual_interface 的l4/l5与误差范数 | 缺 actual variational equation 及 additional e=r+d 的同状态/metric表达；不能重复计Db*xi |
| coverage | vanis2 slab、partial descriptor chain | 缺同source jet的时间/输入律、开邻域导数有效性、tube inclusion/continuation |

“未找到”限于本轮和已定位真实导出的字段，不宣称这些概念不可能构造。
程序输出 missing 数组，不生成名字看似真实但值为 synthetic 的补齐文件。

## 5. 下一最小 witness 与多接口可消费条件

优先交一个同 cell 的 acceleration graph/jet witness：
`M*alpha=R`、`M*Y=DR-DM*alpha`，附同域可逆与可微证明，令 Y=Dalpha。
这样不必先显式展开 M^-1；可直接使用本轮 M/DM/R/DR 表作为系数输入。
仅把这些等式写成约束仍不算证明已生成实际 alpha/Y，必须交对应解与验证证据。

随后必须由实际 P5 source 选择/绑定 W 的 carrier，提供 Wt/DW；若声明 W(q)，
说明 q-state projection 和沿流方向。再给 actual/nominal split 与 b/Db，
并按 `xdot=-F+b`、`xidot=(-DF+Db)xi+e` 定义额外 e。
在同一 domain/source/state key 下组装 C0、Sb 与 e 的 signed metric bounds后，
才可同时消费090/091/093。缺任一项仍 pending，不以哈希相同或局部系数计算替代。

没有改外部源文件、状态、registry 或 formal gate；没有跑本机 Lean或旧轨迹审计。
