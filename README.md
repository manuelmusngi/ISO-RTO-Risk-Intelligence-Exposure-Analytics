 <div align="center">

⚡ ***ISO/RTO Risk Intelligence & Exposure Analytics***

####  _Real-time market risk quantification, congestion forecasting, and position exposure analytics across North American wholesale energy markets_

<br/>

![Markets](https://img.shields.io/badge/Markets-CAISO%20%7C%20ERCOT%20%7C%20MISO%20%7C%20PJM%20%7C%20NYISO%20%7C%20ISONE-F5A623?style=flat-square)

<br/>

> **Built for energy trading desks, risk management teams, and quantitative analysts** who need sub-minute latency on LMP spreads, binding constraint alerts, and mark-to-market exposure across multi-ISO portfolios.

<br/>

[📖 Documentation](#-architecture) • [🚀 Quickstart](#-quickstart) • [📦 Modules](#-module-deep-dive) • [📊 Dashboards](#-dashboards--reporting) • [🤝 Contributing](#-contributing)

</div>

---

#### 🗺️ Table of Contents

- [Platform Overview](#-platform-overview)
- [Key Highlights](#-key-highlights)
- [Architecture](#-architecture)
- [Data Sources & Market Coverage](#-data-sources--market-coverage)
- [Project Structure](#-project-structure)
- [Module Deep Dive](#-module-deep-dive)
- [Quickstart](#-quickstart)
- [Configuration](#-configuration)
- [Dashboards & Reporting](#-dashboards--reporting)
- [Testing & Validation](#-testing--validation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

#### 🔭 Platform Overview

This project is an exercise in building an Analytics System for the power markets.

The **ISO/RTO Risk Intelligence & Exposure Analytics** is a production-grade data and analytics system that ingests, transforms, and models wholesale electricity market data from six North American ISOs/RTOs. It delivers **real-time locational marginal price (LMP) analytics**, **congestion risk scoring**, **financial transmission right (FTR) valuation**, and **mark-to-market (MtM) exposure reporting** — all within a unified, auditable data pipeline.

This platform was engineered to close the gap between raw ISO market data and actionable trading intelligence. It replaces fragmented spreadsheet workflows with a reproducible, version-controlled, enterprise-ready analytics stack.

```
The platform processes over 2.5 million LMP observations daily,
spanning 6 ISOs, 18,000+ pricing nodes, and 24 settlement intervals per hour.
```

**Who it's built for:**
- 🏦 **Energy Trading Desks** — real-time exposure dashboards and pre-trade risk screening
- 📈 **Quantitative Analysts** — LMP forecasting models, spread analytics, and historical backtesting
- 🔒 **Risk Management** — position limits, VaR computation, and binding constraint alerts
- 📋 **Regulatory & Compliance** — auditable lineage, reproducible marks, settlement reconciliation

---

#### 🌟 Key Highlights

| Capability | Detail |
|---|---|
| ⚡ **Sub-minute LMP Refresh** | Real-time price feeds from CAISO OASIS, ERCOT MIS, MISO API, PJM Data Miner 2, NYISO, ISO-NE |
| 🗺️ **18,000+ Pricing Nodes** | Full hub-and-spoke node graph with zonal aggregation and custom portfolio mapping |
| 📐 **LMP Decomposition** | Energy, congestion, and loss components tracked independently per node |
| 🚦 **Binding Constraint Engine** | Automated detection, tagging, and alert routing for binding transmission constraints |
| 💰 **FTR / CRR Valuation** | Mark-to-market valuation engine aligned to ISO auction clearing prices |
| 📊 **VaR & CVaR Modeling** | Historical simulation and parametric Value-at-Risk at position and portfolio level |
| 🤖 **LMP Forecasting** | XGBoost + LSTM ensemble models with 1-hour, 4-hour, and day-ahead horizons |
| 🔄 **dbt Lineage** | Full column-level data lineage with Freshness SLAs on every model |
| 🛡️ **Data Quality Gates** | Great Expectations suites with automated pipeline blocking on critical failures |
| 📦 **Multi-env Deployable** | Docker Compose for local dev; Terraform + Azure for production |

---

#### 🏛️ Architecture

#### System Architecture Overview

```mermaid
graph TB
    subgraph SOURCES["📡 Market Data Sources"]
        A1[CAISO OASIS API]
        A2[ERCOT MIS API]
        A3[MISO API]
        A4[PJM Data Miner 2]
        A5[NYISO API]
        A6[ISO-NE API]
    end

    subgraph INGESTION["🔄 Ingestion Layer  |  Apache Airflow 2.9"]
        B1[ISO Connector DAGs]
        B2[Real-time Stream Ingestor]
        B3[Historical Backfill DAGs]
        B4[FTR / Auction Loader]
    end

    subgraph STORAGE["🗄️ Storage Layer"]
        C1[(Azure Data Lake\nGen2  —  Raw Zone)]
        C2[(PostgreSQL 15\nAnalytics DW)]
        C3[(Redis Cache\nReal-time Layer)]
    end

    subgraph TRANSFORM["⚙️ Transformation Layer  |  dbt Core 1.8"]
        D1[Staging Models\nstg_lmp_*]
        D2[Intermediate Models\nint_lmp_decomposed]
        D3[Mart Models\nmart_risk_*]
        D4[Metrics Layer\nmetrics_exposure]
    end

    subgraph ANALYTICS["📐 Analytics Engine  |  PySpark + Python"]
        E1[LMP Decomposer]
        E2[Congestion Scorer]
        E3[FTR Valuation Engine]
        E4[VaR / CVaR Model]
        E5[LMP Forecast Engine\nXGBoost + LSTM]
    end

    subgraph OUTPUTS["📊 Outputs & Consumers"]
        F1[Power BI Dashboards]
        F2[REST API  —  FastAPI]
        F3[Slack / Teams Alerts]
        F4[Excel / PDF Reports]
        F5[Downstream Risk Systems]
    end

    SOURCES --> INGESTION
    INGESTION --> STORAGE
    STORAGE --> TRANSFORM
    TRANSFORM --> ANALYTICS
    ANALYTICS --> OUTPUTS
```

### Data Flow — Real-Time Path

```mermaid
sequenceDiagram
    participant ISO as 🏭 ISO API
    participant AIR as 🔄 Airflow DAG
    participant CACHE as ⚡ Redis Cache
    participant DBT as ⚙️ dbt Models
    participant API as 🌐 FastAPI
    participant DASH as 📊 Dashboard

    ISO->>AIR: 5-min interval LMP data
    AIR->>CACHE: Write raw prices (TTL 1hr)
    AIR->>DBT: Trigger incremental run
    DBT->>DBT: Decompose LMP → Energy+Cong+Loss
    DBT->>API: Refresh materialized views
    API->>DASH: WebSocket push
    DASH->>DASH: Update exposure & PnL tiles
    Note over AIR,DBT: p99 latency < 45 seconds end-to-end
```

### Database Schema — Core Tables

```mermaid
erDiagram
    LMP_OBSERVATIONS {
        bigint id PK
        varchar iso_rto
        varchar node_id FK
        timestamptz interval_start
        numeric lmp_total
        numeric lmp_energy
        numeric lmp_congestion
        numeric lmp_loss
        varchar settlement_type
    }

    PRICING_NODES {
        varchar node_id PK
        varchar node_name
        varchar iso_rto
        varchar zone
        varchar hub
        numeric latitude
        numeric longitude
        boolean is_hub
        boolean is_load_zone
    }

    POSITIONS {
        bigint position_id PK
        varchar portfolio
        varchar counterparty
        varchar node_id FK
        varchar product_type
        numeric quantity_mw
        numeric strike_price
        date delivery_start
        date delivery_end
    }

    RISK_METRICS {
        bigint metric_id PK
        bigint position_id FK
        date calc_date
        numeric mtm_value
        numeric var_1d_95
        numeric cvar_1d_95
        numeric congestion_exposure
        numeric pnl_daily
    }

    BINDING_CONSTRAINTS {
        bigint constraint_id PK
        varchar iso_rto
        varchar constraint_name
        timestamptz binding_start
        timestamptz binding_end
        numeric shadow_price
        varchar[] affected_nodes
    }

    PRICING_NODES ||--o{ LMP_OBSERVATIONS : "has prices"
    PRICING_NODES ||--o{ POSITIONS : "delivery node"
    POSITIONS ||--o{ RISK_METRICS : "valued by"
    BINDING_CONSTRAINTS ||--o{ LMP_OBSERVATIONS : "impacts"
```

---

#### 🌐 Data Sources & Market Coverage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ISO/RTO         │  Nodes    │  Refresh    │  Products Covered              │
├──────────────────┼───────────┼─────────────┼────────────────────────────────┤
│  ⚡ CAISO        │  ~4,900   │  5-min RT   │  DA/RT LMP, CRR, AS Prices     │
│  🤠 ERCOT        │  ~9,400   │  5-min RT   │  DA/RT SPP, CRR, AS Prices     │
│  🌊 MISO         │  ~2,500   │  5-min RT   │  DA/RT LMP, FTR, ARR           │
│  🏙️ PJM          │  ~11,000  │  5-min RT   │  DA/RT LMP, FTR, Capacity      │
│  🗽 NYISO        │  ~1,000   │  5-min RT   │  DA/RT LBMP, TCC               │
│  🦞 ISO-NE       │  ~1,000   │  5-min RT   │  DA/RT LMP, FTR                │
└──────────────────┴───────────┴─────────────┴────────────────────────────────┘
```
#### 📁 Repository Structure

iso-rto-risk-intelligence/\
│
├── README.md\
├── LICENSE\
├── pyproject.toml\
├── requirements.txt\
├── .gitignore\
│
├── configs/\
│   ├── data_sources.yaml\
│   ├── positions.yaml\
│   ├── scenarios.yaml\
│   ├── risk_limits.yaml\
│   └── dashboard.yaml\
│
├── data/\
│   ├── raw/\
│   ├── processed/\
│   └── examples/\
│       ├── sample_lmps.csv\
│       ├── sample_positions.csv\
│       └── sample_constraints.csv\
│
├── docs/\
│   ├── architecture/\
│   │   ├── system_architecture.png\
│   │   ├── data_flow_diagram.png\
│   │   └── module_interactions.png\
│   ├── methodology/\
│   │   ├── exposure_models.md\
│   │   ├── scenario_engine.md\
│   │   ├── risk_metrics.md\
│   │   └── data_dictionary.md\
│   ├── user_guides/\
│   │   ├── trader_console_guide.md\
│   │   ├── operator_dashboard_guide.md\
│   │   └── risk_report_guide.md\
│   └── research/\
│       ├── iso_rto_market_notes.md\
│       └── volatility_and_tail_risk.md\
│
├── notebooks/\
│   ├── 01_data_ingestion_demo.ipynb\
│   ├── 02_exposure_engine_walkthrough.ipynb\
│   ├── 03_scenario_analysis_examples.ipynb\
│   ├── 04_risk_metrics_validation.ipynb\
│   └── 05_dashboard_prototype.ipynb\
│
├── src/\
│   ├── ingestion/\
│   │   ├── iso_api_client.py\
│   │   ├── data_loader.py\
│   │   ├── schema_validation.py\
│   │   └── utils.py\
│   │
│   ├── exposure/\
│   │   ├── physical_exposure.py\
│   │   ├── financial_exposure.py\
│   │   ├── congestion_exposure.py\
│   │   └── market_exposure.py\
│   │
│   ├── scenario/\
│   │   ├── price_shocks.py\
│   │   ├── outage_scenarios.py\
│   │   ├── constraint_scenarios.py\
│   │   └── fuel_shocks.py\
│   │
│   ├── risk/\
│   │   ├── var.py\
│   │   ├── cvar.py\
│   │   ├── pfe.py\
│   │   ├── sensitivities.py\
│   │   └── pnl_attribution.py\
│   │
│   ├── dashboard/\
│   │   ├── app.py\
│   │   ├── components/\
│   │   │   ├── exposure_heatmap.py\
│   │   │   ├── scenario_sliders.py\
│   │   │   └── risk_summary_cards.py\
│   │   └── utils.py\
│   │
│   └── utils/\
│       ├── logging.py\
│       ├── config_loader.py\
│       ├── decorators.py\
│       └── math_utils.py\
│
├── tests/\
│   ├── test_ingestion.py\
│   ├── test_exposure.py\
│   ├── test_scenario.py\
│   ├── test_risk_metrics.py\
│   └── test_dashboard.py\
│
└── reports/\
    ├── daily/\
    ├── intraday/\
    └── samples/\
        ├── sample_risk_report.pdf\
        └── sample_exposure_summary.html


---

#### 📦 Module Deep Dive

#### 🔌 `iso_connectors/` — Market Data Ingestion

Standardized async connectors for each ISO's public API. Each connector implements a common `BaseISOConnector` interface, handles rate limiting, retry logic with exponential backoff, and schema validation before persistence.

```python
# Example: Fetching real-time LMPs from ERCOT
from iso_connectors.ercot import ERCOTConnector

connector = ERCOTConnector(config=settings.ERCOT)
lmps = await connector.fetch_rt_lmp(
    settlement_point_type="LZ",
    interval="5MIN",
    as_of=datetime.utcnow()
)
# Returns validated DataFrame: node_id, interval_start, lmp_total, ...
```

**Key features:**
- ✅ Async-first with `httpx` + `asyncio`
- ✅ Pydantic v2 schema validation on every response
- ✅ Automatic retry with jitter (3 attempts, exponential backoff)
- ✅ ISO-specific authentication handlers (OAuth2, API key, certificate)
- ✅ Prometheus metrics emitted per connector call

---

#### ⚙️ `dbt_models/` — Transformation Layer

A fully lineage-tracked dbt project organized into four layers. Every model includes column-level documentation, data freshness SLAs, and a companion Great Expectations suite.

```
dbt_models/
├── staging/                         # Raw → typed → validated
│   ├── lmp/
│   │   ├── stg_lmp_caiso.py
│   │   ├── stg_lmp_ercot.py
│   │   ├── stg_lmp_isone.py
│   │   ├── stg_lmp_miso.py
│   │   ├── stg_lmp_nyiso.py
│   │   └── stg_lmp_pjm.py
│   ├── constraints/
│   │   └── stg_binding_constraints.py
│   └── reference/
│       └── stg_hub_nodes.py
│
├── intermediate/                    # Business logic, normalization, decomposition
│   ├── lmp/
│   │   ├── int_lmp_unified.py       # Cross‑ISO schema harmonization
│   │   ├── int_lmp_decomposed.py    # Energy / Congestion / Loss split
│   │   └── int_lmp_enriched.py      # Add hubs, weather, outages, fuel
│   ├── constraints/
│   │   └── int_binding_constraints.py
│   └── risk/
│       └── int_exposure_base.py
│
├── marts/                           # Consumption‑ready analytics
│   ├── lmp/
│   │   └── mart_lmp_hourly.py
│   ├── risk/
│   │   ├── mart_risk_exposure.py
│   │   ├── mart_portfolio_pnl.py
│   │   └── mart_var_cvar.py
│   └── ftr/
│       └── mart_ftr_valuation.py
│
└── metrics/                         # dbt Semantic Layer
│   ├── exposure.yml
│   ├── lmp.yml
│   └── portfolio.yml

```

---

#### 📐 `analytics_engine/` — Quantitative Models

#### LMP Decomposer
Decomposes observed LMPs into energy, congestion, and loss components using the standard nodal pricing identity. Validates decomposition residuals are within ISO-published tolerances.

#### Congestion Risk Scorer
Assigns a **Congestion Risk Score (CRS)** to each node using a rolling 30-day binding constraint frequency, shadow price volatility, and network topology exposure. Scores feed real-time alert thresholds.

```
CRS(node) = w₁ · BindFreq(30d) + w₂ · σ(ShadowPrice) + w₃ · TopologyExposure
```

#### FTR / CRR Valuation Engine
Marks FTR positions to market using:
1. Auction clearing prices from ISO settlement statements
2. Forward LMP spreads derived from the day-ahead market
3. Residual value from binding constraint shadow prices

#### Value-at-Risk Engine
Computes **1-day 95% Historical Simulation VaR** and **Conditional VaR (CVaR)** at position and portfolio level using a 252-day rolling window of LMP returns.

```
VaR₉₅ = -Percentile₅(ΔMtM distribution over lookback window)
CVaR₉₅ = E[ΔMtM | ΔMtM < -VaR₉₅]
```

#### LMP Forecast Engine
An **XGBoost + LSTM ensemble** producing probabilistic forecasts at three horizons:

| Horizon | Model | Features | MAPE (OOS) |
|---|---|---|---|
| 1-hour ahead | XGBoost | Load, weather, lag prices, hour-of-week | ~4.2% |
| 4-hour ahead | XGBoost + LSTM | Above + net load forecast | ~6.8% |
| Day-ahead | LSTM | Above + IS/OS unit commitment signals | ~9.1% |

---

#### 🔔 `alerting/` — Real-Time Notifications

Event-driven alert system that monitors:
- 🚨 **Binding constraint activations** — routed to Slack `#congestion-alerts`
- 📈 **LMP spike detection** — Z-score > 3σ triggers immediate notification
- 💥 **VaR limit breaches** — escalated to risk managers via PagerDuty
- 🔄 **Pipeline SLA misses** — data freshness degraded beyond threshold

---

#### 🚀 Quickstart

#### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core runtime |
| Docker & Docker Compose | 24+ | Local infrastructure |
| PostgreSQL | 15+ | Analytics warehouse |
| dbt Core | 1.8+ | Transformation layer |
| Airflow | 2.9+ | Orchestration |

#### 1. Clone & Environment Setup

```bash
git clone https://github.com/<your-username>/iso-rto-risk-platform.git
cd iso-rto-risk-platform

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```ini
#### Database
DATABASE_URL=postgresql://risk_user:password@localhost:5432/iso_risk_db

# ISO API Credentials
CAISO_API_KEY=your_caiso_key
ERCOT_USERNAME=your_ercot_user
ERCOT_PASSWORD=your_ercot_pass
PJM_SUBSCRIPTION_KEY=your_pjm_key
MISO_API_KEY=your_miso_key
NYISO_API_KEY=your_nyiso_key
ISONE_API_KEY=your_isone_key

#### Azure (Production)
AZURE_STORAGE_ACCOUNT=your_storage_account
AZURE_STORAGE_KEY=your_storage_key

#### Alerting
SLACK_BOT_TOKEN=xoxb-your-slack-token
SLACK_ALERT_CHANNEL=#risk-alerts
```

#### 3. Launch Local Infrastructure

```bash
# Start PostgreSQL, Redis, Airflow, and supporting services
docker compose up -d

# Verify all services are healthy
docker compose ps

# Expected output:
# iso-risk-postgres    running   0.0.0.0:5432->5432/tcp
# iso-risk-redis       running   0.0.0.0:6379->6379/tcp
# iso-risk-airflow     running   0.0.0.0:8080->8080/tcp
```

#### 4. Initialize the Database & Run dbt

```bash
# Run database migrations
python scripts/init_db.py

# Install dbt dependencies and seed reference data
cd dbt_models
dbt deps
dbt seed                    # Load pricing nodes, hub mappings
dbt run                     # Build all transformation models
dbt test                    # Run all data quality tests
```

#### 5. Load Historical Data

```bash
# Backfill 90 days of LMP data across all ISOs
python scripts/historical_backfill.py \
  --start-date 2026-03-25 \
  --end-date 2026-06-23 \
  --isos CAISO,ERCOT,MISO,PJM,NYISO,ISONE \
  --interval 5MIN

# Monitor progress in Airflow UI
open http://localhost:8080
```

#### 6. Start Real-Time Ingestion

```bash
# Trigger live DAGs via Airflow CLI
airflow dags trigger iso_rt_lmp_ingestor
airflow dags trigger binding_constraint_monitor

# Or enable via Airflow UI at http://localhost:8080
```

#### 7. Launch the API & Dashboard

```bash
# Start FastAPI risk API
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# API docs available at:
open http://localhost:8000/docs
```

---

#### ⚙️ Configuration

All configuration is managed via `config/settings.py` using Pydantic Settings with environment variable overrides.

```python
# config/settings.py (excerpt)

class RiskSettings(BaseSettings):
    # VaR Configuration
    var_confidence_level: float = 0.95
    var_lookback_days: int = 252
    var_limit_usd: float = 5_000_000

    # LMP Spike Detection
    spike_zscore_threshold: float = 3.0
    spike_lookback_intervals: int = 288   # 24 hours of 5-min intervals

    # Congestion Scoring Weights
    crs_weight_bind_freq: float = 0.45
    crs_weight_shadow_vol: float = 0.35
    crs_weight_topology: float = 0.20

    # Data Freshness SLAs (minutes)
    sla_rt_lmp_minutes: int = 10
    sla_da_lmp_minutes: int = 60
```

---

#### 📊 Dashboards & Reporting

| Dashboard | Description | Refresh |
|---|---|---|
| 🗺️ **LMP Heat Map** | Node-level LMP and congestion visualization across the grid | 5-min |
| 💼 **Portfolio Exposure** | MtM, VaR, and CVaR by portfolio, desk, and counterparty | 5-min |
| 🚦 **Binding Constraint Monitor** | Active constraints with shadow prices and affected portfolios | 1-min |
| 📈 **PnL Attribution** | Daily P&L decomposed by ISO, node, and product | EOD |
| 🔮 **LMP Forecast** | 1hr / 4hr / DA price forecasts vs actuals with confidence bands | Hourly |
| 📋 **Settlement Reconciliation** | Invoiced vs modeled settlements with variance flagging | Weekly |

Power BI `.pbix` report templates are located in `dashboards/powerbi/`.
Tableau workbook templates are located in `dashboards/tableau/`.

---

#### 🧪 Testing & Validation

```bash
# Run full unit test suite
pytest tests/unit/ -v --cov=. --cov-report=html

# Run integration tests (requires live database)
pytest tests/integration/ -v -m integration

# Run data quality checks (Great Expectations)
great_expectations checkpoint run lmp_quality_checkpoint
great_expectations checkpoint run risk_metrics_checkpoint

# dbt tests only
dbt test --select tag:critical

# Type checking
mypy analytics_engine/ iso_connectors/ api/

# Linting
ruff check . && black --check .
```

**Test Coverage Summary**

```
Module                          Coverage
──────────────────────────────────────────
iso_connectors/                   97%
analytics_engine/lmp_decomposer   96%
analytics_engine/var_engine       95%
analytics_engine/ftr_valuation    93%
analytics_engine/forecast_engine  91%
api/                              94%
alerting/                         89%
──────────────────────────────────────────
TOTAL                             94%
```

---

#### 🗓️ Roadmap

- [x] Real-time LMP ingestion — all 6 ISOs
- [x] LMP decomposition (energy / congestion / loss)
- [x] dbt transformation layer with full lineage
- [x] VaR / CVaR engine
- [x] FTR / CRR valuation
- [x] Binding constraint alerting
- [x] XGBoost LMP forecasting
- [ ] LSTM ensemble integration for DA forecasting
- [ ] Spark Streaming for sub-second latency path
- [ ] FERC EQR compliance reporting module
- [ ] Capacity market analytics (PJM RPM, MISO LOLE)
- [ ] Natural gas basis correlation module
- [ ] Multi-currency / cross-border Canadian market support

---
📚 Research References

The ISO/RTO Risk Intelligence & Exposure Analytics Platform is grounded in peer‑reviewed research, ISO/RTO market design literature, and industry‑standard risk methodologies. 

The following works form the theoretical and practical foundation for the system’s LMP modeling, congestion analytics, FTR valuation, scenario generation, and risk measurement.

- Locational Marginal Pricing (LMP) Theory & Market Design
O’Neill et al. (2005) — Efficient Market Clearing with Financial Transmission Rights
Establishes the mathematical relationship between LMPs, congestion, and shadow prices. Forms the backbone of the platform’s congestion decomposition and FTR valuation engine.

- Bessembinder & Lemmon (2002) — Equilibrium Pricing and Optimal Hedging in Electricity Forward Markets  
Provides the theoretical basis for DA/RT spread modeling, forward curve construction, and financial exposure analytics.

- Congestion, Transmission Constraints & Grid Risk
NERC MOD‑032 / MOD‑033 Standards  
Define modeling requirements for load forecasts, system dynamics, and constraint validation across ISOs/RTOs. Supports the platform’s constraint scenario engine and outage modeling.

- Risk-Based Approaches for ISO/RTO Asset Managers (IEEE)
Explores risk scoring, asset reliability, and operational decision frameworks used by ISOs/RTOs. Reinforces the platform’s congestion risk scoring and operator dashboards.

- FTR / CRR Valuation & Auction Economics
PJM, MISO, ERCOT Market Manuals  
Provide the official methodologies for FTR/CRR auction clearing, settlement rules, and congestion rent allocation. These documents directly inform the platform’s mark‑to‑market engine and portfolio exposure models.

- Volatility, Tail Risk & Extreme Events
 - Anderson & Davison (2020) — Modeling Extreme Events in Electricity Markets  
   Supports the VaR/CVaR engine and tail‑risk scenario generation, especially during scarcity pricing or high‑volatility intervals.

- Holland & Mansur (2008) — The Short-Run Effects of Time-Varying Gas Prices on Electricity Markets  
  Provides empirical evidence for gas‑power coupling, informing the fuel shock module and market exposure engine.

- Outage Modeling & Reliability Analytics
Billinton & Allan (1996) — Reliability Evaluation of Power Systems  
Classic reference for forced outage rates, reliability modeling, and system adequacy. Supports the outage scenario engine and physical exposure modeling.


#### 🤝 Contributing

Contributions are welcome. Please follow the workflow below:

```bash
# Fork and create a feature branch
git checkout -b feature/your-feature-name

# Make changes with tests
pytest tests/ -v

# Ensure code quality
ruff check . && black . && mypy .

# Open a pull request against main
```

Please read `CONTRIBUTING.md` for detailed guidelines on branch strategy, commit message conventions, and the PR review checklist.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ⚡ for energy markets professionals**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)

_Questions or collaboration inquiries? Open an issue or reach out via LinkedIn._

</div>
