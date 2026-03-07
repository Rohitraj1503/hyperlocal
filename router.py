"""
AI Engine — FastAPI Router
--------------------------
Exposes all AI services as REST endpoints.
Mount this in your main FastAPI app:

    from ai_engine.router import router as ai_router
    app.include_router(ai_router, prefix="/ai")

Or run this file directly for a self-contained demo server:
    uvicorn router:app --reload --port 8001
"""

import tempfile
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List

from services.ocr_service import extract_text, parse_inventory
from services.semantic_search_service import semantic_search
from services.proximity_service import find_nearest_store, Store
from services.llm_service import ask_llm

# ── Pydantic models ───────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    products: List[str]
    top_k: int = 5

class ProximityRequest(BaseModel):
    user_lat: float
    user_lon: float
    stores: List[Store]

class LLMRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are a helpful assistant for a quick-commerce grocery platform."


# ── Router / App ──────────────────────────────────────────────────────────────

app = FastAPI(title="HyperLocal AI Engine", version="1.0.0")


@app.post("/ocr/extract")
async def ocr_extract(file: UploadFile = File(...)):
    """Upload a product image → get raw OCR text + parsed inventory."""
    # Save upload to a temp file (pytesseract needs a file path)
    suffix = os.path.splitext(file.filename or "img.png")[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        raw_text = extract_text(tmp_path)
        inventory = parse_inventory(raw_text)
    finally:
        os.unlink(tmp_path)  # clean up

    return {"raw_text": raw_text, "inventory": inventory}


@app.post("/search/semantic")
def semantic_search_endpoint(body: SearchRequest):
    """Return products ranked by semantic similarity to the query."""
    results = semantic_search(body.query, body.products, top_k=body.top_k)
    return {"query": body.query, "results": results}


@app.post("/stores/nearest")
def nearest_stores(body: ProximityRequest):
    """Return stores sorted by distance from the user's location."""
    ranked = find_nearest_store((body.user_lat, body.user_lon), body.stores)
    return {"user_location": {"lat": body.user_lat, "lon": body.user_lon}, "stores": ranked}


@app.post("/llm/ask")
def llm_ask(body: LLMRequest):
    """Forward a prompt to the LLM and return the response."""
    try:
        response = ask_llm(body.prompt, system_prompt=body.system_prompt)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"response": response}


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-engine"}
