import argparse, json, sys
from pathlib import Path
from .report import build_audit_report

def main() -> int:
    parser = argparse.ArgumentParser(description="Audit paired satellite observation summaries.")
    parser.add_argument("input", help="JSON file containing before/after observation records")
    parser.add_argument("--threshold-km2", type=float, default=0.1, help="Candidate-change threshold in km²")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = build_audit_report(payload, args.threshold_km2)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["validation"]["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
