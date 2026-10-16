#!/usr/bin/env python3
"""
Bulk VIN decode to CSV (Python 3.8+, needs `requests`)

Reads VINs (one per line) and decodes them in batches of 50 with POST /vin/batch.

API:     https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api
Support: Telegram @pintoflow

Usage:
    pip install requests
    export RAPIDAPI_KEY=your_key
    python3 bulk_vin_to_csv.py vins.txt --out decoded.csv
"""
import argparse
import csv
import os
import sys
import time

import requests

HOST = "car-specs-api.p.rapidapi.com"
KEY = os.environ.get("RAPIDAPI_KEY")


def batch(vins):
    for attempt, wait in enumerate((0, 2, 5, 15)):
        time.sleep(wait)
        r = requests.post(f"https://{HOST}/vin/batch", json={"vins": vins},
                          headers={"x-rapidapi-host": HOST, "x-rapidapi-key": KEY}, timeout=120)
        if r.status_code in (502, 504):  # only retry upstream errors
            continue
        body = r.json()
        if not body.get("success"):
            sys.exit(f"{body.get('error', {}).get('code')}: {body.get('error', {}).get('message')}")
        data = body["data"]
        return data if isinstance(data, list) else data.get("results", [])
    sys.exit("Data source unavailable, try again later")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="text file with one VIN per line")
    ap.add_argument("--out", default="decoded_vins.csv")
    a = ap.parse_args()
    if not KEY:
        sys.exit("Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your_key")

    vins = list(dict.fromkeys(l.strip().upper() for l in open(a.file) if l.strip()))
    rows = []
    for i in range(0, len(vins), 50):
        for item in batch(vins[i:i + 50]):
            d = item.get("data") or {}
            d = d.get("vin", d) if isinstance(d, dict) else {}
            eng = d.get("engine") or {}
            rows.append({
                "vin": item.get("vin") or d.get("vin"),
                "ok": item.get("success", "error" not in item),
                "year": d.get("modelYear"), "make": d.get("make"), "model": d.get("model"), "trim": d.get("trim"),
                "body": d.get("bodyClass"), "fuel": d.get("fuelType"),
                "engine_l": eng.get("displacementL"), "cylinders": eng.get("cylinders"), "hp": eng.get("horsepower"),
                "error": (item.get("error") or {}).get("message"),
            })
        print(f"Decoded {min(i + 50, len(vins))}/{len(vins)}")

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {len(rows)} rows to {a.out}")


if __name__ == "__main__":
    main()
