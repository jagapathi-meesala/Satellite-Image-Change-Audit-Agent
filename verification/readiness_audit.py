from pathlib import Path
import yaml, json
ROOT = Path(__file__).resolve().parents[1]
required = ["agent.yaml","SOUL.md","README.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md","requirements.txt",".env.example",".gitignore","pytest.ini",
"core/__init__.py","core/validation.py","core/comparison.py","core/report.py","core/cli.py",
"tools/validate-observation-pair.yaml","tools/compare-change-observations.yaml","tools/build-audit-report.yaml",
"skills/image-pair-quality-review/SKILL.md","skills/land-cover-change-audit/SKILL.md","skills/evidence-reporting/SKILL.md",
"tests/test_agent.py","examples/observation_pair.json"]
missing = [x for x in required if not (ROOT/x).is_file()]
if missing:
    print("FAIL: missing files:", missing); raise SystemExit(1)
manifest = yaml.safe_load((ROOT/"agent.yaml").read_text())
assert manifest["spec_version"] == "0.1.0"
assert len(manifest["tools"]) == 3 and len(manifest["skills"]) == 3
for p in (ROOT/"tools").glob("*.yaml"):
    data = yaml.safe_load(p.read_text())
    assert set(data) == {"name","description","input_schema"}, p
    assert data["input_schema"]["type"] == "object"
for p in (ROOT/"skills").glob("*/SKILL.md"):
    assert p.read_text().startswith("---\nname: ")
doc = (ROOT/"EXPLAINABILITY.md").read_text()
for heading in ["## Inputs","## Decision","## Limits","## Tool: validate-observation-pair","## Tool: compare-change-observations","## Tool: build-audit-report"]:
    assert heading in doc, heading
json.loads((ROOT/"examples/observation_pair.json").read_text())
print(f"PASS: all {len(required)}/{len(required)} required files present")
print("PASS: manifest, tool schemas, skill frontmatter, explainability headings, and example JSON")
