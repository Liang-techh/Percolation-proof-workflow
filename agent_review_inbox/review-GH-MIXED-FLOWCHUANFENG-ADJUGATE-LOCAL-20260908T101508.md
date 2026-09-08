---
kind: review_result
review_id: review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-LOCAL-20260908T101508
task_id: GH-MIXED-FLOWCHUANFENG-ADJUGATE
source_agent: Codex-source-witness-only
created_at: "2026-09-08T10:15:08-06:00"
inspected_commit_start: 218f8f45a05b4146951810d99e6ce6fb3badb825
inspected_commit: 90c7e1077f0eae25326bf7d0d6491fcfb8891650
integration_status: pending
admission: pending
admission_label: pending
merge_decision: refuse_source_witness_merge
merge_allowed: false
source_binding_proven: false
actual_same_cell_evidence_constructed: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
proof_status: MISSING_SAME_SOURCE_WITNESS_WITH_EXACT_CANDIDATE_ROW_OBSTRUCTION
requested_action: retain this obstruction review only; do not merge the located artifacts as a source-bound adjugate packet
---

# Flowchuanfeng adjugate handoff — source witness merge refused

## Disposition

**拒绝把当前候选合并为 signed projected-adjugate source witness。**
允许保留本 review 作为 obstruction 记录，不等于允许 source packet 或 registry admission。
缺少真实 witness 与“数学命题为假”不同：此处是证据/对象接线失败，
不是宣称实际机器人加速度无界。

本轮不重复 source-independent Cramer、分母消去或 cancellation family 的证明。
只追踪实际 source、现有 payload、当前 restriction adapter 与同域对象身份。
只新增此 immutable review_result，不修改旧文件、state、registry 或共享脚本。

## 1. 最新候选链的核查结果

保留最新 source lane 已选的 principal restriction，不再另选 domain 或 Schur 路线。
外部根 P 的精确路径为：

    C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized

既有 full-state 候选
P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json
给出角半径 (9/20,19/50,37/100,19/50,37/100,9/20)、逐分量速度半径3、
|w|≤2（scope）、step=1/512。status=RATIONAL_FIRST_NONLINEAR_SLAB、
formal=false。不把历史 analytic slab 当成已认证实际 source/轨迹域。

本轮 fresh 读取/解析显示：

| 当前对象 | 确有内容 | 不能作为的 witness |
|---|---|---|
| force_balance_bridge_dh_v1.json | DH gains、rows=[4,5]、epsilon=1/1000000；X 预条件后的 centered split；a=A*x+delta_a | 实际物理两行成立、signed projected numerator enclosure |
| preconditioned_force_balance_identity_dh_v1.json | 两个 row record，row=4/5；X*((M+epsilon I)*a−tau_DH+C*dq+G)=0 的 support | 未预条件 symmetric 2x2 source row；det(S) 或 observable |
| half_active domain JSON | 6x6 rational preconditioner X、analytic domain/candidate bounds | 实际 acceleration valuation、runtime defect 或固定 observable |
| NEW_PRINCIPAL_RESTRICTION_20260908.lean | 接收三条 heq 前提，保留第3列耦合的纯有限和接口 | 真实 heq inhabitant；自动 source coordinate map |
| NEW_P4_032_AdjugateAcceleration.lean | SameCellEvidence 五项参数及消费者 | 新的 source 实例 |

force_balance_bridge_dh_v1.json 的 unresolved_obligations 明确包括：
“substitute the physical acceleration lift into A*x and delta_a”、
“prove the equality-ideal bridge in Fourier variables”、
DH energy/port-IQC positivity 与 finite-time flowpipe。
这些不是本轮推测；不能在接入 packet 时删掉前两项。

两个 force payload 的 source_hashes 指向当前 half_active domain 与 dhport 字节；
本轮核对这两个引用值与 fresh SHA 一致。这只是直接字节关联，
不认证历史生产器、完整依赖闭包、源语义或 interval correctness。

