#!/usr/bin/env python3
"""Pull Google Play top charts (Top Free, Top Grossing, Trending...) by country into a CSV.

Standard library only. Needs an Apify API token in APIFY_TOKEN
(free at https://console.apify.com/settings/integrations).

    export APIFY_TOKEN=apify_api_...
    python3 example.py                                  # inputs/us-top-free.json
    python3 example.py inputs/games-six-markets.json    # any input file
    python3 example.py --country us --country jp --chart trending --limit 20
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request

ACTOR = "glitchbound~google-play-charts-scraper"
RUN_SYNC = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"
COLUMNS = ["country", "chart", "category", "rank", "rankChange", "newInChart", "title",
           "developer", "installs", "rating", "price", "appId"]


def run(actor_input, token):
    """Start one run, wait for it, and return its rows (the call blocks up to 300 s)."""
    req = urllib.request.Request(
        RUN_SYNC, data=json.dumps(actor_input).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=330) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Apify answered {e.code}: {e.read().decode()[:300]}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", nargs="?", default=os.path.join(here, "inputs", "us-top-free.json"),
                    help="a JSON input file (default: inputs/us-top-free.json)")
    ap.add_argument("--country", action="append", help="two-letter code, e.g. us; repeat for more")
    ap.add_argument("--chart", action="append",
                    help="top-free, top-paid, top-grossing, trending or top-new-free")
    ap.add_argument("--category", action="append", help="e.g. all-games or finance")
    ap.add_argument("--limit", type=int, help="apps per chart, up to 200")
    ap.add_argument("--out", default="charts.csv")
    args = ap.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")

    with open(args.input) as f:
        actor_input = json.load(f)
    for key, value in (("countries", args.country), ("charts", args.chart),
                       ("categories", args.category), ("limit", args.limit)):
        if value:
            actor_input[key] = value

    rows = run(actor_input, token)
    # Chart rows carry `rank`. Anything else is an unbilled row saying which chart
    # or input value could not be read, and why.
    charts = [r for r in rows if "rank" in r]
    for r in rows:
        if "rank" not in r:
            print(f"note: {json.dumps(r)[:200]}", file=sys.stderr)

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(charts)
    print(f"{len(charts)} chart rows written to {args.out}")
    for r in charts[:5]:
        print(f"  {r.get('country')} {r.get('chart')} #{r.get('rank')}: {r.get('title')} ({r.get('developer')})")


if __name__ == "__main__":
    main()
