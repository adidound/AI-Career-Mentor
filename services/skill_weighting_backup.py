import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

ROLE_SKILLS_PATH = "data/role_skill_profiles.csv"
OUTPUT_PATH = "data/role_skill_weights.csv"


# --------------------------------------------------
# CATEGORY WEIGHTS
# --------------------------------------------------

CATEGORY_WEIGHTS = {
    "Programming Language": 1.00,
    "Framework / Library": 1.00,
    "Database / Data Technology": 1.00,
    "Cloud / Infrastructure": 1.00,

    "Data / AI": 1.10,
    "AI / Advanced Analytics": 1.10,

    "Security": 1.10,

    "Testing / QA": 0.90,
    "DevOps / CI-CD": 1.00,
    "DevOps / SRE": 1.00,

    "Design / UX": 0.90,
    "Animation / Multimedia": 1.00,
    "Mobile Development": 1.00,
    "API / Integration": 1.00,
    "Networking": 1.00,

    "Monitoring / Observability": 0.90,

    "Hardware / Embedded": 1.00,
    "Architecture / Design": 1.00,
    "Web Development": 1.00,

    "Business / Management": 0.75,
    "Enterprise / Business Systems": 0.90,

    "IT Operations": 0.90,
    "IT Operations / Administration": 0.90,
    "IT Service Management": 0.80,

    "Research": 0.90,
    "Research / Analytics": 0.90,

    "Finance / Business": 0.80,
    "Marketing / SEO": 0.80,

    "Soft Skill": 0.65,

    "Compliance / Governance": 0.75,

    "Data Engineering": 1.00,
    "Software Engineering": 1.00,

    "Robotics": 1.00,
    "Robotics / Control Systems": 1.00,

    "Game Development": 1.00,
    "Mainframe / Legacy Systems": 1.00,
    "GIS / Geospatial": 1.00,

    "Other / Review": 0.50,
}


# --------------------------------------------------
# LOAD ROLE-SKILL DATA
# --------------------------------------------------

df = pd.read_csv(
    ROLE_SKILLS_PATH
)


# --------------------------------------------------
# VALIDATE REQUIRED COLUMNS
# --------------------------------------------------

required_columns = {
    "normalized_title",
    "canonical_skill",
    "category",
}

missing_columns = (
    required_columns
    - set(df.columns)
)

if missing_columns:
    raise ValueError(
        "Missing columns in "
        f"{ROLE_SKILLS_PATH}: "
        f"{sorted(missing_columns)}"
    )


# --------------------------------------------------
# HANDLE MISSING CATEGORIES
# --------------------------------------------------

df["category"] = (
    df["category"]
    .fillna("Other / Review")
)


# --------------------------------------------------
# CATEGORY WEIGHT
# --------------------------------------------------

df["category_weight"] = (
    df["category"]
    .map(CATEGORY_WEIGHTS)
    .fillna(0.80)
)


# --------------------------------------------------
# RAW WEIGHT
# --------------------------------------------------

df["raw_weight"] = (
    df["category_weight"]
)


# --------------------------------------------------
# NORMALIZE WEIGHTS WITHIN EACH ROLE
# --------------------------------------------------

role_totals = (
    df
    .groupby("normalized_title")["raw_weight"]
    .transform("sum")
)

df["normalized_weight"] = (
    df["raw_weight"]
    / role_totals
)


# --------------------------------------------------
# CONVERT TO PERCENTAGE SCALE
# --------------------------------------------------

df["weight"] = (
    df["normalized_weight"]
    * 100
)


# --------------------------------------------------
# ROUND VALUES
# --------------------------------------------------

df["category_weight"] = (
    df["category_weight"]
    .round(4)
)

df["raw_weight"] = (
    df["raw_weight"]
    .round(4)
)

df["normalized_weight"] = (
    df["normalized_weight"]
    .round(6)
)

df["weight"] = (
    df["weight"]
    .round(2)
)


# --------------------------------------------------
# OUTPUT COLUMNS
# --------------------------------------------------

output_columns = [
    "normalized_title",
    "canonical_skill",
    "category",
    "category_weight",
    "raw_weight",
    "normalized_weight",
    "weight",
]

df = df[output_columns]


# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

role_weight_totals = (
    df
    .groupby("normalized_title")["weight"]
    .sum()
)

max_deviation = (
    abs(role_weight_totals - 100)
    .max()
)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("=" * 60)
print("ROLE SKILL WEIGHTING")
print("=" * 60)

print(
    f"Total role-skill pairs : "
    f"{len(df)}"
)

print(
    f"Unique roles           : "
    f"{df['normalized_title'].nunique()}"
)

print(
    f"Unique skills          : "
    f"{df['canonical_skill'].nunique()}"
)

print()

print("Weight statistics:")

print(
    df["weight"]
    .describe()
    .to_string()
)

print()

print(
    f"Maximum role total deviation "
    f"from 100: {max_deviation:.2f}"
)

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)