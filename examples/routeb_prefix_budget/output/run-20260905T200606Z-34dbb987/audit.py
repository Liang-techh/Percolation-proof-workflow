"""Rational source-resolved, time-dependent conditional J-prefix audit.

No trajectories, float norms, or solver statuses. Whole initial ball, ramp
family and closed time cells. Physical/FD binding is explicitly NOT discharged.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import importlib.util
import json
import sys


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    run = Path(sys.argv[1]).resolve()
    inputs = run / 'inputs'
    lin = module('rational_gain', inputs / 'gain_audit.py')
    alg = module('fourier_algebra', inputs / 'inertial_audit.py')
    alg.SRC = inputs
    data = json.loads((inputs / 'reference.json').read_text(encoding='utf-8'))
    assert data['status'] == 'EXACT_COUPLED_NOMINAL_REFERENCE_PASS'
    cells, degree = 128, 12
    h, grid = F(1, cells), lin.GRID
    A = [[F(x) for x in row] for row in data['augmented_A14']]
    M0 = [[F(x) for x in row] for row in data['M0']]
    H0 = [[F(x) for x in row] for row in data['H0']]
    acc = [[F(x) for x in data['acceleration_q'][i]] +
           [F(x) for x in data['acceleration_v'][i]] +
           [F(data['acceleration_w'][i]), F(0)] for i in range(6)]
    records = alg.rows('routeB_fourier_mass_full_rational.csv')
    M = [[alg.load_poly([r for r in records if
          (int(r['row']), int(r['col'])) == (i+1, j+1)])
          for j in range(6)] for i in range(6)]
    for i in range(6):
        M[i][i] = alg.add(M[i][i], alg.const(F(data['mu'])))
    dM = [[alg.add(alg.const(M0[i][j]), alg.scale(M[i][j], -1))
           for j in range(6)] for i in range(6)]
    assert all(sum(a for a,b in p.values()) == 0 == sum(b for a,b in p.values())
               for row in dM for p in row)
    U = alg.load_poly(alg.rows('routeB_fourier_potential_rational.csv'))
    assert all(b == 0 for a,b in U.values())
    assert all(sum(a for a,b in alg.diff(alg.diff(U,i),j).values()) == H0[i][j]
               for i in range(6) for j in range(6))

    # Store each real linear functional ONCE. Combining mass columns BEFORE
    # taking absolute values retains inverse/acceleration cancellations.
    row_index, rows = {}, []
    def register(row):
        key = tuple(row)
        if key not in row_index:
            row_index[key] = len(rows)
            rows.append(list(row))
        return row_index[key]
    def unit(i): return [F(int(i == j)) for j in range(14)]
    coordinate = []
    for offset in (0,6):
        for i in range(6):
            row = unit(offset+i)
            if i == 2: row[offset+1] += 1  # q2+q3, v2+v3
            coordinate.append(register(row))
    phases = {}
    def phase(nu):
        if nu not in phases: phases[nu] = register(list(map(F,nu))+[F(0)]*8)
        return phases[nu]
    mass_modes = [[] for _ in range(6)]
    for i in range(6):
        modes = set().union(*(p.keys() for p in dM[i]))
        for nu in sorted(modes):
            # Origin cancellation gives cos(theta)-1 for the entire real map.
            real = [sum(dM[i][j].get(nu,(0,0))[0]*acc[j][k] for j in range(6)) for k in range(14)]
            imag = [sum(dM[i][j].get(nu,(0,0))[1]*acc[j][k] for j in range(6)) for k in range(14)]
            mass_modes[i].append((phase(nu),register(real),register(imag)))
    sub = {0:{0:F(1)},1:{1:F(1)},2:{2:F(1),1:F(-1)},
           3:{3:F(1)},4:{4:F(1)},5:{5:F(1)}}
    coriolis = [{} for _ in range(6)]
    for i in range(6):
        for j in range(6):
            for k in range(6):
                p = alg.scale(alg.add(alg.diff(M[i][j],k),alg.diff(M[i][k],j),
                          alg.scale(alg.diff(M[j][k],i),-1)),F(1,2))
                for a,ca in sub[j].items():
                    for b,cb in sub[k].items():
                        pair = tuple(sorted((a,b)))
                        coriolis[i][pair] = alg.add(coriolis[i].get(pair,{}),alg.scale(p,ca*cb))
        coriolis[i] = {pair:p for pair,p in coriolis[i].items() if p}
        for p in coriolis[i].values():
            assert sum(b for a,b in p.values()) == 0
            for nu in p: phase(nu)
    for nu in U: phase(nu)
    rowgrids = [lin.grid([row]) for row in rows]
    E,ee,exp_receipt = lin.step_exponential(A,h)
    series, power = [],lin.eye(14)
    for n in range(degree+1):
        series.append(lin.grid(power))
        if n < degree: power = lin.fscale(lin.fmul(power,A),h/F(n+1))
    a = lin.norm(A)*h
    tail = a**(degree+1)/factorial(degree+1)/(1-a/F(degree+2))
    assert a < degree+2
    P,ep = lin.grid(lin.eye(14))
    kernels = [F(0)]*len(rows)
    cache = []
    diag = [F(3),F(8),F(95,7),F(165,7),F(45),F(90)]
    def up(x, scale=10**12): return F(lin.ceil(x*scale),scale)
    def apply_row(c, ce, interval):
        # c/grid approximates the exact functional with l1 error ce/grid.
        error = ce*max(max(abs(lo),abs(hi)) for r in interval for lo,hi in r)
        out = []
        for j in range(14):
            terms = [(v*interval[k][j][0],v*interval[k][j][1]) for k,v in enumerate(c)]
            low = sum(min(x,y) for x,y in terms)-error
            high = sum(max(x,y) for x,y in terms)+error
            out.append((low//grid,-((-high)//grid)))
        return out
    def nominal(row):
        n2 = F(sum(max(x*x,y*y) for x,y in row[:12]),grid**2)
        cc = F(max(abs(row[13][0]),abs(row[13][1])),grid)
        return up(F(3,20)*lin.sqrtup(n2)+lin.sqrtup(F(3))*cc)
    def kernel2(row):
        z = row[6:12]
        cap = sum(d*max(x*x,y*y) for d,(x,y) in zip(diag,z))
        cap -= 10*min(x*y for x in z[1] for y in z[2])
        assert cap >= 0
        return cap/grid**2
    print('FUNCTIONALS',len(rows),'WHOLE_TIME_CELLS',cells,flush=True)
    for cell in range(cells):
        polys = [lin.product(T,e,P,ep) for T,e in series]
        error = sum(e for T,e in polys)+lin.ceil(tail*(lin.norm(P)+ep))
        interval = [[(polys[0][0][i][j]+sum(min(0,T[i][j]) for T,e in polys[1:])-error,
                      polys[0][0][i][j]+sum(max(0,T[i][j]) for T,e in polys[1:])+error)
                     for j in range(14)] for i in range(14)]
        noms,ks = [],[]
        for i,(cs,ce) in enumerate(rowgrids):
            row = apply_row(cs[0],ce,interval)
            kernels[i] = up(kernels[i]+h*kernel2(row))
            noms.append(nominal(row));ks.append(up(lin.sqrtup(kernels[i])))
        cache.append((noms,ks))
        P,ep = lin.product(E,ee,P,ep)
    def forcing(cell, budget):
        noms,ks = cache[cell]
        root = up(lin.sqrtup(budget))
        radii = [up(n+k*root) for n,k in zip(noms,ks)]
        theta = {nu:radii[idx] for nu,idx in phases.items()}
        velocity = [radii[i] for i in coordinate[6:]]
        parts = []
        for i in range(6):
            mc = sum(min(F(2),radii[p]**2/2)*radii[r]+min(F(1),radii[p])*radii[b]
                     for p,r,b in mass_modes[i])
            cc = F(0)
            for (v,w),poly in coriolis[i].items():
                center = sum(a for a,b in poly.values())
                variation = sum(abs(a)*min(F(2),theta[nu]**2/2)+abs(b)*min(F(1),theta[nu])
                                for nu,(a,b) in poly.items())
                total = sum(abs(a)+abs(b) for a,b in poly.values())
                cc += min(total,abs(center)+variation)*velocity[v]*velocity[w]
            gc = sum(abs(a*nu[i])*min(theta[nu]**3/6,theta[nu]+1) for nu,(a,b) in U.items())
            parts.append((up(mc),up(cc),up(gc)))
        caps = [sum(part) for part in parts]
        # The positive absolute cross term is deliberately an upper envelope,
        # NOT a claim that the exact signed Q term has changed.
        Qcap = up(sum(d*r*r for d,r in zip(diag,caps))+10*caps[1]*caps[2])
        return Qcap,parts,radii
    fixed = []
    for budget in (F(0),F(1,20),F(1,4),F(1)):
        bounds = [forcing(i,budget)[0] for i in range(cells)]
        integrated = sum(bounds)*h
        fixed.append(dict(hypothetical_J_cap=str(budget),Q_r_integral_upper=str(integrated),
                          display=float(integrated),strict_bootstrap_gate=integrated<budget,
                          per_cell_Q_upper=list(map(str,bounds))))
        print('HYPOTHETICAL_J',str(budget),'CONDITIONAL_FORCE_BUDGET_UPPER',float(integrated),flush=True)

    # Prefix induction uses a strict first-exit inequality on each whole cell.
    # A failed sufficient gate is NOT evidence of an unsafe actual trajectory.
    previous = F(0)
    prefix,failed = [],None
    for cell in range(cells):
        candidate = max(previous+F(1,10**8),previous*F(6,5))
        passing = None
        while candidate <= 1:
            rhs = previous+h*forcing(cell,candidate)[0]
            if rhs < candidate:
                passing = candidate
                break
            candidate = max(candidate*F(3,2),up(rhs*F(101,100)))
        if passing is None:
            failed = dict(cell=cell,time=[str(cell*h),str((cell+1)*h)],previous_bound=str(previous),
                          attempted_candidate=str(candidate),reason='no tested strict scalar enclosure below J=1')
            break
        lo,hi = previous,passing
        for _ in range(10):
            mid = (lo+hi)/2
            if previous+h*forcing(cell,mid)[0] < mid: hi = mid
            else: lo = mid
        new = up(hi)
        # Rounding changes the right hand side too: re-evaluate the gate.
        rhs,parts,radii = forcing(cell,new)
        assert previous+h*rhs < new
        prefix.append(dict(cell=cell,time=[str(cell*h),str((cell+1)*h)],
                           previous_J_upper=str(previous),strict_barrier=str(new),
                           derived_J_upper=str(previous+h*rhs),Q_r_upper=str(rhs),
                           r_parts_mass_C_gravity=[[str(x) for x in part] for part in parts],
                           actual_coordinate_caps=[str(radii[i]) for i in coordinate]))
        previous = up(previous+h*rhs)
    result = dict(status='RATIONAL_CONDITIONAL_PREFIX_SOURCE_ENVELOPE_AUDIT',
        initial_class='full12 Euclidean radius3/20, w=c*t, c^2<=3, T=1',
        fixed_hypothetical_caps=fixed,strict_prefix_cells=prefix,first_unclosed_cell=failed,
        conditional_prefix_horizon=str(len(prefix)*h),conditional_J_upper=str(previous),
        full_horizon_analytic_budget_closed=len(prefix)==cells,
        actual_DH_J_proved=False,physical_FD_Float64_binding=False,Lean_verified=False,
        formal_certificate_allowed=False,eta_assumed_zero_for_this_analytic_audit=True,
        exact_functionals=len(rows),time_cells=cells,local_degree=degree,
        step_exponential=exp_receipt,coordinate_order=['q1','q2','q2+q3','q4','q5','q6',
                                                      'v1','v2','v2+v3','v4','v5','v6'],
        warning='Failure concerns this sufficient scalar envelope, not the physical target. Prefix entries require actual-nominal variation of constants, M>=L, analytic Fourier source, regularity and identical initial/input. No source implementation or registry admission.',
        input_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir() if p.is_file()})
    (run/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('CONDITIONAL_PREFIX_HORIZON',result['conditional_prefix_horizon'],'J_UPPER',float(previous))
    print('ACTUAL_DH_J_PROVED=false')


if __name__ == '__main__': main()
