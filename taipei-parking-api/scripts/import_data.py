import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.database import get_connection, init_db

INPUT = ROOT / "data" / "parking_lots.json"

def first(d, *keys, default=None):
    for key in keys:
        if key in d and d[key] not in ("", None):
            return d[key]
    return default

def number(v):
    if v in ("", None):
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None

def real(v):
    if v in ("", None):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def extract_records(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict) and isinstance(data.get("park"), list):
            return data["park"]
        for key in ("park", "result", "results"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ValueError("Cannot find parking list in JSON")

def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "data/parking_lots.json not found. Run: python scripts/download_data.py"
        )

    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    records = extract_records(payload)

    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM parking_lots")

    imported = 0
    for p in records:
        pid = first(p, "id", "ID", "parkId")
        name = first(p, "name", "parkName", default="未命名停車場")
        if pid is None:
            continue

        conn.execute(
            """
            INSERT OR REPLACE INTO parking_lots
            (id, name, area, address, tel, summary, payex,
             tw97x, tw97y, totalcar, totalmotor, charging_station)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(pid), str(name), first(p, "area"),
                first(p, "address", "addr"), first(p, "tel", "telephone"),
                first(p, "summary"), first(p, "payex", "payEx"),
                real(first(p, "tw97x", "TW97X", "x")),
                real(first(p, "tw97y", "TW97Y", "y")),
                number(first(p, "totalcar", "totalCar")),
                number(first(p, "totalmotor", "totalMotor")),
                number(first(p, "ChargingStation", "chargingStation")),
            ),
        )
        imported += 1

    conn.commit()
    conn.close()
    print(f"Imported {imported} parking lots into SQLite.")

if __name__ == "__main__":
    main()
