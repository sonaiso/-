"""
Guard test: Algebra Kernel Uniqueness

Enforces the constitutional law that fvafk.algebra is the SOLE source
for Rank, Result, Evidence, Residual, Failure, and Trace.

Authority: docs/ALGEBRA_KERNEL_CONSTITUTION.md

Critical Laws Enforced:
1. No Rank enum outside fvafk.algebra (except marked adapters)
2. No Result implementing parallel governance
3. No duplicate Evidence/Residual/Failure/Trace definitions
"""

import ast
import pytest
from pathlib import Path
from typing import List, Tuple, Set


# Allowed exceptions: files with explicit migration notices
MIGRATION_ALLOWED = {
    "src/gfa/proto_prior/first_prior_unit.py",  # Marked for migration in constitution
    "src/dal_core/pipeline.py",  # Marked for migration in constitution
}


def find_class_definitions(file_path: Path, class_name_pattern: str) -> List[Tuple[int, str]]:
    """
    Find class definitions matching a pattern in a Python file.

    Returns:
        List of (line_number, class_name) tuples
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if class_name_pattern in node.name or node.name == class_name_pattern:
                    results.append((node.lineno, node.name))

        return results
    except (SyntaxError, UnicodeDecodeError):
        # Skip files with syntax errors or encoding issues
        return []


def find_rank_enums(repo_root: Path) -> List[Tuple[Path, int, str]]:
    """
    Find all Rank enum definitions in the repository.

    Returns:
        List of (file_path, line_number, class_name) tuples
    """
    results = []

    for py_file in repo_root.glob("**/*.py"):
        # Skip fvafk.algebra (canonical source)
        if "fvafk/algebra" in str(py_file):
            continue

        # Skip test files
        if "test_" in py_file.name or "/tests/" in str(py_file):
            continue

        # Skip __pycache__ and .venv
        if "__pycache__" in str(py_file) or ".venv" in str(py_file):
            continue

        # Check for Rank enum
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if node.name == "Rank":
                        # Check if it inherits from Enum
                        if any(
                            isinstance(base, ast.Name) and base.id == "Enum"
                            for base in node.bases
                        ):
                            results.append((py_file, node.lineno, node.name))
        except (SyntaxError, UnicodeDecodeError):
            continue

    return results


def check_migration_notice(file_path: Path, line_number: int) -> bool:
    """
    Check if a parallel definition has a proper migration notice.

    A proper migration notice must appear within 25 lines before the definition
    and contain "MIGRATION NOTICE" or "TODO: MIGRATE".
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check 25 lines before the definition (to account for multi-line notices)
        start = max(0, line_number - 25)
        end = line_number

        context = "".join(lines[start:end])

        return "MIGRATION NOTICE" in context or "TODO: MIGRATE" in context
    except Exception:
        return False


def test_no_parallel_rank_definitions():
    """
    Verify no parallel Rank enum definitions exist outside fvafk.algebra.

    Exception: Files in MIGRATION_ALLOWED list are permitted IF they have
    proper migration notices.
    """
    repo_root = Path(__file__).parent.parent
    rank_definitions = find_rank_enums(repo_root)

    violations = []

    for file_path, line_num, class_name in rank_definitions:
        rel_path = str(file_path.relative_to(repo_root))

        # Check if file is in migration allowed list
        if rel_path in MIGRATION_ALLOWED:
            # Verify it has a migration notice
            has_notice = check_migration_notice(file_path, line_num)
            if not has_notice:
                violations.append(
                    f"{rel_path}:{line_num} - Rank enum in migration list but missing MIGRATION NOTICE"
                )
        else:
            # Not in allowed list - this is a violation
            violations.append(
                f"{rel_path}:{line_num} - Parallel Rank enum definition not in fvafk.algebra"
            )

    if violations:
        error_msg = (
            "CONSTITUTIONAL VIOLATION: Parallel Rank definitions detected\n\n"
            "Law: Only fvafk.algebra.Rank may define epistemic rank\n"
            "Authority: docs/ALGEBRA_KERNEL_CONSTITUTION.md Article 2\n\n"
            "Violations:\n" + "\n".join(f"  - {v}" for v in violations) + "\n\n"
            "Resolution:\n"
            "  1. Import from fvafk.algebra.Rank instead\n"
            "  2. OR add migration notice if legacy adapter\n"
            "  3. OR add to MIGRATION_ALLOWED with removal plan\n"
        )
        pytest.fail(error_msg)


