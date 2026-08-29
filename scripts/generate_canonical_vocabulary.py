import pandas as pd

from services.skill_normalizer import normalize_skill


DATASETS = {
    "role": "data/role_skill_vocabulary.csv",
    "job": "data/job_skill_vocabulary.csv",
}


for name, input_path in DATASETS.items():

    df = pd.read_csv(input_path)
    column = df.columns[0]

    canonical_skills = sorted(
        {
            normalize_skill(skill)
            for skill in df[column].dropna().astype(str)
            if normalize_skill(skill)
        }
    )

    output_path = f"data/{name}_canonical_skill_vocabulary.csv"

    pd.DataFrame(
        {"canonical_skill": canonical_skills}
    ).to_csv(
        output_path,
        index=False
    )

    print("=" * 60)
    print(name.upper())
    print("=" * 60)
    print(f"Original skills : {len(df)}")
    print(f"Canonical skills: {len(canonical_skills)}")
    print(f"Saved to        : {output_path}")
    print()