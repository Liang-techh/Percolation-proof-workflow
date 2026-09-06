# Route-B source contract adapter

This narrow adapter is the first source-binding layer after the compiled
kinematic contract core. It consumes the already verified fixed frame-slot
bridge and proves equality of the source origin/axis functions with a
frame-slot contract. It then lifts those equalities to body mass through the
contract-core congruence theorem.

It intentionally does not unfold DH entries, Julia `Float64`, trigonometric
machine semantics, or the full six-body mass evaluator.
