# Fixture Import Hygiene (PR #156)

## Constitutional Purpose

Enforce clean import patterns in test fixtures to maintain:
- Reproducible test execution
- Clear module boundaries
- No runtime sys.path mutation
- Standard Python package imports

## Problem Statement (من PR #155)

PR #155 implemented Golden No-Op Adapter Chain Fixtures successfully, but left a minor technical debt:

```python
# tests/fixtures/dal_core/golden_noop_adapter_chains.py (BEFORE PR #156)
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from noop_adapter_fixtures import ...
```

This pattern works but:
- Modifies sys.path at import time (side effect)
- Less clean than standard package imports
- Requires tests to also modify sys.path
- Harder to reason about import resolution

## Solution (PR #156)

### Change 1: Remove sys.path.insert from golden_noop_adapter_chains.py

**Before:**
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from noop_adapter_fixtures import (
    AdapterChainLink,
    AdapterChainRegistry,
    ...
)
```

**After:**
```python
from tests.fixtures.dal_core.noop_adapter_fixtures import (
    AdapterChainLink,
    AdapterChainRegistry,
    ...
)
```

### Change 2: Remove sys.path.insert from test_golden_noop_adapter_chains.py

**Before:**
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../fixtures/dal_core'))

from golden_noop_adapter_chains import (
    GoldenNoOpChainFixture,
    ...
)

from noop_adapter_fixtures import (
    NoOpInputAdapter,
    ...
)
```

**After:**
```python
from tests.fixtures.dal_core.golden_noop_adapter_chains import (
    GoldenNoOpChainFixture,
    ...
)

from tests.fixtures.dal_core.noop_adapter_fixtures import (
    NoOpInputAdapter,
    ...
)
```

### Change 3: Add Test for Import Hygiene

New test in `test_golden_noop_adapter_chains.py`:

```python
def test_fixture_files_do_not_modify_sys_path():
    """
    Verify fixture files do NOT modify sys.path.

    Constitutional Requirement (PR #156):
        Fixture imports MUST use package paths, NOT sys.path mutation.
    """
    import golden_noop_adapter_chains
    import noop_adapter_fixtures

    # Read source files
    import inspect
    golden_source = inspect.getsource(golden_noop_adapter_chains)
    noop_source = inspect.getsource(noop_adapter_fixtures)

    # Check that sys.path.insert is NOT present in executable code
    for source, module_name in [(golden_source, "golden_noop_adapter_chains"),
                                  (noop_source, "noop_adapter_fixtures")]:
        lines = source.split('\n')
        in_docstring = False
        for line_num, line in enumerate(lines, 1):
            # Track docstring state
            if '"""' in line:
                in_docstring = not in_docstring
                continue
            if in_docstring:
                continue

            # Skip comment lines
            if line.strip().startswith('#'):
                continue

            # Check for sys.path.insert in executable code
            if 'sys.path.insert' in line:
                pytest.fail(
                    f"Found sys.path.insert in {module_name}:{line_num}\n"
                    f"Line: {line}\n"
                    f"Constitutional Requirement: Fixture imports MUST use package paths"
                )
```

## Verification

Run verification:
```bash
PYTHONPATH=src python3 -c "
from tests.fixtures.dal_core.golden_noop_adapter_chains import all_golden_noop_chain_fixtures
fixtures = all_golden_noop_chain_fixtures()
print(f'✓ Successfully imported {len(fixtures)} golden fixtures')
print(f'✓ No sys.path.insert needed')
"
```

Expected output:
```
✓ Successfully imported 6 golden fixtures
✓ No sys.path.insert needed
```

## Adapter Boundary Patterns

### Pattern 1: Fixture Modules (tests/fixtures/*)

**Location:** `tests/fixtures/dal_core/`

**Import Pattern:**
```python
# From production code
from dal_core.training_example import TrainingExample
from dal_core.t5_adapter_interface_contracts import AdapterInput

# From other fixtures (same package)
from tests.fixtures.dal_core.noop_adapter_fixtures import NoOpInputAdapter
```

**Constitutional Rules:**
- ✅ Import from `dal_core` (production contracts)
- ✅ Import from `tests.fixtures.dal_core` (peer fixtures)
- ❌ NO sys.path mutation
- ❌ NO relative imports across fixture/test boundary

### Pattern 2: Test Modules (tests/dal_core/*)

**Location:** `tests/dal_core/`

**Import Pattern:**
```python
# From production code
from dal_core.training_example import TrainingExample

# From fixtures
from tests.fixtures.dal_core.golden_noop_adapter_chains import (
    GoldenNoOpChainFixture,
    all_golden_noop_chain_fixtures,
)
```

**Constitutional Rules:**
- ✅ Import from `dal_core` (production code)
- ✅ Import from `tests.fixtures.dal_core` (fixtures)
- ❌ NO sys.path mutation
- ❌ NO relative imports

### Pattern 3: Production Code (src/dal_core/*)

**Location:** `src/dal_core/`

**Import Pattern:**
```python
# Only internal imports
from dal_core.other_module import SomeClass
```

**Constitutional Rules:**
- ✅ Import from `dal_core` only
- ❌ NEVER import from `tests`
- ❌ NEVER import from `tests.fixtures`
- ❌ Production code MUST NOT know about test fixtures

## PYTHONPATH Setup

For tests to run correctly:
```bash
export PYTHONPATH=src:$PWD
```

This allows:
- `import dal_core` → resolves to `src/dal_core`
- `import tests.fixtures.dal_core` → resolves to `tests/fixtures/dal_core`

## Constitutional Laws

1. **No sys.path mutation in fixtures:** Fixture modules MUST use standard package imports
2. **No sys.path mutation in tests:** Test modules MUST use standard package imports
3. **Unidirectional imports:** Production → (never) → Tests/Fixtures
4. **Clear boundaries:** Tests may import fixtures; fixtures may import production; production NEVER imports tests

## Benefits

✅ **Reproducibility:** No side effects at import time
✅ **Clarity:** Import paths show exact module location
✅ **Maintainability:** Standard Python package patterns
✅ **Testability:** New test guards against regression

## Migration from sys.path.insert Pattern

If you find code using:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from some_module import Something
```

Replace with:
```python
from tests.fixtures.dal_core.some_module import Something
# or
from dal_core.some_module import Something
```

Depending on whether `some_module` is a fixture or production code.

## Related PRs

- **PR #152:** T5 Adapter Interface Contracts (contracts only, no execution)
- **PR #153:** No-Op Adapter Fixtures (fixture implementation, no execution)
- **PR #155:** Golden No-Op Adapter Chain Fixtures (golden test data)
- **PR #156:** Fixture Import Hygiene (this PR - cleanup sys.path usage)

## Next Steps

**NOT recommended yet:**
- ❌ Hugging Face integration
- ❌ T5 tokenization
- ❌ Real model execution

**Recommended next:**
- ✅ Adapter boundary review
- ✅ Constitutional guard hardening
- ✅ Additional golden fixtures for edge cases

---

**Created:** 2026-05-29
**Purpose:** Document import hygiene improvements from PR #156
**Status:** Complete - All sys.path.insert patterns removed from fixtures
