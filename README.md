# 臺北市停車場 RESTful API

本專案以臺北市資料大平臺「臺北市停車場資訊 V2」為 Open Data，使用 Python + FastAPI + SQLite 建立 RESTful API。

## 執行

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python scripts/download_data.py
python scripts/import_data.py
uvicorn app.main:app --reload
```

Swagger UI:
`http://127.0.0.1:8000/docs`

ReDoc:
`http://127.0.0.1:8000/redoc`

## API

| Method | URL | 說明 |
|---|---|---|
| GET | `/api/v1/parking-lots` | 取得停車場清單 |
| GET | `/api/v1/parking-lots/{id}` | 查詢單一停車場 |
| POST | `/api/v1/parking-lots` | 新增停車場 |
| PUT | `/api/v1/parking-lots/{id}` | 更新停車場 |
| DELETE | `/api/v1/parking-lots/{id}` | 刪除停車場 |

篩選：
`GET /api/v1/parking-lots?area=中山區`
`GET /api/v1/parking-lots?keyword=公園`
`GET /api/v1/parking-lots?skip=0&limit=20`

API Client:
```bash
python client.py
```

單元測試：
```bash
python -m unittest tests/test_api.py
```

## 專案架構

```text
臺北市 Open Data
       ↓
parking_lots.json
       ↓
SQLite
       ↓
FastAPI RESTful API
   ┌───┼────┐
   ↓   ↓    ↓
Swagger Client Browser
```
