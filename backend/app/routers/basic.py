"""Endpoints básicos de indicadores."""

import logging

from fastapi import APIRouter, HTTPException

from ..config import AGGREGATES, DEFAULT_PERIODS
from ..services import fetch_ibge, parse_simple_series, build_summary

router = APIRouter(prefix="/api/ibge", tags=["Indicadores Básicos"])

logger = logging.getLogger(__name__)


def _basic_indicator_payload(indicator_key: str, *, include_series: bool) -> dict:
    cfg = AGGREGATES.get(indicator_key)
    if not cfg:
        raise HTTPException(status_code=404, detail="Indicador não encontrado")

    raw = fetch_ibge(cfg["id"], cfg["var"], DEFAULT_PERIODS)
    series = parse_simple_series(raw)
    payload: dict = {
        "success": True,
        "indicator": cfg["name"],
        "summary": build_summary(series),
    }
    if "unit" in cfg:
        payload["unit"] = cfg["unit"]
    if include_series:
        payload["series"] = series
    return payload


def _handle_unexpected_error(exc: Exception) -> None:
    logger.exception("Falha ao obter dados do IBGE")
    raise HTTPException(status_code=502, detail="Falha ao obter dados do IBGE")

@router.get("/unemployment")
async def get_unemployment():
    """Taxa de desocupação nacional"""
    try:
        return _basic_indicator_payload("unemployment", include_series=True)
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/unemployment/summary")
async def get_unemployment_summary():
    """Resumo da taxa de desocupação"""
    try:
        return _basic_indicator_payload("unemployment", include_series=False)
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/occupied")
async def get_occupied():
    """População ocupada"""
    try:
        return _basic_indicator_payload("occupied", include_series=True)
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/income")
async def get_income():
    """Rendimento médio"""
    try:
        return _basic_indicator_payload("income", include_series=True)
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/informality")
async def get_informality():
    """Massa de rendimento"""
    try:
        return _basic_indicator_payload("mass", include_series=True)
    except Exception as e:
        _handle_unexpected_error(e)
