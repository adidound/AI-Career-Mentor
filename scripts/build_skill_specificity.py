import pandas as pd
import math


INPUT_PATH = "data/role_skill_prevalence.csv"
OUTPUT_PATH = "data/skill_specificity.csv"


df = pd.read_csv(INPUT_PATH)

total_roles = df["normalized_title"].nunique()

skill_document_frequency = (
    df.groupby("canonical_skill")["normalized_title"]
    .nunique()
    .reset_index(name="role_count")
)


skill_document_frequency["specificity"] = (
    skill_document_frequency["role_count"]
    .apply(lambda x: math.log(total_roles / x))
)


skill_document_frequency = (
    skill_document_frequency
    .sort_values("specificity", ascending=False)
    .reset_index(drop=True)
)


skill_document_frequency.to_csv(
    OUTPUT_PATH,
    index=False
)


print("=" * 60)
print("SKILL SPECIFICITY")
print("=" * 60)

print(f"Total roles          : {total_roles}")
print(
    f"Unique canonical skills: "
    f"{len(skill_document_frequency)}"
)

print()
print("Most specific skills:")
print(
    skill_document_frequency
    .head(20)
    .to_string(index=False)
)

print()
print(f"Saved to: {OUTPUT_PATH}")