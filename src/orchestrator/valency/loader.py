# -*- coding: utf-8 -*-
"""
Load valency seed JSON and build root → frame dictionary.
Cached; triliteral roots only (normalized to no-dash form).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .models import ValencyFrame, CONF_EXACT_KB

_VALENCY_CACHE: Dict[str, ValencyFrame] | None = None
_VALENCY_SEED_FALLBACK: Dict[str, Dict[str, Any]] = {
    "ضرب": {
        "class": "transitive_one_object",
        "required_roles": ["فاعل", "مفعول به"],
        "optional_roles": [],
    }
}


def _data_dir() -> Path:
    here = Path(__file__).resolve()
    repo_root = here.parents[3] if len(here.parents) >= 4 else Path.cwd()
    for base in [Path.cwd(), repo_root, here.parent.parent.parent]:
        d = base / "data" / "valency_seed.json"
        if d.exists():
            return d.parent
    return Path.cwd() / "data"


def _normalize_root(r: str) -> str:
    """Normalize root for key: strip, remove dashes and spaces."""
    if not r or not isinstance(r, str):
        return ""
    return (r.strip().replace("-", "").replace(" ", ""))


def load_valency_kb(force_reload: bool = False) -> Dict[str, ValencyFrame]:
    """
    Load valency seed JSON once, normalize roots, build root → ValencyFrame.
    Returns dict keyed by normalized triliteral/quadrilateral root (e.g. ضرب, ظلم).
    Cached; use force_reload=True to clear cache.
    """
    global _VALENCY_CACHE
    if _VALENCY_CACHE is not None and not force_reload:
        return _VALENCY_CACHE
    path = _data_dir() / "valency_seed.json"
    out: Dict[str, ValencyFrame] = {}
    raw_items: List[Dict[str, Any]] = []
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                raw_items.extend([item for item in data if isinstance(item, dict)])
        except (json.JSONDecodeError, OSError):
            pass
    if not raw_items:
        raw_items = [{"root": k, **v} for k, v in _VALENCY_SEED_FALLBACK.items()]

    for item in raw_items:
        if not isinstance(item, dict):
            continue
        root_raw = (item.get("root") or "").strip()
        if not root_raw:
            continue
        root_norm = _normalize_root(root_raw)
        if not root_norm:
            continue
        valency_class = (item.get("class") or "unknown").strip()
        required = list(item.get("required_roles") or [])
        optional = list(item.get("optional_roles") or [])
        if not isinstance(required, list):
            required = []
        if not isinstance(optional, list):
            optional = []
        frame = ValencyFrame(
            root=root_norm,
            valency_class=valency_class,
            required_roles=required,
            optional_roles=optional,
            source="valency_seed.json",
            confidence=CONF_EXACT_KB,
        )
        out[root_norm] = frame
    for seed_root, seed_frame in _VALENCY_SEED_FALLBACK.items():
        root_norm = _normalize_root(seed_root)
        if root_norm in out:
            continue
        out[root_norm] = ValencyFrame(
            root=root_norm,
            valency_class=str(seed_frame.get("class") or "unknown"),
            required_roles=list(seed_frame.get("required_roles") or []),
            optional_roles=list(seed_frame.get("optional_roles") or []),
            source="valency_seed.json",
            confidence=CONF_EXACT_KB,
        )
    _VALENCY_CACHE = out
    return out
