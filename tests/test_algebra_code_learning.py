"""Tests for :class:`fvafk.algebra.CodeLearningTrace`."""

from __future__ import annotations

from fvafk.algebra import (
    CodeChange,
    CodeLearningTrace,
    Evidence,
    Failure,
    KnowledgeStore,
    Rank,
    Residual,
)


def _change() -> CodeChange:
    return CodeChange(path="src/x.py", before="a = 1\n", after="a = 2\n")


def test_code_change_with_only_evidence_promotes_to_certified():
    trace = CodeLearningTrace(
        change=_change(),
        evidence=(
            Evidence(kind="tests.passing", source="src/x.py", detail="42/42"),
        ),
    )
    result = trace.to_result()
    assert result.rank is Rank.CERTIFIED


def test_code_change_with_residual_is_licensed_only():
    """An untested branch is a residual → cannot promote past LICENSED."""
    trace = CodeLearningTrace(
        change=_change(),
        evidence=(
            Evidence(kind="tests.passing", source="src/x.py", detail="40/40"),
        ),
        residuals=(
            Residual(kind="branch.untested", description="else-branch not covered"),
        ),
    )
    result = trace.to_result()
    assert result.rank is Rank.LICENSED
    assert result.certificate_allowed is False


def test_code_change_without_evidence_cannot_be_certified():
    """No evidence → at most CANDIDATE."""
    trace = CodeLearningTrace(
        change=_change(),
        residuals=(
            Residual(kind="tests.missing", description="no tests yet"),
        ),
    )
    result = trace.to_result()
    assert result.rank is Rank.CANDIDATE


def test_fatal_failure_forces_refuted():
    trace = CodeLearningTrace(
        change=_change(),
        failures=(Failure(kind="tests.regression", description="boom", fatal=True),),
    )
    result = trace.to_result()
    assert result.rank is Rank.REFUTED


def test_replay_roundtrip_preserves_fields():
    trace = CodeLearningTrace(
        change=_change(),
        evidence=(Evidence(kind="k", source="src/x.py", detail="d"),),
        residuals=(Residual(kind="r", description="x"),),
    )
    replay = trace.replay()
    assert replay["change"]["path"] == "src/x.py"
    assert replay["evidence"][0]["kind"] == "k"
    assert replay["residuals"][0]["kind"] == "r"


def test_knowledge_store_accumulates_evidence_kinds():
    store = KnowledgeStore()
    trace = CodeLearningTrace(
        change=_change(),
        evidence=(
            Evidence(kind="tests.passing", source="src/x.py", detail="ok"),
            Evidence(kind="types.passing", source="src/x.py", detail="ok"),
        ),
    )
    store.ingest(trace.to_result())
    assert store.results_ingested == 1
    assert set(store.kinds()) == {"tests.passing", "types.passing"}
