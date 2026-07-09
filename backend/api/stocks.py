from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from data_handler.storage import DataStorage
from sqlalchemy import text

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

storage = DataStorage()


@router.get("")
async def get_stocks(limit: Optional[int] = 100, keyword: Optional[str] = None, market: Optional[str] = None):
    query = """
        SELECT ts_code, name, area, industry, market, list_date, list_status
        FROM stock_basic_info
        WHERE list_status = 'L'
    """
    params = []
    if keyword:
        query += " AND (ts_code LIKE %s OR name LIKE %s)"
        params.extend([f'%{keyword}%', f'%{keyword}%'])
    if market:
        query += " AND market = %s"
        params.append(market)
    query += " ORDER BY list_date DESC LIMIT %s"
    params.append(limit)
    import pandas as pd
    df = pd.read_sql(query, storage.engine, params=tuple(params))
    return df.to_dict(orient='records')


@router.get("/{code}")
async def get_stock(code: str):
    query = """
        SELECT ts_code, name, area, industry, market, list_date, list_status, fullname, is_hs
        FROM stock_basic_info
        WHERE ts_code = %s
    """
    import pandas as pd
    df = pd.read_sql(query, storage.engine, params=(code,))
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock not found")
    return df.iloc[0].to_dict()


@router.put("/{code}")
async def update_stock(code: str, data: dict):
    query = text("""
        UPDATE stock_basic_info
        SET name = :name, area = :area, industry = :industry, market = :market,
            list_date = :list_date, list_status = :list_status, fullname = :fullname, is_hs = :is_hs
        WHERE ts_code = :code
    """)
    params = {
        'name': data.get('name') or None,
        'area': data.get('area') or None,
        'industry': data.get('industry') or None,
        'market': data.get('market') or None,
        'list_date': data.get('list_date') or None,
        'list_status': data.get('list_status') or 'L',
        'fullname': data.get('fullname') or None,
        'is_hs': data.get('is_hs') or 'N',
        'code': code
    }
    with storage.engine.connect() as conn:
        conn.execute(query, params)
        conn.commit()
    return {"message": "Stock updated successfully"}