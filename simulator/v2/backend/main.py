# main.py
from fastapi import FastAPI
from simulator.v2.backend.app.api.v1.endpoints import printers

app = FastAPI()
app.include_router(printers.router, prefix="/api/v1/printers" )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simulator.v2.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )