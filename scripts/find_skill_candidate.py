import pandas as pd
import re
from collections import defaultdict


def basic_normalize(skill):
    """Apply safe formatting normalization."""
    skill = str(skill).strip().lower()
    skill = re.sub(r"\s+", " ", skill)
    return skill


def load_skills(path):
    df = pd.read_csv(path)

    # Vocabulary files contain one skill column.
    column = df.columns[0]

    return df[column].dropna().astype(str).tolist()


def find_formatting_duplicates(skills):
    groups = defaultdict(list)

    for skill in skills:
        normalized = basic_normalize(skill)
        groups[normalized].append(skill)

    # Keep only groups containing different raw representations.
    candidates = {}

    for normalized, raw_skills in groups.items():
        unique_raw = sorted(set(raw_skills))

        if len(unique_raw) > 1:
            candidates[normalized] = unique_raw

    return candidates


role_skills = load_skills("data/role_skill_vocabulary.csv")
job_skills = load_skills("data/job_skill_vocabulary.csv")

all_skills = role_skills + job_skills

candidates = find_formatting_duplicates(all_skills)

print(f"Total candidate groups: {len(candidates)}")
print()

for canonical, variants in sorted(candidates.items()):
    print(f"{canonical}")
    for variant in variants:
        print(f"    - {variant}")
    print()