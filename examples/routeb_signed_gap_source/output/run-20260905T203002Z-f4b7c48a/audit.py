"""All-six-axis Gaussian-rational Fourier audit and signed endpoint enclosures.

Execute only via verify.py. No trajectories, floating tests, state writes,
source mutation, or force-budget regression. Decimal output is display only.
"""
import csv
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
from math import factorial
from pathlib import Path
import re

RUN = Path(__file__).resolve().parent
INPUTS = RUN/'inputs'
ZERO = (0,)*6


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def save(name, value):
    (RUN/name).write_text(json.dumps(value, default=str, indent=2)+'\n', encoding='utf-8')


def square_decomposition(matrix):
    """Exact indefinite rational square completion; no eigenvalue tolerance."""
    rest = [row[:] for row in matrix]
    terms = []
    while any(any(row) for row in rest):
        pivots = [i for i in range(6) if rest[i][i]]
        if not pivots:
            # Pure offdiagonal residual: 2bij zi zj = bij/2[(zi+zj)^2-(zi-zj)^2].
            for i in range(6):
                for j in range(i+1, 6):
                    b = rest[i][j]
                    if not b: continue
                    plus = [F(int(k == i or k == j)) for k in range(6)]
                    minus = [F(int(k == i)-int(k == j)) for k in range(6)]
                    terms.extend([(b/2, plus), (-b/2, minus)])
            break
        i = max(pivots, key=lambda k: abs(rest[k][k]))
        weight = rest[i][i]
        row = [x/weight for x in rest[i]]
        terms.append((weight, row))
        rest = [[rest[j][k]-weight*row[j]*row[k] for k in range(6)] for j in range(6)]
        assert all(x == 0 for x in rest[i])
    normalized = {}
    for weight, row in terms:
        first = next(x for x in row if x)
        row = tuple(x/first for x in row)
        normalized[row] = normalized.get(row, F(0))+weight*first**2
    terms = [(weight, row) for row, weight in normalized.items() if weight]
    rebuilt = [[sum(w*r[i]*r[j] for w,r in terms) for j in range(6)] for i in range(6)]
    assert rebuilt == matrix
    return terms


