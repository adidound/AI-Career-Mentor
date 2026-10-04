import pandas as pd


INPUT_PATH = "data/IT_Job_Roles_Skills.csv"
OUTPUT_PATH = "data/role_skill_weights.csv"


df = pd.read_csv(
    INPUT_PATH,
    encoding="cp1252"
)

records = []

for _, row in df.iterrows():

    role = str(row["Job Title"]).strip().lower()

    if not role:
        continue

    raw_skills = str(row["Skills"]).split(",")

    skills = {
        skill.strip().lower()
        for skill in raw_skills
        if skill.strip()
    }

    for skill in skills:
        records.append({
            "role": role,
            "skill": skill,
        })


role_skill = pd.DataFrame(records)

role_skill = role_skill.drop_duplicates(
    subset=["role", "skill"]
)

role_counts = (
    role_skill
    .groupby("role")
    .size()
    .rename("skill_count")
)

role_skill["weight"] = (
    role_skill
    .groupby("role")["skill"]
    .transform("count")
)

role_skill["weight"] = (
    role_skill["weight"] / role_skill["role"].map(
        role_skill.groupby("role").size()
    )
)

role_skill.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("ROLE SKILL WEIGHTS")
print("=" * 60)

print(f"Total role-skill relationships: {len(role_skill)}")
print(f"Unique roles: {role_skill['role'].nunique()}")
print(f"Unique skills: {role_skill['skill'].nunique()}")

print()
print(f"Saved to: {OUTPUT_PATH}")