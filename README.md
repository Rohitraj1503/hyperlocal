# HyperLocal QCommerce — AI Engine

Five focused services that power the AI layer of the platform.

## Services

| File | What it does |
|---|---|
| `services/ocr_service.py` | Extracts text from product images (pytesseract) + parses to JSON |
| `services/semantic_search_service.py` | Ranks products by semantic similarity (all-MiniLM-L6-v2) |
| `services/proximity_service.py` | Sorts stores by Haversine distance (stdlib only) |
| `services/llm_service.py` | Calls OpenRouter (gpt-4o-mini) for open-ended tasks |
| `router.py` | FastAPI router wiring all services to REST endpoints |

---

## Quick start

```bash
# 1. Create & activate virtualenv
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (macOS/Linux) Install Tesseract OCR binary
#    macOS:  brew install tesseract
#    Ubuntu: sudo apt install tesseract-ocr

# 4. Add your OpenRouter key
echo "OPENROUTER_API_KEY=sk-or-..." > .env

# 5. Run the AI server
uvicorn router:app --reload --port 8001
```

API docs → http://localhost:8001/docs

---

## Endpoints

### `POST /ai/ocr/extract`
Upload a product image, get back raw OCR text and parsed inventory.
```json
// Response
{
  "raw_text": "Milk 20\nBread 10\nEggs 30",
  "inventory": [
    {"product_name": "Milk",  "quantity": 20},
    {"product_name": "Bread", "quantity": 10},
    {"product_name": "Eggs",  "quantity": 30}
  ]
}
```

### `POST /ai/search/semantic`
```json
// Request
{ "query": "cold drink", "products": ["Coca Cola", "Pepsi", "Amul Milk"] }

// Response
{ "query": "cold drink", "results": [{"product": "Coca Cola", "score": 0.72}, ...] }
```

### `POST /ai/stores/nearest`
```json
// Request
{
  "user_lat": 13.0827, "user_lon": 80.2707,
  "stores": [{"name": "FreshMart", "lat": 13.08, "lon": 80.27}]
}
// Response — stores sorted by distance_km
```

### `POST /ai/llm/ask`
```json
// Request
{ "prompt": "Suggest alternatives to Amul Butter" }
// Response
{ "response": "You could try Britannia Butter, Mother Dairy Butter, or Nutralite." }
```

---

## Mounting in your main FastAPI app

```python
# main.py
from fastapi import FastAPI
from ai_engine.router import app as ai_router

app = FastAPI()
app.mount("/ai", ai_router)
```

---

## Running each service standalone

Every service file is self-contained and executable:

```bash
python services/ocr_service.py path/to/image.jpg
python services/semantic_search_service.py
python services/proximity_service.py
python services/llm_service.py
```
