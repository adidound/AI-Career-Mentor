import pandas as pd

INPUT_FILE = "data/IT_Job_Roles_Skills.csv"
OUTPUT_FILE = "data/it_roles_clean.csv"


def normalize_title(title):
    return (
        str(title)
        .strip()
        .lower()
        .replace("  ", " ")
    )


# Load original dataset
df = pd.read_csv(INPUT_FILE, encoding="latin1")

# Normalize job titles
df["normalized_title"] = (
    df["Job Title"]
    .apply(normalize_title)
)

# Combine duplicate role records
clean_df = (
    df.groupby("normalized_title", as_index=False)
      .agg({
          "Job Title": "first",
          "Job Description": "first",
          "Skills": "first",
          "Certifications": "first"
      })
)

# Save cleaned dataset
clean_df.to_csv(OUTPUT_FILE, index=False)

print("Original records:", len(df))
print("Clean role records:", len(clean_df))
print("Saved to:", OUTPUT_FILE)

print("\nFirst 20 roles:")
print(clean_df[["Job Title", "Skills"]].head(20).to_string(index=False))