# Attempt history

## 2026-09-06 — run-FN4YFKjZ

The four-theorem source adapter was written over the Mathlib-only body core
and the verified frame-slot bridge. The initial run was stopped after the
elaboration memory budget began growing.

## 2026-09-06 — run-Qkh7N6kR

The recursive `#print axioms` commands were removed to avoid dependency
traversal. The adapter still exceeded the practical narrow-leaf compile
budget after about five minutes, so it was stopped. No theorem was admitted
and no persistent state changed. The core and slot artifacts remain the
authoritative verified prerequisites.

## 2026-09-06 — run-ZVjs6CKr

The adapter proof wrappers were changed to `simpa only` so only the outer Jv/Jw
definitions could unfold. Elaboration still exceeded the practical narrow-leaf
budget after about four minutes. The run was stopped; no theorem or registry
entry was created.