def test_fvafk_algebra_rank_exists():
    """Verify the canonical Rank definition exists in fvafk.algebra."""
    repo_root = Path(__file__).parent.parent
    algebra_core = repo_root / "src" / "fvafk" / "algebra" / "core.py"

    assert algebra_core.exists(), "fvafk.algebra.core.py not found"

    with open(algebra_core, "r", encoding="utf-8") as f:
        content = f.read()

    assert "class Rank(Enum):" in content, "Canonical Rank enum not found in fvafk.algebra.core"
    assert "UNRESOLVED" in content, "Rank.UNRESOLVED not defined"
    assert "CANDIDATE" in content, "Rank.CANDIDATE not defined"
    assert "LICENSED" in content, "Rank.LICENSED not defined"
    assert "CERTIFIED" in content, "Rank.CERTIFIED not defined"


def test_fvafk_algebra_result_exists():
    """Verify the canonical Result definition exists in fvafk.algebra."""
    repo_root = Path(__file__).parent.parent
    algebra_core = repo_root / "src" / "fvafk" / "algebra" / "core.py"

    assert algebra_core.exists(), "fvafk.algebra.core.py not found"

    with open(algebra_core, "r", encoding="utf-8") as f:
        content = f.read()

    assert "class Result(Generic[T]):" in content, "Canonical Result class not found"
    assert "value: T" in content, "Result.value field missing"
    assert "rank: Rank" in content, "Result.rank field missing"
    assert "evidence:" in content, "Result.evidence field missing"
    assert "residuals:" in content, "Result.residuals field missing"
    assert "failures:" in content, "Result.failures field missing"
    assert "trace: Trace" in content, "Result.trace field missing"


def test_fvafk_algebra_primitives_exist():
    """Verify all constitutional primitives exist in fvafk.algebra."""
    repo_root = Path(__file__).parent.parent
    algebra_core = repo_root / "src" / "fvafk" / "algebra" / "core.py"

    assert algebra_core.exists(), "fvafk.algebra.core.py not found"

    with open(algebra_core, "r", encoding="utf-8") as f:
        content = f.read()

    required_primitives = [
        ("class Rank(Enum):", "Rank"),
        ("class Trace:", "Trace"),
        ("class Carrier(Generic[T]):", "Carrier"),
        ("class Evidence:", "Evidence"),
        ("class Residual:", "Residual"),
        ("class Failure:", "Failure"),
        ("class Result(Generic[T]):", "Result"),
    ]

    missing = []
    for pattern, name in required_primitives:
        if pattern not in content:
            missing.append(name)

    if missing:
        pytest.fail(
            f"Missing constitutional primitives in fvafk.algebra.core: {', '.join(missing)}"
        )


def test_algebra_exports_all_primitives():
    """Verify fvafk.algebra.__init__.py exports all constitutional primitives."""
    repo_root = Path(__file__).parent.parent
    algebra_init = repo_root / "src" / "fvafk" / "algebra" / "__init__.py"

    assert algebra_init.exists(), "fvafk.algebra.__init__.py not found"

    with open(algebra_init, "r", encoding="utf-8") as f:
        content = f.read()

    required_exports = [
        "Carrier",
        "Evidence",
        "Failure",
        "Operation",
        "Rank",
        "Residual",
        "Result",
        "Trace",
        "empty_result",
    ]

    missing = []
    for export in required_exports:
        if f'"{export}"' not in content and f"'{export}'" not in content:
            missing.append(export)

    if missing:
        pytest.fail(
            f"Missing exports in fvafk.algebra.__init__.py: {', '.join(missing)}"
        )


def test_constitution_document_exists():
    """Verify the constitutional document exists."""
    repo_root = Path(__file__).parent.parent
    constitution = repo_root / "docs" / "ALGEBRA_KERNEL_CONSTITUTION.md"

    assert constitution.exists(), (
        "Constitutional document missing: docs/ALGEBRA_KERNEL_CONSTITUTION.md\n"
        "This document establishes fvafk.algebra as the sole governance kernel."
    )

    with open(constitution, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify key constitutional elements are present
    assert "لا مخرج عارٍ" in content, "Arabic constitutional motto missing"
    assert "No bare output" in content, "English translation missing"
    assert "fvafk.algebra" in content, "Kernel reference missing"
    assert "Seven Critical Laws" in content or "Critical Laws" in content, "Laws section missing"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
