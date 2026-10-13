from datetime import date
from typing import Any

REQUIRED = ("image_id", "acquired_at", "sensor", "footprint_id", "cloud_cover_pct", "class_area_km2")

def _valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False

def validate_observation_pair(pair: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(pair, dict):
        return {"valid": False, "errors": ["Pair must be an object."], "warnings": []}
    for side in ("before", "after"):
        obs = pair.get(side)
        if not isinstance(obs, dict):
            errors.append(f"{side}: must be an object.")
            continue
        for field in REQUIRED:
            if field not in obs:
                errors.append(f"{side}.{field}: required field missing.")
        if "acquired_at" in obs and not _valid_date(obs["acquired_at"]):
            errors.append(f"{side}.acquired_at: expected ISO date YYYY-MM-DD.")
        if "cloud_cover_pct" in obs:
            value = obs["cloud_cover_pct"]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 100:
                errors.append(f"{side}.cloud_cover_pct: expected number from 0 to 100.")
            elif value > 40:
                warnings.append(f"{side}: cloud cover is above 40%; reported comparison may be less reliable.")
        if "class_area_km2" in obs:
            areas = obs["class_area_km2"]
            if not isinstance(areas, dict):
                errors.append(f"{side}.class_area_km2: expected an object of class labels to area values.")
            else:
                for label, area in areas.items():
                    if not isinstance(label, str) or not label.strip():
                        errors.append(f"{side}.class_area_km2: class labels must be non-empty strings.")
                    if not isinstance(area, (int, float)) or isinstance(area, bool) or area < 0:
                        errors.append(f"{side}.class_area_km2.{label}: area must be a non-negative number.")
    before, after = pair.get("before"), pair.get("after")
    if isinstance(before, dict) and isinstance(after, dict):
        if _valid_date(before.get("acquired_at")) and _valid_date(after.get("acquired_at")):
            if date.fromisoformat(before["acquired_at"]) >= date.fromisoformat(after["acquired_at"]):
                errors.append("before.acquired_at: must be earlier than after.acquired_at.")
        if before.get("footprint_id") and after.get("footprint_id") and before["footprint_id"] != after["footprint_id"]:
            warnings.append("Footprint identifiers differ; areas may not be directly comparable.")
        if before.get("sensor") and after.get("sensor") and before["sensor"] != after["sensor"]:
            warnings.append("Sensor labels differ; sensor-specific differences may affect comparability.")
    return {"valid": not errors, "errors": errors, "warnings": warnings}
