import sys
import os

submarine_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'submarine')
submarine_path = os.path.abspath(submarine_path)
sys.path.insert(0, submarine_path)
print(f"Submarine path: {submarine_path}")

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json

from data_handler.storage import DataStorage
from sqlalchemy import text

app = FastAPI(title="Submarine Quant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api/strategies")
async def get_strategies(category: Optional[str] = None):
    df = storage.get_strategy_types(category)
    return df.to_dict(orient='records')

@app.get("/api/strategies/{code}")
async def get_strategy(code: str):
    strategy = storage.get_strategy_type(code)
    if strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@app.get("/api/stocks")
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

@app.get("/api/stocks/{code}")
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

@app.put("/api/stocks/{code}")
async def update_stock(code: str, data: dict):
    from sqlalchemy import text
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

@app.get("/api/backtest/results")
async def get_backtest_results(
    ts_code: Optional[str] = None,
    strategy_type: Optional[str] = None,
    limit: Optional[int] = 100
):
    df = storage.get_backtest_results(ts_code, strategy_type, limit)
    return df.to_dict(orient='records')

@app.get("/api/backtest/results/{result_id}")
async def get_backtest_result(result_id: int):
    df = storage.get_backtest_results(limit=1)
    if df.empty:
        raise HTTPException(status_code=404, detail="Result not found")
    return df.iloc[0].to_dict()

@app.delete("/api/backtest/results")
async def delete_backtest_results(ids: List[int] = Body(...)):
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    
    # 构建安全的占位符
    placeholders = ','.join([':id{}'.format(i) for i in range(len(ids))])
    params = {'id{}'.format(i): val for i, val in enumerate(ids)}
    
    # 定义 3 个删除语句
    queries = [
        f"DELETE FROM backtest_trade WHERE result_id IN ({placeholders})",
        f"DELETE FROM backtest_equity_curve WHERE result_id IN ({placeholders})",
        f"DELETE FROM backtest_result WHERE id IN ({placeholders})"
    ]
    
    # 使用事务执行（保证原子性，要么全删，要么都不删）
    with storage.engine.begin() as conn:
        for query in queries:
            conn.execute(text(query), params)
            
    return {"message": f"Deleted {len(ids)} results successfully"}

@app.get("/api/backtest/equity/{result_id}")
async def get_equity_curve(result_id: int):
    df = storage.get_backtest_equity_curve(result_id)
    return df.to_dict(orient='records')

@app.get("/api/backtest/trades/{result_id}")
async def get_trades(result_id: int):
    df = storage.get_backtest_trades(result_id)
    return df.to_dict(orient='records')

@app.post("/api/backtest/run")
async def run_backtest(request: BacktestRequest):
    import subprocess
    import shlex
    
    args = [
        'python', 'strategy/run_backtest.py',
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
        result = subprocess.run(
            args,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
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

@app.get("/api/backtest/stats")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)