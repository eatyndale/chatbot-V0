from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pathlib import Path
import json
from app.services.crisis_support import detect_crisis_signals

router = APIRouter(
    prefix="/crisis",
    tags=["Crisis Support"]
)

DATA_PATH = Path(__file__).parent.parent / "data" / "crisis_hotlines.json"

# Helper to load hotlines

def load_hotlines():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["hotlines"]

@router.get("/resources", summary="Get global and regional crisis hotlines", response_model=None)
def get_crisis_resources():
    hotlines = load_hotlines()
    return {"hotlines": hotlines, "message": "If you or someone you know is in crisis, please reach out to a professional or use one of these hotlines immediately."}

@router.get("/sos", summary="Quick SOS access to crisis hotlines", response_model=None)
def get_sos():
    hotlines = load_hotlines()
    return {
        "hotlines": hotlines,
        "message": "Immediate help is available. Please contact a hotline below or seek local emergency services if you are in danger.",
        "action": "You are not alone. Reach out now."
    }

@router.post("/check", summary="Check a message for crisis signals", response_model=None)
def check_crisis_message(
    message: str = Body(..., embed=True, example="I feel like I can't go on")
):
    detected, phrase = detect_crisis_signals(message)
    hotlines = load_hotlines() if detected else []
    if detected:
        return {
            "crisis_detected": True,
            "message": "Crisis signals detected. Please seek immediate help. You can contact a hotline below or talk to a trusted person.",
            "matched_phrase": phrase,
            "resources": hotlines,
            "safety_message": "If you are in immediate danger, call emergency services or a crisis hotline now.",
            "resources_link": "/api/crisis/resources"
        }
    else:
        return {
            "crisis_detected": False,
            "message": "No urgent crisis signals detected. If you still need help, see available resources.",
            "resources_link": "/api/crisis/resources"
        }
