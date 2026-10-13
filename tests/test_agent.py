from core.validation import validate_observation_pair
from core.comparison import compare_change_observations
from core.report import build_audit_report
from copy import deepcopy
import json
from pathlib import Path

def sample():
    return json.loads(Path("examples/observation_pair.json").read_text())

def test_sample_pair_valid():
    assert validate_observation_pair(sample())["valid"]

def test_class_delta_computed():
    result = compare_change_observations(sample())
    rows = {x["class"]: x for x in result["classes"]}
    assert round(rows["forest"]["delta_km2"], 2) == -0.6
    assert rows["built_up"]["candidate_change"]

def test_new_class_baseline_zero_percent_none():
    pair = sample()
    pair["after"]["class_area_km2"]["new_class"] = 1.0
    row = {x["class"]: x for x in compare_change_observations(pair)["classes"]}["new_class"]
    assert row["percent_delta"] is None

def test_missing_field_fails():
    pair = sample()
    del pair["before"]["sensor"]
    assert not validate_observation_pair(pair)["valid"]

def test_bad_cloud_cover_fails():
    pair = sample()
    pair["after"]["cloud_cover_pct"] = 110
    assert not validate_observation_pair(pair)["valid"]

def test_high_cloud_warning():
    pair = sample()
    pair["after"]["cloud_cover_pct"] = 65
    assert any("cloud cover" in w for w in validate_observation_pair(pair)["warnings"])

def test_footprint_mismatch_warns():
    pair = sample()
    pair["after"]["footprint_id"] = "tile-99"
    assert any("Footprint" in w for w in validate_observation_pair(pair)["warnings"])

def test_report_states_limits():
    report = build_audit_report(sample())
    assert report["limitations"]
    assert report["recommended_next_steps"]
    assert report["agent"] == "satellite-image-change-audit-agent"
