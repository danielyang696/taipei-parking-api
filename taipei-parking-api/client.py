import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/parking-lots"

def show(title, response):
    print(f"\n=== {title} ===")
    print("Status:", response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)

def main():
    show("GET list", requests.get(BASE_URL, params={"limit": 5}, timeout=10))

    payload = {
        "id": "DEMO-001",
        "name": "API 測試停車場",
        "area": "中正區",
        "address": "測試地址 1 號",
        "tel": "02-0000-0000",
        "summary": "RESTful API Client 測試資料",
        "payex": "每小時 30 元",
        "tw97x": 301000.0,
        "tw97y": 2770000.0,
        "totalcar": 100,
        "totalmotor": 50,
        "charging_station": 2
    }

    show("POST create", requests.post(BASE_URL, json=payload, timeout=10))
    show("GET one", requests.get(f"{BASE_URL}/DEMO-001", timeout=10))

    update_payload = {**payload, "name": "API 測試停車場（已更新）", "totalcar": 120}
    show("PUT update", requests.put(
        f"{BASE_URL}/DEMO-001", json=update_payload, timeout=10
    ))

    show("DELETE", requests.delete(f"{BASE_URL}/DEMO-001", timeout=10))

if __name__ == "__main__":
    main()
