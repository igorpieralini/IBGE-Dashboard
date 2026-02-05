"""Endpoints de análise avançada."""

import logging
from collections.abc import Mapping

from fastapi import APIRouter, HTTPException, Query

from ..config import AGGREGATES_REGIONAL, AGGREGATES_TRIMESTRAL, CLASSIFICATIONS, PERIODS_TRIMESTRAL
from ..services import build_summary, fetch_ibge, parse_classified_series, parse_multi_series

router = APIRouter(prefix="/api/analysis", tags=["Análise Avançada"])

logger = logging.getLogger(__name__)


def _category_ids_without_total(categories: Mapping[str, str]) -> str:
    return ",".join([category_id for category_id, name in categories.items() if name != "Total"])


def _classified_analysis_payload(*, classification_key: str, indicator: str, suffix: str, label: str) -> dict:
    cfg_key = f"{indicator}_{suffix}"
    cfg = AGGREGATES_TRIMESTRAL.get(cfg_key)
    if not cfg:
        raise HTTPException(status_code=400, detail=f"Indicador '{indicator}' não disponível")

    cats = CLASSIFICATIONS[classification_key]["categories"]
    cat_ids = _category_ids_without_total(cats)
    raw = fetch_ibge(
        cfg["id"],
        cfg["var"],
        PERIODS_TRIMESTRAL,
        classificacao=f"{cfg['class_id']}[{cat_ids}]",
    )
    categories = parse_classified_series(raw, cats)
    return {
        "success": True,
        "classification": label,
        "categories": categories,
        "summaries": {item["name"]: build_summary(item["series"]) for item in categories},
    }


def _handle_unexpected_error(exc: Exception) -> None:
    logger.exception("Falha ao obter dados do IBGE")
    raise HTTPException(status_code=502, detail="Falha ao obter dados do IBGE")

@router.get("/sex")
async def analysis_by_sex(indicator: str = Query("unemployment")):
    """Análise por sexo"""
    try:
        return _classified_analysis_payload(
            classification_key="sex",
            indicator=indicator,
            suffix="sex",
            label="Sexo",
        )
    except HTTPException:
        raise
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/race")
async def analysis_by_race(indicator: str = Query("unemployment")):
    """Análise por cor/raça"""
    try:
        return _classified_analysis_payload(
            classification_key="race",
            indicator=indicator,
            suffix="race",
            label="Cor ou Raça",
        )
    except HTTPException:
        raise
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/age")
async def analysis_by_age():
    """Análise por faixa etária"""
    try:
        cfg = AGGREGATES_TRIMESTRAL["unemployment_age"]
        cats = CLASSIFICATIONS["age"]["categories"]
        cat_ids = _category_ids_without_total(cats)

        raw = fetch_ibge(
            cfg["id"],
            cfg["var"],
            PERIODS_TRIMESTRAL,
            classificacao=f"{cfg['class_id']}[{cat_ids}]",
        )
        categories = parse_classified_series(raw, cats)

        return {
            "success": True,
            "classification": "Faixa Etária",
            "categories": categories,
            "summaries": {item["name"]: build_summary(item["series"]) for item in categories},
        }
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/education")
async def analysis_by_education(indicator: str = Query("unemployment")):
    """Análise por escolaridade"""
    try:
        return _classified_analysis_payload(
            classification_key="education",
            indicator=indicator,
            suffix="education",
            label="Escolaridade",
        )
    except HTTPException:
        raise
    except Exception as e:
        _handle_unexpected_error(e)

@router.get("/region")
async def analysis_by_region(indicator: str = Query("unemployment")):
    """Análise por região"""
    try:
        if indicator not in AGGREGATES_REGIONAL:
            raise HTTPException(status_code=400, detail=f"Indicador '{indicator}' não disponível por região")
        
        cfg = AGGREGATES_REGIONAL[indicator]
        raw = fetch_ibge(cfg["id"], cfg["var"], PERIODS_TRIMESTRAL, localidades="N2[all]")
        categories = parse_multi_series(raw)
        
        return {
            "success": True,
            "classification": "Região",
            "categories": categories,
            "summaries": {s["name"]: build_summary(s["series"]) for s in categories}
        }
    except HTTPException:
        raise
    except Exception as e:
        _handle_unexpected_error(e)
