from typing import Optional
from fastapi import FastAPI, HTTPException, Query, status
from app.database import get_connection, init_db
from app.schemas import ParkingLot, ParkingLotCreate, ParkingLotUpdate

app = FastAPI(
    title="Taipei Parking Lot RESTful API",
    description="臺北市停車場資訊 Open Data CRUD API",
    version="1.0.0",
)

@app.on_event("startup")
def startup():
    init_db()

def row_to_dict(row):
    return dict(row) if row else None

@app.get("/", tags=["System"])
def root():
    return {
        "message": "Taipei Parking Lot API",
        "docs": "/docs",
        "resource": "/api/v1/parking-lots"
    }

@app.get("/api/v1/parking-lots", response_model=list[ParkingLot], tags=["Parking Lots"])
def list_parking_lots(
    area: Optional[str] = Query(None, description="行政區，例如中山區"),
    keyword: Optional[str] = Query(None, description="名稱或地址關鍵字"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    conn = get_connection()
    sql = "SELECT * FROM parking_lots WHERE 1=1"
    params = []

    if area:
        sql += " AND area = ?"
        params.append(area)

    if keyword:
        sql += " AND (name LIKE ? OR address LIKE ?)"
        pattern = f"%{keyword}%"
        params.extend([pattern, pattern])

    sql += " ORDER BY name LIMIT ? OFFSET ?"
    params.extend([limit, skip])

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

@app.get("/api/v1/parking-lots/{parking_id}", response_model=ParkingLot, tags=["Parking Lots"])
def get_parking_lot(parking_id: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM parking_lots WHERE id = ?", (parking_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return row_to_dict(row)

@app.post(
    "/api/v1/parking-lots",
    response_model=ParkingLot,
    status_code=status.HTTP_201_CREATED,
    tags=["Parking Lots"],
)
def create_parking_lot(data: ParkingLotCreate):
    conn = get_connection()
    exists = conn.execute(
        "SELECT id FROM parking_lots WHERE id = ?", (data.id,)
    ).fetchone()
    if exists:
        conn.close()
        raise HTTPException(status_code=409, detail="Parking lot ID already exists")

    conn.execute(
        """
        INSERT INTO parking_lots
        (id, name, area, address, tel, summary, payex, tw97x, tw97y,
         totalcar, totalmotor, charging_station)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.id, data.name, data.area, data.address, data.tel,
            data.summary, data.payex, data.tw97x, data.tw97y,
            data.totalcar, data.totalmotor, data.charging_station
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM parking_lots WHERE id = ?", (data.id,)
    ).fetchone()
    conn.close()
    return row_to_dict(row)

@app.put("/api/v1/parking-lots/{parking_id}", response_model=ParkingLot, tags=["Parking Lots"])
def update_parking_lot(parking_id: str, data: ParkingLotUpdate):
    conn = get_connection()
    exists = conn.execute(
        "SELECT id FROM parking_lots WHERE id = ?", (parking_id,)
    ).fetchone()
    if not exists:
        conn.close()
        raise HTTPException(status_code=404, detail="Parking lot not found")

    conn.execute(
        """
        UPDATE parking_lots SET
        name=?, area=?, address=?, tel=?, summary=?, payex=?,
        tw97x=?, tw97y=?, totalcar=?, totalmotor=?, charging_station=?
        WHERE id=?
        """,
        (
            data.name, data.area, data.address, data.tel,
            data.summary, data.payex, data.tw97x, data.tw97y,
            data.totalcar, data.totalmotor, data.charging_station,
            parking_id
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM parking_lots WHERE id = ?", (parking_id,)
    ).fetchone()
    conn.close()
    return row_to_dict(row)

@app.delete("/api/v1/parking-lots/{parking_id}", tags=["Parking Lots"])
def delete_parking_lot(parking_id: str):
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM parking_lots WHERE id = ?", (parking_id,)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return {"message": "Parking lot deleted", "id": parking_id}
