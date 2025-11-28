import os
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI

app = FastAPI(
    title="Orion ERP API",
    version="1.0.0"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://orion_user:orion_pass@db:5432/orion_db"
)


@app.get("/health")
def health():
    return {
        "service": "orion-api",
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/companies")
def list_companies():
    # DB'ye bağlan, tabloyu oku, JSON olarak döndür
    with psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, tax_no, 'ERP' AS source FROM companies ORDER BY id;")
            rows = cur.fetchall()
    return rows

