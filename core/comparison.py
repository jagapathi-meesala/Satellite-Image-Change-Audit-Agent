from typing import Any
from .validation import validate_observation_pair

def compare_change_observations(pair: dict[str, Any], min_area_delta_km2: float = 0.1) -> dict[str, Any]:
    validation = validate_observation_pair(pair)
    if not validation["valid"]:
        return {"valid": False, "errors": validation["errors"], "warnings": validation["warnings"], "classes": []}
    before, after = pair["before"], pair["after"]
    b_areas, a_areas = before["class_area_km2"], after["class_area_km2"]
    rows = []
    for label in sorted(set(b_areas) | set(a_areas)):
        b = float(b_areas.get(label, 0.0))
        a = float(a_areas.get(label, 0.0))
        delta = a - b
        pct = None if b == 0 else (delta / b) * 100.0
        rows.append({
            "class": label, "before_km2": b, "after_km2": a,
            "delta_km2": delta, "percent_delta": pct,
            "candidate_change": abs(delta) >= min_area_delta_km2
        })
    return {"valid": True, "errors": [], "warnings": validation["warnings"], "classes": rows,
            "threshold_km2": min_area_delta_km2,
            "interpretation": "Candidate changes in supplied area summaries; not pixel-level verified detections."}