def main():
    manifest = json.loads((RUN/'before_run.json').read_text(encoding='utf-8'))
    assert 'audit.py' in manifest['snapshots']
    for name, entry in manifest['snapshots'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest() == entry['sha256']
    alg = module('snapshot_fourier', INPUTS/'inertial_audit.py')
    lin = module('snapshot_gain', INPUTS/'gain_audit.py')
    alg.SRC = INPUTS
    reference = json.loads((INPUTS/'reference.json').read_text(encoding='utf-8'))
    prefix = json.loads((INPUTS/'prefix_results.json').read_text(encoding='utf-8'))
    assert reference['status'] == 'EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    massrows = alg.rows('routeB_fourier_mass_full_rational.csv')
    crows = alg.rows('routeB_fourier_coriolis_rational.csv')
    urows = alg.rows('routeB_fourier_potential_rational.csv')
    assert len(massrows) == 610 and len(urows) == 17
    M = [[alg.load_poly([r for r in massrows if (int(r['row']),int(r['col'])) == (i+1,j+1)])
          for j in range(6)] for i in range(6)]
    def reality(p):
        assert all(p.get(tuple(-x for x in nu),(0,0)) == (a,-b) for nu,(a,b) in p.items())
    for i in range(6):
        for j in range(6):
            assert M[i][j] == M[j][i]
            reality(M[i][j])
    assert all(nu[0] == nu[5] == 0 for row in M for p in row for nu in p)
    U = alg.load_poly(urows)
    reality(U)
    mu = F(re.search(r'const MASS_REGULARIZER\s*=\s*([\deE.+-]+)',
                     (INPUTS/'dhport_lib.jl').read_text(encoding='utf-8'))[1])
    assert mu == F(1,1000000) == F(reference['mu'])
    M0 = [[sum(a for a,b in M[i][j].values())+mu*(i == j) for j in range(6)] for i in range(6)]
    H0 = [[sum(a for a,b in alg.diff(alg.diff(U,i),j).values()) for j in range(6)] for i in range(6)]
    assert M0 == [[F(x) for x in row] for row in reference['M0']]
    assert H0 == [[F(x) for x in row] for row in reference['H0']]
    assert all(sum(a for a,b in alg.diff(U,i).values()) == 0 for i in range(6))
    inverse = [[F(x) for x in row] for row in reference['M0_inverse']]
    assert lin.fmul(M0,inverse) == lin.eye(6) == lin.fmul(inverse,M0)
    acceleration = [[F(x) for x in reference['acceleration_q'][i]]+
                    [F(x) for x in reference['acceleration_v'][i]]+
                    [F(reference['acceleration_w'][i]),F(0)] for i in range(6)]
    nominal_force = [[-H0[i][j]-(F(reference['Kp'][i]) if i == j else 0) for j in range(6)]+
                     [-F(reference['D'][i])*(i == j) for j in range(6)]+[F(reference['G'][i]),F(0)] for i in range(6)]
    assert lin.fmul(M0,acceleration) == nominal_force
    A14 = [[F(x) for x in row] for row in reference['augmented_A14']]
    expected_A = lin.zeros(14,14)
    for i in range(6): expected_A[i][6+i] = F(1); expected_A[6+i] = acceleration[i]
    expected_A[12][13] = F(1)
    assert A14 == expected_A
    grouped = {}
    for r in crows:
        key = tuple(int(r[k])-1 for k in ('row','dq_j','dq_k'))
        assert all(0 <= i < 6 for i in key)
        grouped.setdefault(key,[]).append(r)
    Gamma = {}
    for i,j,k in itertools.product(range(6),repeat=3):
        source = alg.load_poly(grouped.get((i,j,k),[]))
        derived = alg.scale(alg.add(alg.diff(M[i][j],k),alg.diff(M[i][k],j),
                                   alg.scale(alg.diff(M[j][k],i),-1)),F(1,2))
        assert source == derived, ('CHRISTOFFEL_MISMATCH',i+1,j+1,k+1)
        reality(source)
        Gamma[i,j,k] = source
    assert sum(len(p) for p in Gamma.values()) == len(crows)
    assert all(Gamma[i,j,k] == Gamma[i,k,j] for i,j,k in Gamma)
    # Coefficientwise skew identity for the usual C-matrix, Cmat_ij=sum_k Gamma_ijk vk.
    for i,j,k in itertools.product(range(6),repeat=3):
        assert alg.add(Gamma[i,j,k],Gamma[j,i,k]) == alg.diff(M[i][j],k)
    triples = list(itertools.combinations_with_replacement(range(6),3))
    power_left = {triple:{} for triple in triples}
    power_right = {triple:{} for triple in triples}
    for i,j,k in itertools.product(range(6),repeat=3):
        triple = tuple(sorted((i,j,k)))
        power_left[triple] = alg.add(power_left[triple],Gamma[i,j,k])
        power_right[triple] = alg.add(power_right[triple],alg.scale(alg.diff(M[i][j],k),F(1,2)))
    assert power_left == power_right
    frequencies = sorted(set().union(*(p.keys() for p in power_left.values()),
                                     *(p.keys() for row in M for p in row)))
    power_checks = []
    for triple in triples:
        for nu in frequencies:
            a = power_left[triple].get(nu,(F(0),F(0)))
            b = power_right[triple].get(nu,(F(0),F(0)))
            assert a == b
            power_checks.append(dict(velocity_indices=[x+1 for x in triple],nu=nu,
                                     lhs_real=a[0],lhs_imag=a[1],rhs_real=b[0],rhs_imag=b[1]))
    save('power_coefficients.json',power_checks)
    with (RUN/'christoffel_full.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['row','dq_j','dq_k',*[f'nu{i}' for i in range(1,7)],'real_num','real_den','imag_num','imag_den'])
        for (i,j,k),p in sorted(Gamma.items()):
            for nu,(a,b) in sorted(p.items()):
                writer.writerow([i+1,j+1,k+1,*nu,a.numerator,a.denominator,b.numerator,b.denominator])
    print('EXACT full Christoffel:',len(Gamma),'entries,',len(crows),'source rows;',
          len(triples),'cubic monomials,',len(power_checks),'complex coefficient slots',flush=True)

    # Exact gravity sector, including the complete signed twist.
    u=(0,1,0,0,0,0);s=(0,1,1,0,0,0);x=(0,0,0,1,0,0);y=(0,0,0,0,1,0)
    sp=tuple(a+b for a,b in zip(s,y));sm=tuple(a-b for a,b in zip(s,y))
    ga,gb,gc=F(762237,200000),F(242307,200000),F(20601,400000)
    tx=alg.add(alg.const(1),alg.scale(alg.trig(x),-1))
    twist=alg.product(alg.trig(s,True),tx,alg.trig(y,True))
    gravity_expected=alg.add(alg.const(F(10791,4000)),alg.scale(alg.trig(u),ga),
                            alg.scale(alg.trig(s),gb),alg.scale(alg.trig(sp),gc),alg.scale(twist,gc))
    assert U == gravity_expected
    ps=alg.product(alg.trig(s),tx,alg.trig(y,True))
    px=alg.product(alg.trig(s,True),alg.trig(x,True),alg.trig(y,True))
    py=alg.product(alg.trig(s,True),tx,alg.trig(y))
    for i in range(6):
        assert alg.diff(twist,i) == alg.add(alg.scale(ps,s[i]),alg.scale(px,x[i]),alg.scale(py,y[i]))
    sinplus=alg.add(alg.trig(s,True),alg.trig(y,True))
    sinminus=alg.add(alg.trig(s,True),alg.scale(alg.trig(y,True),-1))
    assert twist == alg.scale(alg.mul(tx,alg.add(alg.mul(sinplus,sinplus),
                                       alg.scale(alg.mul(sinminus,sinminus),-1))),F(1,4))
    dM=[[alg.add(alg.const(M0[i][j]-mu*(i==j)),alg.scale(M[i][j],-1)) for j in range(6)] for i in range(6)]
    assert all(sum(a for a,b in p.values()) == 0 == sum(b for a,b in p.values()) for row in dM for p in row)
    # Complete Fourier-polynomial Sgap in original q,v coordinates.
    payload=[]
    for i in range(6):
        for j in range(i,6):
            factor=F(1,2) if i==j else F(1)
            for nu,(a,b) in sorted(alg.scale(dM[i][j],factor).items()):
                payload.append(dict(kind='v_quadratic',i=i+1,j=j+1,nu=nu,real=a,imag=b))
            if H0[i][j]:
                payload.append(dict(kind='q_quadratic',i=i+1,j=j+1,nu=ZERO,real=factor*H0[i][j],imag=F(0)))
    U0=sum(a for a,b in U.values())
    potential_gap=alg.add(alg.const(U0),alg.scale(U,-1))
    for nu,(a,b) in sorted(potential_gap.items()):
        payload.append(dict(kind='scalar',i=0,j=0,nu=nu,real=a,imag=b))
    save('Sgap_fourier_coefficients.json',dict(convention='coefficient*(q_i q_j or v_i v_j or 1)*exp(i nu.q); unordered i<=j, mixed factors already included',coefficients=payload))
    # Differentiate its kinetic coefficients: every acceleration/velocity coefficient and cubic term.
    differentiated_power={triple:{} for triple in triples}
    for i,j,k in itertools.product(range(6),repeat=3):
        triple=tuple(sorted((i,j,k)))
        differentiated_power[triple]=alg.add(differentiated_power[triple],alg.scale(alg.diff(dM[i][j],k),F(1,2)))
    assert all(differentiated_power[t] == alg.scale(power_left[t],-1) for t in triples)
    assert all(alg.diff(potential_gap,i) == alg.scale(alg.diff(U,i),-1) for i in range(6))
    # Full signed force ledger for 7x7 assembly: r0=dM*a0 + H0*q-grad U-C.
    residual=[]
    for i in range(6):
        for j in range(14):
            p=alg.add(*[alg.scale(dM[i][k],acceleration[k][j]) for k in range(6)],
                      alg.const(H0[i][j]) if j<6 else {})
            for nu,(a,b) in sorted(p.items()):
                residual.append(dict(row=i+1,kind='Y_linear',j=j+1,k=0,nu=nu,real=a,imag=b))
        for nu,(a,b) in sorted(alg.scale(alg.diff(U,i),-1).items()):
            residual.append(dict(row=i+1,kind='scalar',j=0,k=0,nu=nu,real=a,imag=b))
        for j in range(6):
            for k in range(j,6):
                p=alg.scale(Gamma[i,j,k],-1 if j==k else -2)
                for nu,(a,b) in sorted(p.items()):
                    residual.append(dict(row=i+1,kind='v_quadratic',j=j+1,k=k+1,nu=nu,real=a,imag=b))
    save('r0_fourier_coefficients.json',dict(convention='original physical force rows; Y=(q1..q6,v1..v6,w,c); mixed velocity factors included; eta excluded',coefficients=residual))

    # v=S*z with z=(v1,v2,v2+v3,v4,v5,v6). Group conjugates BEFORE completing squares.
    S=lin.eye(6);S[2][1]=F(-1)
    ST=list(map(list,zip(*S)))
    signed_modes=[]
    functionals=[];index={}
    def register(row):
        row=tuple(map(F,row))
        if row not in index: index[row]=len(functionals);functionals.append(row)
        return index[row]
    def phase(nu): return register(list(nu)+[0]*8)
    def coefficient_matrix(nu,part):
        original=[[M[i][j].get(nu,(F(0),F(0)))[part] for j in range(6)] for i in range(6)]
        return lin.fmul(lin.fmul(ST,original),S)
    modes=sorted({nu for row in M for p in row for nu in p if nu!=ZERO and next(t for t in nu if t)>0})
    decomposition_checks=0
    for nu in modes:
        entry=dict(nu=nu,phase=phase(nu))
        for label,part in (('cosine',0),('sine',1)):
            matrix=coefficient_matrix(nu,part)
            terms=square_decomposition(matrix)
            decomposition_checks+=36
            squares=[]
            for weight,row in terms:
                # z=T v, where T_32=1. This pullback is evaluated as one functional.
                original=list(row);original[1]+=row[2]
                squares.append(dict(weight=weight,z_row=row,velocity_functional=register([0]*6+original+[0,0])))
            entry[label]=dict(matrix_z=matrix,squares=squares)
            # Reconstruct the original complex kinetic coefficient, including origin cancellation.
            back=lin.eye(6);back[2][1]=F(1)
            reconstructed=lin.fmul(lin.fmul(list(map(list,zip(*back))),matrix),back)
            assert reconstructed==[[M[i][j].get(nu,(F(0),F(0)))[part] for j in range(6)] for i in range(6)]
        signed_modes.append(entry)
    # Check half dM equals the grouped real form entry by entry, including constant mode.
    for i in range(6):
        for j in range(6):
            grouped_gap={}
            for nu in modes:
                a,b=M[i][j].get(nu,(F(0),F(0)))
                grouped_gap=alg.add(grouped_gap,alg.scale(alg.add(alg.const(1),alg.scale(alg.trig(nu),-1)),a),alg.scale(alg.trig(nu,True),b))
            assert grouped_gap==alg.scale(dM[i][j],F(1,2))
    gravity_ids={name:phase(nu) for name,nu in [('u',u),('s',s),('x',x),('y',y),('s_plus_y',sp),('s_minus_y',sm)]}
    save('signed_square_decomposition.json',dict(velocity_coordinates=['v1','v2','v2+v3','v4','v5','v6'],
         formula='Sgap=sum_nu[(1-cos(theta))*sum cosine.weight*(z_row.z)^2 + sin(theta)*sum sine.weight*(z_row.z)^2] - A*Psi(u)-B*Psi(s)-Cg*Psi(s+y)-Cg*p',
         gravity=dict(A=ga,B=gb,Cg=gc,U_constant=F(10791,4000),U0=U0,
             Psi='z^2/2+cos(z)-1',p='sin(s)*(1-cos(x))*sin(y)',
             negative_twist_positive_part='Cg/4*(1-cos(x))*(sin(s)-sin(y))^2',
             negative_twist_negative_part='Cg/4*(1-cos(x))*(sin(s)+sin(y))^2'),modes=signed_modes))
    witnesses=[]
    for name,d in [('positive_gap',(0,0,1,2,-1,0)),('negative_gap',(0,1,0,0,0,0))]:
        quartic=-sum(a*sum(ni*di for ni,di in zip(nu,d))**4 for nu,(a,b) in U.items())/24
        remainder=sum(abs(a)*abs(sum(ni*di for ni,di in zip(nu,d)))**6 for nu,(a,b) in U.items())/720
        lower=quartic-remainder/F(400);upper=quartic+remainder/F(400)
        assert lower>0 if name=='positive_gap' else upper<0
        assert F(sum(di*di for di in d),400)<=F(9,400)
        witnesses.append(dict(name=name,q='t*d',v='0',d=d,range='0<abs(t)<=1/20',
                              Sgap_t4_coefficient=quartic,remainder_abs_le_coefficient_times_t6=remainder,
                              Sgap_over_t4_lower=lower,Sgap_over_t4_upper=upper))
    print('EXACT signed modes:',len(modes),'square factors:',sum(len(m[k]['squares']) for m in signed_modes for k in ('cosine','sine')),
          'linear functionals:',len(functionals),flush=True)

    # Targeted re-use of existing nominal + J support/kernel machinery, no force-budget rerun.
    save('functionals.json',dict(coordinates=['q1','q2','q3','q4','q5','q6','v1','v2','v3','v4','v5','v6','w','c'],rows=functionals,gravity_ids=gravity_ids))
    assert prefix['coordinate_order']==['q1','q2','q2+q3','q4','q5','q6','v1','v2','v2+v3','v4','v5','v6']
    strict=prefix['strict_prefix_cells']
    assert prefix['conditional_prefix_horizon']=='9/16' and len(strict)==72
    for i,cell in enumerate(strict):
        assert cell['cell']==i and list(map(F,cell['time']))==[F(i,128),F(i+1,128)]
        assert F(cell['derived_J_upper'])<F(cell['strict_barrier'])<=1
    Q=lin.zeros(6,6)
    for i,d in enumerate((F(3),F(8),F(95,7),F(165,7),F(45),F(90))): Q[i][i]=d
    Q[1][2]=Q[2][1]=F(-5)
    # Exact PSD factorization of Q's nontrivial 2x2 block validates scalar kernel positivity.
    assert Q[2][2]-Q[1][2]**2/Q[1][1]==F(585,56)>0
    h=F(1,128);degree=12;grid=lin.GRID
    def up(value,scale=10**12): return F(lin.ceil(value*scale),scale)
    def down(value): return -up(-value)
    E,ee,exp_receipt=lin.step_exponential(A14,h)
    series=[];power=lin.eye(14)
    for n in range(degree+1):
        series.append(lin.grid(power))
        if n<degree: power=lin.fscale(lin.fmul(power,A14),h/F(n+1))
    normh=lin.norm(A14)*h
    assert normh<degree+2
    tail=normh**(degree+1)/factorial(degree+1)/(1-normh/F(degree+2))
    rowgrids=[lin.grid([list(row)]) for row in functionals]
    kernel_integrals=[F(0)]*len(functionals)
    P,ep=lin.grid(lin.eye(14))
    supports=[];bounds=[]
    def apply(row,error,interval):
        uncertainty=error*max(max(abs(a),abs(b)) for r in interval for a,b in r)
        out=[]
        for j in range(14):
            low=high=0
            for k,c in enumerate(row):
                a,b=interval[k][j]
                low+=min(c*a,c*b);high+=max(c*a,c*b)
            out.append(((low-uncertainty)//grid,-((-(high+uncertainty))//grid)))
        return out
    def bound_from_radii(radii):
        kinetic_lo=kinetic_hi=F(0)
        mode_bounds=[]
        for mode in signed_modes:
            theta=radii[mode['phase']];co=min(F(2),theta**2/2);si=min(F(1),theta)
            caps={}
            for label in ('cosine','sine'):
                positive=sum(t['weight']*radii[t['velocity_functional']]**2 for t in mode[label]['squares'] if t['weight']>0)
                negative=sum(-t['weight']*radii[t['velocity_functional']]**2 for t in mode[label]['squares'] if t['weight']<0)
                caps[label]=(positive,negative)
            cp,cn=caps['cosine'];bp,bn=caps['sine']
            # One shared sine for the entire signed quadratic, hence max, not sum.
            sinecap=si*max(bp,bn)
            lo=-co*cn-sinecap;hi=co*cp+sinecap
            kinetic_lo+=lo;kinetic_hi+=hi
            mode_bounds.append([down(lo),up(hi)])
        g={name:radii[i] for name,i in gravity_ids.items()}
        psi=lambda z:min(z**4/24,z**2/2)
        sectors=ga*psi(g['u'])+gb*psi(g['s'])+gc*psi(g['s_plus_y'])
        cx=min(F(2),g['x']**2/2)
        # Signed difference of squares and the correlated phases s-y, s+y.
        twist_positive=gc*cx*min(F(1),g['s_minus_y']/2)**2
        twist_negative=gc*cx*min(F(1),g['s_plus_y']/2)**2
        direct=gc*cx*min(F(1),g['s'])*min(F(1),g['y'])
        lower=kinetic_lo-sectors-min(twist_negative,direct)
        upper=kinetic_hi+min(twist_positive,direct)
        return dict(lower=down(lower),upper=up(upper),kinetic_lower=down(kinetic_lo),kinetic_upper=up(kinetic_hi),
                    restoring_sector_upper=up(sectors),twist_positive_upper=up(min(twist_positive,direct)),
                    twist_negative_upper=up(min(twist_negative,direct)),mode_bounds=mode_bounds)
    initial_radii=[up(F(3,20)*lin.sqrtup(sum(c*c for c in row[:12]))) for row in functionals]
    initial_bound=bound_from_radii(initial_radii)
    # Whole-ball refinement exploits shared position/velocity radius for each mass term.
    # max a^2 b^2=r^4/4, max a b^2=2 r^3/(3 sqrt(3)), a^2+b^2<=r^2.
    initlo=inithi=F(0);rho=F(3,20)
    for mode in signed_modes:
        nn=sum(k*k for k in mode['nu'])
        sums={}
        for label in ('cosine','sine'):
            pp=nnn=F(0)
            for t in mode[label]['squares']:
                norm2=sum(c*c for c in functionals[t['velocity_functional']][6:12])
                if t['weight']>0: pp+=t['weight']*norm2
                else: nnn-=t['weight']*norm2
            sums[label]=(pp,nnn)
        cp,cn=sums['cosine'];bp,bn=sums['sine']
        co=F(nn)*rho**4/8
        si=lin.sqrtup(F(nn,3))*2*rho**3/3
        initlo-=co*cn+si*max(bp,bn);inithi+=co*cp+si*max(bp,bn)
    initial_bound['shared_ball_kinetic_lower']=down(initlo)
    initial_bound['shared_ball_kinetic_upper']=up(inithi)
    initial_bound['lower']=max(initial_bound['lower'],down(initlo-initial_bound['restoring_sector_upper']-initial_bound['twist_negative_upper']))
    initial_bound['upper']=min(initial_bound['upper'],up(inithi+initial_bound['twist_positive_upper']))
    for cell in range(128):
        polys=[lin.product(T,e,P,ep) for T,e in series]
        error=sum(e for T,e in polys)+lin.ceil(tail*(lin.norm(P)+ep))
        interval=[[(polys[0][0][i][j]+sum(min(0,T[i][j]) for T,e in polys[1:])-error,
                    polys[0][0][i][j]+sum(max(0,T[i][j]) for T,e in polys[1:])+error)
                   for j in range(14)] for i in range(14)]
        nominal=[];kernels=[]
        for i,(row,er) in enumerate(rowgrids):
            out=apply(row[0],er,interval)
            n2=F(sum(max(a*a,b*b) for a,b in out[:12]),grid**2)
            c=F(max(abs(out[13][0]),abs(out[13][1])),grid)
            nominal.append(up(F(3,20)*lin.sqrtup(n2)+lin.sqrtup(F(3))*c))
            z=out[6:12]
            cap=sum(Q[j][j]*max(a*a,b*b) for j,(a,b) in enumerate(z))-10*min(a*b for a in z[1] for b in z[2])
            assert cap>=0
            kernel_integrals[i]=up(kernel_integrals[i]+h*cap/grid**2)
            kernels.append(up(lin.sqrtup(kernel_integrals[i])))
        supports.append(dict(cell=cell,time=[cell*h,(cell+1)*h],nominal=nominal,kernel_sqrt= kernels,
                             transition_error=F(ep,grid)))
        cases={}
        for name,budget in [('nominal_J0',F(0)),('conditional_J1',F(1))]+(
                [('existing_strict_prefix',F(strict[cell]['strict_barrier']))] if cell<len(strict) else []):
            root=F(0) if budget==0 else up(lin.sqrtup(budget))
            radii=[up(n+k*root) for n,k in zip(nominal,kernels)]
            if name=='existing_strict_prefix':
                oldcaps=list(map(F,strict[cell]['actual_coordinate_caps']))
                for i,row in enumerate(functionals):
                    assert row[12]==row[13]==0
                    converted=list(row[:12]);converted[1]-=row[2];converted[7]-=row[8]
                    published=sum(abs(c)*r for c,r in zip(converted,oldcaps))
                    radii[i]=min(radii[i],published)
            result=bound_from_radii(radii)
            cases[name]=dict(J_cap=budget,**result)
        bounds.append(dict(cell=cell,time=[cell*h,(cell+1)*h],cases=cases))
        P,ep=lin.product(E,ee,P,ep)
        if (cell+1)%16==0: print('SIGNED_ENDPOINT_CELLS',cell+1,'/128',flush=True)
    save('nominal_J_functional_bounds.json',dict(formula='abs(ell.Y(t)) <= nominal[cell,ell] + kernel_sqrt[cell,ell]*sqrt(Jcap)',
         coverage='entire closed time cells, all full12 initial radius3/20 and c^2<=3, w0=0',
         step_exponential=exp_receipt,local_degree=degree,local_tail=tail,cells=supports))
    save('endpoint_bounds.json',dict(initial_ball=initial_bound,cells=bounds,
          premise='actual-nominal variation of constants with identical initial state and input; J bound on the current prefix; reference/source semantics; existing strict prefix needs all its original premises, including eta=0'))
    summary={}
    for name in ('nominal_J0','conditional_J1','existing_strict_prefix'):
        selected=[b for b in bounds if name in b['cases']]
        summary[name]=dict(horizon=selected[-1]['time'][1],
            uniform_lower=min(b['cases'][name]['lower'] for b in selected),uniform_upper=max(b['cases'][name]['upper'] for b in selected),
            final_cell_lower=selected[-1]['cases'][name]['lower'],final_cell_upper=selected[-1]['cases'][name]['upper'])
    result=dict(status='EXACT_ALL6_SIGNED_SOURCE_POWER_AND_CONDITIONAL_ENDPOINT_BOUNDS_PASS',
        arithmetic='Fraction and integer outward enclosures; floats only for terminal displays',
        full_mass_rows=len(massrows),full_coriolis_rows=len(crows),potential_rows=len(urows),
        christoffel_entries=216,christoffel_skew_velocity_coefficients=216,cubic_velocity_monomials=56,
        cubic_fourier_frequencies=len(frequencies),cubic_complex_coefficient_checks=len(power_checks),
        cubic_nonzero_rows=sum(len(p) for p in power_left.values()),
        signed_modes=len(modes),signed_square_matrix_entry_checks=decomposition_checks,
        square_factors=sum(len(m[k]['squares']) for m in signed_modes for k in ('cosine','sine')),
        exact_functionals=len(functionals),Sgap_coefficient_rows=len(payload),r0_coefficient_rows=len(residual),
        source_reference_M0_H0_inverse_A14_checks=True,constant_regularizer_cancels_from_gap=True,
        gravity_constants=dict(A=ga,B=gb,Cg=gc,U_constant=F(10791,4000),U0=U0),
        signed_gap_witnesses=witnesses,endpoint_summary=summary,initial_ball=initial_bound,
        endpoint_bounds_are_conditional=True,J1_proved=False,seven_by_seven_feasibility_proved=False,
        physical_DH_binding_proved=False,FD_Float64_binding_proved=False,Lean_verified=False,
        open_premises=['physical identification of Fourier mass/potential and analytic Christoffel force',
          'regularity, existence, and continuation through every required prefix',
          'same initial state/input and variation of constants with delta=a-a0',
          'strict prefix transfer requires its original mass lower bound and eta=0 idealization',
          'implementation/source defect eta enclosure counted exactly once',
          'actual full-horizon J<=1 is conditional here',
          'choose P,k,Z,b; certify assembled 7x7 matrix PSD on covered cells and storage/supply budget'],
        prohibited_actions_performed=False)
    save('audit_results.json',result)
    print(result['status'],flush=True)
    print('INITIAL SGAP',float(initial_bound['lower']),float(initial_bound['upper']),flush=True)
    for name,value in summary.items():
        print(name,'horizon',value['horizon'],'uniform',float(value['uniform_lower']),float(value['uniform_upper']),
              'last cell',float(value['final_cell_lower']),float(value['final_cell_upper']),flush=True)
    for name,entry in manifest['snapshots'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest()==entry['sha256']


if __name__=='__main__': main()
