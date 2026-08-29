import pandas as pd

from services.skill_normalizer import normalize_skill, SKILL_ALIASES


DATASETS = [
    "data/role_skill_vocabulary.csv",
    "data/job_skill_vocabulary.csv",
]


def load_skills(path):
    df = pd.read_csv(path)
    column = df.columns[0]

    return df[column].dropna().astype(str).tolist()


all_skills = []

for path in DATASETS:
    all_skills.extend(load_skills(path))


print("=" * 60)
print("CANONICAL MAP AUDIT")
print("=" * 60)

for raw_skill, canonical_skill in sorted(SKILL_ALIASES.items()):

    occurrences = [
        skill
        for skill in all_skills
        if skill.strip().lower() == raw_skill
    ]

    print(f"\n{raw_skill}")
    print(f"  → {canonical_skill}")
    print(f"  Dataset occurrences: {len(occurrences)}")