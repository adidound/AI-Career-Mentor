import pandas as pd

from services.skill_normalizer import normalize_skill


def inspect_vocabulary(path):
    df = pd.read_csv(path)
    column = df.columns[0]

    groups = {}

    for skill in df[column].dropna().astype(str):
        canonical = normalize_skill(skill)

        if canonical:
            groups.setdefault(canonical, []).append(skill)

    return groups


for name, path in [
    ("Dataset A", "data/role_skill_vocabulary.csv"),
    ("Dataset B", "data/job_skill_vocabulary.csv"),
]:

    groups = inspect_vocabulary(path)

    duplicate_groups = {
        canonical: sorted(set(raw_skills))
        for canonical, raw_skills in groups.items()
        if len(set(raw_skills)) > 1
    }

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Canonical skills: {len(groups)}")
    print(f"Collapsed groups: {len(duplicate_groups)}")
    print()

    for canonical, raw_skills in sorted(duplicate_groups.items()):
        print(f"{canonical}")
        for raw in raw_skills:
            print(f"    - {raw}")
        print()