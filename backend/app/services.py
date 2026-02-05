"""Serviço para buscar e normalizar dados do IBGE."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import requests

from .config import IBGE_BASE

_MISSING_VALUES = {"...", None, "-", "X"}


def fetch_ibge(
    aggregate_id: str,
    variable_id: str,
    periods: Sequence[str],
    *,
    localidades: str = "N1[all]",
    classificacao: str | None = None,
) -> list[dict[str, Any]]:
    period_query = "|".join(list(periods)[-48:])
    endpoint = f"{IBGE_BASE}/agregados/{aggregate_id}/periodos/{period_query}/variaveis/{variable_id}"
    params: dict[str, str] = {"localidades": localidades}
    if classificacao:
        params["classificacao"] = classificacao

    response = requests.get(endpoint, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else []

def format_period(period: str) -> str:
    if len(period) == 6:
        return f"{period[:4]}-{period[4:]}"
    return period


def _safe_float(value: Any) -> float | None:
    if value in _MISSING_VALUES:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def parse_serie(serie: Mapping[str, Any]) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = [
        {"period": format_period(period), "value": _safe_float(value)} for period, value in serie.items()
    ]
    parsed.sort(key=lambda item: item["period"])
    return parsed

def parse_simple_series(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    try:
        serie = data[0]["resultados"][0]["series"][0]["serie"]
        return parse_serie(serie)
    except (KeyError, IndexError, TypeError):
        return []

def parse_multi_series(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    try:
        series_list = data[0]["resultados"][0]["series"]
    except (KeyError, IndexError, TypeError):
        return []

    parsed: list[dict[str, Any]] = []
    for item in series_list:
        parsed.append(
            {
                "name": item.get("localidade", {}).get("nome", "?"),
                "series": parse_serie(item.get("serie", {})),
            }
        )
    return parsed

def parse_classified_series(
    data: list[dict[str, Any]],
    categories: Mapping[str, str],
) -> list[dict[str, Any]]:
    try:
        resultados = data[0]["resultados"]
    except (KeyError, IndexError, TypeError):
        return []

    parsed: list[dict[str, Any]] = []
    for resultado in resultados:
        classificacoes = resultado.get("classificacoes", [])
        if classificacoes:
            categoria = classificacoes[0].get("categoria", {})
            cat_id = next(iter(categoria.keys()), None) if categoria else None
            cat_name = categories.get(str(cat_id), "?")
        else:
            cat_name = "Total"
        
        series = resultado.get("series", [])
        if series:
            parsed.append({"name": cat_name, "series": parse_serie(series[0].get("serie", {}))})
    
    return parsed

def build_summary(series: list[dict[str, Any]]) -> dict[str, Any]:
    values = [item["value"] for item in series if item["value"] is not None]
    if not values:
        return {
            "latest": None,
            "latestPeriod": None,
            "min": None,
            "max": None,
            "average": None,
            "trend": None,
        }

    latest_item = next((item for item in reversed(series) if item["value"] is not None), None)
    
    prev_value = None
    if latest_item:
        for item in reversed(series):
            if item["period"] != latest_item["period"] and item["value"] is not None:
                prev_value = item["value"]
                break

    trend = (latest_item["value"] - prev_value) if latest_item and prev_value is not None else None

    return {
        "latest": latest_item["value"] if latest_item else None,
        "latestPeriod": latest_item["period"] if latest_item else None,
        "min": min(values),
        "max": max(values),
        "average": round(sum(values) / len(values), 2),
        "trend": round(trend, 2) if trend is not None else None,
    }
