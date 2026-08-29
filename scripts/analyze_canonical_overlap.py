import pandas as pd


ROLE_PATH = "data/role_canonical_skill_vocabulary.csv"
JOB_PATH = "data/job_canonical_skill_vocabulary.csv"


role_df = pd.read_csv(ROLE_PATH)
job_df = pd.read_csv(JOB_PATH)


role_skills = set(role_df["canonical_skill"].dropna())
job_skills = set(job_df["canonical_skill"].dropna())


common_skills = sorted(role_skills & job_skills)


print("=" * 60)
print("CANONICAL SKILL OVERLAP")
print("=" * 60)

print(f"Dataset A canonical skills : {len(role_skills)}")
print(f"Dataset B canonical skills : {len(job_skills)}")
print(f"Common canonical skills    : {len(common_skills)}")

print()
print("Common skills:")
print()

for skill in common_skills:
    print(f"- {skill}")