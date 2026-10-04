import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

ROLE_SKILLS_PATH = "data/role_skill_profiles.csv"
SPECIFICITY_PATH = "data/skill_specificity.csv"
ROLE_FAMILY_PATH = "data/role_family_mapping.csv"

OUTPUT_PATH = "data/role_skill_weights.csv"


# --------------------------------------------------
# CATEGORY WEIGHTS
# --------------------------------------------------

CATEGORY_WEIGHTS = {
    "Programming Language": 1.00,
    "Framework / Library": 1.00,
    "Database / Data Technology": 1.00,
    "Cloud / Infrastructure": 1.00,

    "Data / AI": 1.05,
    "AI / Advanced Analytics": 1.05,

    "Security": 1.05,

    "Testing / QA": 0.95,

    "DevOps / CI-CD": 1.00,
    "DevOps / SRE": 1.00,

    "Design / UX": 0.95,
    "Animation / Multimedia": 1.00,
    "Mobile Development": 1.00,
    "API / Integration": 1.00,
    "Networking": 1.00,

    "Monitoring / Observability": 0.95,

    "Hardware / Embedded": 1.00,
    "Architecture / Design": 1.00,
    "Web Development": 1.00,

    "Business / Management": 0.80,
    "Enterprise / Business Systems": 0.90,

    "IT Operations": 0.90,
    "IT Operations / Administration": 0.90,
    "IT Service Management": 0.85,

    "Research": 0.90,
    "Research / Analytics": 0.90,

    "Finance / Business": 0.80,
    "Marketing / SEO": 0.80,

    "Soft Skill": 0.70,

    "Compliance / Governance": 0.80,

    "Data Engineering": 1.00,
    "Software Engineering": 1.00,

    "Robotics": 1.00,
    "Robotics / Control Systems": 1.00,

    "Game Development": 1.00,
    "Mainframe / Legacy Systems": 1.00,
    "GIS / Geospatial": 1.00,

    "Other / Review": 0.60,
}


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

role_skills = pd.read_csv(
    ROLE_SKILLS_PATH
)

specificity = pd.read_csv(
    SPECIFICITY_PATH
)

role_families = pd.read_csv(
    ROLE_FAMILY_PATH
)


# --------------------------------------------------
# VALIDATE REQUIRED COLUMNS
# --------------------------------------------------

required_role_columns = {
    "normalized_title",
    "canonical_skill",
    "category",
}

required_specificity_columns = {
    "canonical_skill",
    "specificity",
}

required_family_columns = {
    "normalized_title",
    "role_family",
}

if not required_role_columns.issubset(
    role_skills.columns
):
    raise ValueError(
        "role_skill_profiles.csv is missing "
        "required columns"
    )

if not required_specificity_columns.issubset(
    specificity.columns
):
    raise ValueError(
        "skill_specificity.csv is missing "
        "required columns"
    )

if not required_family_columns.issubset(
    role_families.columns
):
    raise ValueError(
        "role_family_mapping.csv is missing "
        "required columns"
    )


# --------------------------------------------------
# MERGE SPECIFICITY
# --------------------------------------------------

df = role_skills.merge(
    specificity[
        [
            "canonical_skill",
            "specificity",
        ]
    ],
    on="canonical_skill",
    how="left",
)


# --------------------------------------------------
# SELECT PRIMARY ROLE FAMILY
# --------------------------------------------------

family_priority = (
    role_families
    .groupby("normalized_title")
    .first()
    .reset_index()
)


df = df.merge(
    family_priority[
        [
            "normalized_title",
            "role_family",
        ]
    ],
    on="normalized_title",
    how="left",
)


# --------------------------------------------------
# HANDLE MISSING VALUES
# --------------------------------------------------

df["category"] = (
    df["category"]
    .fillna("Other / Review")
)

df["role_family"] = (
    df["role_family"]
    .fillna("Unclassified")
)


# --------------------------------------------------
# CAP SPECIFICITY
# --------------------------------------------------

SPECIFICITY_MIN = 1.6
SPECIFICITY_MAX = 3.5

df["specificity_capped"] = (
    df["specificity"]
    .fillna(2.5)
    .clip(
        lower=SPECIFICITY_MIN,
        upper=SPECIFICITY_MAX,
    )
)


# --------------------------------------------------
# SPECIFICITY FACTOR
# --------------------------------------------------

df["specificity_factor"] = (
    0.95
    +
    (
        (
            df["specificity_capped"]
            - SPECIFICITY_MIN
        )
        /
        (
            SPECIFICITY_MAX
            - SPECIFICITY_MIN
        )
    )
    * 0.10
)


# --------------------------------------------------
# CATEGORY FACTOR
# --------------------------------------------------

df["category_factor"] = (
    df["category"]
    .map(CATEGORY_WEIGHTS)
    .fillna(0.80)
)


# --------------------------------------------------
# ROLE-FAMILY ALIGNMENT
# --------------------------------------------------

