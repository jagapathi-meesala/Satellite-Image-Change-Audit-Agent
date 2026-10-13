from typing import Any
from .validation import validate_observation_pair
from .comparison import compare_change_observations

def build_audit_report(pair: dict[str, Any], min_area_delta_km2: float = 0.1) -> dict[str, Any]:
    validation = validate_observation_pair(pair)
    comparison = compare_change_observations(pair, min_area_delta_km2)
    findings = []
    findings.extend({"type": "validation_error", "detail": x} for x in validation["errors"])
    findings.extend({"type": "comparability_warning", "detail": x} for x in validation["warnings"])
    if comparison["valid"]:
        for row in comparison["classes"]:
            if row["candidate_change"]:
                findings.append({"type": "candidate_class_change", "class": row["class"],
                                 "delta_km2": row["delta_km2"],
                                 "detail": "Area-summary delta meets or exceeds the configured threshold."})
    if not validation["errors"] and not any(x["type"] == "candidate_class_change" for x in findings):
        findings.append({"type": "no_threshold_exceedance", "detail": "No supplied class-area delta met the configured threshold; this does not prove no real change occurred."})
    return {
        "agent": "satellite-image-change-audit-agent",
        "status": "needs_input_correction" if validation["errors"] else ("review_required" if findings else "no_flags"),
        "observations": {
            "before_image_id": pair.get("before", {}).get("image_id") if isinstance(pair, dict) and isinstance(pair.get("before"), dict) else None,
            "after_image_id": pair.get("after", {}).get("image_id") if isinstance(pair, dict) and isinstance(pair.get("after"), dict) else None
        },
        "validation": validation,
        "comparison": comparison,
        "findings": findings,
        "limitations": [
            "Only supplied metadata and class-area summaries were evaluated.",
            "No raster pixels, image alignment, classification model, or ground-truth data were inspected.",
            "Seasonality, cloud/shadow, sensor, projection, and classification uncertainty may explain apparent differences."
        ],
        "recommended_next_steps": [
            "Verify acquisition metadata, coordinate reference systems, and common footprint.",
            "Check cloud/shadow masks and co-registration in a GIS/remote-sensing workflow.",
            "Review classification accuracy and reference samples before operational use."
        ]
    }
