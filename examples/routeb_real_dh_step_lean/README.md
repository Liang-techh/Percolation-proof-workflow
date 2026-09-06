# Route-B ideal-real DH step bridge

This sidecar proves the exact entrywise bridge between the six complex
Fourier DH step matrices and explicit real DH step matrices.  It reuses the
pinned Laurent-to-exponential phase bridge and the exact Route-B parameters.

It is deliberately below the deployed-source boundary: it does not prove
Julia `Float64` equality, frame recursion, axis/origin extraction, COM/Jacobian
semantics, or the full mass identity.  Those remain separate obligations.
