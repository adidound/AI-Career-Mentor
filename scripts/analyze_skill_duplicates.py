import pandas as pd
import re

ROLE_FILE = "data/role_skill_vocabulary.csv"
JOB_FILE = "data/job_skill_vocabulary.csv"


def basic_normalize(skill):
    skill = str(skill).strip().lower()
    skill = re.sub(r"\s+", " ", skill)
    return skill


def analyze(file_path, name):

    df = pd.read_csv(file_path)

    df["normalized"] = df["skill"].apply(basic_normalize)

    raw_count = len(df)
    normalized_count = df["normalized"].nunique()

    print(f"\n{name}")
    print("-" * 40)
    print("Raw skills:", raw_count)
    print("After basic normalization:", normalized_count)
    print("Potential duplicates:", raw_count - normalized_count)

    groups = (
        df[df.duplicated("normalized", keep=False)]
        .groupby("normalized")["skill"]
        .apply(list)
    )

    print("\nDuplicate groups:")

    for normalized, skills in groups.head(100).items():
        unique_skills = sorted(set(skills))

        if len(unique_skills) > 1:
            print(f"\n{normalized}")

            for skill in unique_skills:
                print(f"  - {skill}")


# Analyze both datasets
analyze(ROLE_FILE, "Dataset A")
analyze(JOB_FILE, "Dataset B")