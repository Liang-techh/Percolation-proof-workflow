using Pkg
Pkg.activate(joinpath(@__DIR__, "ref_tssos_patched"))
# MOSEK paths: overridable via the environment (rerun_julia.bat sets them;
# edit the .bat, not this file, when moving machines)
if !haskey(ENV, "MOSEKBINDIR")
    ENV["MOSEKBINDIR"] = "C:\\Program Files\\Mosek\\11.0\\tools\\platform\\win64x86\\bin"
end
if !haskey(ENV, "MOSEKLM_LICENSE_FILE")
    ENV["MOSEKLM_LICENSE_FILE"] = "C:\\Users\\z5242\\mosek\\mosek.lic"
end

using DynamicPolynomials
using MultivariatePolynomials
using DelimitedFiles
using LinearAlgebra
using Random
using Printf
using SHA
using Dates

include("dhport_lib.jl")

# =====================================================================
# routeB_export_traj.jl  (route-B chart data for the robot_final
# package)
#
# Rebuilds the certified storage V from routeB_certificate_V.csv (no
# re-solve), simulates N DH-chain trajectories under the explicitly recorded
# mass-regularizer / central-finite-difference C/G semantics from the initial ball
# inside D_q under the full ramp disturbance, and saves per-trajectory
# time series: t, V(t), the tube bound t^2, the block-region p(t), the
# route-B bracket ratio ||l||^2/bound, bound, ||l||^2.
# =====================================================================

