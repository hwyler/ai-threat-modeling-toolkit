#!/usr/bin/env python3
"""
Generate a scoped markdown checklist from the vulnerability and threat vector
catalogs in data/, filtered by AI system type and, optionally, sourcing model.

Usage:
    python tools/generate_checklist.py --system-type generative
    python tools/generate_checklist.py --system-type agentic --sourcing procured
    python tools/generate_checklist.py --system-type predictive --output checklist.md

Requires PyYAML (pip install pyyaml).
"""

import argparse
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.exit("This script requires PyYAML. Install it with: pip install pyyaml")

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

SOURCING_NOTE = {
    "built": "Full data-level and pipeline testing is in scope. Weight the "
             "data governance and model lifecycle categories heavily.",
    "procured": "Direct data and pipeline access is likely unavailable. "
                "Weight the third-party and supply chain category, and rely "
                "on API-level and output-level testing plus vendor due "
                "diligence for anything upstream of the interface.",
    "hybrid": "Treat the base model as procured and the fine-tuning, "
              "orchestration, and retrieval layers as built in-house; apply "
              "both sets of weighting.",
}


def load_yaml(filename):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def applies(entry_applies_to, system_type):
    return "all" in entry_applies_to or system_type in entry_applies_to


def build_checklist(system_type, sourcing):
    vulnerabilities = load_yaml("vulnerabilities.yaml")
    threat_vector_data = load_yaml("threat_vectors.yaml")
    threat_vectors = threat_vector_data["vectors"]

    scoped_vulns = [v for v in vulnerabilities if applies(v["applies_to"], system_type)]
    scoped_vectors = [t for t in threat_vectors if applies(t["applies_to"], system_type)]

    lines = []
    lines.append(f"# Scoped Assessment Checklist: {system_type} AI system")
    if sourcing:
        lines.append("")
        lines.append(f"**Sourcing model**: {sourcing}")
        lines.append("")
        lines.append(SOURCING_NOTE.get(sourcing, ""))
    lines.append("")
    lines.append(
        "Generated from data/vulnerabilities.yaml and data/threat_vectors.yaml. "
        "Check each item against the asset inventory for this system; an "
        "unchecked item with no matching asset is out of scope, not a gap."
    )

    lines.append("")
    lines.append("## Threat vectors to assess")
    lines.append("")
    for t in scoped_vectors:
        lines.append(f"- [ ] **{t['id']} {t['name']}** — {t['description']}")
        lines.append(f"      Framework reference: {t.get('framework', 'n/a')}")

    lines.append("")
    lines.append("## Vulnerabilities to check for")
    lines.append("")
    current_category = None
    for v in sorted(scoped_vulns, key=lambda x: x["category"]):
        if v["category"] != current_category:
            current_category = v["category"]
            lines.append(f"### {current_category.replace('_', ' ').title()}")
            lines.append("")
        lines.append(f"- [ ] **{v['id']} {v['name']}** — {v['description']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--system-type",
        required=True,
        choices=["predictive", "generative", "agentic"],
        help="AI system type to scope the checklist to.",
    )
    parser.add_argument(
        "--sourcing",
        choices=["built", "procured", "hybrid"],
        help="Optional sourcing model, adds a testing-scope note.",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="Write the checklist to this file instead of stdout.",
    )
    args = parser.parse_args()

    checklist = build_checklist(args.system_type, args.sourcing)

    if args.output:
        args.output.write_text(checklist, encoding="utf-8")
        print(f"Checklist written to {args.output}")
    else:
        print(checklist)


if __name__ == "__main__":
    main()
