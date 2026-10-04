import pandas as pd

from services.skill_normalizer import normalize_skill
from services.skill_classifier import classify_skill


INPUT_PATH = "data/it_roles_clean.csv"
OUTPUT_PATH = "data/role_skill_profiles.csv"


df = pd.read_csv(
    INPUT_PATH,
    encoding="cp1252"
)

records = []

for _, row in df.iterrows():

    role = str(row["normalized_title"]).strip()

    if not role:
        continue

    raw_skills = str(row["Skills"]).split(",")

    canonical_skills = set()

    for raw_skill in raw_skills:

        skill = normalize_skill(raw_skill)

        if skill:
            canonical_skills.add(skill)

    for skill in canonical_skills:

        records.append({
            "normalized_title": role,
            "canonical_skill": skill,
            "category": classify_skill(skill),
        })


result = pd.DataFrame(records)

result = (
    result
    .drop_duplicates(
        subset=["normalized_title", "canonical_skill"]
    )
    .sort_values(
        ["normalized_title", "canonical_skill"]
    )
    .reset_index(drop=True)
)

result.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("ROLE SKILL PROFILES")
print("=" * 60)

print(f"Total role-skill relationships: {len(result)}")
print(f"Unique roles: {result['normalized_title'].nunique()}")
print(f"Unique canonical skills: {result['canonical_skill'].nunique()}")

print()
print(f"Saved to: {OUTPUT_PATH}")