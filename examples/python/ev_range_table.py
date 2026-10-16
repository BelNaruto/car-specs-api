#!/usr/bin/env python3
"""
EV range, efficiency and charge time for a list of models (Python 3.8+, needs `requests`)

API:     https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api
Support: Telegram @pintoflow

Usage:
    pip install requests
    export RAPIDAPI_KEY=your_key
    python3 ev_range_table.py "tesla|model 3|2023" "hyundai|ioniq 5|2023" "ford|mustang mach-e|2023"
"""
import os
import sys

import requests

HOST = "car-specs-api.p.rapidapi.com"
KEY = os.environ.get("RAPIDAPI_KEY")


def get(path, **params):
    r = requests.get(f"https://{HOST}{path}", params=params,
                     headers={"x-rapidapi-host": HOST, "x-rapidapi-key": KEY}, timeout=60)
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"{body.get('error', {}).get('code')}: {body.get('error', {}).get('message')}")
    return body["data"]


def main():
    if not KEY:
        sys.exit("Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your_key")
    cars = sys.argv[1:] or ["tesla|model 3|2023", "hyundai|ioniq 5|2023"]
    print(f"{'Model':<44}{'Range mi':>9}{'MPGe':>6}{'kWh/100mi':>11}{'Charge h':>9}")
    for c in cars:
        make, model, year = c.split("|")
        try:
            data = get("/specs", make=make, model=model, year=year, perPage=12)
        except RuntimeError as e:
            print(f"{c:<44}{e}")
            continue
        for s in (data if isinstance(data, list) else data.get("specs", [])):
            el = (s.get("fuelEconomy") or {}).get("electric")
            if not el:
                continue
            name = f"{s['year']} {s['make']} {s['model']}"[:43]
            print(f"{name:<44}{el.get('rangeMiles') or '–':>9}{s['fuelEconomy']['mpg']['combined']:>6}"
                  f"{el['kWhPer100Miles']['combined']:>11}{el.get('chargeTimeHours240V') or '–':>9}")


if __name__ == "__main__":
    main()