ja, jb = 4, 5
a = [1.0, 0.8, 0.7, 0.6, 0.5, 0.4] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05] .+ [0.8, 0.5, 0.3, 0.15, 0.08, 0.03] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
c = ([0.5, 0.4, 0.35, 0.3, 0.25, 0.2] + [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]) ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
Ival = [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
kc = 0.05
pw = [1.5, 0.8]
T = 1.0
R = 1.0
R_init = 0.15
eta_star = 5.6
q_lim = Dict(1 => (-pi, pi), 2 => (-pi, pi), 3 => (-5 * pi / 6, 5 * pi / 6),
             4 => (-pi, pi), 5 => (-pi, pi), 6 => (-2 * pi, 2 * pi))
# route-B bracket constants (sf=2, eta=5.6)
sig_block = 1.84e-4
sig2 = 0.17969
sig4 = 0.05102
Anom_q2 = 0.094873
Cv_q2 = 0.029345
Anom_w2 = 0.070596
Cv_w2 = 0.002716
lam2p = 5 * sig2^2 + 20 * (Anom_q2 + Cv_q2)
lam3p = 5 * sig4^2
Wpart = 20 * (Anom_w2 + Cv_w2)
lam1p = 5 * sig_block^2

M0 = readdlm(joinpath(@__DIR__, "routeB_Mq_M0.csv"), ',', Float64)
M0_BB = [M0[ja, ja] 0.0; 0.0 M0[jb, jb]]
const G0_ref = arm_MCG(zeros(6), zeros(6))[3]

@polyvar qa qb dqa dqb t w
# rebuild V from the saved certificate
V = zero(typeof(qa^2 + 0.5 * qb^2))
rows = readdlm(joinpath(@__DIR__, "routeB_certificate_V.csv"), ',', String)
V_coeffs = Float64[]
V_exps = NTuple{5,Int}[]
for r in eachrow(rows)
    global V
    r[1][1] == 'c' && continue  # header
    cf = parse(Float64, r[1])
    ex = Int.(round.(parse.(Float64, r[2:6])))
    push!(V_coeffs, cf)
    push!(V_exps, (ex[1], ex[2], ex[3], ex[4], ex[5]))
    V += cf * qa^ex[1] * qb^ex[2] * dqa^ex[3] * dqb^ex[4] * t^ex[5]
end
println("V rebuilt, degree ", maxdegree(V))

function in_limits_q(q)
    for i in 1:6
        lo, hi = q_lim[i]
        (lo <= q[i] <= hi) || return false
    end
    return true
end

function sim_traj(q0, dq0, cw)
    dt = 0.005
    n = Int(T / dt)
    q = copy(q0)
    dq = copy(dq0)
    qs = zeros(6, n + 1)
    dqs = zeros(6, n + 1)
    qs[:, 1] = q
    dqs[:, 1] = dq
    for k in 1:n
        tk = (k - 1) * dt
        wv = cw * tk
        tau = -Kp .* q - (Kd + b_fr) .* dq + G0_ref + (gw_coef .* I_val) .* wv
        Mq, Cdq, Gq = arm_MCG(q, dq)
        acc = Mq \ (tau - Cdq - Gq)
        q = q + dt * dq + 0.5 * dt^2 * acc
        dq = dq + dt * acc
        qs[:, k+1] = q
        dqs[:, k+1] = dq
    end
    return qs, dqs
end

function evalV_fast(qv, dqv, tv)
    # Avoid allocating a substituted polynomial at every 5 ms sample.  The
    # old `subs(V, ...)` path accumulated substantial temporary allocations
    # over 1000 trajectories and could terminate the exporter mid-batch.
    x1, x2, x3, x4, x5 = qv[4], qv[5], dqv[4], dqv[5], tv
    total = 0.0
    @inbounds for ii in eachindex(V_coeffs)
        e = V_exps[ii]
        total += V_coeffs[ii] * x1^e[1] * x2^e[2] * x3^e[3] * x4^e[4] * x5^e[5]
    end
    return total
end

a_c = (Kp + mgl) ./ I_val
c_c = (b_fr + Kd) ./ I_val

# reproduce the certificate verification's Monte-Carlo groups (the same
# seeds as run_coverage in routeB_pmi_certificate.jl), so the chart
# data's max bracket ratio matches the verified 0.1591
function gen_trajectories()
    traj_rows = Any[]
    state_rows = Any[]
    n_ok = 0
    for (cbound, seed, Ngrp) in ((sqrt(3) * 0.2, 20260840, 500),
                                 (sqrt(3), 20260841, 500))
        Random.seed!(seed)
        for kk in 1:Ngrp
            local q0, dq0
            while true
                u = randn(12); u ./= norm(u)
                r = R_init * rand()^(1 / 12)
                x = r .* u
                if in_limits_q(x[1:6])
                    q0 = x[1:6]; dq0 = x[7:12]
                    break
                end
            end
            cw = cbound * (2 * rand() - 1)
            local qs, dqs
            try
                qs, dqs = sim_traj(q0, dq0, cw)
            catch err
                println("trajectory simulation failed; skipping sample: ", sprint(showerror, err))
                continue
            end
            traj_inlim = true
            for k in 1:size(qs, 2)
                in_limits_q(qs[:, k]) || (traj_inlim = false; break)
            end
            traj_inlim || continue
            n_ok += 1
            vmax = -Inf
            for k in 1:size(qs, 2)
                tk = (k - 1) * 0.005
                wv = cw * tk
                Vv = evalV_fast(qs[:, k], dqs[:, k], tk)
                vmax = max(vmax, Vv)
                pv = pw[1] * (qs[4, k]^2 + qs[5, k]^2) + pw[2] * (dqs[4, k]^2 + dqs[5, k]^2)
                fv = [-a_c[i] * qs[i, k] - c_c[i] * dqs[i, k] + gw_coef[i] * wv for i in 1:6]
                fv[4] += kc * qs[5, k]
                fv[5] += kc * qs[4, k]
                Mq, Cdq, Gq = arm_MCG(qs[:, k], dqs[:, k])
                tau = -Kp .* qs[:, k] - (Kd + b_fr) .* dqs[:, k] + G0_ref + (gw_coef .* I_val) .* wv
                a_ex = Mq \ (tau - Cdq - Gq)
                lv = [Ival[4] * fv[4], Ival[5] * fv[5]] - M0_BB * a_ex[4:5]
                l2 = norm(lv)^2
                qdq2v = sum(qs[:, k] .^ 2) + sum(dqs[:, k] .^ 2)
                bound = lam1p * norm(a_ex[4:5])^2 + lam2p * qdq2v + lam3p * qdq2v^2 + Wpart * wv^2
                push!(traj_rows, [Float64(n_ok), tk, Vv, tk^2, pv,
                                  l2 / max(bound, 1e-12), bound, l2])
            end
            println("trajectory ", n_ok, ": max V = ", round(vmax, digits = 4))
            # The DH finite-difference kernel allocates many short-lived
            # matrices.  Collect periodically so a long 1000-trajectory
            # export cannot be terminated by transient heap growth.
            (n_ok % 10 == 0) && GC.gc()
            flush(stdout)
            # state samples: the first 20 trajectories of each group
            if (n_ok <= 20) || (n_ok > 500 && n_ok <= 520)
                for (tk, tidx) in ((0.0, 1), (0.5, 101), (1.0, 201))
                    push!(state_rows, [Float64(n_ok), tk, qs[4, tidx], qs[5, tidx],
                                       dqs[4, tidx], dqs[5, tidx]])
                end
            end
        end
    end
    return traj_rows, state_rows, n_ok
end

traj_rows, state_rows, n_ok = gen_trajectories()
println("total in-limits trajectories: ", n_ok)
open(joinpath(@__DIR__, "routeB_traj_all.csv"), "w") do io
    writedlm(io, ["traj" "t" "V" "tube" "p" "ratio" "bound" "l2"], ',')
    for row in traj_rows
        writedlm(io, [row], ',')
    end
end
open(joinpath(@__DIR__, "routeB_state_samples.csv"), "w") do io
    writedlm(io, ["traj" "t" "q4" "q5" "dq4" "dq5"], ',')
    for row in state_rows
        writedlm(io, [row], ',')
    end
end
# remove the superseded per-trajectory files
for f in filter(f -> occursin("routeB_traj_", f), readdir(@__DIR__))
    startswith(f, "routeB_traj_all") && continue
    rm(joinpath(@__DIR__, f))
end
println("saved routeB_traj_all.csv with ", n_ok, " trajectories")
function sha256_file(path)
    return bytes2hex(SHA.sha256(read(path)))
end
open(joinpath(@__DIR__, "routeB_export_manifest.toml"), "w") do io
    println(io, "schema_version = \"routeB-export-manifest-v1\"")
    println(io, "evidence_level = \"empirical\"")
    println(io, "coverage_kind = \"trajectory_monte_carlo_only\"")
    println(io, "global_box_coverage = false")
    println(io, "run_timestamp_local = \"", Dates.now(), "\"")
    println(io, "julia_version = \"", VERSION, "\"")
    println(io, "export_source_sha256 = \"", sha256_file(@__FILE__), "\"")
    println(io, "certificate_V_sha256 = \"", sha256_file(joinpath(@__DIR__, "routeB_certificate_V.csv")), "\"")
    println(io, "trajectory_output_sha256 = \"", sha256_file(joinpath(@__DIR__, "routeB_traj_all.csv")), "\"")
    println(io, "state_samples_output_sha256 = \"", sha256_file(joinpath(@__DIR__, "routeB_state_samples.csv")), "\"")
    println(io, "trajectory_count = ", n_ok)
    println(io, "trajectory_seeds = \"20260840,20260841\"")
    println(io, "coverage_samples_each = 500")
    println(io, "mass_regularizer = ", MASS_REGULARIZER)
    println(io, "coriolis_gravity_fd_step = ", CG_FINITE_DIFF_STEP)
    println(io, "dynamics_semantics = \"", DYNAMICS_SEMANTICS, "\"")
end
println("saved routeB_export_manifest.toml")
