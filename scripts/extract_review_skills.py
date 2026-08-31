import pandas as pd


INPUT_PATH = "data/role_skill_classification.csv"
OUTPUT_PATH = "data/skills_for_review.csv"


df = pd.read_csv(INPUT_PATH)

review = df[
    df["category"] == "Other / Review"
][["canonical_skill"]].copy()

review.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("SKILLS REQUIRING REVIEW")
print("=" * 60)

print(f"Total review skills: {len(review)}")
print(f"Saved to: {OUTPUT_PATH}")

print()
print("All review skills:")
print()

for skill in review["canonical_skill"]:
    print(skill)