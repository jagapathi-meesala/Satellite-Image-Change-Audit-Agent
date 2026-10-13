# Satellite Image Change Audit Agent

A small, portable agent project that audits **paired satellite-image observation records** for consistency, comparability, and evidence gaps. It helps organize a defensible change-audit report; it does not perform pixel-level remote-sensing analysis.

## Capabilities
- Validate observation dates, IDs, footprints, sensor labels, cloud-cover values, and supplied class summaries.
- Compare before/after class-area summaries and identify potentially meaningful reported changes.
- Flag comparability risks such as different footprints, sensors, seasonal windows, or high cloud cover.
- Produce a JSON audit report with evidence, limitations, and review recommendations.

## Scope and safeguards
Inputs are structured JSON observation summaries, not raw raster imagery. Reported differences are **candidate changes**, not proof of real-world change or causation. Validate projection, co-registration, atmospheric correction, classification accuracy, and seasonal effects in a suitable GIS/remote-sensing workflow before making decisions.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 verification/readiness_audit.py
python3 -m core.cli examples/observation_pair.json
```

## Input format
Each observation has `image_id`, `acquired_at` (ISO date), `sensor`, `footprint_id`, `cloud_cover_pct` (0–100), and `class_area_km2` (mapping class labels to non-negative areas). Two observations are provided as `before` and `after`.

## OpenGAP
Manifest follows the project's targeted OpenGAP v0.1.0 structure. If the official CLI is installed in your environment, run:
```bash
opengap validate
```
