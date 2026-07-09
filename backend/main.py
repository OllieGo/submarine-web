import sys
import os

submarine_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'submarine')
submarine_path = os.path.abspath(submarine_path)
sys.path.insert(0, submarine_path)
print(f"Submarine path: {submarine_path}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.strategies import router as strategies_router
from api.stocks import router as stocks_router
from api.backtest import router as backtest_router

app = FastAPI(title="Submarine Quant API", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(strategies_router)
app.include_router(stocks_router)
app.include_router(backtest_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)