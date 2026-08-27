import re


SKILL_ALIASES = {
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "ai/ml": "artificial intelligence",
    "aws cloud": "aws",
    "amazon web services": "aws",
    "js": "javascript",
    "react.js": "react",
    "node.js": "node",
}


def normalize_skill(skill):
    """
    Convert a raw skill name into a canonical skill name.
    """

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    # Normalize whitespace
    skill = re.sub(r"\s+", " ", skill)

    # Apply known aliases
    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    return skill


def normalize_skills(skills):
    """
    Normalize a list of skills and remove duplicates.
    """

    normalized = {
        normalize_skill(skill)
        for skill in skills
        if normalize_skill(skill)
    }

    return sorted(normalized)