"""Rational source-coefficient bounds on an explicit candidate pre-exit box.

No trajectory is generated or asserted to lie in this box. The full initial
ball is covered, but flow invariance is a separate, open obligation.
"""
import importlib.util
import json
import hashlib
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
STRUCTURE=HERE.parent/'routeb_inertial_structure'
spec=importlib.util.spec_from_file_location('inertia_audit',STRUCTURE/'audit.py')
algebra=importlib.util.module_from_spec(spec)
spec.loader.exec_module(algebra)


def decode(rows):
    return {tuple(row['nu']):(Q(row['real']),Q(row['imag'])) for row in rows}


def absolute_bound(poly,X,Y):
    """Complex triangle plus |exp(it)-1|<=min(2,|t|), exact rational ledger.

    Group remote modes first, so cancellations at q4=q5=0 are retained.
    Neither remote angles nor q1/q6 are frozen. Norm(c)<=|Re c|+|Im c|.
    """
    grouped={}
    variation=Q(0)
    global_bound=Q(0)
    for nu,(a,b) in poly.items():
        key=(nu[0],nu[1],nu[2],nu[5])
        ca,cb=grouped.get(key,(Q(0),Q(0)))
        grouped[key]=(ca+a,cb+b)
        size=abs(a)+abs(b)
        global_bound+=size
        variation+=size*min(Q(2),abs(nu[3])*X+abs(nu[4])*Y)
    centered=sum(abs(a)+abs(b) for a,b in grouped.values())+variation
    return min(global_bound,centered)


def rewritten_transport(data):
    # Actual v3=V-v2, V=v2+v3. Combine exact polynomial coefficients BEFORE
    # any absolute value so the principal remote cancellation survives.
    sub={0:{0:Q(1)},1:{1:Q(1)},2:{2:Q(1),1:Q(-1)},
         3:{3:Q(1)},4:{4:Q(1)},5:{5:Q(1)}}
    out={4:{},5:{}}
    for key,rows in data['half_kinetic_block_derivative'].items():
        axis=int(key[1]); j=int(key.split('_v')[1].split('v')[0])-1
        ell=int(key.rsplit('v',1)[1])-1
        poly=decode(rows)
        for a,ca in sub[j].items():
            for b,cb in sub[ell].items():
                pair=tuple(sorted((a,b)))
                out[axis][pair]=algebra.add(out[axis].get(pair,{}),algebra.scale(poly,ca*cb))
    return {i:{p:c for p,c in entries.items() if c} for i,entries in out.items()}


def main():
    path=STRUCTURE/'audit_results.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data['status']=='EXACT_MBD_AND_CHRISTOFFEL_IDENTITIES_VERIFIED'
    transport=rewritten_transport(data)
    # Candidate support: |q4|,|q5|<=2/5; velocities (v1,v2,V,v4,v5,v6).
    X=Y=Q(2,5)
    radii=[Q(3,5),Q(5,2),Q(2),Q(4,5),Q(4,5),Q(2,5)]
    A0,m,J,k,b,d,j,e=[Q(data['constants'][s]) for s in ('A0','m','J','k','b','d','j','e')]
    F=A0+k*Y**2+Y*(d+e+b+k+j*X)
    f=X*Y*(b+k)
    h=(m+b+d+e)*X+2*j
    g=m+b
    sigma4=k*Y**2*radii[3]+F*radii[0]+f*radii[2]+d*X*Y*radii[1]+J*radii[5]
    sigma5=h*radii[0]+g*radii[2]+d*radii[1]
    ledger={}
    caps={}
    naive={}
    for i in (4,5):
        terms=[]
        for (a,bv),p in sorted(transport[i].items()):
            bound=absolute_bound(p,X,Y)
            terms.append(dict(variables=[a,bv],coefficient_bound=str(bound),
                              contribution=str(bound*radii[a]*radii[bv])))
        caps[i]=sum(Q(row['contribution']) for row in terms)
        ledger[str(i)]=terms
        # Comparison only; naively bound v3 by |V|+|v2| before combining.
        oldr=radii.copy();oldr[2]=radii[1]+radii[2]
        naive[i]=sum(absolute_bound(decode(rows),X,Y)*oldr[int(key.split('_v')[1].split('v')[0])-1]*
                     oldr[int(key.rsplit('v',1)[1])-1]
                     for key,rows in data['half_kinetic_block_derivative'].items() if int(key[1])==i)
    c=Q(20601,400000)
    grav4=c*X*Y;grav5=c
    result=dict(evidence='EXACT_RATIONAL_CONDITIONAL_COEFFICIENT_BOUNDS',
        box_invariance_proved=False,full_initial_ball_contained=True,
        initial_containment_reason='Every |qi|,|vi|<=3/20 and |v2+v3|<=3/10; candidate caps are larger. Remaining coordinate/joint domains are not proved.',
        block_position_caps=[str(X),str(Y)],variables=['v1','v2','v2+v3','v4','v5','v6'],
        velocity_caps=list(map(str,radii)),remote_angles='unrestricted in coefficient bound',
        sigma_caps=list(map(str,[sigma4,sigma5])),T_caps=[str(caps[i]) for i in (4,5)],
        analytic_h_caps_excluding_implementation=[str(caps[4]+grav4),str(caps[5]+grav5)],
        naive_T_caps=[str(naive[i]) for i in (4,5)],coefficient_ledger=ledger,
        full_target_or_total_R_proved=False,Lean_verified=False,
        gravity_constant_g0='zero for ideal encoded potential; computed G0 and all implementation errors remain separate',
        source_audit_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'bounds.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('sigma_caps','T_caps','analytic_h_caps_excluding_implementation','naive_T_caps')}))
    print('DECIMAL_DIAGNOSTIC',*[float(v) for v in (sigma4,sigma5,caps[4],caps[5],caps[4]+grav4,caps[5]+grav5)])


if __name__=='__main__': main()
