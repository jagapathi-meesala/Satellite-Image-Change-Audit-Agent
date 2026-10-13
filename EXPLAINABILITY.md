# Explainability

## Inputs
The agent accepts two structured observation records labelled `before` and `after`, including acquisition date, sensor, footprint identifier, cloud cover, and per-class area summaries.

## Decision
It validates the records, checks comparability, computes class-area deltas, and assigns review flags using explicit thresholds documented in code. Results are descriptive audit findings, not verified pixel-level detections.

## Limits
The agent does not read satellite raster files, run image registration, classify pixels, or establish causation. Cloud cover, sensor differences, seasonal variation, projection mismatch, classification error, and inconsistent footprints can create apparent change.

## Tool: validate_observation_pair

### Inputs and Data Sources
Two observation dictionaries supplied by the caller.

### Decision and Reasoning
Checks required fields, ISO dates, cloud-cover range, class-area mappings, and basic before/after chronology.

### Outputs and Evidence
Returns validation errors and warnings tied to input field names.

### Limits and Constraints
It validates structure and simple constraints only; it does not validate the underlying imagery.

### Failure Handling
Malformed or absent fields are reported without silently substituting values.

### Human Review
Resolve all validation errors and verify metadata against the original imagery before relying on the comparison.

## Tool: compare_change_observations

### Inputs and Data Sources
A validated pair of observation records.

### Decision and Reasoning
Compares class areas, calculates absolute and percentage differences, and flags differences above a configurable area threshold.

### Outputs and Evidence
Returns per-class before/after area, delta, percentage delta when defined, and candidate-change status.

### Limits and Constraints
The result reflects supplied summaries only; it is not a pixel-level change map or ground-truth claim.

### Failure Handling
Invalid pairs return actionable validation messages rather than a misleading comparison.

### Human Review
Review large or unexpected differences in GIS using co-registered imagery and suitable reference data.

## Tool: build_audit_report

### Inputs and Data Sources
The before/after records, computed comparison, and validation findings.

### Decision and Reasoning
Combines input evidence, comparability warnings, and class-area calculations into a structured report.

### Outputs and Evidence
Produces a JSON-compatible report with summary, findings, limitations, and recommended next steps.

### Limits and Constraints
The report cannot establish why a change occurred or whether a reported change is legally or operationally significant.

### Failure Handling
Missing or invalid inputs are represented as findings; no values are invented.

### Human Review
A qualified analyst should review source imagery, processing metadata, and confidence/accuracy information before action.
