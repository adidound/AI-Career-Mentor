import pandas as pd

from services.skill_classifier import classify_skill


INPUT_PATH = "data/role_canonical_skill_vocabulary.csv"
OUTPUT_PATH = "data/role_skill_classification.csv"


df = pd.read_csv(INPUT_PATH)

df["category"] = df["canonical_skill"].apply(classify_skill)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("SKILL CLASSIFICATION")
print("=" * 60)

print(f"Total skills: {len(df)}")
print(f"Saved to: {OUTPUT_PATH}")

print()
print("Category counts:")
print(df["category"].value_counts().to_string())

print()

review_count = (df["category"] == "Other / Review").sum()

print(f"Skills requiring review: {review_count}")