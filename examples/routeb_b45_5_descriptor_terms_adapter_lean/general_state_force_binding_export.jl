#!/usr/bin/env julia

"""Minimal general-state exporter for the B45-5 source-binding seam.

This file is an executable contract, not a theorem and not a tau-equivalence
claim.  It must be run with Julia from the canonical source environment.
"""

using LinearAlgebra
using Random
using SHA
using Dates

const WORKFLOW_ROOT = normpath(joinpath(@__DIR__, "..", "..", ".."))
const DHPORT_PATH = joinpath(WORKFLOW_ROOT, "6dof_sos_optimized", "6dof_sos_optimized",
                            "robot_final", "dhport_lib.jl")
include(DHPORT_PATH)

const B = [4, 5]
const D = [1, 2, 3, 6]
const SEED = 20260907
const SAMPLE_COUNT = 16
const TOL = 1e-12
const OUT_DIR = joinpath(@__DIR__, "output", "general-state-export-20260907")
const CSV_OUT = joinpath(OUT_DIR, "force_binding_states.csv")
const RECEIPT_OUT = joinpath(OUT_DIR, "FORCE_BINDING_RECEIPT.md")

function expected_source_force_B(q, dq, w, c, g, g0)
    # This is the exact-real interface instantiated from the deployed B rows;
    # c/g/g0 are exported from the same arm_MCG calls as rhs.
    return [
        -Kp[4] * q[4] - (Kd[4] + b_fr[4]) * dq[4] + (gw_coef[4] * I_val[4]) * w + g0[4] - c[4] - g[4],
        -Kp[5] * q[5] - (Kd[5] + b_fr[5]) * dq[5] + (gw_coef[5] * I_val[5]) * w + g0[5] - c[5] - g[5],
    ]
end

function csv_row(idx, q, dq, w, c, g, g0, tau, rhs, a, Mq, desc, e1, e2)
    return Any[
        idx, q[4], q[5], dq[4], dq[5], w,
        c[4], c[5], g[4], g[5], g0[4], g0[5],
        tau[4], tau[5], rhs[4], rhs[5], rhs[4], rhs[5],
        a[4], a[5], a[1], a[2], a[3], a[6],
        Mq[4, 4], Mq[4, 5], Mq[5, 4], Mq[5, 5],
        Mq[4, 1], Mq[4, 2], Mq[4, 3], Mq[4, 6],
        Mq[5, 1], Mq[5, 2], Mq[5, 3], Mq[5, 6],
        desc[1], desc[2], e1[1], e1[2], e2[1], e2[2],
    ]
end

mkpath(OUT_DIR)
Random.seed!(SEED)
states = Tuple{Vector{Float64}, Vector{Float64}, Float64}[]
push!(states, (zeros(6), zeros(6), 0.0))
for _ in 2:SAMPLE_COUNT
    q = 0.08 .* randn(6)
    dq = 0.08 .* randn(6)
    w = sqrt(3.0) * (2rand() - 1)
    push!(states, (q, dq, w))
end

G0 = arm_MCG(zeros(6), zeros(6))[3]
rows = Any[]
e1_rows = Vector{Vector{Float64}}()
e2_rows = Vector{Vector{Float64}}()

for (idx, (q, dq, w)) in enumerate(states)
    Mq, Cdq, Gq = arm_MCG(q, dq)
    tau = -Kp .* q - (Kd + b_fr) .* dq + G0 + (gw_coef .* I_val) .* w
    rhs = tau - Cdq - Gq
    a = Mq \ rhs

    cB = Cdq[B]
    gB = Gq[B]
    g0B = G0[B]
    expectedB = expected_source_force_B(q, dq, w, Cdq, Gq, G0)
    sourceBlockForce = rhs[B]

    MqBB = Mq[B, B]
    MqBD = Mq[B, D]
    descriptorB = MqBB * a[B] + MqBD * a[D]
    e1 = sourceBlockForce - expectedB
    e2 = sourceBlockForce - descriptorB
    push!(e1_rows, e1)
    push!(e2_rows, e2)
    push!(rows, csv_row(idx, q, dq, w, Cdq, Gq, G0, tau, rhs, a, Mq,
                        descriptorB, e1, e2))
end

header = [
    "sample", "q4", "q5", "dq4", "dq5", "w",
    "CdqB4", "CdqB5", "GqB4", "GqB5", "G0B4", "G0B5",
    "tauB4", "tauB5", "rhsB4", "rhsB5",
    "sourceBlockForce4", "sourceBlockForce5", "aB4", "aB5",
    "aD1", "aD2", "aD3", "aD6",
    "MqBB11", "MqBB12", "MqBB21", "MqBB22",
    "MqBD41", "MqBD42", "MqBD43", "MqBD46",
    "MqBD51", "MqBD52", "MqBD53", "MqBD56",
    "sourceDescriptorRhs4", "sourceDescriptorRhs5",
    "E1_4", "E1_5", "E2_4", "E2_5",
]

open(CSV_OUT, "w") do io
    println(io, join(header, ','))
    for row in rows
        println(io, join(string.(row), ','))
    end
end

max_e1 = maximum(maximum(abs.(e)) for e in e1_rows)
max_e2 = maximum(maximum(abs.(e)) for e in e2_rows)
status = max(max_e1, max_e2) <= TOL ? "PASS_RUNTIME_FLOAT64" : "FAIL_RUNTIME_FLOAT64"
source_sha = bytes2hex(SHA.sha256(read(DHPORT_PATH)))
exporter_sha = bytes2hex(SHA.sha256(read(@__FILE__)))

open(RECEIPT_OUT, "w") do io
    println(io, "# B45-5 general-state force binding export")
    println(io)
    println(io, "- status: `", status, "`")
    println(io, "- generated_at_utc: `", Dates.format(now(UTC), dateformat"yyyy-mm-ddTHH:MM:SSZ"), "`")
    println(io, "- source: `", DHPORT_PATH, "`")
    println(io, "- source_sha256: `", source_sha, "`")
    println(io, "- exporter_sha256: `", exporter_sha, "`")
    println(io, "- seed: `", SEED, "`; samples: `", length(states), "`")
    println(io, "- B order: `[4,5]`; D order: `[1,2,3,6]`")
    println(io, "- mass_regularizer: `", MASS_REGULARIZER, "`; fd_step: `", CG_FINITE_DIFF_STEP, "`")
    println(io, "- max E1 residual: `", max_e1, "`")
    println(io, "- max E2 residual: `", max_e2, "`")
    println(io, "- CSV: `", CSV_OUT, "`")
    println(io)
    println(io, "`sourceBlockForce` is exported as `rhs[B]`. `sourceDescriptorRhs` is")
    println(io, "exported as `Mq[B,B]*a[B] + Mq[B,D]*a[D]` from the same state and solve.")
    println(io, "E1 is `sourceBlockForce - expectedSourceForce`; E2 is")
    println(io, "`sourceBlockForce - sourceDescriptorRhs` componentwise.")
    println(io)
    println(io, "This receipt is runtime/source-binding evidence only. It does not claim")
    println(io, "a Float64-to-exact-real theorem, a deployed-tau equivalence, or registry")
    println(io, "promotion.")
end

println("GENERAL_STATE_FORCE_BINDING_EXPORT_STATUS=", status)
println("CSV_OUT=", CSV_OUT)
println("RECEIPT_OUT=", RECEIPT_OUT)
println("SOURCE_SHA256=", source_sha)
println("EXPORTER_SHA256=", exporter_sha)
println("MAX_E1=", max_e1)
println("MAX_E2=", max_e2)
