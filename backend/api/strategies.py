from fastapi import APIRouter, HTTPException
from typing import Optional

from data_handler.storage import DataStorage

router = APIRouter(prefix="/api/strategies", tags=["strategies"])

storage = DataStorage()


@router.get("")
async def get_strategies(category: Optional[str] = None):
    df = storage.get_strategy_types(category)
    return df.to_dict(orient='records')


@router.get("/{code}")
async def get_strategy(code: str):
    strategy = storage.get_strategy_type(code)
    if strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy