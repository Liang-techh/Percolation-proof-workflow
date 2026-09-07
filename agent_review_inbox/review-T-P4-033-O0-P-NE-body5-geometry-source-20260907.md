# T-P4-033 O0/P-NE：human body-5（zero-based 4）exact DH source review

状态：CONDITIONAL_BODY5_GEOMETRY_DERIVATION。本 review 只处理 human body-5，即 body = (4 : Fin 6)；不消费 baseline/Schur，不修改主 state/registry，未运行本机 Lean/Lake。

## 绑定与 CSV gate

source_key = routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)
state_key  = routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
orientation = source-frame DH, prefix frame slots, body Gram = m Jv^T Jv + kappa Jw^T Jw

当前 O1_BODY_5_TARGET_CHECK.json 报告 csv_row_count=57 且 keyed_coefficient_map_matches=true；trace evaluator 的 body count 也给出 body-5 为 57 rows。因此没有发现当前 body_5_piecewise 与冻结 CSV support 的数学不一致。缺口是 source expansion 与 tagged fold 的 Lean proof，而不是 CSV support。

## 1. Prefix slots 与 axes

令

q0 := q 0, q1 := q 1, q2 := q 2, q3 := q 3
phi := q1 + q2
er := (cos q0, sin q0, 0)
et := (-sin q0, cos q0, 0)
e3 := (0,0,1)
a := 2/25, b := 21/100, d0 := 1/10
d := 1/20, f := 19/100
U := a + b sin q1
B := b sin q1
C := b cos q1

routeBFrameSlot 的 body-5 所需 prefix reductions 是：

slot 0 : I
slot 1 : I · T0
slot 2 : (I · T0) · T1
slot 3 : ((I · T0) · T1) · T2
slot 4 : (((I · T0) · T1) · T2) · T3
slot 5 : ((((I · T0) · T1) · T2) · T3) · T4

origin slots 精确化为：

o0 = 0
o1 = a er + d0 e3
o2 = U er + (d0 + C) e3
o3 = o2 + d et
o4 = o3 + f z3
o5 = o4

最后一个等式来自当前参数 a4=0,d4=0：step-4 改变 orientation 但不改变 origin。

定义：

x3 := cos phi er - sin phi e3
z3 := sin phi er + cos phi e3
z4 := -sin q3 x3 + cos q3 et

source-axis slots 为：

z0 = e3
z1 = et
z2 = et
z3 = sin phi er + cos phi e3
z4 = -sin q3 (cos phi er - sin phi e3) + cos q3 et

z4 是 slot-4 的 parent axis，不能误取为 step-4 之后的 z-axis。q4,q5 不进入 body-5 target：q4 只旋转 zero-translation step-4，q5 对 body-5 是 inactive joint 5。

## 2. COM、active Jv/Jw columns

body-5 使用 COM slots 4 and 5，故：

c4 = bodyCom(...,4) = (o4+o5)/2 = o4
A := U + f sin phi
P := C + f cos phi
Q := B + f sin phi
r0 = c4-o0 = A er + d et + (d0+C+f cos phi)e3
r1 = c4-o1 = (B+f sin phi)er + d et + (C+f cos phi)e3
r2 = c4-o2 = f sin phi er + d et + f cos phi e3
r3 = c4-o3 = f z3
r4 = c4-o4 = 0

ancestor-active 的 joint columns 是 j=0,1,2,3,4；但非零线速度列只有 0,1,2：

v0 := Jv[0] = z0 × r0 = A et - d er
v1 := Jv[1] = z1 × r1 = P er - Q e3
v2 := Jv[2] = z2 × r2 = f(cos phi er - sin phi e3) = f x3
v3 := Jv[3] = z3 × r3 = 0
v4 := Jv[4] = z4 × r4 = 0
v5 := 0  (inactive)

w0 := Jw[0] = e3
w1 := Jw[1] = et
w2 := Jw[2] = et
w3 := Jw[3] = z3
w4 := Jw[4] = z4
w5 := 0  (inactive)

不能把“5 个 ancestor”误读为 5 个非零 Jv。CSV 的 (0,4)、(1,4)、(2,4) 项来自 Jw dot products，不来自 Jv[4]。

## 3. 未展开 exact Gram

当前 source constants 是 m4=3/10、kappa4=1/30。未展开 Gram 为：

Gv =
[[ A^2+d^2,       -d P,                  -d f cos phi, 0, 0 ],
 [ -d P,          P^2+Q^2,               f(P cos phi+Q sin phi), 0, 0 ],
 [ -d f cos phi,  f(P cos phi+Q sin phi), f^2,          0, 0 ],
 [ 0,             0,                     0,            0, 0 ],
 [ 0,             0,                     0,            0, 0 ]]

Gw =
[[1, 0, 0, cos phi,             sin phi sin q3],
 [0, 1, 1, 0,                    cos q3],
 [0, 1, 1, 0,                    cos q3],
 [cos phi, 0, 0, 1,               0],
 [sin phi sin q3, cos q3, cos q3, 0, 1]]

关键 trig entries：

e3·z4 = sin phi sin q3
       = (cos(phi-q3)-cos(phi+q3))/2
et·z4 = cos q3
z3·z4 = 0

## 4. 严格冻结的 body_5_piecewise / CSV target

令 T4 := (3/10)Gv + (1/30)Gw。非零 entries 必须 exactly 为：

