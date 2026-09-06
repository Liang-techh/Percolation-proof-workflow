# Minimal origins/axes contract core

This Mathlib-only layer defines the one-way kinematic contract consumed by
body semantics: seven origins and six joint axes. It proves congruence lifting
from contract functions to Jv, Jw, and body mass, plus the block-(4,5)
inactive/active cutoffs. Source adapters only need to establish the two
function equalities; they do not import frame or DH definitions.
