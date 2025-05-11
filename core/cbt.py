import re

CBT_DISTORTIONS = {
    "all-or-nothing": {
        "name": "All-or-Nothing Thinking",
        "description": "Seeing things in black-or-white terms, without middle ground.",
        "keywords": [r"\balways\b", r"\bnever\b", r"\bcompletely\b", r"\btotally\b", r"\bperfect\b"],
        "reframe": "Try to see the gray areas and exceptions instead of absolutes."
    },
    "catastrophizing": {
        "name": "Catastrophizing",
        "description": "Expecting the worst possible outcome in every situation.",
        "keywords": [r"\bdisaster\b", r"\bruined\b", r"\bworst\b", r"\bterrible\b", r"\bawful\b"],
        "reframe": "Consider more likely and less extreme outcomes."
    },
    "overgeneralization": {
        "name": "Overgeneralization",
        "description": "Making broad conclusions based on a single event.",
        "keywords": [r"\balways\b", r"\bnever\b", r"\bevery\b", r"\bnobody\b", r"\beveryone\b"],
        "reframe": "Focus on specific instances rather than generalizing."
    },
    "mental_filter": {
        "name": "Mental Filter",
        "description": "Focusing only on the negative details and ignoring positives.",
        "keywords": [r"\bonly\b", r"\bjust\b", r"\bnothing\b"],
        "reframe": "Try to notice positive aspects as well."
    },
    "disqualifying_positive": {
        "name": "Disqualifying the Positive",
        "description": "Rejecting positive experiences by insisting they don’t count.",
        "keywords": [r"\bdoesn't matter\b", r"\bnot good enough\b"],
        "reframe": "Accept positive experiences and acknowledge your successes."
    },
    "jumping_to_conclusions": {
        "name": "Jumping to Conclusions",
        "description": "Making negative interpretations without evidence.",
        "keywords": [r"\bmust\b", r"\bshould\b", r"\bcan't\b", r"\bwon't\b"],
        "reframe": "Look for evidence before concluding."
    },
    "emotional_reasoning": {
        "name": "Emotional Reasoning",
        "description": "Assuming feelings reflect reality.",
        "keywords": [r"\bfeel\b", r"\bfeelings\b", r"\bseems\b"],
        "reframe": "Remember that feelings are not facts."
    },
    "should_statements": {
        "name": "Should Statements",
        "description": "Having rigid rules about how you or others should behave.",
        "keywords": [r"\bshould\b", r"\bought to\b", r"\bmust\b"],
        "reframe": "Be flexible and realistic with expectations."
    },
    "labeling": {
        "name": "Labeling",
        "description": "Assigning global negative labels to yourself or others.",
        "keywords": [r"\bfailure\b", r"\bstupid\b", r"\bidiot\b", r"\bloser\b"],
        "reframe": "Focus on specific behaviors rather than labels."
    },
    "personalization": {
        "name": "Personalization",
        "description": "Blaming yourself for things outside your control.",
        "keywords": [r"\bmy fault\b", r"\bI caused\b", r"\bI am to blame\b"],
        "reframe": "Recognize what you can and cannot control."
    }
}

def analyze_cbt_thought(text):
    """
    Analyze the input thought text for cognitive distortions.

    Args:
        text (str): The user's free-text thought.

    Returns:
        dict: {
            'distortions': [
                {
                    'name': str,
                    'description': str,
                    'reframe': str
                },
                ...
            ]
        }
    """
    detected = []

    # Lowercase text for case-insensitive matching
    text_lower = text.lower()

    for key, distortion in CBT_DISTORTIONS.items():
        # Check if any keyword matches the text (using regex word boundaries)
        for pattern in distortion['keywords']:
            if re.search(pattern, text_lower):
                detected.append({
                    "name": distortion['name'],
                    "description": distortion['description'],
                    "reframe": distortion['reframe']
                })
                break  # Avoid duplicate detection of same distortion

    return {"distortions": detected}

