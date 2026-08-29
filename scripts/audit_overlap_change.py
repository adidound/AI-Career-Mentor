import pandas as pd

from services.skill_normalizer import basic_normalize, normalize_skill


def load_skills(path):
    df = pd.read_csv(path)
    column = df.columns[0]

    return set(
        basic_normalize(skill)
        for skill in df[column].dropna().astype(str)
        if basic_normalize(skill)
    )


def load_canonical_skills(path):
    df = pd.read_csv(path)

    return set(
        df["canonical_skill"]
        .dropna()
        .astype(str)
    )


# ---------------------------------------------------------
# Original/basic-normalized vocabularies
# ---------------------------------------------------------

role_raw = load_skills("data/role_skill_vocabulary.csv")
job_raw = load_skills("data/job_skill_vocabulary.csv")

raw_common = role_raw & job_raw


# ---------------------------------------------------------
# Canonical vocabularies
# ---------------------------------------------------------

role_canonical = load_canonical_skills(
    "data/role_canonical_skill_vocabulary.csv"
)

job_canonical = load_canonical_skills(
    "data/job_canonical_skill_vocabulary.csv"
)

canonical_common = role_canonical & job_canonical


# ---------------------------------------------------------
# Compare
# ---------------------------------------------------------

lost = sorted(raw_common - canonical_common)
gained = sorted(canonical_common - raw_common)


print("=" * 60)
print("OVERLAP CHANGE AUDIT")
print("=" * 60)

print(f"Original common skills  : {len(raw_common)}")
print(f"Canonical common skills : {len(canonical_common)}")
print(f"Lost common skills      : {len(lost)}")
print(f"Gained common skills    : {len(gained)}")

print()
print("SKILLS LOST AFTER CANONICALIZATION")
print("-" * 60)

for skill in lost:
    print(skill)

print()
print("SKILLS GAINED AFTER CANONICALIZATION")
print("-" * 60)

for skill in gained:
    print(skill)