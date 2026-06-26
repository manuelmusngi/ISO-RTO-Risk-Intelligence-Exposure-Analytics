"""
End-to-end ISO/RTO risk pipeline

Flow:
1. Load configs
2. Ingest & validate data
3. Build exposures
4. Run scenarios
5. Compute risk metrics
6. Write simple reports
"""

from pathlib import Path
import pandas as pd

from src.utils.logging import get_logger
from src.utils.config_loader import (
    load_data_sources,
    load_positions,
    load_scenarios,
    load_risk_limits,
)

from src.ingestion.data_loader import load_sample_lmps
from src.ingestion.schema_validation import validate_lmp_schema

from src.exposure.physical_exposure import compute_physical_exposure
from src.exposure.financial_exposure import compute_ftr_mtm
from src.exposure.congestion_exposure import compute_congestion_exposure
from src.exposure.market_exposure import compute_market_exposure

from src.scenario.price_shocks import apply_price_shock
from src.scenario.outage_scenarios import build_outage_scenario
from src.scenario.constraint_scenarios import build_constraint_scenario
from src.scenario.fuel_shocks import build_fuel_shock

from src.risk.var import compute_var
from src.risk.cvar import compute_cvar
from src.risk.pfe import compute_pfe
from src.risk.sensitivities import compute_sensitivities
from src.risk.pnl_attribution import attribute_pnl


logger = get_logger("pipeline")


def ensure_report_dirs():
    base = Path("reports")
    (base / "daily").mkdir(parents=True, exist_ok=True)
    (base / "intraday").mkdir(parents=True, exist_ok=True)
    (base / "samples").mkdir(parents=True, exist_ok=True)
    return base


def ingest_stage() -> pd.DataFrame:
    logger.info("=== STAGE 1: Ingestion ===")
    lmp_df = load_sample_lmps()
    lmp_df = validate_lmp_schema(lmp_df)
    logger.info(f"LMP rows: {len(lmp_df)}")
    return lmp_df


def exposure_stage(lmp_df: pd.DataFrame):
    logger.info("=== STAGE 2: Exposure ===")
    physical = compute_physical_exposure(lmp_df)
    financial = compute_ftr_mtm(lmp_df[lmp_df["market"] == "DA"])
    congestion = compute_congestion_exposure(pd.DataFrame())  # placeholder
    market = compute_market_exposure(lmp_df, pd.DataFrame())  # placeholder

    return {
        "physical": physical,
        "financial": financial,
        "congestion": congestion,
        "market": market,
    }


def scenario_stage(lmp_df: pd.DataFrame):
    logger.info("=== STAGE 3: Scenarios ===")
    scenarios_cfg = load_scenarios()

    # price shock example
    shocked_lmp = apply_price_shock(lmp_df, "moderate_up")

    # outage example
    outage = build_outage_scenario("single_cc_outage")

    # constraint example
    constraint = build_constraint_scenario("key_interface_binding")

    # fuel shock example
    fuel = build_fuel_shock("gas_plus_2")

    return {
        "shocked_lmp": shocked_lmp,
        "outage": outage,
        "constraint": constraint,
        "fuel": fuel,
        "cfg": scenarios_cfg,
    }


def risk_stage(exposures: dict, scenarios: dict):
    logger.info("=== STAGE 4: Risk Metrics ===")

    # stub P&L paths: in real system, derive from exposures + scenarios
    pnl_paths = [0.0, -10000.0, 5000.0, -25000.0, 15000.0]
    exposure_paths = [abs(x) for x in pnl_paths]

    var_95 = compute_var(pnl_paths, alpha=0.95)
    cvar_95 = compute_cvar(pnl_paths, alpha=0.95)
    pfe_95 = compute_pfe(exposure_paths, alpha=0.95)

    sens = compute_sensitivities()
    attribution = attribute_pnl()

    return {
        "var_95": var_95,
        "cvar_95": cvar_95,
        "pfe_95": pfe_95,
        "sensitivities": sens,
        "attribution": attribution,
    }


def report_stage(report_dir: Path, exposures: dict, scenarios: dict, risk: dict):
    logger.info("=== STAGE 5: Reporting ===")
    out = report_dir / "samples" / "sample_exposure_summary.txt"

    lines = []
    lines.append("ISO/RTO Risk Intelligence — Sample Exposure & Risk Summary\n")
    lines.append("\n[Risk Metrics]\n")
    lines.append(f"VaR 95%: {risk['var_95']:.2f}\n")
    lines.append(f"CVaR 95%: {risk['cvar_95']:.2f}\n")
    lines.append(f"PFE 95%: {risk['pfe_95']:.2f}\n")

    lines.append("\n[Sensitivities]\n")
    lines.append(str(risk["sensitivities"]) + "\n")

    lines.append("\n[P&L Attribution]\n")
    lines.append(str(risk["attribution"]) + "\n")

    out.write_text("".join(lines))
    logger.info(f"Wrote sample report to {out}")


def main():
    logger.info("Starting end-to-end ISO/RTO risk pipeline")

    report_dir = ensure_report_dirs()

    # 1. Ingest
    lmp_df = ingest_stage()

    # 2. Exposures
    exposures = exposure_stage(lmp_df)

    # 3. Scenarios
    scenarios = scenario_stage(lmp_df)

    # 4. Risk
    risk = risk_stage(exposures, scenarios)

    # 5. Reports
    report_stage(report_dir, exposures, scenarios, risk)

    logger.info("Pipeline completed")


if __name__ == "__main__":
    main()
