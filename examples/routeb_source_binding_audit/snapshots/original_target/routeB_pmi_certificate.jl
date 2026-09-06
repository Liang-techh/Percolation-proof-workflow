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

using TSSOS
using DynamicPolynomials
using JuMP
using MosekTools
using MultivariatePolynomials
using DelimitedFiles
using LinearAlgebra
using Random
using SHA
using Dates

include("dhport_lib.jl")

# =====================================================================
# routeB_pmi_certificate.jl  (route B: the FINAL certificate
# package, empirical level per the user's direction -- no full
# symbolic psatz)
#
# The block (4,5) certificate with finite-sample gain estimates and the q4/q5 joint
# limits is solved (scalar + PMI, alpha=12), its storage V is
# extracted, and the empirical certification chain is closed:
#   (1) the certified polynomials are MC-verified nonnegative on their
#       domains (D on the box, pinit, ploc, pterm);
#   (2) DH-chain Monte-Carlo trajectories under the explicitly recorded
#       mass-regularizer / central-finite-difference C/G semantics: tube containment V <=
#       R^2 t^2/T^2, terminal containment qpoly(T) <= alpha, and the
#       route-B residual-difference bracket ratio
#         ||l||^2 <= 5 sig_block^2 ||a_45||^2 + lam2p qdq^2
#                   + 5 sig4^2 qdq^4 + Wpart w^2
#       (sf=2 constants, ratio <= 1) checked at EVERY trajectory point;
#   (3) the certificate package is saved (V coefficients + the
#       verification CSV/log).
# =====================================================================

