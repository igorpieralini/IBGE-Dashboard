# IBGE Dashboard

A full-stack dashboard for visualizing Brazilian labor market data from IBGE (Brazilian Institute of Geography and Statistics) PNAD Contínua survey.

![Vue.js](https://img.shields.io/badge/Vue.js-3.4-4FC08D?logo=vuedotjs)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chartdotjs)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)

## Overview

This project provides an interactive dashboard to explore Brazilian employment statistics including unemployment rates, employed population, average in'come, and income mass. Data is fetched in real-time from the official IBGE API.

## Features

- **Real-time Data** - Direct integration with IBGE's public API
- **Interactive Charts** - Line and bar charts with Chart.js
- **Demographic Analysis** - Breakdown by sex, race, age, education, and region
- **Responsive Design** - Works on desktop and mobile
- **RESTful API** - Well-documented FastAPI backend
- **CSV Export** - Download data for external analysis

## Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| FastAPI | 0.109 | Web framework |
| Uvicorn | 0.27 | ASGI server |
| HTTPX | 0.26 | Async HTTP client |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.4 | UI framework |
| Vite | 5.0 | Build tool |
| Chart.js | 4.4 | Charts |
| Axios | 1.6 | HTTP client |
| Vue Router | 4.3 | Navigation |

## Project Structure

```
IBGE-API/
├── backend/
│   ├── main.py                 # Application entry point
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── config.py           # IBGE aggregates & periods
│       ├── services.py         # Data fetching & parsing
│       └── routers/
│           ├── basic.py        # Basic indicator endpoints
│           └── analysis.py     # Advanced analysis endpoints
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue             # Root component
│       ├── main.js             # Entry point
│       ├── style.css           # Global styles
│       ├── router/
│       │   └── index.js        # Route definitions
│       ├── pages/
│       │   ├── HomePage.vue    # Landing page
│       │   ├── DashboardPage.vue   # Main dashboard
│       │   └── AnalisePage.vue     # Demographic analysis
│       ├── components/
│       │   ├── AppHeader.vue
│       │   ├── AppFooter.vue
│       │   ├── StatCard.vue
│       │   ├── ChartCard.vue
│       │   ├── FilterPanel.vue
│       │   ├── LoadingSpinner.vue
│       │   └── ErrorMessage.vue
│       └── services/
│           └── ibgeApi.js      # API client
│
├── start.bat                   # Windows startup script
├── start.sh                    # Linux/Mac startup script
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- pip (comes with Python)
- npm (comes with Node.js)

### Option 1: Automatic Setup

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup

**1. Start the Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**2. Start the Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

### Access the Application

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:5173 |
| API Documentation | http://localhost:8001/docs |
| Health Check | http://localhost:8001/health |

## API Endpoints

### Basic Indicators

| Endpoint | Description |
|----------|-------------|
| `GET /api/ibge/unemployment` | Unemployment rate time series |
| `GET /api/ibge/unemployment/summary` | Unemployment statistical summary |
| `GET /api/ibge/occupied` | Employed population |
| `GET /api/ibge/income` | Average real income |
| `GET /api/ibge/informality` | Income mass |

### Advanced Analysis

| Endpoint | Description |
|----------|-------------|
| `GET /api/analysis/sex` | Analysis by sex |
| `GET /api/analysis/race` | Analysis by race/ethnicity |
| `GET /api/analysis/age` | Analysis by age group |
| `GET /api/analysis/education` | Analysis by education level |
| `GET /api/analysis/region` | Analysis by geographic region |

All analysis endpoints accept an optional `indicator` query parameter:
- `unemployment` (default)
- `income`

## Dashboard Views

### Home Page
Landing page with project overview and navigation.

### Dashboard
Main view with 4 key indicators:
- **Unemployment Rate (%)** - Line chart
- **Employed Population (thousands)** - Line chart
- **Average Real Income (R$)** - Bar chart
- **Income Mass (millions R$)** - Line chart

Plus summary cards showing latest values and trends.

### Analysis Page
Demographic breakdowns with insights:
- **By Sex** - Male vs Female comparison
- **By Race** - White, Black, Brown, Other
- **By Age** - Youth (14-17), Young Adults (18-24), Adults (25-39, 40-59), Seniors (60+)
- **By Education** - From incomplete elementary to higher education
- **By Region** - North, Northeast, Southeast, South, Central-West

## Data Source

All data comes from **PNAD Contínua** (Continuous National Household Sample Survey) conducted by IBGE:

| Aggregate | ID | Description |
|-----------|-----|-------------|
| Unemployment | 6381 | Unemployment rate (%) |
| Occupied | 6318 | Employed population (thousands) |
| Income | 6387 | Average real income (R$) |
| Mass | 6392 | Income mass (millions R$) |
| Regional | 6468 | Regional unemployment rates |

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Windows - find process using port
netstat -ano | findstr :8001

# Linux/Mac
lsof -i :8001
```

### CORS errors
Ensure the backend is running on port 8001 before starting the frontend. The Vite config proxies `/api` requests to the backend.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [IBGE](https://www.ibge.gov.br/) for providing the public API
- [SIDRA](https://sidra.ibge.gov.br/) for the data aggregation system
- PNAD Contínua survey methodology