def family_alignment(row):

    family = row["role_family"]
    category = row["category"]

    alignment = {

        "AI / Machine Learning": {
            "Data / AI",
            "AI / Advanced Analytics",
            "Programming Language",
            "Framework / Library",
            "Data Engineering",
        },

        "Data / Analytics": {
            "Data / AI",
            "AI / Advanced Analytics",
            "Data Engineering",
            "Database / Data Technology",
            "Programming Language",
        },

        "Software Engineering": {
            "Software Engineering",
            "Programming Language",
            "Framework / Library",
            "API / Integration",
            "Database / Data Technology",
        },

        "Web Development": {
            "Web Development",
            "Programming Language",
            "Framework / Library",
            "Design / UX",
            "API / Integration",
        },

        "Cloud / Infrastructure": {
            "Cloud / Infrastructure",
            "Networking",
            "IT Operations",
            "Security",
        },

        "DevOps / SRE": {
            "DevOps / SRE",
            "DevOps / CI-CD",
            "Cloud / Infrastructure",
            "Monitoring / Observability",
            "Networking",
        },

        "Cybersecurity": {
            "Security",
            "Cloud / Infrastructure",
            "Networking",
            "IT Operations",
            "Compliance / Governance",
        },

        "Networking": {
            "Networking",
            "Cloud / Infrastructure",
            "Security",
            "IT Operations",
        },

        "Database": {
            "Database / Data Technology",
            "Data Engineering",
            "Data / AI",
        },

        "Mobile Development": {
            "Mobile Development",
            "Programming Language",
            "Framework / Library",
            "Design / UX",
            "API / Integration",
        },

        "UI / UX": {
            "Design / UX",
            "Web Development",
            "Animation / Multimedia",
        },

        "Animation / Multimedia": {
            "Animation / Multimedia",
            "Design / UX",
        },

        "Hardware / Embedded": {
            "Hardware / Embedded",
            "Robotics / Control Systems",
        },

        "Robotics": {
            "Robotics",
            "Hardware / Embedded",
            "Robotics / Control Systems",
        },

        "Enterprise / Business Systems": {
            "Enterprise / Business Systems",
            "Database / Data Technology",
            "Software Engineering",
        },

        "IT Operations": {
            "IT Operations",
            "IT Operations / Administration",
            "Cloud / Infrastructure",
            "Networking",
            "Monitoring / Observability",
        },

        "Project / Product Management": {
            "Business / Management",
            "Enterprise / Business Systems",
            "Soft Skill",
        },

        "Research": {
            "Research",
            "Research / Analytics",
            "Data / AI",
            "AI / Advanced Analytics",
        },

        "Marketing / SEO": {
            "Marketing / SEO",
            "Design / UX",
        },

        "Finance / Business": {
            "Finance / Business",
            "Business / Management",
            "Enterprise / Business Systems",
        },

        "GIS / Geospatial": {
            "GIS / Geospatial",
        },

        "Game Development": {
            "Game Development",
            "Animation / Multimedia",
            "Programming Language",
            "Framework / Library",
        },

        "API / Integration": {
            "API / Integration",
            "Software Engineering",
            "Framework / Library",
        },
    }

    aligned_categories = alignment.get(
        family,
        set()
    )

    if category in aligned_categories:
        return 1.05

    return 1.00


df["family_factor"] = (
    df.apply(
        family_alignment,
        axis=1
    )
)


# --------------------------------------------------
# CALCULATE RAW WEIGHT
# --------------------------------------------------

df["raw_weight"] = (
    df["category_factor"]
    *
    df["specificity_factor"]
    *
    df["family_factor"]
)


# --------------------------------------------------
# NORMALIZE WITHIN EACH ROLE
# --------------------------------------------------

role_totals = (
    df
    .groupby("normalized_title")["raw_weight"]
    .transform("sum")
)

df["normalized_weight"] = (
    df["raw_weight"]
    /
    role_totals
)


# --------------------------------------------------
# CONVERT TO PERCENTAGE
# --------------------------------------------------

df["weight"] = (
    df["normalized_weight"]
    * 100
)


# --------------------------------------------------
# ROUND VALUES
# --------------------------------------------------

df["specificity"] = (
    df["specificity"]
    .round(4)
)

df["specificity_capped"] = (
    df["specificity_capped"]
    .round(4)
)

df["specificity_factor"] = (
    df["specificity_factor"]
    .round(4)
)

df["category_factor"] = (
    df["category_factor"]
    .round(4)
)

df["family_factor"] = (
    df["family_factor"]
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
# OUTPUT
# --------------------------------------------------

output_columns = [
    "normalized_title",
    "canonical_skill",
    "category",
    "role_family",
    "specificity",
    "specificity_capped",
    "specificity_factor",
    "category_factor",
    "family_factor",
    "raw_weight",
    "normalized_weight",
    "weight",
]

df = df[output_columns]


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