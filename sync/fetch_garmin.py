# Road to 1:35 — Garmin Connect sync
# Copyright (c) 2026 Antonio. All rights reserved. Proprietary; see LICENSE.
#
# Runs inside GitHub Actions. Logs into Garmin Connect with the credentials
# stored as repository secrets, pulls recent running activities, and writes
# activities.json in the format the tracker app imports.
#
# Uses the unofficial `garminconnect` library (pip install garminconnect).

import json
import os
import sys
from datetime import datetime, timedelta

from garminconnect import Garmin

OUT_FILE = "activities.json"
SINCE = "2026-07-17"          # ignore anything before the training block
MAX_ACTIVITIES = 100          # how many recent activities to scan
RUN_TYPES = {"running", "treadmill_running", "trail_running", "track_running",
             "indoor_running", "street_running"}


def main() -> int:
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    if not email or not password:
        print("ERROR: GARMIN_EMAIL / GARMIN_PASSWORD secrets are not set")
        return 1

    g = Garmin(email, password)
    g.login()

    raw = g.get_activities(0, MAX_ACTIVITIES)
    out = []
    for a in raw:
        type_key = (a.get("activityType") or {}).get("typeKey", "")
        if type_key not in RUN_TYPES:
            continue

        start_local = a.get("startTimeLocal") or a.get("startTimeGMT") or ""
        date = start_local[:10]
        if not date or date < SINCE:
            continue

        dist_km = round((a.get("distance") or 0) / 1000.0, 2)
        if dist_km < 0.2:
            continue

        moving = a.get("movingDuration") or a.get("duration") or 0
        elapsed = a.get("elapsedDuration") or a.get("duration") or moving

        out.append({
            "date": date,
            # "YYYY-MM-DD HH:MM:SS" -> ISO-ish "YYYY-MM-DDTHH:MM:SS"
            "startISO": start_local.replace(" ", "T") if start_local else None,
            "dist": dist_km,
            "time": round(moving),
            "elapsed": round(elapsed),
            "avgHR": round(a["averageHR"]) if a.get("averageHR") else None,
            "maxHR": round(a["maxHR"]) if a.get("maxHR") else None,
            "avgCad": round(a["averageRunningCadenceInStepsPerMinute"])
                      if a.get("averageRunningCadenceInStepsPerMinute") else None,
            "gain": round(a["elevationGain"]) if a.get("elevationGain") else None,
            "src": "garmin-sync",
        })

    out.sort(key=lambda x: x["startISO"] or x["date"])

    payload = {
        "generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "activities": out,
    }
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)

    print(f"Wrote {len(out)} running activities to {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
