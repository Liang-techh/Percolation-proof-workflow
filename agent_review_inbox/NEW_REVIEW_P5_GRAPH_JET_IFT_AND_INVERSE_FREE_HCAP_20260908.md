---
kind: review_result
review_id: NEW_REVIEW_P5_GRAPH_JET_IFT_AND_INVERSE_FREE_HCAP_20260908
task_id: P5-GRAPH-JET-IFT-INVERSE-FREE-HCAP
agent: Sartre
status: CONDITIONAL_MATH_LEAVES_DERIVED_SOURCE_CERTIFICATES_PENDING
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# G0/G1 的下一叶：block-triangular IFT 与 inverse-free H-cap

本轮读取现有提取器、graph-jet review，以及真实 first-slab checker 的字段接口；
不重跑 checker/提取器、不生成 alpha/Y、不运行 Lean。仅新增本 immutable review。

实际增量是两个明确的数学叶：

1. 84维 graph 的未知量 Jacobian 有14个同源 M 对角块，其 determinant 为(det M)^14；
   G0/G1本身不能反推 M 可逆。
2. additive H-cap 可用一个7x7矩阵正性证书加 G0 的 exact ideal multiplier
   证明，无须展开 M^-1，也无须先求 alpha/Y 数值。

## A. 固定原 source jet，不能从 graph 方程倒推可逆

继续使用 z=(q,v,w)∈R13、alpha∈R6、Y=[Y_1,...,Y_13]∈R6x13：

```
G0 = M alpha - R
G1_k = M Y_k - R_k + M_k alpha
```

其中 R_k=∂_kR，M_k=∂_kM；速度/输入七个方向的M_k为零。
角度方向必须是物理pullback导数。所有项均取同一z、同一cell/source身份。

逻辑否证（不是机器人反例或伪造alpha值）：若 M 有非零核向量 n，
只要某个G0/G1联合解存在，固定alpha并将任一列Y_k替换为Y_k+t*n，
对所有t仍满足相同G0/G1。因此联合graph方程不蕴含Y唯一，更不蕴含M可逆。
若graph无解，graph上的全称不等式还可能只是空集真。
这说明 invertibility/totality 是必需证据，不能由“方程已写出”替代。

## B. 84维 Jacobian 的结构证书

将未知量按 u=(alpha,Y_1,...,Y_13) 排列。对u求导得到：

```
             alpha  Y1    Y2   ... Y13
G0              M    0     0        0
G1_1           M1    M     0        0
G1_2           M2    0     M        0
 ...           ...
G1_13         M13    0     0        M
```

这是 block lower triangular 84x84 矩阵，14个6x6对角块全部是同一M。
因此 det(D_u G)=(det M)^14。M_k的复杂度不影响未知量方向可逆性。
该等式是有限维代数结构，不需要把巨大84x84 determinant展开成多项式。
未来证书字段只需 variable/block ordering、各块 equality、block determinant theorem。

正则性必须分层：

- 若M,R为C1且M可逆，对G0做IFT得到alpha为C1；再微分G0并用M可逆，确认Y=Dalpha。
  此时Y通常只保证连续，不应无条件宣称Y为C1。
- 若要对整个G0/G1联合系统直接使用C1 IFT，M_k/R_k也必须C1，故需要M,R至少C2。
  对当前有限有理多项式与sin/cos pullback，数学表示本身C∞，可以提供这一叶；
  但仍须绑定到实际CSV evaluator和选定analytic source，而不是Float64执行。

存在性不用数值见证：M可逆给每点G0唯一线性解，随后每列G1唯一线性解。
局部IFT分支由唯一性拼合。这是有限维数学论证，不是本轮已完成的kernel证据。

## C. 现有同cell invertibility字段如何接上（不重做旧审计）

