# A bounded E1 falsifier, NOT interval reachability or a proof of an integral.
# Reads original Julia-FD RHS; no certificate source or output is overwritten.
using LinearAlgebra, SHA, Dates, DelimitedFiles, Printf

const SIDE = @__DIR__
const SOURCE = normpath(joinpath(SIDE, "..", "..", "..", "6dof_sos_optimized",
    "6dof_sos_optimized", "routeB_dense_Mq", "dhport_lib.jl"))
const SOURCE_HASH = bytes2hex(sha256(read(SOURCE)))
include(SOURCE)
const DAMP = Kd + b_fr
const INPUT = gw_coef .* I_val
const GZERO = arm_MCG(zeros(6), zeros(6))[3]
const MREF = [350003/3000000, 200739/4000000]

function diagnostics(x, t, c)
    q = x[1:6]; v = x[7:12]
    w = c*t
    Mq, cv, g = arm_MCG(q, v)
    tau = -Kp .* q - DAMP .* v + GZERO + INPUT .* w
    a = Mq \ (tau-cv-g)
    e = MREF .* a[4:5] + Kp[4:5] .* q[4:5] + DAMP[4:5] .* v[4:5] - INPUT[4:5] .* w
    cost = e[1]^2/(8/5) + e[2]^2/(13/10)
    vb = sum(MREF .* v[4:5].^2)/2 + 3/10*q[4]^2 + 1/4*q[5]^2
    p = 3/2*sum(q[4:5].^2) + 4/5*sum(v[4:5].^2)
    qt = 3*sum(q[4:5].^2) + 2*sum(v[4:5].^2)
    return (;a,e,cost,vb,p,qt)
end

function rhs(x,t,c)
    d = diagnostics(x,t,c)
    return [x[7:12]; d.a; d.cost]
end

function run_case(x0,c,steps,out,label)
    x=[x0;0.0]; dt=1/steps
    maxp=maxqt=maxcost=0.0; maxabs=zeros(12)
    open(joinpath(out,label*".csv"),"w") do io
        println(io,"t,"*join(["q$i" for i=1:6],",")*","*join(["v$i" for i=1:6],",")*",R,VB,p,qterminal,e4,e5,cost")
        for n=0:steps
            t=n*dt; d=diagnostics(x,t,c)
            all(isfinite,x) || error("nonfinite state retained at $label t=$t")
            maxp=max(maxp,d.p);maxqt=max(maxqt,d.qt);maxcost=max(maxcost,d.cost)
            maxabs=max.(maxabs,abs.(x[1:12]))
            if n%max(1,steps÷100)==0 || n==steps
                writedlm(io,permutedims([t;x;d.vb;d.p;d.qt;d.e;d.cost]),',')
            end
            n==steps && break
            k1=rhs(x,t,c);k2=rhs(x+dt/2*k1,t+dt/2,c)
            k3=rhs(x+dt/2*k2,t+dt/2,c);k4=rhs(x+dt*k3,t+dt,c)
            x += dt/6*(k1+2k2+2k3+k4)
        end
    end
    d=diagnostics(x,1.0,c)
    return (;R=x[13],vb=d.vb,p=d.p,qt=d.qt,maxp,maxqt,maxcost,maxabs)
end

function main()
    steps=length(ARGS)>=1 ? parse(Int,ARGS[1]) : 400
    selected=length(ARGS)>=2 ? parse.(Int,split(ARGS[2],',')) : collect(1:8)
    100<=steps<=3200 || error("bounded screen supports 100..3200 steps")
    cases=[("origin_ramp",0,0.0,1.7), ("q2_plus",2,0.149,1.7),
           ("q2_minus",2,-0.149,1.7), ("q3_plus",3,0.149,1.7),
           ("v6_plus",12,0.149,1.7), ("v6_minus",12,-0.149,1.7),
           ("q4_zero_input",4,0.149,0.0), ("v2_plus",8,0.149,1.7)]
    all(i->1<=i<=length(cases),selected) || error("unknown case")
    out=joinpath(SIDE,"output","run-"*Dates.format(now(),"yyyymmdd-HHMMSS")*"-"*string(time_ns()))
    mkpath(out)
    cp(@__FILE__,joinpath(out,"screen.jl"))
    open(joinpath(out,"metadata.txt"),"w") do io
        println(io,"EVIDENCE=E1_NUMERICAL_SCREEN_ONLY")
        println(io,"steps=$steps selected=$(join(selected,',')) Julia=$VERSION")
        println(io,"source=$SOURCE\nsource_sha256=$SOURCE_HASH")
        println(io,"screen_sha256="*bytes2hex(sha256(read(@__FILE__))))
        println(io,"R uses RK4 quadrature of TOTAL reference force error; no error enclosure")
        println(io,"initial nonzero entry is +/-0.149; ramp c=1.7 or0; all full12 initial data retained")
        println(io,"reference masses=$MREF; G0=$GZERO; DAMP=$DAMP; INPUT=$INPUT")
    end
    println("RUN=$out");flush(stdout)
    open(joinpath(out,"summary.csv"),"w") do io
        println(io,"case_index,label,steps,c,R_T,VB_T,p_T,qterminal_T,max_p,max_qterminal,max_cost,initial_norm_squared")
        for i in selected
            label,axis,value,c=cases[i]; x0=zeros(12)
            axis>0 && (x0[axis]=value)
            @assert sum(abs2,x0)<=0.15^2 && c^2<=3
            elapsed=@elapsed d=run_case(x0,c,steps,out,label)
            writedlm(io,permutedims(Any[i,label,steps,c,d.R,d.vb,d.p,d.qt,d.maxp,d.maxqt,d.maxcost,sum(abs2,x0)]),',')
            flush(io)
            @printf("case=%d %s R=%.12g maxp=%.8g qT=%.8g elapsed=%.2fs\n",i,label,d.R,d.maxp,d.qt,elapsed)
            flush(stdout)
            open(joinpath(out,label*"_maxabs.csv"),"w") do aux
                writedlm(aux,permutedims(d.maxabs),',')
            end
        end
    end
    @assert bytes2hex(sha256(read(SOURCE)))==SOURCE_HASH "source changed during screen"
    println("SCREEN_FINISHED_NO_PROOF source_unchanged=true")
end
main()
