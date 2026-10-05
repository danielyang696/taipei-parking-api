import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, get_connection

class ParkingAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        conn = get_connection()
        conn.execute("DELETE FROM parking_lots")
        conn.commit()
        conn.close()
        cls.client = TestClient(app)

    def test_crud(self):
        payload = {
            "id": "TEST-001",
            "name": "測試停車場",
            "area": "大安區",
            "address": "測試路 1 號",
            "tel": "02-1234-5678",
            "summary": "test",
            "payex": "30",
            "tw97x": 300000,
            "tw97y": 2770000,
            "totalcar": 10,
            "totalmotor": 20,
            "charging_station": 1
        }

        r = self.client.post("/api/v1/parking-lots", json=payload)
        self.assertEqual(r.status_code, 201)

        r = self.client.get("/api/v1/parking-lots/TEST-001")
        self.assertEqual(r.status_code, 200)

        payload["name"] = "更新後的測試停車場"
        r = self.client.put("/api/v1/parking-lots/TEST-001", json=payload)
        self.assertEqual(r.status_code, 200)

        r = self.client.delete("/api/v1/parking-lots/TEST-001")
        self.assertEqual(r.status_code, 200)

        r = self.client.get("/api/v1/parking-lots/TEST-001")
        self.assertEqual(r.status_code, 404)

if __name__ == "__main__":
    unittest.main()
