import pandas as pd
import ast

ROLE_FILE = "data/it_roles_clean.csv"
JOB_FILE = "data/all_job_post.csv"


def parse_role_skills(value):
    if pd.isna(value):
        return []

    return [
        skill.strip()
        for skill in str(value).split(",")
        if skill.strip()
    ]


def parse_job_skills(value):
    if pd.isna(value):
        return []

    try:
        skills = ast.literal_eval(value)

        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]

    except (ValueError, SyntaxError):
        return []


# Load datasets
roles = pd.read_csv(ROLE_FILE, encoding="latin1")
jobs = pd.read_csv(JOB_FILE, encoding="latin1")


# Extract skills
role_skills = set()

for skills in roles["Skills"].dropna():
    role_skills.update(parse_role_skills(skills))


job_skills = set()

for skills in jobs["job_skill_set"].dropna():
    job_skills.update(parse_job_skills(skills))


# Sort for reproducibility
role_skills = sorted(role_skills, key=str.lower)
job_skills = sorted(job_skills, key=str.lower)


# Save vocabularies
role_vocab_df = pd.DataFrame({
    "skill": role_skills
})

job_vocab_df = pd.DataFrame({
    "skill": job_skills
})


role_vocab_df.to_csv(
    "data/role_skill_vocabulary.csv",
    index=False
)

job_vocab_df.to_csv(
    "data/job_skill_vocabulary.csv",
    index=False
)


print("Dataset A unique skills:", len(role_skills))
print("Dataset B unique skills:", len(job_skills))

print("\nSaved:")
print("data/role_skill_vocabulary.csv")
print("data/job_skill_vocabulary.csv")

print("\nDataset A first 20 skills:")
print(role_skills[:20])

print("\nDataset B first 20 skills:")
print(job_skills[:20])


# --------------------------------------------------
# Find skills common to both datasets
# --------------------------------------------------

role_normalized = {
    skill.strip().lower()
    for skill in role_skills
}

job_normalized = {
    skill.strip().lower()
    for skill in job_skills
}


common_skills = sorted(
    role_normalized & job_normalized
)


# Save common skills
common_skill_df = pd.DataFrame({
    "skill": common_skills
})


common_skill_df.to_csv(
    "data/common_skill_vocabulary.csv",
    index=False
)


print("\nCommon normalized skills:", len(common_skills))
print("Saved: data/common_skill_vocabulary.csv")