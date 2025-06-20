from typing import List, Dict, Any

def calculate_assessment(responses: List[int]) -> Dict[str, Any]:
    """
    Calculates the total score, severity, and provides next steps based on PHQ-9.
    """
    total_score = sum(responses)

    if 0 <= total_score <= 4:
        severity = "Minimal depression"
        next_steps = "Your score suggests minimal to no depressive symptoms. Monitor your mood and continue practicing self-care."
    elif 5 <= total_score <= 9:
        severity = "Mild depression"
        next_steps = "Your score suggests mild depressive symptoms. Consider discussing your feelings with a trusted friend, family member, or a professional."
    elif 10 <= total_score <= 14:
        severity = "Moderate depression"
        next_steps = "Your score indicates moderate depressive symptoms. It would be beneficial to talk with a counselor or therapist for guidance and support."
    elif 15 <= total_score <= 19:
        severity = "Moderately severe depression"
        next_steps = "Your score suggests moderately severe depressive symptoms. It is strongly recommended to seek help from a mental health professional."
    else: # 20 <= total_score <= 27
        severity = "Severe depression"
        next_steps = "Your score indicates severe depressive symptoms. Please seek professional help immediately. A therapist or psychiatrist can provide the support you need."

    return {
        "total_score": total_score,
        "severity": severity,
        "next_steps": next_steps,
    }