最新 HALF-ACTIVE source review 已指出 controller chart correction 与
actual balance/FD/runtime defect 尚未完成。本轮使用其明确的 missing-witness
结论作追踪，不重新推导 controller 差值，也不重复已有 Cramer 工作。

## 2. 新的精确 obstruction：当前两条 preconditioned 行不足以恢复物理行

不仅“可能缺 inverse”：当前保存的 X 本身就给出一个可审阅线性代数反例。
以下索引为物理一基 1..6，X 为上述哈希绑定 domain JSON 的 preconditioner。

令

    A=X41, B=X42, C=X51, D=X52,
    d=A*D−B*C.

一次只读 Python Fraction 检查解析 X 的全部6x6有理项，得到 d<0，故 d≠0。
不输出巨大分数的十进制近似；其精确值由四个已固定 JSON rational token
及此公式唯一决定。再构造

    z1=(B*X54−D*X44)/d,
    z2=(C*X44−A*X54)/d,
    z3=0, z4=1, z5=0, z6=0.

同一次 exact rational 检查验证

    (X*z)4=0, (X*z)5=0, 但 z4=1.

因此，对当前 X，两个 preconditioned residual 行为零 **不能单独推出**
物理 residual 第4行为零，遑论填好 packet 的两个实际 row witness。
等价地，若用这两行的线性组合恢复 e4^T，消掉第1/2列会迫使组合系数全零，
与第4坐标应为1矛盾。

这个 z 是当前候选 X 的代数残差测试向量，不声称它是任何机器人状态下的
实际残差，也不声称它满足额外未提供的 source constraints。
若后续给出真实 residual 的额外约束，它们可能排除 z；
但必须提交这些约束，不能由两个当前行记录推定。

Fraction 检查不是 Lean/kernel 证明，也没有认证 JSON 的 X 就是历史/运行时 X。
它足以否定“仅靠当前两条 X-row 就可无条件恢复物理两行”的候选合并理由。
未生成额外脚本、packet、bound 或测试输出文件。

## 3. 固定同源对象：不再拼接不同 residual/metric/observable

以所选 analytic DH chart 表示单次 source acceleration ahat，且实际等式仍待证明：

    M_A*ahat=F_DH_analytic+e_DH.

M_A 含且只含一次相同 regularizer。
principal restriction 固定 B=(4,5)、E=(1,2,3)，保留 joint6：

    S=(M_A)_BB,
    u=(ahat4,ahat5),
    f=(F_DH_analytic+e_DH)_B
       −(M_A)_BE*ahat_E−(M_A)_B6*ahat6.

actual rows4/5 若直接证明即可使用此入口，不必为了两行 restriction 强求 row6；
但不得把缺少的耦合置零，也不得声称已经得到三行/Schur 消元 witness。
当前 restriction adapter 自身的 heq 输入并未提供这些实际行。

须从这个**同一** S、f、状态、cell 和 fixed observable covector ell 形成：

    determinant = det(S),
    signed numerator = ell^T adj(S) f,
    observable acceleration = ell1*ahat4+ell2*ahat5.

以下替换一律拒绝：
- origin determinant、mass-Schur pivot 或3x3 determinant 冒充 det(S(x))；
- preconditioned support、port norm cap 或6维 acceleration remainder 冒充 |Ntheta|；
- lBase nominal residual 向量冒充 affine observable 的 covector ell；
- analytic force、FD force、runtime solve 的误差项未绑定即相互替换；
- 两条 X-row 的“identity”标签冒充未预条件实际方程；
- 不同 cell 的 delta/R 或不同 normalization 的 det/numerator 混合。

保留 cancellation 的最小要求是：在完整 f（包括 retained coupling 与完整 defect）
上先做 signed adjugate contraction，再对整个 scalar Ntheta enclosure。
在任一内部阶段先丢符号、分拆所有独立绝对值再合并，虽然可能给更松的有效上界，
却不能宣称保留原 cancellation；也不能拿旧零 numerator 覆盖新增实际 defect。
不重复已有 cancellation family。

