from fastapi import APIRouter, HTTPException, Body
from typing import Optional, List
import subprocess
import os
import sys

from data_handler.storage import DataStorage
from sqlalchemy import text
from pydantic import BaseModel

router = APIRouter(prefix="/api/backtest", tags=["backtest"])

storage = DataStorage()


class BacktestRequest(BaseModel):
    strategy_type: str
    ts_code: str
    initial_capital: Optional[float] = 100000
    commission_rate: Optional[float] = 0.0003
    slippage_rate: Optional[float] = 0.001
    short_window: Optional[int] = 5
    mid_window: Optional[int] = 20
    long_window: Optional[int] = 60
    volume_filter: Optional[bool] = False
    volume_ratio: Optional[float] = 1.5
    limit: Optional[int] = 500


@router.get("/results")
async def get_backtest_results(
    ts_code: Optional[str] = None,
    strategy_type: Optional[str] = None,
    limit: Optional[int] = 100
):
    df = storage.get_backtest_results(ts_code, strategy_type, limit)
    return df.to_dict(orient='records')


@router.get("/results/{result_id}")
async def get_backtest_result(result_id: int):
    df = storage.get_backtest_results(limit=1)
    if df.empty:
        raise HTTPException(status_code=404, detail="Result not found")
    return df.iloc[0].to_dict()


@router.delete("/results")
async def delete_backtest_results(ids: List[int] = Body(...)):
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided")

    placeholders = ','.join([':id{}'.format(i) for i in range(len(ids))])
    params = {'id{}'.format(i): val for i, val in enumerate(ids)}

    queries = [
        f"DELETE FROM backtest_trade WHERE result_id IN ({placeholders})",
        f"DELETE FROM backtest_equity_curve WHERE result_id IN ({placeholders})",
        f"DELETE FROM backtest_result WHERE id IN ({placeholders})"
    ]

    with storage.engine.begin() as conn:
        for query in queries:
            conn.execute(text(query), params)

    return {"message": f"Deleted {len(ids)} results successfully"}


@router.get("/equity/{result_id}")
async def get_equity_curve(result_id: int):
    df = storage.get_backtest_equity_curve(result_id)
    return df.to_dict(orient='records')


@router.get("/trades/{result_id}")
async def get_trades(result_id: int):
    df = storage.get_backtest_trades(result_id)
    return df.to_dict(orient='records')


@router.post("/run")
async def run_backtest(request: BacktestRequest):
    args = [
        sys.executable, 'strategy/run_backtest.py',
        '--strategy', request.strategy_type,
        '--stock', request.ts_code,
        '--initial-capital', str(request.initial_capital),
        '--commission-rate', str(request.commission_rate),
        '--slippage-rate', str(request.slippage_rate),
        '--limit', str(request.limit)
    ]

    if hasattr(request, 'short_window') and request.short_window:
        args.extend(['--short', str(request.short_window)])
    if hasattr(request, 'mid_window') and request.mid_window:
        args.extend(['--mid', str(request.mid_window)])
    if hasattr(request, 'long_window') and request.long_window:
        args.extend(['--long', str(request.long_window)])

    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        result = subprocess.run(
            args,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        return {"success": True, "output": result.stdout}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Backtest timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_backtest_stats():
    query = """
        SELECT
            COUNT(*) as total_tests,
            COUNT(DISTINCT ts_code) as total_stocks,
            COUNT(DISTINCT strategy_type) as total_strategies,
            AVG(total_return) as avg_return,
            AVG(sharpe_ratio) as avg_sharpe,
            MIN(max_drawdown) as min_drawdown,
            MAX(max_drawdown) as max_drawdown
        FROM backtest_result
    """
    import pandas as pd
    df = pd.read_sql(query, storage.engine)
    return df.iloc[0].to_dict()