T4[0,0] = 1441/30000
          + (63/6250) sin q1
          + (57/6250) sin(q1+q2)
          - (1323/200000) cos(2q1)
          + (1197/100000) cos q2
          - (1197/100000) cos(2q1+q2)
          - (1083/200000) cos(2q1+2q2)
T4[0,1] = T4[1,0] = -(57/20000) cos(q1+q2) - (63/20000) cos q1
T4[0,2] = T4[2,0] = -(57/20000) cos(q1+q2)
T4[0,3] = T4[3,0] = (1/30) cos(q1+q2)
T4[0,4] = T4[4,0] = (1/60)(cos(q1+q2-q3)-cos(q1+q2+q3))
T4[1,1] = 8609/150000 + (1197/50000) cos q2
T4[1,2] = T4[2,1] = 13249/300000 + (1197/100000) cos q2
T4[1,4] = T4[4,1] = (1/30) cos q3
T4[2,2] = 13249/300000
T4[2,3] = T4[3,2] = (1/30) cos q3
T4[2,4] = T4[4,2] = (1/30) cos q3
T4[3,3] = 1/30
T4[4,4] = 1/30

其余 entries 为 0。按 entry 计数：T00=13、T01/T10=8、T02/T20=4、T03/T30=4、T04/T40=8、T11=3、T12/T21=6、T14/T41=4、T22=1、T24/T42=4、T33=1、T44=1，总计 57。

support representatives（省略 conjugate negatives）为：

T00: (0,0,0),(1,0,0),(1,1,0),(2,0,0),(0,1,0),(2,1,0),(2,2,0)
T01/T10: (1,0,0),(1,1,0)
T02/T20,T03/T30: (1,1,0)
T04/T40: (1,1,-1),(1,1,1)
T11,T12/T21: (0,0,0),(0,1,0)
T14/T41,T24/T42: (0,0,1)
T22,T33,T44: (0,0,0)

## 5. 最小 Lean child

1. body5_frame_slot_0_to_5：逐一展开 routeBFrameSlot q i；显式处理 Matrix.mul_apply、Matrix.mul_assoc、one_mul、mul_one，保留 prefix shape。
2. body5_slot_origin_exact：证明 o0,...,o5，特别是 o5=o4。
3. body5_source_axis_exact：证明 z0=e3、z1=z2=et、z3=sin(phi)er+cos(phi)e3、z4=-sin(q3)x3+cos(q3)et。
4. body5_com_exact：证明 bodyCom origins 4=o4，并给出 r0,...,r4。
5. body5_jv_columns_exact：证明 v0,v1,v2 及 v3=v4=0；用 inactive lemma 关闭 j=5。
6. body5_jw_columns_exact：证明 w0,...,w4；用 inactive lemma 关闭 j=5。
7. body5_orthogonal_trig_lemmas：封装 er/et/e3 dot/cross、sin_sq_add_cos_sq、cos_sub、sin_mul_sin。
8. body5_gram_entries_exact：按上面的 Gv/Gw 逐 entry 证明，先不 fold Fourier atoms。
9. body5_mass_entries_exact：代入 m=3/10,kappa=1/30，exact rational normalize 到 body_5_piecewise。
10. body5_fourier_atom_fold_exact：对 body=4、row、col、(q1,q2,q3) frequency 做 finite tagged-fold case split，严格生成 57-row support。
11. h_body_5_source_to_trace_compiled：最终 statement 固定为 forall q i j, sourceBodyMass q (4 : Fin 6) i j = bodyTraceEvaluator 4 q i j，并要求同 key 的 compiled proof、#print axioms、zero sorry/admit receipt。

## Fail-closed 结论

当前可确认的是 exact target/checker support，不是 source theorem。O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json 明确将 source expansion、trace fold、h_body_5 标记为 OPEN_NO_PROOF；因此不宣称 O0/P-NE closure。当前没有 adapter/CSV 的数学 support mismatch。

## Evidence

| artifact | SHA-256 | role |
|---|---|---|
| examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyTraceAdapter.lean | 25F099EC5EB7F699C789AE29AA45DF0FBB24FF06547F498740968F5E1B3C9976 | 当前 body_5_piecewise 与 proposition targets |
| examples/routeb_b45_source_comparator_lean/O1_BODY_5_TARGET_CHECK.json | E761B8950929562F350F768A2C1A9B2DCD62A5CE62FB9921626172332C6EA40E | 57-row exact target checker |
| examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean | B9845D37B5DCD16E1F9E142CB2E4D0E5571452993E843C85AC8CD643F6BA5DEA | generated finite evaluator |
| examples/routeb_b45_source_comparator_lean/O1_BODY_TRACE_EVALUATOR_CHECK.json | 8024F6A57F6BEF890F08825A71EFF056499D995616E6A9D297FDB82773C2DB89 | body-count/support gate |
| artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv | AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9 | frozen body trace CSV |
| examples/routeb_real_dh_step_lean/RealDHStep.lean | 9C04DA5B9627EE749C53009733006934F95B2D33265E46CA59D0725AA453786A | exact DH step definitions |
| examples/routeb_frame_slot_accessor_lean/FrameSlotAccessor.lean | F497BD1F45FAE4DD385F4D0F46DF79252C92E5CD027B29D5DC55011F91525C31 | prefix slot/source-axis access |
| examples/routeb_body_semantic_core_lean/BodySemanticCore.lean | FE15F6CA9993F55FC56E6D2C9CCA5FA8C7F6E9530B9B900A6F111ED96715149C | COM/Jv/Jw/body Gram semantics |

