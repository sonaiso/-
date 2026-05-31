"""
Carve-out scope test for the T5 real adapter (PR-A enforcement).

Constitutional purpose:
    Prove that the execution carve-out documented in
    ``docs/T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`` is mechanically narrow:

    1. The path-aware scanner
       ``GovernedT5IntegrationSkeleton.scan_path_for_execution_markers``
       returns an empty tuple for files under
       ``src/dal_core/adapters/t5/`` and only those files.

    2. Every source file under ``src/dal_core/`` that is NOT in the
       carve-out path is free of FORBIDDEN_EXECUTION_MARKERS substrings in
       source code (excluding ``docs/`` and the constants list itself).

This file deliberately uses no fixtures from the carve-out: it stays
runnable without ``transformers`` / ``torch`` installed.
"""
from __future__ import annotations

from pathlib import Path
import re

import pytest

from dal_core.governed_t5_integration_skeleton import (
    FORBIDDEN_EXECUTION_MARKERS,
    GovernedT5IntegrationSkeleton,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DAL_CORE_DIR = REPO_ROOT / "src" / "dal_core"
CARVEOUT_DIR = DAL_CORE_DIR / "adapters" / "t5"

# Files that legitimately *mention* the forbidden marker strings as data
# (constants, documentation, scanner self-test). They are not execution
# sites and must therefore be excluded from the source-tree audit.
DATA_ONLY_FILES = {
    DAL_CORE_DIR / "governed_t5_integration_skeleton.py",  # defines the constants
    DAL_CORE_DIR / "t5_adapter_interface_contracts.py",   # documents forbidden fields
}


def _iter_dal_core_py_files() -> list[Path]:
    files = []
    for path in DAL_CORE_DIR.rglob("*.py"):
        files.append(path)
    return files


# ---------------------------------------------------------------------------
# 1. Path-aware scanner behaviour
# ---------------------------------------------------------------------------

class TestScanPathForExecutionMarkers:
    """The carve-out is a *path* filter only."""

    SAMPLE_FORBIDDEN_TEXT = (
        "import transformers\n"
        "from transformers import AutoTokenizer\n"
        "model = T5ForConditionalGeneration.from_pretrained('t5-small')\n"
        "out = model.generate(input_ids)\n"
    )

    def test_carveout_path_absolute_returns_empty(self):
        path = str(CARVEOUT_DIR / "runner.py")
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            path, self.SAMPLE_FORBIDDEN_TEXT
        )
        assert detected == ()

    def test_carveout_path_relative_returns_empty(self):
        path = "src/dal_core/adapters/t5/runner.py"
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            path, self.SAMPLE_FORBIDDEN_TEXT
        )
        assert detected == ()

    def test_carveout_path_windows_separators_returns_empty(self):
        path = r"src\dal_core\adapters\t5\runner.py"
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            path, self.SAMPLE_FORBIDDEN_TEXT
        )
        assert detected == ()

    def test_non_carveout_path_still_strict(self):
        path = str(DAL_CORE_DIR / "case_signs.py")
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            path, self.SAMPLE_FORBIDDEN_TEXT
        )
        assert "import transformers" in detected
        assert ".from_pretrained(" in detected
        assert ".generate(" in detected

    def test_empty_path_falls_back_to_strict(self):
        """No path supplied → strict behaviour applies (defensive)."""
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            "", self.SAMPLE_FORBIDDEN_TEXT
        )
        assert "import transformers" in detected

    def test_carveout_does_not_remove_constants(self):
        """The carve-out MUST be a filter, not a deletion."""
        assert "import transformers" in FORBIDDEN_EXECUTION_MARKERS
        assert "import torch" in FORBIDDEN_EXECUTION_MARKERS
        assert ".from_pretrained(" in FORBIDDEN_EXECUTION_MARKERS
        assert ".generate(" in FORBIDDEN_EXECUTION_MARKERS

    def test_existing_strict_scanner_unchanged(self):
        """PR #150 strict scanner must keep its original behaviour."""
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(
            self.SAMPLE_FORBIDDEN_TEXT
        )
        assert "import transformers" in detected
        assert ".from_pretrained(" in detected

    def test_lookalike_path_outside_carveout_is_strict(self):
        """A path containing 't5' but not under adapters/t5/ is not exempt."""
        path = str(DAL_CORE_DIR / "governed_t5_integration_skeleton.py")
        detected = GovernedT5IntegrationSkeleton.scan_path_for_execution_markers(
            path, self.SAMPLE_FORBIDDEN_TEXT
        )
        assert "import transformers" in detected


# ---------------------------------------------------------------------------
# 2. Repository-wide audit: no leakage outside the carve-out
# ---------------------------------------------------------------------------

class TestNoExecutionMarkerLeakage:
    """Walk src/dal_core/ and assert no leakage outside adapters/t5/."""

    @pytest.mark.parametrize("py_file", _iter_dal_core_py_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
    def test_no_forbidden_execution_in_source(self, py_file: Path):
        # The carve-out path is allowed to contain markers.
        try:
            py_file.relative_to(CARVEOUT_DIR)
            pytest.skip("File is inside the T5 carve-out path")
        except ValueError:
            pass

        if py_file in DATA_ONLY_FILES:
            pytest.skip("File legitimately documents the forbidden constants")

        source = py_file.read_text(encoding="utf-8")

        # Strip docstrings and comments so we only audit *executable* code.
        # Triple-quoted strings: remove non-greedily.
        code_only = re.sub(r'"""[\s\S]*?"""', "", source)
        code_only = re.sub(r"'''[\s\S]*?'''", "", code_only)
        # Line comments
        code_only = re.sub(r"#[^\n]*", "", code_only)

        for marker in FORBIDDEN_EXECUTION_MARKERS:
            assert marker not in code_only, (
                f"Constitutional carve-out leak: {py_file.relative_to(REPO_ROOT)} "
                f"contains forbidden execution marker {marker!r} outside the "
                f"src/dal_core/adapters/t5/ carve-out."
            )

    def test_carveout_dir_is_well_known(self):
        """The carve-out directory must exist (or be intentionally absent for PR-A only)."""
        # Existence is asserted by PR-B; here we only assert the *path*
        # contract is what the scanner expects.
        assert CARVEOUT_DIR.parts[-3:] == ("dal_core", "adapters", "t5")