## 4. Exact missing-witness contract 与 reopen 条件

同一个非空、已标识的 source cell 上，至少还需：

1. **实际 row witness：** source/config与actual acceleration的解释，加上
   S*u=f 的两条物理等式；可由足够的 full residual evidence 加合法 row recovery
   得到。现在的两个 X-row 不足，见第2节。
2. **同一 denominator witness：** 对此 S 的正有理 delta 与逐点 delta≤det(S)。
   单个原点矩阵/其他块/其他 cell 的数值不可代用。
3. **signed observable numerator witness：** 冻结 ell、同一 f 与 source valuation，
   对完整 ell^T adj(S)f 提供有理 R 的 enclosure，包含必要 FD/model/solve terms。
4. **observable witness：** 实际 fixed affine observable、坐标/时间单位、
   二阶导数与 source acceleration 绑定；不能只新填一个独立 observable 函数字段。
5. **packet gate：** 同一 delta,R,A 满足 delta>0、R≤delta*A；
   若提出全域/trajectory结论，再补 cover/inclusion/containment。

这里没有发明 delta、R、A，也没有通过定义 synthetic src 来填空。
界、源等式、编译证据与 registry admission 四层仍独立。
即使 source-independent consumer 或 restriction adapter 后来有编译结果，
也不能填上述未提供的 source 前提。

**结论：未找到可接收的真实 same-source packet；merge_allowed=false。**
只有收到以上实际证据才重新审查；本 review 可作为阻塞说明入档，
不可作为 source binding 完成项或 registry promotion 依据。

## 5. Exact paths / fresh SHA-256 / audit scope

下表 W=当前 workspace 根
C:/Users/z5242/Desktop/重构版/工作流；
P=第1节外部根。前缀与相对路径拼接唯一确定绝对路径。

| 路径 | SHA-256 |
|---|---|
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean | A39485ADEA19FFD31A2F46A9B6CF0160D888D08CA36C64F4D0E9461FB406B616 |
| W/examples/routeb_p4_3d_to_2d_restriction_lean/NEW_PRINCIPAL_RESTRICTION_20260908.lean | 1D93E5DB2EA613B1F2AAACB6D84AA9613374C62CF3A147CD1B61D8A15A106DC4 |
| W/agent_review_inbox/review-GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE-LOCAL-20260908T160907Z.md | 2D1C6AB7031791661132A1363C3BCBED6C62E3EC0BE2262EB1C813F7EFBE4126 |
| P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| P/robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json | 3045EA1923148C90C8473C8402C7522E99EEDA2C1590A494322CA3950D76A107 |
| P/robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | E0969AADE062FE7C7648A655EA95282E8FD27F9EB7D47C3FFC1B38E33C920F48 |
| P/routeB_dense_Mq/dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |

还完整读取当前 ACTUAL-CELL-PACKET 与 ACTUAL-THREE-ROW-WITNESS reviews 用于定位；
其 source 结论通过上述 payload 的有限元数据/引用检查重新定位，不据旧 review
宣称任何新 source theorem。

检索范围：workspace examples/agent_review_inbox/artifacts 的相关 Lean/JSON/review
符号，以及 P/robot_formal_v1/interval_bounds、P/routeB_dense_Mq 的对应 JSON/packet/witness
字段。未找到完整 packet 仅限此范围。大型 force payload 的最初全文输出被截断；
本轮只审计随后结构化读取的元数据、obligation、hash 引用与上述 X，未审计全部多项式项。

仅运行只读文本/JSON/SHA 与一次有针对性的 Fraction 检查。
无 Lean/Lake、Julia、source producer、全回归或 admission/ingestion。
起始已观察到 state.json、共享脚本与其他 lane 的并发变更；本轮未写入/恢复这些文件。

