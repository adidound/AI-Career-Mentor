import pandas as pd

from services.skill_normalizer import normalize_skill


INPUT_PATH = "data/it_roles_clean.csv"
OUTPUT_PATH = "data/role_skill_prevalence.csv"


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

    # Normalize and canonicalize skills for this source record.
    skills = set()

    for raw_skill in raw_skills:
        skill = normalize_skill(raw_skill)

        if skill:
            skills.add(skill)

    for skill in skills:
        records.append({
            "normalized_title": role,
            "canonical_skill": skill,
        })


role_skill = pd.DataFrame(records)


# Remove duplicate skill occurrences within the same source record.
role_skill = role_skill.drop_duplicates(
    subset=["normalized_title", "canonical_skill"]
)


# Number of source records available for each role.
role_record_counts = (
    df.groupby("normalized_title")
    .size()
    .rename("role_record_count")
)


# Number of source records in which each skill appears.
skill_record_counts = (
    role_skill.groupby(
        ["normalized_title", "canonical_skill"]
    )
    .size()
    .rename("skill_record_count")
)


result = (
    skill_record_counts
    .reset_index()
)


result["role_record_count"] = (
    result["normalized_title"]
    .map(role_record_counts)
)


result["prevalence"] = (
    result["skill_record_count"]
    / result["role_record_count"]
)


result = result.sort_values(
    ["normalized_title", "prevalence", "canonical_skill"],
    ascending=[True, False, True]
)


result = result.reset_index(drop=True)


result.to_csv(
    OUTPUT_PATH,
    index=False
)


print("=" * 60)
print("ROLE SKILL PREVALENCE")
print("=" * 60)

print(f"Source records       : {len(df)}")
print(f"Normalized roles     : {df['normalized_title'].nunique()}")
print(f"Role-skill pairs     : {len(result)}")
print(f"Unique skills        : {result['canonical_skill'].nunique()}")

print()
print(f"Saved to             : {OUTPUT_PATH}")