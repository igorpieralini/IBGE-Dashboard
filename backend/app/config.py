"""Configurações e constantes do sistema"""

IBGE_BASE = "https://servicodados.ibge.gov.br/api/v3"

AGGREGATES = {
    "unemployment": {"id": "6381", "var": "4099", "name": "Taxa de desocupação", "unit": "%"},
    "occupied": {"id": "6318", "var": "1641", "name": "População ocupada", "unit": "Mil pessoas"},
    "income": {"id": "6387", "var": "5935", "name": "Rendimento médio", "unit": "R$"},
    "mass": {"id": "6392", "var": "6293", "name": "Massa de rendimento", "unit": "Milhões R$"},
}

AGGREGATES_REGIONAL = {
    "unemployment": {"id": "6468", "var": "4099", "name": "Taxa de desocupação", "unit": "%"},
    "occupied": {"id": "6461", "var": "4090", "name": "População ocupada", "unit": "Mil pessoas"},
    "income": {"id": "6475", "var": "5935", "name": "Rendimento médio", "unit": "R$"},
}

AGGREGATES_TRIMESTRAL = {
    "unemployment_sex": {"id": "4093", "var": "4099", "class_id": "2"},
    "income_sex": {"id": "5436", "var": "5935", "class_id": "2"},
    "occupied_sex": {"id": "4093", "var": "4090", "class_id": "2"},
    "unemployment_race": {"id": "6402", "var": "4099", "class_id": "86"},
    "income_race": {"id": "6405", "var": "5935", "class_id": "86"},
    "unemployment_age": {"id": "6397", "var": "4099", "class_id": "58"},
    "unemployment_education": {"id": "4095", "var": "4099", "class_id": "1568"},
    "occupied_education": {"id": "4095", "var": "4090", "class_id": "1568"},
    "income_position": {"id": "5439", "var": "5932", "class_id": "12029"},
    "income_category": {"id": "5440", "var": "5932", "class_id": "11913"},
}

CLASSIFICATIONS = {
    "sex": {
        "id": "2",
        "categories": {"6794": "Total", "4": "Homens", "5": "Mulheres"}
    },
    "race": {
        "id": "86",
        "categories": {"95251": "Total", "2776": "Branca", "2777": "Preta", "2779": "Parda"}
    },
    "age": {
        "id": "58",
        "categories": {
            "95253": "Total", "114535": "14 a 17 anos", "100052": "18 a 24 anos",
            "108875": "25 a 39 anos", "99127": "40 a 59 anos", "3302": "60 anos ou mais"
        }
    },
    "education": {
        "id": "1568",
        "categories": {
            "120704": "Total", "11779": "Fundamental incompleto", "11628": "Fundamental completo",
            "11630": "Médio completo", "11632": "Superior completo"
        }
    },
}

STATES = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL",
    "28": "SE", "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP", "41": "PR",
    "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"
}

DEFAULT_PERIODS = [f"{y}{m:02d}" for y in range(2023, 2026) for m in range(1, 13)]
PERIODS_TRIMESTRAL = [f"{y}0{q}" for y in range(2023, 2026) for q in range(1, 5)]
