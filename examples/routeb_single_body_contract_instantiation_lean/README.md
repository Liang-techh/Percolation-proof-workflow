# Route-B single-body contract instantiation

This leaf specializes the source/frame kinematic contract to the two
block-(4,5) bodies. It closes the generic inactive link-4 and active link-5
Jacobian cutoffs and lifts the source/frame contract equality to each body
mass separately. It does not expand DH entries or claim a Float64/full-mass
binding.
