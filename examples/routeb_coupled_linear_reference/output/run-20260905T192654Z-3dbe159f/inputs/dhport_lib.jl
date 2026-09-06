# dhport_lib.jl -- Julia port of arm_MCG.m + work27 parameters (shared by
# the stage-11 scripts).  Include-only; do not run standalone.
using LinearAlgebra

L = [0.10; 0.08; 0.21; 0.19; 0.05; 0.07]
DH = [0.0 0.10 0.08 -pi/2;
      -pi/2 0.0 0.21 0.0;
      pi/2 0.05 0.0 pi/2;
      0.0 0.19 0.0 -pi/2;
      0.0 0.0 0.0 pi/2;
      0.0 0.07 0.0 0.0]
m = [1.0, 0.8, 0.6, 0.4, 0.3, 0.15]
I_val = [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
Kp = [1.0, 0.8, 0.7, 0.6, 0.5, 0.4]
Kd = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
b_fr = [0.5, 0.4, 0.35, 0.3, 0.25, 0.2]
gw_coef = [1.0, 0.5, 0.3, 0.2, 0.1, 0.05] ./ I_val
mgl = [0.8, 0.5, 0.3, 0.15, 0.08, 0.03]
p_w = [1.5, 0.8]
eta_ref = 0.81

# The numerical Route-B port has two deliberately explicit semantics knobs.
# The default retains the historical 1e-6 mass regularization so existing
# certificates remain reproducible; a strict DH-chain audit can call
# `mass_matrix(q; regularization=0.0)` / `arm_MCG(...; mass_regularization=0.0)`
# and must record that choice in its manifest.
const MASS_REGULARIZER = 1e-6
const CG_FINITE_DIFF_STEP = 1e-5
const DYNAMICS_SEMANTICS = "DH-chain M with explicit mass regularizer; C/G central finite differences"

function fk_frames(q)
    Tc = [Matrix{Float64}(I, 4, 4)]
    o = zeros(3, 7)
    z = zeros(3, 6)
    for ii in 1:6
        z[:, ii] = Tc[end][1:3, 3]
        th = q[ii] + DH[ii, 1]; d = DH[ii, 2]; a = DH[ii, 3]; al = DH[ii, 4]
        ct, st, ca, sa = cos(th), sin(th), cos(al), sin(al)
        A = [ct -st*ca st*sa a*ct; st ct*ca -ct*sa a*st; 0 sa ca d; 0 0 0 1]
        push!(Tc, Tc[end] * A)
        o[:, ii+1] = Tc[end][1:3, 4]
    end
    return Tc, o, z
end

function mass_matrix(q; regularization::Real = MASS_REGULARIZER)
    Tc, o, z = fk_frames(q)
    M = zeros(6, 6)
    for ii in 1:6
        pcom = 0.5 .* (o[:, ii] + o[:, ii+1])
        Ri = Tc[ii+1][1:3, 1:3]
        Ii = (I_val[ii] / 3) .* Matrix{Float64}(I, 3, 3)
        Jv = zeros(3, 6); Jw = zeros(3, 6)
        for jj in 1:ii
            Jv[:, jj] = cross(z[:, jj], pcom - o[:, jj])
            Jw[:, jj] = z[:, jj]
        end
    M += m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw
    end
    return M + Float64(regularization) .* Matrix{Float64}(I, 6, 6)
end

function potential(q)
    _, o = fk_frames(q)
    P = 0.0
    for ii in 1:6
        pcom = 0.5 .* (o[:, ii] + o[:, ii+1])
        P += m[ii] * 9.81 * pcom[3]
    end
    return P
end

function arm_MCG(q, dq; mass_regularization::Real = MASS_REGULARIZER,
                 fd_step::Real = CG_FINITE_DIFF_STEP)
    Mq = mass_matrix(q; regularization = mass_regularization)
    h = Float64(fd_step)
    dM = zeros(6, 6, 6)
    for kk in 1:6
        qp = copy(q); qp[kk] += h
        qm = copy(q); qm[kk] -= h
        dM[:, :, kk] = (mass_matrix(qp; regularization = mass_regularization) -
                        mass_matrix(qm; regularization = mass_regularization)) ./ (2h)
    end
    Cdq = zeros(6)
    for ii in 1:6
        acc = 0.0
        for jj in 1:6, kk in 1:6
            cijk = 0.5 * (dM[ii, jj, kk] + dM[ii, kk, jj] - dM[jj, kk, ii])
            acc += cijk * dq[jj] * dq[kk]
        end
        Cdq[ii] = acc
    end
    Gq = zeros(6)
    for kk in 1:6
        qp = copy(q); qp[kk] += h
        qm = copy(q); qm[kk] -= h
        Gq[kk] = (potential(qp) - potential(qm)) / (2h)
    end
    return Mq, Cdq, Gq
end

function exact_ddq(q, dq, w; mass_regularization::Real = MASS_REGULARIZER,
                   fd_step::Real = CG_FINITE_DIFF_STEP)
    Mq, Cdq, Gq = arm_MCG(q, dq; mass_regularization = mass_regularization,
                           fd_step = fd_step)
    _, _, G0v = arm_MCG(zeros(6), zeros(6);
                        mass_regularization = mass_regularization, fd_step = fd_step)
    tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w
    return Mq \ (tau - Cdq - Gq)
end
