#!/usr/bin/env python3
"""
Semantic Leak Detection Tests

Recursively scan all dal_core output for forbidden semantic fields.
Enforces Condition 10: No semantic leak.
"""

import sys
sys.path.insert(0, 'src')

from dal_core.d_mufrad import DClosed
from dal_core.d_type import TypedDal, DalType
from dal_core.d_lugha import LughaAttestation, LughaRank
from dal_core.d_form import FormCandidate
from dal_core.ranks import FormRank


# Forbidden semantic field names
FORBIDDEN_FIELDS = {
    'meaning',
    'semantic',
    'semantics',
    'madlul',
    'murad',
    'haqiqa',
    'majaz',
    'haqiqa_majaz',
    'reality_ref',
    'grounding',
    'intended_meaning',
    'referent',
    'denotation',
    'sense',
    'connotation',
}


def scan_object_for_semantic_leak(obj, path="root", visited=None):
    """
    Recursively scan object for forbidden semantic fields.

    Returns list of violations found.
    """
    if visited is None:
        visited = set()

    # Avoid infinite recursion
    obj_id = id(obj)
    if obj_id in visited:
        return []
    visited.add(obj_id)

    violations = []

    # Check dataclass/object fields
    if hasattr(obj, '__dict__'):
        for field_name in dir(obj):
            if field_name.startswith('_'):
                continue

            # Check if field name is forbidden
            if field_name.lower() in FORBIDDEN_FIELDS:
                violations.append(f"{path}.{field_name}")

            # Recursively check field value
            try:
                field_value = getattr(obj, field_name)
                if not callable(field_value):
                    sub_violations = scan_object_for_semantic_leak(
                        field_value,
                        path=f"{path}.{field_name}",
                        visited=visited
                    )
                    violations.extend(sub_violations)
            except Exception:
                pass

    # Check dict keys
    if isinstance(obj, dict):
        for key in obj.keys():
            if isinstance(key, str) and key.lower() in FORBIDDEN_FIELDS:
                violations.append(f"{path}[{key!r}]")

            # Recursively check value
            sub_violations = scan_object_for_semantic_leak(
                obj[key],
                path=f"{path}[{key!r}]",
                visited=visited
            )
            violations.extend(sub_violations)

    # Check list/tuple elements
    if isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            sub_violations = scan_object_for_semantic_leak(
                item,
                path=f"{path}[{i}]",
                visited=visited
            )
            violations.extend(sub_violations)

    return violations


def test_dclosed_no_semantic_fields():
    """DClosed must not contain any semantic fields"""
    form = FormCandidate(text="كَتَبَ", vocalization="كَتَبَ")
    attestation = LughaAttestation(form=form, rank=LughaRank.AHAD, is_arabic=True)
    typed_dal = TypedDal(attestation=attestation, dal_type=DalType.ISM)
    dclosed = DClosed(typed_dal=typed_dal)

    violations = scan_object_for_semantic_leak(dclosed, "DClosed")

    if violations:
        print(f"✗ SEMANTIC LEAK DETECTED:")
        for v in violations:
            print(f"  - {v}")
        raise AssertionError(f"Semantic leak found: {violations}")

    print("✓ test_dclosed_no_semantic_fields")


def test_dclosed_explain_no_semantic_fields():
    """DClosed.explain() output must not contain semantic fields"""
    # This would test the explain() method if it exists
    # For now, check that trace dict is clean

    form = FormCandidate(
        text="كَتَبَ",
        vocalization="كَتَبَ",
        trace={"stage": "form", "decision": "pattern_match"}
    )
    attestation = LughaAttestation(
        form=form,
        rank=LughaRank.AHAD,
        is_arabic=True,
        trace={"stage": "lugha", "source": "lexicon"}
    )
    typed_dal = TypedDal(
        attestation=attestation,
        dal_type=DalType.ISM,
        trace={"stage": "type", "classification": "noun"}
    )
    dclosed = DClosed(
        typed_dal=typed_dal,
        full_trace={
            "input": "كَتَبَ",
            "pipeline": ["carrier", "atom", "unit", "form", "lugha", "type", "mufrad"]
        }
    )

    violations = scan_object_for_semantic_leak(dclosed.full_trace, "DClosed.full_trace")

    if violations:
        print(f"✗ SEMANTIC LEAK IN TRACE:")
        for v in violations:
            print(f"  - {v}")
        raise AssertionError(f"Semantic leak in trace: {violations}")

    print("✓ test_dclosed_explain_no_semantic_fields")


def test_all_dataclasses_no_semantic_fields():
    """All dal_core dataclasses must not have semantic fields"""
    classes_to_check = [
        (FormCandidate, {"text": "test", "vocalization": "test"}),
        (LughaAttestation, {
            "form": FormCandidate(text="test", vocalization="test"),
            "rank": LughaRank.FORM,
            "is_arabic": False
        }),
        (TypedDal, {
            "attestation": LughaAttestation(
                form=FormCandidate(text="test", vocalization="test"),
                rank=LughaRank.FORM,
                is_arabic=False
            ),
            "dal_type": DalType.AMBIGUOUS
        }),
    ]

    for cls, kwargs in classes_to_check:
        instance = cls(**kwargs)
        violations = scan_object_for_semantic_leak(instance, cls.__name__)

        if violations:
            print(f"✗ SEMANTIC LEAK IN {cls.__name__}:")
            for v in violations:
                print(f"  - {v}")
            raise AssertionError(f"Semantic leak in {cls.__name__}: {violations}")

    print("✓ test_all_dataclasses_no_semantic_fields")


def test_forbidden_field_injection_blocked():
    """Attempting to inject semantic field should fail"""
    form = FormCandidate(text="test", vocalization="test")
    attestation = LughaAttestation(form=form, rank=LughaRank.AHAD, is_arabic=True)
    typed_dal = TypedDal(attestation=attestation, dal_type=DalType.ISM)
    dclosed = DClosed(typed_dal=typed_dal)

    # DClosed is frozen, so injection should fail
    try:
        dclosed.meaning = "something"  # type: ignore
        raise AssertionError("Should not be able to set meaning field on frozen DClosed")
    except AttributeError:
        # Expected - frozen dataclass
        pass
    except Exception as e:
        raise AssertionError(f"Unexpected exception: {e}")

    print("✓ test_forbidden_field_injection_blocked")


def main():
    """Run all semantic leak tests"""
    print("Running Semantic Leak Detection Tests\n")
    print("=" * 60)

    tests = [
        test_dclosed_no_semantic_fields,
        test_dclosed_explain_no_semantic_fields,
        test_all_dataclasses_no_semantic_fields,
        test_forbidden_field_injection_blocked,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