ja, jb = 4, 5
a = [1.0, 0.8, 0.7, 0.6, 0.5, 0.4] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05] .+ [0.8, 0.5, 0.3, 0.15, 0.08, 0.03] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
c = ([0.5, 0.4, 0.35, 0.3, 0.25, 0.2] + [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]) ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
gw = [1.0, 0.5, 0.3, 0.2, 0.1, 0.05] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
Ival = [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
kc = 0.05
pw = [1.5, 0.8]
qw = [3.0, 2.0]
T = 1.0
R = 1.0
R_init = 0.15
EPS = 1e-3
eta_star = 5.6
# Solve the deliverable alpha first so a lower-alpha success cannot silently
# select a different certificate.  The status table still records every
# attempt that is actually run.
alpha_tries = [12.0, 8.0, 16.0, Inf]
sres = 5.0
# finite-sample stage-11 gain estimates from the DH-chain port (section 30;
# not global bounds and not a literal exact-arithmetic model)
lam1 = 1.3505585708406844e-7
lam2 = 0.1291510728162954
lam3 = 0.010410446611542263
q_lim = Dict(1 => (-pi, pi), 2 => (-pi, pi), 3 => (-5 * pi / 6, 5 * pi / 6),
             4 => (-pi, pi), 5 => (-pi, pi), 6 => (-2 * pi, 2 * pi))
# route-B bracket constants (eta=5.6, debug_12d/12e, sf=2 safety factors)
sig_block = 1.84e-4
sig2 = 0.17969
sig4 = 0.05102
Anom_q2 = 0.094873
Cv_q2 = 0.029345
Anom_w2 = 0.070596
Cv_w2 = 0.002716
sf = 2.0
lam2p = 5 * sig2^2 + sf * 10 * (Anom_q2 + Cv_q2)
lam3p = 5 * sig4^2
Wpart = sf * 10 * (Anom_w2 + Cv_w2)
lam1p = 5 * sig_block^2

M0 = readdlm(joinpath(@__DIR__, "routeB_Mq_M0.csv"), ',', Float64)
M0_BB = [M0[ja, ja] 0.0; 0.0 M0[jb, jb]]
M11 = M0_BB[1, 1]
M22 = M0_BB[2, 2]
const G0_ref = arm_MCG(zeros(6), zeros(6))[3]

@polyvar qa qb dqa dqb l1 l2 t w y1 y2 y3 y4
x4 = [qa; qb; dqa; dqb]
x5 = [qa; qb; dqa; dqb; t]
dv6 = [qa; qb; dqa; dqb; t; w]
dv8 = [qa; qb; dqa; dqb; t; w; y1; y2]
dv8b = [qa; qb; dqa; dqb; t; w; y3; y4]

f1 = -a[ja] * qa - c[ja] * dqa + kc * qb + gw[ja] * w
f2 = -a[jb] * qb - c[jb] * dqb + kc * qa + gw[jb] * w
p = pw[1] * (qa^2 + qb^2) + pw[2] * (dqa^2 + dqb^2)
qpoly = qw[1] * (qa^2 + qb^2) + qw[2] * (dqa^2 + dqb^2)
g = t * (T - t)
h_t = R^2 * t^2 / T^2
r0 = qa^2 + qb^2 + dqa^2 + dqb^2 - R_init^2
qdq2 = qa^2 + qb^2 + dqa^2 + dqb^2

p_lim4 = (q_lim[4][2] - qa) * (qa - q_lim[4][1])
p_lim5 = (q_lim[5][2] - qb) * (qb - q_lim[5][1])
lims45 = [p_lim4, p_lim5]

function monomials_upto(vars, deg)
    vcat([MultivariatePolynomials.monomials(vars, i) for i in 0:deg]...)
end

const ACTIVE_PMI_BLOCKS = Ref{Vector{Any}}(Any[])

function pmi_block!(model, poly, z)
    nz = length(z)
    P = @variable(model, [1:nz, 1:nz], PSD)
    quad = sum(z[i] * P[i, j] * z[j] for i in 1:nz, j in 1:nz)
    @constraint(model, MultivariatePolynomials.coefficients(quad - poly) .== 0)
    push!(ACTIVE_PMI_BLOCKS[], (P = P, poly = poly, z = z))
    return P
end

function numpoly(P)
    trm = MultivariatePolynomials.terms(P)
    return sum(JuMP.value(MultivariatePolynomials.coefficient(trm)) *
               MultivariatePolynomials.monomial(trm) for trm in trm)
end

function model_status_string(f, model)
    try
        return string(f(model))
    catch
        return "UNAVAILABLE"
    end
end

function compute_pmi_gram_min_eig(blocks)
    isempty(blocks) && return NaN
    vals = Float64[]
    for blk in blocks
        P = blk.P
        n = size(P, 1)
        G = [try Float64(value(P[i, j])) catch; NaN end for i in 1:n, j in 1:n]
        all(isfinite, G) || return NaN
        push!(vals, eigmin(Symmetric((G + G') / 2)))
    end
    return minimum(vals)
end

function compute_pmi_reconstruction_error(blocks)
    isempty(blocks) && return NaN
    err = 0.0
    for blk in blocks
        P = blk.P
        z = blk.z
        quad_num = sum(Float64(value(P[i, j])) * z[i] * z[j]
                       for i in axes(P, 1), j in axes(P, 2))
        residual = quad_num - numpoly(blk.poly)
        cf = MultivariatePolynomials.coefficients(residual)
        isempty(cf) || (err = max(err, maximum(abs.(Float64.(cf)))))
    end
    return err
end

function write_pmi_gram_artifacts(blocks, alpha)
    """Export the solved PMI Gram blocks and their monomial bases.

    This is deliberately a data export, not a proof claim: the independent
    checker must still validate PSD and coefficient identities from these
    files.  A long-form CSV avoids silently dropping off-diagonal entries.
    """
    gram_path = joinpath(@__DIR__, "routeB_pmi_gram_alpha12.csv")
    basis_path = joinpath(@__DIR__, "routeB_pmi_basis_alpha12.csv")
    basis_exp_path = joinpath(@__DIR__, "routeB_pmi_basis_exponents_alpha12.csv")
    target_path = joinpath(@__DIR__, "routeB_pmi_polynomial_alpha12.csv")
    manifest_path = joinpath(@__DIR__, "routeB_pmi_gram_manifest.csv")
    all_vars = [qa, qb, dqa, dqb, t, w, y1, y2, y3, y4]
    function exponent_vector(mon)
        tm = MultivariatePolynomials.monomial(first(MultivariatePolynomials.terms(mon)))
        e = zeros(Int, length(all_vars))
        for (k, v) in enumerate(MultivariatePolynomials.variables(tm))
            idx = findfirst(x -> x == v, all_vars)
            idx === nothing && error("PMI export encountered an unknown variable: ", v)
            e[idx] = tm.z[k]
        end
        return e
    end
    open(gram_path, "w") do io
        println(io, "alpha,block,i,j,value")
        for (bidx, blk) in enumerate(blocks)
            P = blk.P
            for i in axes(P, 1), j in axes(P, 2)
                println(io, join((alpha, bidx, i, j, Float64(value(P[i, j]))), ','))
            end
        end
    end
    open(basis_path, "w") do io
        println(io, "alpha,block,index,monomial")
        for (bidx, blk) in enumerate(blocks)
            for (i, z) in enumerate(blk.z)
                mon = replace(string(z), '"' => "'")
                println(io, alpha, ',', bidx, ',', i, ",'", mon, "'")
            end
        end
    end
    open(basis_exp_path, "w") do io
        println(io, "alpha,block,index,", join(["e" * string(i) for i in 1:length(all_vars)], ','))
        for (bidx, blk) in enumerate(blocks)
            for (i, z) in enumerate(blk.z)
                println(io, join((alpha, bidx, i, exponent_vector(z)...), ','))
            end
        end
    end
    open(target_path, "w") do io
        println(io, "alpha,block,term,", join(["e" * string(i) for i in 1:length(all_vars)], ','), ",coefficient")
        for (bidx, blk) in enumerate(blocks)
            poly_num = numpoly(blk.poly)
            for (term_idx, trm) in enumerate(MultivariatePolynomials.terms(poly_num))
                println(io, join((alpha, bidx, term_idx, exponent_vector(MultivariatePolynomials.monomial(trm))...,
                                  Float64(MultivariatePolynomials.coefficient(trm))), ','))
            end
        end
    end
    open(manifest_path, "w") do io
        println(io, "alpha,block,dimension,gram_min_eig,reconstruction_error,gram_sha256,basis_sha256,basis_exponents_sha256,target_sha256")
        gh = sha256_file(gram_path)
        bh = sha256_file(basis_path)
        beh = sha256_file(basis_exp_path)
        th = sha256_file(target_path)
        for (bidx, blk) in enumerate(blocks)
            P = blk.P
            G = [Float64(value(P[i, j])) for i in axes(P, 1), j in axes(P, 2)]
            eig = eigmin(Symmetric((G + G') / 2))
            quad_num = sum(G[i, j] * blk.z[i] * blk.z[j]
                           for i in axes(P, 1), j in axes(P, 2))
            err = isempty(MultivariatePolynomials.coefficients(quad_num - numpoly(blk.poly))) ?
                  0.0 : maximum(abs.(Float64.(MultivariatePolynomials.coefficients(quad_num - numpoly(blk.poly)))))
            println(io, join((alpha, bidx, size(P, 1), eig, err, gh, bh, beh, th), ','))
        end
    end
    return gram_path, basis_path, basis_exp_path, target_path, manifest_path
end

function sha256_file(path)
    return bytes2hex(SHA.sha256(read(path)))
end

const SCALAR_AUX_POLYS = Ref{Any}(nothing)

function build_cert(a_try::Float64; pmi::Bool)
    ACTIVE_PMI_BLOCKS[] = Any[]
    model = Model(optimizer_with_attributes(
        Mosek.Optimizer,
        "MSK_DPAR_OPTIMIZER_MAX_TIME" => 180.0,
        "MSK_IPAR_NUM_THREADS" => 4,
    ))
    set_silent(model)
    V0, V0c, V0b = add_poly!(model, [qa; qb; t], 4)
    A1, A1c, A1b = add_poly!(model, [qa; qb; t], 1)
    A2, A2c, A2b = add_poly!(model, [qa; qb; t], 1)
    Q11 = @variable(model)
    Q12 = @variable(model)
    Q22 = @variable(model)
    c1, c1c, c1b = add_poly!(model, [qa; qb; dqa; dqb; t], 2)
    c2, c2c, c2b = add_poly!(model, [qa; qb; dqa; dqb; t], 2)
    s1p, s1pc, s1pb = add_poly!(model, dv6, 2)
    s2p, s2pc, s2pb = add_poly!(model, dv6, 2)
    s4p, s4pc, s4pb = add_poly!(model, x4, 2)
    s6p, s6pc, s6pb = add_poly!(model, x5, 2)
    s7p, s7pc, s7pb = add_poly!(model, x5, 2)
    s6 = EPS + s6p
    rt1 = (A1 + Q11 * dqa + Q12 * dqb) / M11
    rt2 = (A2 + Q12 * dqa + Q22 * dqb) / M22
    KE = 0.5 * (Q11 * dqa^2 + 2 * Q12 * dqa * dqb + Q22 * dqb^2)
    q1 = sres * (1 - lam1 / M11^2)
    q2 = sres * (1 - lam1 / M22^2)
    nu1 = rt1 + 2 * sres * lam1 * Ival[ja] * f1 / M11^2
    nu2 = rt2 + 2 * sres * lam1 * Ival[jb] * f2 / M22^2
    D0 = -differentiate(V0, t) - differentiate(V0, qa) * dqa - differentiate(V0, qb) * dqb +
         rt1 * (-Ival[ja] * f1) + rt2 * (-Ival[jb] * f2) + w^2 +
         s1p * (p - eta_star) - s2p * g -
         sres * lam2 * qdq2 - sres * lam3 * qdq2^2 -
         sres * lam1 * ((Ival[ja] * f1)^2 / M11^2 + (Ival[jb] * f2)^2 / M22^2)
    D_elim_c = D0 - c1 - c2
    Pm1 = 4 * q1 * y1^2 + 2 * nu1 * y1 * y2 + c1 * y2^2
    Pm2 = 4 * q2 * y3^2 + 2 * nu2 * y3 * y4 + c2 * y4^2
    pinit = -subs(V0, t => 0.0) - subs(A1, t => 0.0) * dqa - subs(A2, t => 0.0) * dqb - KE + s4p * r0
    ploc = -(p - eta_star) * s6 + V0 + A1 * dqa + A2 * dqb + KE - R^2 * h_t - s7p * g
    mults = [(s1p, dv6, 1), (s2p, dv6, 1), (s4p, x4, 1), (s6p, x5, 1), (s7p, x5, 1)]
    pterm = nothing
    s5p = nothing
    if isfinite(a_try)
        s5p, s5pc, s5pb = add_poly!(model, x4, 2)
        s5 = EPS + s5p
        pterm = -(qpoly - a_try) * s5 + subs(V0, t => T) + subs(A1, t => T) * dqa + subs(A2, t => T) * dqb + KE - R^2
        push!(mults, (s5p, x4, 1))
    end
    if pmi
        pmi_block!(model, Pm1, monomials_upto(dv8, 2))
        pmi_block!(model, Pm2, monomials_upto(dv8b, 2))
        for (poly, vars, ord) in mults
            pmi_block!(model, poly, monomials_upto(vars, ord))
        end
        s_limD1, s_limD1c, s_limD1b = add_poly!(model, dv6, 2)
        s_limD2, s_limD2c, s_limD2b = add_poly!(model, dv6, 2)
        s_limI1, s_limI1c, s_limI1b = add_poly!(model, x4, 2)
        s_limI2, s_limI2c, s_limI2b = add_poly!(model, x4, 2)
        s_limL1, s_limL1c, s_limL1b = add_poly!(model, x5, 2)
        s_limL2, s_limL2c, s_limL2b = add_poly!(model, x5, 2)
        pmi_block!(model, D_elim_c - s_limD1 * p_lim4 - s_limD2 * p_lim5, monomials_upto(dv6, 2))
        pmi_block!(model, pinit - s_limI1 * p_lim4 - s_limI2 * p_lim5, monomials_upto(x4, 2))
        pmi_block!(model, ploc - s_limL1 * p_lim4 - s_limL2 * p_lim5, monomials_upto(x5, 2))
        for spoly in (s_limD1, s_limD2)
            pmi_block!(model, spoly, monomials_upto(dv6, 1))
        end
        for spoly in (s_limI1, s_limI2)
            pmi_block!(model, spoly, monomials_upto(x4, 1))
        end
        for spoly in (s_limL1, s_limL2)
            pmi_block!(model, spoly, monomials_upto(x5, 1))
        end
        if pterm !== nothing
            s_limT1, s_limT1c, s_limT1b = add_poly!(model, x4, 2)
            s_limT2, s_limT2c, s_limT2b = add_poly!(model, x4, 2)
            pmi_block!(model, pterm - s_limT1 * p_lim4 - s_limT2 * p_lim5, monomials_upto(x4, 2))
            for spoly in (s_limT1, s_limT2)
                pmi_block!(model, spoly, monomials_upto(x4, 1))
            end
        end
    else
        add_psatz!(model, Pm1, dv8, [], [], 2, TS = "block", SO = 1)
        add_psatz!(model, Pm2, dv8b, [], [], 2, TS = "block", SO = 1)
        add_psatz!(model, D_elim_c, dv6, lims45, [], 2, TS = "block", SO = 1)
        add_psatz!(model, pinit, x4, lims45, [], 2, TS = "block", SO = 1)
        add_psatz!(model, ploc, x5, lims45, [], 2, TS = "block", SO = 1)
        if pterm !== nothing
            add_psatz!(model, pterm, x4, lims45, [], 2, TS = "block", SO = 1)
        end
        for (poly, vars, ord) in mults
            add_psatz!(model, poly, vars, [], [], ord, TS = "block", SO = 1)
        end
    end
    return model, V0, A1, A2, Q11, Q12, Q22, D_elim_c, pinit, ploc, pterm, mults
end

println("=== route-B final certificate package ===")
println("constants: lam1=", lam1, " lam2=", lam2, " lam3=", lam3)
println("route-B bracket (sf=", sf, "): lam2p=", round(lam2p, digits = 4),
        " lam3p=", round(lam3p, digits = 5), " Wpart=", round(Wpart, digits = 4),
        " lam1p=", lam1p)

# ---- 1. certificate solve: PMI consistency + scalar evaluation ----
println("--- certificate solve ---")
alpha_star = NaN
target_alpha = 12.0
pmi_status = Dict{Float64, String}()
pmi_primal_status = Dict{Float64, String}()
pmi_dual_status = Dict{Float64, String}()
pmi_gram_min_eig_by_alpha = Dict{Float64, Float64}()
pmi_reconstruction_error_by_alpha = Dict{Float64, Float64}()
pmi_numeric_check_by_alpha = Dict{Float64, Bool}()
pmi_block_registry = Dict{Float64, Vector{Any}}()
for a_try in alpha_tries
    modelp, V0p, A1p, A2p, Q11p, Q12p, Q22p, _, _, _, _, _ = build_cert(a_try; pmi = true)
    pmi_block_registry[a_try] = copy(ACTIVE_PMI_BLOCKS[])
    t_el = @elapsed optimize!(modelp)
    st = string(termination_status(modelp))
    pmi_status[a_try] = st
    pmi_primal_status[a_try] = model_status_string(primal_status, modelp)
    pmi_dual_status[a_try] = model_status_string(dual_status, modelp)
    pmi_gram_min_eig_by_alpha[a_try] = compute_pmi_gram_min_eig(pmi_block_registry[a_try])
    pmi_reconstruction_error_by_alpha[a_try] = compute_pmi_reconstruction_error(pmi_block_registry[a_try])
    pmi_numeric_check_by_alpha[a_try] = isfinite(pmi_gram_min_eig_by_alpha[a_try]) &&
        isfinite(pmi_reconstruction_error_by_alpha[a_try]) &&
        pmi_gram_min_eig_by_alpha[a_try] >= -1e-8 &&
        pmi_reconstruction_error_by_alpha[a_try] <= 1e-6
    println("PMI alpha=", a_try, ": ", st, " (", round(t_el, digits = 2), "s)")
    println("  primal=", pmi_primal_status[a_try], " dual=", pmi_dual_status[a_try],
            " Gram eigmin=", pmi_gram_min_eig_by_alpha[a_try],
            " reconstruction maxerr=", pmi_reconstruction_error_by_alpha[a_try],
            " numeric_check=", pmi_numeric_check_by_alpha[a_try])
end
if get(pmi_status, target_alpha, "MISSING") != "OPTIMAL"
    error("PMI certificate is not OPTIMAL at target alpha=$(target_alpha): ",
          get(pmi_status, target_alpha, "MISSING"))
end
write_pmi_gram_artifacts(pmi_block_registry[target_alpha], target_alpha)

scalar_status = Dict{Float64, String}()
scalar_primal_status = Dict{Float64, String}()
scalar_dual_status = Dict{Float64, String}()
function solve_scalar()
    for a_try in alpha_tries
        models, V0s, A1s, A2s, Q11s, Q12s, Q22s, Ds, pinits, plocs, pterms, mults_s = build_cert(a_try; pmi = false)
        t_el = @elapsed optimize!(models)
        st = termination_status(models)
        scalar_status[a_try] = string(st)
        scalar_primal_status[a_try] = model_status_string(primal_status, models)
        scalar_dual_status[a_try] = model_status_string(dual_status, models)
        println("scalar alpha=", a_try, ": ", st, " (", round(t_el, digits = 2), "s)")
        println("  primal=", scalar_primal_status[a_try],
                " dual=", scalar_dual_status[a_try])
        if st == MOI.OPTIMAL
            SCALAR_AUX_POLYS[] = (V = numpoly(V0s), A1 = numpoly(A1s), A2 = numpoly(A2s),
                                  D_elim = numpoly(Ds), pinit = numpoly(pinits),
                                  ploc = numpoly(plocs),
                                  pterm = pterms === nothing ? nothing : numpoly(pterms),
                                  multipliers = [(n = i, poly = numpoly(m[1]))
                                                 for (i, m) in enumerate(mults_s)])
            return (a_try, numpoly(V0s), numpoly(A1s), numpoly(A2s),
                    value(Q11s), value(Q12s), value(Q22s),
                    numpoly(Ds), numpoly(pinits), numpoly(plocs),
                    pterms === nothing ? nothing : numpoly(pterms))
        end
    end
    error("scalar certificate infeasible at all alpha tries")
end

function write_scalar_aux_artifacts()
    aux = SCALAR_AUX_POLYS[]
    aux === nothing && error("scalar auxiliary polynomial registry is empty")
    path = joinpath(@__DIR__, "routeB_certificate_multipliers.csv")
    open(path, "w") do io
        println(io, "polynomial,term,coefficient")
        entries = [("V", aux.V), ("A1", aux.A1), ("A2", aux.A2),
                   ("D_elim", aux.D_elim), ("pinit", aux.pinit), ("ploc", aux.ploc)]
        aux.pterm === nothing || push!(entries, ("pterm", aux.pterm))
        for (label, poly) in entries
            for trm in MultivariatePolynomials.terms(poly)
                mon = replace(string(MultivariatePolynomials.monomial(trm)), '"' => "'")
                coeff = Float64(MultivariatePolynomials.coefficient(trm))
                println(io, "\"", label, "\",\"", mon, "\",", coeff)
            end
        end
        for m in aux.multipliers
            for trm in MultivariatePolynomials.terms(m.poly)
                mon = replace(string(MultivariatePolynomials.monomial(trm)), '"' => "'")
                coeff = Float64(MultivariatePolynomials.coefficient(trm))
                println(io, "\"multiplier_", m.n, "\",\"", mon, "\",", coeff)
            end
        end
    end
    return path
end

alpha_star, V0n, A1n, A2n, Q11v, Q12v, Q22v, Dn, pinitn, plocn, ptermn = solve_scalar()
if alpha_star != target_alpha || get(scalar_status, target_alpha, "MISSING") != "OPTIMAL"
    error("scalar certificate selected alpha=$(alpha_star), expected OPTIMAL alpha=$(target_alpha)")
end
write_scalar_aux_artifacts()
println("alpha used: ", alpha_star)
Vn = V0n + A1n * dqa + A2n * dqb + 0.5 * (Q11v * dqa^2 + 2 * Q12v * dqa * dqb + Q22v * dqb^2)
println("storage V degree: ", maxdegree(Vn))

function write_solver_diagnostics()
    open(joinpath(@__DIR__, "routeB_certificate_solver_diagnostics.csv"), "w") do io
        println(io, "alpha,pmi_status,pmi_primal_status,pmi_dual_status,",
                "pmi_gram_min_eig,pmi_reconstruction_error,pmi_numeric_check,scalar_status,",
                "scalar_primal_status,scalar_dual_status")
        for a_try in alpha_tries
            println(io, join([a_try,
                              get(pmi_status, a_try, "MISSING"),
                              get(pmi_primal_status, a_try, "MISSING"),
                              get(pmi_dual_status, a_try, "MISSING"),
                              get(pmi_gram_min_eig_by_alpha, a_try, NaN),
                              get(pmi_reconstruction_error_by_alpha, a_try, NaN),
                              get(pmi_numeric_check_by_alpha, a_try, false),
                              get(scalar_status, a_try, "NOT_RUN"),
                              get(scalar_primal_status, a_try, "NOT_RUN"),
                              get(scalar_dual_status, a_try, "NOT_RUN")], ','))
        end
    end
end

function write_status_file()
    open(joinpath(@__DIR__, "routeB_certificate_status.csv"), "w") do io
        println(io, "alpha,pmi_status,scalar_status,pmi_primal_status,pmi_dual_status,",
                "pmi_gram_min_eig,pmi_reconstruction_error,pmi_numeric_check,scalar_primal_status,",
                "scalar_dual_status")
        for a_try in alpha_tries
            println(io, join([a_try,
                              get(pmi_status, a_try, "MISSING"),
                              get(scalar_status, a_try, "NOT_RUN"),
                              get(pmi_primal_status, a_try, "MISSING"),
                          get(pmi_dual_status, a_try, "MISSING"),
                          get(pmi_gram_min_eig_by_alpha, a_try, NaN),
                          get(pmi_reconstruction_error_by_alpha, a_try, NaN),
                          get(pmi_numeric_check_by_alpha, a_try, false),
                          get(scalar_primal_status, a_try, "NOT_RUN"),
                              get(scalar_dual_status, a_try, "NOT_RUN")], ','))
        end
    end
end

function write_manifest()
    coverage_completed = get(ENV, "ROUTEB_DIAGNOSTIC_ONLY", "0") != "1"
    open(joinpath(@__DIR__, "routeB_certificate_manifest.toml"), "w") do io
        println(io, "schema_version = \"routeB-certificate-manifest-v1\"")
        println(io, "evidence_level = \"empirical_plus_numerical_candidate\"")
        println(io, "coverage_completed = ", coverage_completed)
        println(io, "coverage_kind = \"trajectory_monte_carlo_only\"")
        println(io, "global_box_coverage = false")
        println(io, "run_timestamp_local = \"", Dates.now(), "\"")
        println(io, "julia_version = \"", VERSION, "\"")
        println(io, "certificate_source_sha256 = \"", sha256_file(@__FILE__), "\"")
        println(io, "dhport_source_sha256 = \"", sha256_file(joinpath(@__DIR__, "dhport_lib.jl")), "\"")
        println(io, "export_source_sha256 = \"", sha256_file(joinpath(@__DIR__, "routeB_export_traj.jl")), "\"")
        println(io, "project_toml_sha256 = \"", sha256_file(joinpath(@__DIR__, "ref_tssos_patched", "Project.toml")), "\"")
        println(io, "manifest_toml_sha256 = \"", sha256_file(joinpath(@__DIR__, "ref_tssos_patched", "Manifest.toml")), "\"")
        println(io, "mosek_bindir = \"", replace(get(ENV, "MOSEKBINDIR", ""), "\\" => "/"), "\"")
        println(io, "alpha_target = ", target_alpha)
        println(io, "alpha_selected = ", alpha_star)
        println(io, "eta_star = ", eta_star)
        println(io, "horizon_T = ", T)
        println(io, "initial_radius = ", R_init)
        println(io, "routeB_seed_1 = 20260840")
        println(io, "routeB_seed_2 = 20260841")
        println(io, "mc_polynomial_seed = 20260840")
        println(io, "coverage_samples_each = 500")
        println(io, "joint_block = \"4,5\"")
        println(io, "joint_limits = \"q1,q2=(-pi,pi); q3=(-5pi/6,5pi/6); q4,q5=(-pi,pi); q6=(-2pi,2pi)\"")
        println(io, "state_region = \"p=1.5*(q4^2+q5^2)+0.8*(dq4^2+dq5^2)<=5.6\"")
        println(io, "disturbance = \"w(t)=c*t, |c|<=sqrt(3)\"")
        println(io, "mass_regularizer = ", MASS_REGULARIZER)
        println(io, "coriolis_gravity_fd_step = ", CG_FINITE_DIFF_STEP)
        println(io, "dynamics_semantics = \"", DYNAMICS_SEMANTICS, "\"")
        if coverage_completed
            for (key, name) in (("V", "routeB_certificate_V.csv"),
                                ("verify", "routeB_certificate_verify.csv"),
                                ("status", "routeB_certificate_status.csv"),
                                ("solver_diagnostics", "routeB_certificate_solver_diagnostics.csv"),
                                ("multipliers", "routeB_certificate_multipliers.csv"),
                                ("pmi_gram", "routeB_pmi_gram_alpha12.csv"),
                                ("pmi_basis", "routeB_pmi_basis_alpha12.csv"),
                                ("pmi_basis_exponents", "routeB_pmi_basis_exponents_alpha12.csv"),
                                ("pmi_polynomial", "routeB_pmi_polynomial_alpha12.csv"),
                                ("pmi_gram_manifest", "routeB_pmi_gram_manifest.csv"))
                path = joinpath(@__DIR__, name)
                isfile(path) && println(io, key, "_output_sha256 = \"", sha256_file(path), "\"")
            end
        end
    end
end

write_solver_diagnostics()
write_status_file()
write_manifest()
if get(ENV, "ROUTEB_DIAGNOSTIC_ONLY", "0") == "1"
    println("ROUTEB_DIAGNOSTIC_ONLY=1: solver diagnostics written; skipping MC and trajectory stages")
    exit(0)
end

# ---- 2. MC verification of the certified polynomials ----
function mc_min(P, vranges; n::Int = 60000)
    vmin = Inf
    for _ in 1:n
        Q = P
        for (v, lo, hi) in vranges
            Q = subs(Q, v => lo + (hi - lo) * rand())
        end
        val = Q isa Number ? Float64(Q) :
              Float64(sum(JuMP.value.(MultivariatePolynomials.coefficients(Q))))
        vmin = min(vmin, val)
    end
    return vmin
end
println("--- certified-polynomial MC verification ---")
Random.seed!(20260840)
mD = mc_min(Dn, [(qa, -pi, pi), (qb, -pi, pi), (dqa, -3.0, 3.0), (dqb, -3.0, 3.0),
                  (t, -1.0, 2.0), (w, -5.0, 5.0)])
mI = mc_min(pinitn, [(qa, -pi, pi), (qb, -pi, pi), (dqa, -3.0, 3.0), (dqb, -3.0, 3.0)])
mL = mc_min(plocn, [(qa, -pi, pi), (qb, -pi, pi), (dqa, -3.0, 3.0), (dqb, -3.0, 3.0),
                    (t, -1.0, 2.0)])
mT = ptermn === nothing ? NaN :
     mc_min(ptermn, [(qa, -pi, pi), (qb, -pi, pi), (dqa, -3.0, 3.0), (dqb, -3.0, 3.0)])
println("MC min (60k, box domain): D_elim=", round(mD, digits = 5),
        " pinit=", round(mI, digits = 5), " ploc=", round(mL, digits = 5),
        " pterm=", ptermn === nothing ? "na" : round(mT, digits = 5))

# ---- 3/4. trajectory coverage + route-B bracket ratio ----
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
        a = Mq \ (tau - Cdq - Gq)
        q = q + dt * dq + 0.5 * dt^2 * a
        dq = dq + dt * a
        qs[:, k+1] = q
        dqs[:, k+1] = dq
    end
    return qs, dqs
end

function evalpoly_num(P, qv, dqv, tv, wv)
    Q = P
    Q = subs(Q, qa => qv[4], qb => qv[5], dqa => dqv[4], dqb => dqv[5], t => tv, w => wv)
    return Q isa Number ? Float64(Q) :
           Float64(sum(JuMP.value.(MultivariatePolynomials.coefficients(Q))))
end

function run_coverage(N::Int, cbound::Float64, seed::Int)
    Random.seed!(seed)
    tube_ok = 0
    term_ok = 0
    inlim_all = 0
    bracket_ratio_max = 0.0
    bracket_viol = 0.0
    a_c = (Kp + mgl) ./ I_val
    c_c = (b_fr + Kd) ./ I_val
    for kk in 1:N
        x = nothing
        while true
            u = randn(12); u ./= norm(u)
            r = R_init * rand()^(1 / 12)
            x = r .* u
            in_limits_q(x[1:6]) && break
        end
        q0 = x[1:6]; dq0 = x[7:12]
        cw = cbound * (2 * rand() - 1)
        qs, dqs = sim_traj(q0, dq0, cw)
        traj_inlim = true
        for k in 1:size(qs, 2)
            in_limits_q(qs[:, k]) || (traj_inlim = false; break)
        end
        traj_inlim || continue
        inlim_all += 1
        ok_tube = true
        ok_term = true
        for k in 1:size(qs, 2)
            tk = (k - 1) * 0.005
            wv = cw * tk
            Vv = evalpoly_num(Vn, qs[:, k], dqs[:, k], tk, wv)
            if Vv > R^2 * (tk^2 / T^2) + 1e-6
                ok_tube = false
            end
            pv = pw[1] * (qs[4, k]^2 + qs[5, k]^2) + pw[2] * (dqs[4, k]^2 + dqs[5, k]^2)
            if pv > eta_star + 1e-6
                ok_tube = false
            end
            # route-B residual-difference bracket ratio
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
            ratio = l2 / max(bound, 1e-12)
            bracket_ratio_max = max(bracket_ratio_max, ratio)
            bracket_viol = max(bracket_viol, l2 - bound)
        end
        qp_T = qw[1] * (qs[4, end]^2 + qs[5, end]^2) + qw[2] * (dqs[4, end]^2 + dqs[5, end]^2)
        if isfinite(alpha_star) && qp_T > alpha_star + 1e-6
            ok_term = false
        end
        tube_ok += ok_tube ? 1 : 0
        term_ok += ok_term ? 1 : 0
    end
    println("MC N=", N, " c_bound=", round(cbound, digits = 3),
            ": in-limits ", inlim_all, "/", N,
            ", tube ", tube_ok, "/", inlim_all,
            ", terminal ", term_ok, "/", inlim_all,
            ", max route-B bracket ratio = ", round(bracket_ratio_max, digits = 4),
            ", max bracket violation = ", bracket_viol)
    return (inlim = inlim_all, tube = tube_ok, term = term_ok,
            ratio = bracket_ratio_max, viol = bracket_viol)
end

println("--- trajectory coverage + route-B bracket ---")
r1 = run_coverage(500, sqrt(3) * 0.2, 20260840)
r2 = run_coverage(500, sqrt(3), 20260841)

# ---- 5. save the certificate package ----
open(joinpath(@__DIR__, "routeB_certificate_V.csv"), "w") do io
    writedlm(io, ["coeff" "e_qa" "e_qb" "e_dqa" "e_dqb" "e_t"], ',')
    for term in MultivariatePolynomials.terms(Vn)
        cf = MultivariatePolynomials.coefficient(term)
        mon = MultivariatePolynomials.monomial(term)
        z = mon.z
        # variables of Vn: subset of (qa,qb,dqa,dqb,t) -- map by order
        vpol = MultivariatePolynomials.variables(mon)
        ex = zeros(Int, 5)
        for (kk, v) in enumerate(vpol)
            idx = v == qa ? 1 : v == qb ? 2 : v == dqa ? 3 : v == dqb ? 4 : 5
            ex[idx] = z[kk]
        end
        writedlm(io, [[Float64(cf); ex]], ',')
    end
end
open(joinpath(@__DIR__, "routeB_certificate_verify.csv"), "w") do io
    writedlm(io, ["item" "value"], ',')
    writedlm(io, [["lam1" lam1]], ',')
    writedlm(io, [["lam2" lam2]], ',')
    writedlm(io, [["lam3" lam3]], ',')
    writedlm(io, [["lam2p_routeB" lam2p]], ',')
    writedlm(io, [["lam3p_routeB" lam3p]], ',')
    writedlm(io, [["Wpart_routeB" Wpart]], ',')
    writedlm(io, [["lam1p_routeB" lam1p]], ',')
    writedlm(io, [["alpha" alpha_star]], ',')
    writedlm(io, [["mc_min_D" mD]], ',')
    writedlm(io, [["mc_min_pinit" mI]], ',')
    writedlm(io, [["mc_min_ploc" mL]], ',')
    writedlm(io, [["mc_min_pterm" mT]], ',')
    writedlm(io, [["coverage_0.346_inlim" r1.inlim]], ',')
    writedlm(io, [["coverage_0.346_tube" r1.tube]], ',')
    writedlm(io, [["coverage_0.346_term" r1.term]], ',')
    writedlm(io, [["coverage_0.346_ratio" r1.ratio]], ',')
    writedlm(io, [["coverage_1.732_inlim" r2.inlim]], ',')
    writedlm(io, [["coverage_1.732_tube" r2.tube]], ',')
    writedlm(io, [["coverage_1.732_term" r2.term]], ',')
    writedlm(io, [["coverage_1.732_ratio" r2.ratio]], ',')
end
open(joinpath(@__DIR__, "routeB_certificate.log"), "w") do io
    println(io, "route-B final certificate package (empirical level)")
    println(io, "block (4,5), finite-sample gain estimates lam1=", lam1,
            " lam2=", lam2, " lam3=", lam3)
    println(io, "eta=5.6, alpha=", alpha_star, ", s_res=5, degV0=4, degA=1, q4/q5 limits")
    println(io, "scalar alpha=", target_alpha, ": ", scalar_status[target_alpha],
            "; PMI alpha=", target_alpha, ": ", pmi_status[target_alpha])
    println(io, "PMI primal=", pmi_primal_status[target_alpha],
            " dual=", pmi_dual_status[target_alpha],
            " Gram eigmin=", pmi_gram_min_eig_by_alpha[target_alpha],
            " reconstruction maxerr=", pmi_reconstruction_error_by_alpha[target_alpha],
            " numeric_check=", pmi_numeric_check_by_alpha[target_alpha])
    println(io, "scalar primal=", scalar_primal_status[target_alpha],
            " dual=", scalar_dual_status[target_alpha])
    println(io, "certified-polynomial MC minima (60k, box domain x wide ranges):")
    println(io, "  D_elim=", mD, " pinit=", mI, " ploc=", mL, " pterm=", mT)
    println(io, "route-B bracket constants (sf=2): lam2p=", lam2p,
            " lam3p=", lam3p, " Wpart=", Wpart, " lam1p=", lam1p)
    println(io, "coverage c=0.346: in-limits ", r1.inlim, " tube ", r1.tube,
            " terminal ", r1.term, " max bracket ratio ", r1.ratio)
    println(io, "coverage c=1.732: in-limits ", r2.inlim, " tube ", r2.tube,
            " terminal ", r2.term, " max bracket ratio ", r2.ratio)
end
write_manifest()
println("saved routeB_certificate_V.csv / routeB_certificate_verify.csv / routeB_certificate.log / routeB_certificate_status.csv / routeB_certificate_manifest.toml")
