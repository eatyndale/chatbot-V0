from typing import List, Dict

tapping_points = [
    "eyebrow", "side of eye", "under eye", "under nose", "chin", "collarbone", "under arm", "top of head"
]

def generate_setup_statements(problem: str, emotion: str, body_location: str, still: bool = False) -> List[str]:
    base = f"Even though I{' STILL' if still else ''} feel {emotion} in my {body_location} because {problem}, I deeply and completely accept myself."
    alt1 = f"Even though this{' STILL' if still else ''} {emotion} in my {body_location} is overwhelming, I choose to accept myself."
    alt2 = f"Even though I{' STILL' if still else ''} notice this {emotion} in my {body_location} about {problem}, I accept who I am."
    return [base, alt1, alt2]

def generate_reminder_statements(problem: str, emotion: str, body_location: str, still: bool = False) -> Dict[str, str]:
    base_phrase = f"{'STILL ' if still else ''}{emotion} in my {body_location}"
    return {
        point: f"Even though I{' STILL' if still else ''} feel {emotion} in my {body_location} about {problem}" if point == "eyebrow" else base_phrase
        for point in tapping_points
    }

def generate_tapping_session(problem: str, emotion: str, body_location: str, intensity: int, still: bool = False):
    setup_statements = generate_setup_statements(problem, emotion, body_location, still=still)
    tapping_reminders = generate_reminder_statements(problem, emotion, body_location, still=still)
    return setup_statements, tapping_reminders
