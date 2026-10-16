"""
FastAPI Server for Modern Power Flow Studio Web Application.
Provides RESTful APIs for real-time validation, Y-bus synthesis, Newton-Raphson solving,
and benchmark case delivery. Serves the responsive Single Page Application.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .solver_service import (
    validate_grid_data,
    compute_ybus_matrix,
    solve_power_flow,
    PRESETS
)

# App Setup
app = FastAPI(
    title="Modern Power Flow Studio API",
    description="REST API for Newton-Raphson AC Power Flow and Interactive Grid Telemetry",
    version="2.0.0"
)

# Enable CORS for local cross-origin development if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


# Pydantic Request Models
class BusItem(BaseModel):
    bus: int
    type: str
    pg_pu: float = 0.0
    qg_pu: float = 0.0
    pd_pu: float = 0.0
    qd_pu: float = 0.0
    vm_pu: float = 1.0
    va_deg: float = 0.0
    q_min_pu: Optional[float] = None
    q_max_pu: Optional[float] = None
    q_min_Mvar: Optional[float] = None
    q_max_Mvar: Optional[float] = None

class LineItem(BaseModel):
    from_bus: int
    to_bus: int
    r_pu: float
    x_pu: float

class GridPayload(BaseModel):
    buses: List[Dict[str, Any]]
    lines: List[Dict[str, Any]]
    base_mva: float = 100.0
    tolerance: float = 1e-6
    max_iterations: int = 30


# API Endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "Modern Power Flow Studio API"}


@app.get("/api/presets")
async def list_presets():
    """Return available benchmark scenarios (3-bus, 5-bus)."""
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "bus_count": len(p["buses"]),
            "line_count": len(p["lines"])
        }
        for p in PRESETS.values()
    ]


@app.get("/api/presets/{preset_id}")
async def get_preset(preset_id: str):
    """Retrieve full bus and line records for a benchmark scenario."""
    if preset_id not in PRESETS:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy kịch bản mẫu '{preset_id}'")
    return PRESETS[preset_id]


@app.post("/api/validate")
async def api_validate(payload: GridPayload):
    """Real-time validation of user inputs."""
    result = validate_grid_data(payload.buses, payload.lines)
    return result


@app.post("/api/build-ybus")
async def api_build_ybus(payload: GridPayload):
    """Synthesize the Y-bus admittance matrix from line and bus entries."""
    val = validate_grid_data(payload.buses, payload.lines)
    if not val["valid"]:
        raise HTTPException(status_code=400, detail="; ".join(val["errors"]))

    buses_df = pd.DataFrame(payload.buses)
    lines_df = pd.DataFrame(payload.lines)
    
    # Ensure proper column types
    buses_df['bus'] = buses_df['bus'].astype(int)
    lines_df['from_bus'] = lines_df['from_bus'].astype(int)
    lines_df['to_bus'] = lines_df['to_bus'].astype(int)
    for col in ['r_pu', 'x_pu']:
        lines_df[col] = lines_df[col].astype(float)

    ybus_result = compute_ybus_matrix(buses_df, lines_df)
    return ybus_result


@app.post("/api/solve")
async def api_solve(payload: GridPayload):
    """Execute Newton-Raphson AC power flow with detailed telemetry."""
    buses_df = pd.DataFrame(payload.buses)
    lines_df = pd.DataFrame(payload.lines)

    # Cast fields
    try:
        buses_df['bus'] = buses_df['bus'].astype(int)
        buses_df['type'] = buses_df['type'].astype(str)
        for col in ['pg_pu', 'qg_pu', 'pd_pu', 'qd_pu', 'vm_pu', 'va_deg']:
            if col in buses_df.columns:
                buses_df[col] = buses_df[col].astype(float)

        lines_df['from_bus'] = lines_df['from_bus'].astype(int)
        lines_df['to_bus'] = lines_df['to_bus'].astype(int)
        lines_df['r_pu'] = lines_df['r_pu'].astype(float)
        lines_df['x_pu'] = lines_df['x_pu'].astype(float)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi chuyển đổi kiểu dữ liệu: {str(e)}")

    result = solve_power_flow(
        buses_df=buses_df,
        lines_df=lines_df,
        base_mva=payload.base_mva,
        tolerance=payload.tolerance,
        max_iterations=payload.max_iterations
    )
    return result


# Mount Static Frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
