from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "parking.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS parking_lots (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    area TEXT,
    address TEXT,
    tel TEXT,
    summary TEXT,
    payex TEXT,
    tw97x REAL,
    tw97y REAL,
    totalcar INTEGER,
    totalmotor INTEGER,
    charging_station INTEGER
)
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()
