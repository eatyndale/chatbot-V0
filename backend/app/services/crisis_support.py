from typing import Tuple
import re

CRISIS_KEYWORDS = [
    "I want to hurt myself",
    "end my life",
    "suicidal",
    "I can't go on",
    "better off dead",
    "kill myself",
    "take my own life",
    "don't want to live",
    "self-harm",
    "hurt myself on purpose"
]

# Lowercase and strip for matching
CRISIS_KEYWORDS = [k.lower() for k in CRISIS_KEYWORDS]


def detect_crisis_signals(text: str) -> Tuple[bool, str | None]:
    """
    Returns (crisis_detected, matched_phrase) if a crisis phrase is found in the text.
    """
    text_lc = text.lower()
    for phrase in CRISIS_KEYWORDS:
        # Use word boundaries for single words, substring for phrases
        if phrase in text_lc:
            return True, phrase
    return False, None
