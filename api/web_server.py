#!/usr/bin/env python3
"""
UI/UX Pro Max FastAPI Service
Wraps the BM25 search engine for HTTP access by hive coordinators.
Port: 9056
"""

import sys
from pathlib import Path

# Add the scripts directory to sys.path so we can import core/design_system
SCRIPTS_DIR = Path(__file__).parent.parent / "src" / "ui-ux-pro-max" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from core import search, search_stack, AVAILABLE_STACKS, CSV_CONFIG
from design_system import DesignSystemGenerator

app = FastAPI(title="UI/UX Pro Max API", version="1.0.0")
generator = DesignSystemGenerator()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ui-ux-pro-max",
        "version": "1.0.0",
        "domains": list(CSV_CONFIG.keys()),
        "stacks": AVAILABLE_STACKS
    }


@app.get("/api/design-system")
async def design_system(
    query: str = Query(..., description="Search query (e.g. 'fintech banking dashboard')"),
    project: str = Query(None, description="Project name")
):
    """Generate a complete design system recommendation."""
    try:
        result = generator.generate(query, project)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/search")
async def search_domain(
    query: str = Query(..., description="Search query"),
    domain: str = Query(None, description="Search domain (style, color, typography, ux, chart, landing, product, icons, react, web)"),
    n: int = Query(3, description="Max results", ge=1, le=10)
):
    """Search a specific domain."""
    try:
        result = search(query, domain, n)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/search/stack")
async def search_stack_endpoint(
    query: str = Query(..., description="Search query"),
    stack: str = Query("html-tailwind", description="Technology stack"),
    n: int = Query(3, description="Max results", ge=1, le=10)
):
    """Search stack-specific guidelines."""
    try:
        result = search_stack(query, stack, n)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9056)
