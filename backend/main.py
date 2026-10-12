
import os
import secrets
from datetime import datetime, timezone
from typing import Literal

import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

app = FastAPI(
    title="Enterprise IT Asset Management API",
    version="4.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)


def verify_api_key(
    api_key: str | None = Security(api_key_header)
):
    expected = os.environ.get("ASSET_API_KEY")

    if (
        not expected
        or not api_key
        or not secrets.compare_digest(api_key, expected)
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


class AssetInput(BaseModel):
    asset_name: str = Field(min_length=1, max_length=100)
    asset_type: str = Field(min_length=1, max_length=50)
    status: Literal["active", "inactive", "maintenance"] = "active"


def db_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
        row_factory=dict_row
    )


def database_error():
    raise HTTPException(
        status_code=503,
        detail="Database temporarily unavailable"
    )


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-backend",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/assets", dependencies=[Depends(verify_api_key)])
def get_assets():
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM assets ORDER BY id"
                )
                return {"assets": cur.fetchall()}
    except (psycopg.Error, KeyError):
        database_error()


@app.post("/api/assets", status_code=201,
          dependencies=[Depends(verify_api_key)])
def create_asset(asset: AssetInput):
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO assets
                    (asset_name, asset_type, status)
                    VALUES (%s, %s, %s)
                    RETURNING *
                    """,
                    (asset.asset_name, asset.asset_type, asset.status)
                )
                return cur.fetchone()
    except (psycopg.Error, KeyError):
        database_error()


@app.put("/api/assets/{asset_id}",
         dependencies=[Depends(verify_api_key)])
def update_asset(asset_id: int, asset: AssetInput):
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE assets
                    SET asset_name = %s,
                        asset_type = %s,
                        status = %s
                    WHERE id = %s
                    RETURNING *
                    """,
                    (
                        asset.asset_name,
                        asset.asset_type,
                        asset.status,
                        asset_id
                    )
                )
                result = cur.fetchone()

                if result is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Asset not found"
                    )
                return result
    except (psycopg.Error, KeyError):
        database_error()


@app.delete("/api/assets/{asset_id}",
            dependencies=[Depends(verify_api_key)])
def delete_asset(asset_id: int):
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM assets WHERE id = %s RETURNING id",
                    (asset_id,)
                )
                result = cur.fetchone()

                if result is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Asset not found"
                    )

                return {
                    "message": "Asset deleted",
                    "id": result["id"]
                }
    except (psycopg.Error, KeyError):
        database_error()