外部 E=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`。
已读取 E/robot_formal_v1/exact_checks/check_initial_analytic_slab.py:27–47。
现有 vanis2 cell 的可用候选字段为 source_hashes、mass_intervals、preconditioner X、
contraction_matrix C、weights、kappa。这里仅指定需要转化的 theorem premise：

`forall q in cell, ||I-X*M(q)||_weights <= kappa < 1`。

该同源uniform premise一旦认证，即可用已有线性可逆性接口输入B节；本轮不重新
计算/优化它，也不从 historical Python pass 宣称当前source theorem已认证。
必须补的字段是：

1. exact M与mass_intervals的函数包含证明，含regularizer和物理lift域；
2. X、C、positive weights、strict gap及它们与本轮系数表/同cell的身份；
3. 对应线性可逆性定理实例的证据引用；
4. cell边界附近的source光滑延拓。

正则性无需先重新找一整块更大的数值box：M连续使
U={z:det M(q)≠0}为开集。若cell上可逆已证，则cell⊂U。
有限多项式/trig表达式在U上C∞，足够定义邻域graph和导数。
若需要统一邻域半径或导数上界，才另补定量margin/邻域覆盖；不能把本条定性
开集结论包装成带数值半径或trajectory coverage的证据。

## D. 同graph additive H-cap 的7x7证书

固定真实port表达式 d=L(z)alpha+d0(z)，维数m（block456时m=3）；
H(z)=H(z)^T∈Rmxm为实际consumer metric，Delta(z)为标量cap。
L、d0、H、Delta必须来自同source/同状态，不能由此设计自动取得。
尤其d0不能默认为0。

选择一个对称6x6 multiplier Q(z)。定义7x7 symmetric matrix：

```
K(z) = [ M^T Q M - L^T H L          -L^T H d0
         -d0^T H L             Delta - R^T Q R - d0^T H d0 ]
```

对任意alpha，有 exact identity：

```
Delta - (L alpha+d0)^T H (L alpha+d0)
 = [alpha;1]^T K [alpha;1]
   - (M alpha-R)^T Q (M alpha+R).
```

Q对称保证最后一项等于(Malpha)^TQ(Malpha)-R^TQR，交叉项精确抵消。
因此若在同cell上K(z) PSD，则在G0=0的真实唯一graph上立即有 d^THd≤Delta。
Q本身不必PSD；必须对称，真正要认证的是K PSD。
这是一条充分条件，不宣称对固定多项式Q/Delta的参数化必要，也不承诺存在可行Q。
无 inverse entries、无alpha/Y数值、无方向采样；Y不需要进入幅值cap证书。

若H/Delta/Q是有理函数，先记录所有denominators及正的clearing factors；
不得不分符号清分母。若是有理多项式，可给K的matrix-SOS域证书或exact PSD factor：
系数恒等式、Gram/LDL数据、box/circle约束与domain包含证明均需实际提供。
仅打印“K PSD”或局部PSD数值不构成certificate。

也可直接提交更一般的graph ideal positivity witness。上面的identity只是一个
小而显式的模板，不要求下游一定用这7x7充分条件，不新增任何实际bound数值。

## E. 接 additive consumer 的精确边界

令实际signed residual分解为 l_actual=v_ref+d，
P_actual=beta-l_actual^T H l_actual。需另外证明linear metric transport T满足
sq(Tu)=u^THu，统一作用于baseline、port、total。
然后已有GenericSchurAllocation20260908.combined_of_port_budget取：

```
ell=T v_ref, r=T d, scalar-cap W=Delta, base=beta, lam>1
(lam-1)*(beta-target-lam*Delta)-lam*v_ref^T H v_ref >= 0
```

D节给hport，最后一行给halloc，才得到target≤P_actual。
不删除additive偏置，不将scalar W与P5 moving metric混同；allocation与实际
P_actual身份不由graph可逆性/IFT产生。

对于真实solve defect M alpha=R+z_defect，D节原certificate不能直接使用：
必须将R一致地替换成R+z_defect并保留其source/cap；Y方程还要加入Dz_defect。
若z_defect不具备C1 source map，不能直接套B节IFT。不得为闭环设它为零。

## F. 当前完成与下一最小对象

已经设计的数学叶：G0/G1非空/唯一所需条件、84维block-Jacobian结构、C1/C2分层、
同cell开域处理、7x7 H-cap multiplier identity和现有additive consumer的接线。
未提供实际source证书：invertibility实例、coefficient-to-source equality、
L/d0/H真实定义、Q/Delta及K的同域PSD证据、allocation、时间/输入律/coverage。

下一最小交付应是一份同cell证书bundle，明确绑定：

`jet_digest + cell_hash + invertibility_witness + regularity/source_identity`

并在已选实际port/metric后补：

`L,d0,H,Delta,Q + exact K identity + cell PSD witness + consumer allocation`。

不能在L/d0/H未绑定时先求一个synthetic Q并宣布pass。无需先给alpha/Y样本。
W/Wt/DW、b/Db/e只在实际P5 source声明后另接；上述port H-cap不是这些字段的替代。

读取时提取器SHA仍为
3BD8AC1D468B6F73A5FF230F031CE3D38315B608C90AB0381762054BF0C5A6AE。
本轮未重验上轮coefficient digest、未运行外部脚本或Lean；所有source/admission字段pending。
没有修改state、registry、formal gate、旧review或任何外部项目文件。
