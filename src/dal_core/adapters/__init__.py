"""dal_core adapters package.

This namespace hosts adapter implementations that bridge the constitutional
algebra (which never executes models) and external ML runtimes. Every
subpackage here is governed by its own carve-out document; the strict
default is "no model execution under ``dal_core``".

Current subpackages:
    - ``t5``: First real T5 Input/Output adapter (inference only).
      See ``docs/T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`` for the
      constitutional carve-out and ``docs/T5_REAL_ADAPTER.md`` for usage.
"""
