"""IBGE Dashboard API - Main Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import basic, analysis

app = FastAPI(
    title="IBGE Dashboard API",
    version="3.0.0",
    description="API profissional para análise do mercado de trabalho brasileiro"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basic.router)
app.include_router(analysis.router)

@app.get("/")
async def root():
    return {
        "message": "IBGE Dashboard API",
        "version": "3.0.0",
        "endpoints": {
            "basicos": ["/api/ibge/unemployment", "/api/ibge/occupied", "/api/ibge/income"],
            "analise": ["/api/analysis/sex", "/api/analysis/race", "/api/analysis/age", "/api/analysis/education", "/api/analysis/region"]
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
