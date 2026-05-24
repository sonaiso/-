# ALGEBRA KERNEL CONSTITUTION

`fvafk.algebra` is the repository's constitutional kernel.

It is the single source of truth for the governing algebra declared in
`/home/runner/work/-/-/src/fvafk/algebra/__init__.py`:

> لا مخرج عارٍ.  
> Every Result = value + rank + evidence + residuals + failures + replay.

## Constitutional rules

1. No `Rank` outside `fvafk.algebra.Rank`.
2. No `Result` outside `fvafk.algebra.Result`.
3. No `Evidence` outside `fvafk.algebra.Evidence`.
4. No `Residual` outside `fvafk.algebra.Residual`.
5. No `Failure` outside `fvafk.algebra.Failure`.
6. No `Trace` outside `fvafk.algebra.Trace`.
7. Every governed output must be `Result[T]` or be losslessly liftable into `Result[T]`.

## Lossless liftability

Types such as inspection reports, workflow decisions, and audit outcomes are
not parallel result systems. They are domain values carried inside
`Result[T]`, or transitional adapters that can be lifted into `Result[T]`
without dropping rank, evidence, residuals, failures, or replay/trace data.

## Migration note

Legacy or domain-local adapters that still spell `Rank`, `Evidence`,
`Residual`, or related kernel names must migrate to `fvafk.algebra` imports.
If a temporary adapter must remain, it must:

- reference this constitution explicitly,
- document why migration is not yet complete,
- keep a removal plan,
- avoid becoming a new governing source of truth.

Any historical `gfa.governance.Rank`-style construct, or any other parallel
kernel naming, must migrate to `fvafk.algebra.Rank` or a documented adapter
that is scheduled for removal.
