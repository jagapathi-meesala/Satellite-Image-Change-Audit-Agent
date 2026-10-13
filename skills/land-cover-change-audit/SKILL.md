---
name: land-cover-change-audit
description: Compare user-supplied land-cover area summaries conservatively.
---
# Land-Cover Change Audit
- Compare the union of class labels in the two records.
- Calculate after-minus-before area and percentage change when baseline area is nonzero.
- Mark a candidate change only when the absolute area delta meets the configured threshold.
- Describe outputs as summary differences, not pixel-verified detections.
