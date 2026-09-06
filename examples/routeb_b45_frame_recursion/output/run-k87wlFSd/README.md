# B45-1.2 frame recursion

This sidecar formalizes the smallest reusable parent-axis/current-step
contract for the Route-B DH chain.  `prefixFrames` records the current parent
frame first and updates the parent by exact left multiplication:

`parent, current, ...  ↦  parent :: prefixFrames (parent * current) ...`

`routeBStepMatrix` instantiates the step with the exact phase, alpha, `a`, and
`d` constants already formalized in
`examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean`.  The final
product theorem shows that the last frame is the parent multiplied by the
finite step product in the declared order.

Evidence level: `COMPILED_CANDIDATE_COMPARATOR_PENDING`.  This is an exact
matrix-recursion theorem; it does not yet bind the Julia `Float64` transform,
COM/Jacobian conventions, frame-axis indexing in the source implementation,
or the full mass function.
