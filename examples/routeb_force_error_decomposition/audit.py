"""Read-only source constants, reference mass, gravity support and SHA audit."""
import csv
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
SRC=HERE.parents[2]/"6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq"


def read(name):
    with (SRC/name).open(newline="",encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    controller=(SRC/"dhport_lib.jl").read_text(encoding="utf-8")
    def vector(name):
        return [Q(x.strip()) for x in re.search(r"\b"+name+r"\s*=\s*\[([^\]]+)\]",controller)[1].split(",")]
    kp=vector("Kp"); d=[x+y for x,y in zip(vector("Kd"),vector("b_fr"))]
    g=vector("gw_coef")
    assert kp[3:5]==[Q(3,5),Q(1,2)]
    assert d[3:5]==[Q(4,5),Q(13,20)] and g[3:5]==[Q(1,5),Q(1,10)]
    masses=read("routeB_fourier_mass_full_rational.csv")
    def mass(i,j):
        out={}
        for row in masses:
            if (int(row["row"]),int(row["col"]))!=(i,j): continue
            nu=tuple(int(row[f"nu{k}"]) for k in range(1,7))
            assert nu not in out and Q(int(row["imag_num"]),int(row["imag_den"]))==0
            out[nu]=Q(int(row["real_num"]),int(row["real_den"]))
        return out
    zero=(0,)*6
    assert mass(4,4)=={(0,0,0,0,-2,0):Q(-147,3200000),zero:Q(560441,4800000),
                       (0,0,0,0,2,0):Q(-147,3200000)}
    assert mass(4,5)==mass(5,4)=={}
    assert mass(5,5)=={zero:Q(40147,800000)}
    reg=Q(1,1000000)
    reference=[sum(mass(4,4).values())+reg,sum(mass(5,5).values())+reg]
    assert reference==[Q(350003,3000000),Q(200739,4000000)]
    pot=read("routeB_fourier_potential_rational.csv")
    assert len(pot)==17
    assert all(abs(int(r[f"nu{k}"]))<=1 for r in pot for k in (4,5))
    assert all(Q(int(r["imag_num"]),int(r["imag_den"]))==0 for r in pot)
    c=Q(20601,400000); h=Q(1,100000)
    gravity_ledger={int(r["row"]):Q(int(r["num"]),int(r["den"]))
                    for r in read("routeB_fourier_fd_error_bounds.csv") if r["kind"]=="gravity_derivative"}
    refined_fd=c*h*h/6
    assert refined_fd==gravity_ledger[4] and 2*refined_fd==gravity_ledger[5]
    files=[SRC/n for n in ("dhport_lib.jl","routeB_fourier_mass_full_rational.csv",
           "routeB_fourier_potential_rational.csv","routeB_fourier_fd_error_bounds.csv",
           "routeB_compact_direct_descriptor_structure.jl",
           "routeB_factorized_descriptor_model.jl","routeB_fourier_lifted_descriptor_model.jl",
           "routeB_compact_dh_nominal_distal_bridge_audit.jl",
           "routeB_compact_port_implicit_accel_elimination.py")]
    files += [HERE.parent/"routeb_dh_power_binding/DHPowerBinding.lean",
              HERE.parent/"routeb_block_potential/BlockPotential.lean"]
    result=dict(status="EXACT_CONSTANTS_MASS_AND_GRAVITY_SUPPORT_CHECKED",
                block_one_based=[4,5],remote_one_based=[1,2,3,6],Kp_B=kp[3:5],D_B=d[3:5],G_B=g[3:5],
                reference_mass_diagonal=reference,
                structural_mass_mismatch="(-(147/800000)*sin(q5)^2*a4, 0)",
                gravity_scale=c,fd_step=h,gravity_fd_multiplier="sin(h)/h",
                gravity4="c*sin(q2+q3)*sin(q4)*sin(q5)",
                gravity5="-c*(cos(q2+q3)*sin(q5)+sin(q2+q3)*cos(q4)*cos(q5))",
                both_gravity_absolute_bounds=c,both_refined_fd_truncation_bounds=refined_fd,
                gravity_vector_squared_bound=c*c,
                gravity_weighted_cost_bound=Q(10,13)*c*c,
                old_DH_nominal_offset=["-(3/20)*q4+(1/100)*q5","(1/200)*q4-(2/25)*q5"],
                old_fourier_extra_velocity_offset=["(3/10)*v4","0"],
                total_integrated_budget_proved=False,float64_errors_enclosed=False,
                sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (HERE/"source_evidence.json").write_text(json.dumps(result,default=str,indent=2)+"\n",encoding="utf-8")
    print(result["status"])
    print("Mref diagonal:",reference,"gravity c:",c,"refined FD gravity error:",refined_fd)
    print("TOTAL_INTEGRATED_BUDGET_PROVED=false")


if __name__=="__main__": main()
