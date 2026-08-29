import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CANONICAL_MAP_PATH = BASE_DIR / "data" / "canonical_skill_map.csv"


def basic_normalize(skill):
    """
    Perform safe formatting normalization.
    """

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    # Collapse multiple whitespace characters.
    skill = re.sub(r"\s+", " ", skill)

    return skill


def load_canonical_map():
    """
    Load raw-skill -> canonical-skill mappings from CSV.
    """

    aliases = {}

    if not CANONICAL_MAP_PATH.exists():
        return aliases

    with open(
        CANONICAL_MAP_PATH,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            raw_skill = basic_normalize(row["raw_skill"])
            canonical_skill = basic_normalize(row["canonical_skill"])

            if raw_skill and canonical_skill:
                aliases[raw_skill] = canonical_skill

    return aliases


SKILL_ALIASES = load_canonical_map()


def normalize_skill(skill):
    """
    Convert a raw skill into its canonical representation.

    Processing:

        Raw skill
             ↓
        Basic normalization
             ↓
        Canonical lookup
             ↓
        Canonical skill
    """

    skill = basic_normalize(skill)

    if not skill:
        return ""

    return SKILL_ALIASES.get(skill, skill)


def normalize_skills(skills):
    """
    Normalize a collection of skills and remove duplicates.
    """

    normalized = {
        normalize_skill(skill)
        for skill in skills
        if normalize_skill(skill)
    }

    return sorted(normalized)