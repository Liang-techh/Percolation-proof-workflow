# Route-B finite frame-prefix index leaf

This sidecar expands the recursive six-step Route-B frame chain into an
explicit seven-frame prefix list and proves equality with the source-level
recursion. It is intentionally separate from body-mass theorems so downstream
indexed lemmas do not carry a dependent `List.length` proof through every
elaboration.
