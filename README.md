# IBGE Dashboard

A full-stack dashboard for visualizing Brazilian labor market data from the IBGE (PNAD Contínua survey).

![Vue.js](https://img.shields.io/badge/Vue.js-3.4-4FC08D?logo=vuedotjs)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chartdotjs)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)

## Overview

Interactive dashboard for exploring Brazilian employment indicators such as unemployment rate, employed population, average income, and income mass. Data is fetched in real time from the official IBGE API.

## Features

* Real-time data from IBGE
* Interactive charts (line and bar)
* Demographic breakdowns (sex, race, age, education, region)
* Responsive UI
* REST API built with FastAPI
* CSV export

## Tech Stack

**Backend**

* Python 3.10+
* FastAPI
* Uvicorn
* HTTPX

**Frontend**

* Vue.js 3
* Vite
* Chart.js
* Axios
* Vue Router

## Project Structure

```
IBGE-API/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── app/
│       ├── config.py
│       ├── services.py
│       └── routers/
│           ├── basic.py
│           └── analysis.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── main.js
│       ├── router/
│       ├── pages/
│       ├── components/
│       └── services/
│
├── start.bat
├── start.sh
└── README.md
```

## Getting Started

### Requirements

* Python 3.10+
* Node.js 18+

### Automatic Setup

**Windows**

```bash
start.bat
```

**Linux / macOS**

```bash
chmod +x start.sh
./start.sh
```

### Manual Setup

**Backend**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

### Access

| Service      | URL                                                          |
| ------------ | ------------------------------------------------------------ |
| Dashboard    | [http://localhost:5173](http://localhost:5173)               |
| API Docs     | [http://localhost:8001/docs](http://localhost:8001/docs)     |
| Health Check | [http://localhost:8001/health](http://localhost:8001/health) |

## API

### Core Indicators

* `GET /api/ibge/unemployment`
* `GET /api/ibge/occupied`
* `GET /api/ibge/income`
* `GET /api/ibge/informality`

### Analysis

* `GET /api/analysis/sex`
* `GET /api/analysis/race`
* `GET /api/analysis/age`
* `GET /api/analysis/education`
* `GET /api/analysis/region`

Optional query parameter:

```
indicator=unemployment | income
```

## Dashboard

* Unemployment rate
* Employed population
* Average real income
* Income mass

Includes summary cards with latest values and trends.

## Data Source

All data comes from **IBGE – PNAD Contínua**, via the SIDRA API.

## Acknowledgments

* IBGE
* SIDRA
* PNAD Contínua methodology
