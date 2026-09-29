"""Original tabletop design check. No printer or real user is involved.

Each copy starts on a new physical sheet; one document page per side.
The physical arrangement, not another arithmetic summary, is the oracle.
"""

import argparse
import json
from math import ceil
from pathlib import Path


CASES = [
    ("odd_pages_two_copies", 5, 2, True),
    ("even_pages_two_copies", 4, 2, True),
    ("single_page_three_copies", 1, 3, True),
    ("odd_pages_three_copies", 3, 3, True),
    ("simplex_two_copies", 5, 2, False),
    ("single_page_one_copy", 1, 1, True),
    ("even_pages_one_copy", 4, 1, True),
    ("seven_pages_two_copies", 7, 2, True),
]


def physical_sheets(pages, copies, duplex):
    per_copy = []
    for copy_number in range(1, copies + 1):
        sheets = []
        page_number = 1
        while page_number <= pages:
            front = page_number
            page_number += 1
            back = None
            if duplex and page_number <= pages:
                back = page_number
                page_number += 1
            sheets.append({"copy": copy_number, "front": front, "back": back})
        per_copy.append(sheets)
    return per_copy


def draft_summary(pages, copies, duplex):
    return ceil(pages * copies / (2 if duplex else 1))


def revised_summary(pages, copies, duplex):
    return copies * ceil(pages / (2 if duplex else 1))


def run(mode):
    summary = draft_summary if mode == "draft" else revised_summary
    results = []
    for name, pages, copies, duplex in CASES:
        layout = physical_sheets(pages, copies, duplex)
        expected = sum(len(copy) for copy in layout)
        actual = summary(pages, copies, duplex)
        # Check the oracle really preserves each full, separate document copy.
        for copy in layout:
            present = [side for sheet in copy for side in (sheet["front"], sheet["back"]) if side is not None]
            assert present == list(range(1, pages + 1))
        results.append({
            "case": name,
            "input": {"pages_per_copy": pages, "copies": copies, "duplex": duplex},
            "expected_sheets_from_layout": expected,
            "actual_summary_sheets": actual,
            "passed": actual == expected,
            "physical_layout": layout,
        })
    return {
        "mode": mode,
        "test_type": "deterministic tabletop check; no user test, payment, or printer execution",
        "case_count": len(results),
        "passed": sum(item["passed"] for item in results),
        "failed": sum(not item["passed"] for item in results),
        "results": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("draft", "revised"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run(args.mode)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, ensure_ascii=False))
    for item in report["results"]:
        if not item["passed"]:
            print(f"FAIL {item['case']}: expected {item['expected_sheets_from_layout']}, actual {item['actual_summary_sheets']}")
    raise SystemExit(1 if report["failed"] else 0)
