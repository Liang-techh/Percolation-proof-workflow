# Minimal body-semantic core

This module contains the reusable mathematical core for body COM/Jacobian and
link-mass semantics. It imports only `Mathlib`, so frame/source adapters can be
compiled separately without re-elaborating DH matrices or dependent list
indices. It includes the block-(4,5) inactive/active cutoff lemmas.

It is an ideal semantic module and does not claim source or Float64 equality.
