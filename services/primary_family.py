import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

ROLE_FAMILY_PATH = "data/role_family_mapping.csv"
ROLE_SKILL_PROFILE_PATH = "data/role_skill_profiles.csv"
ROLE_SKILL_WEIGHT_PATH = "data/role_skill_weights.csv"

OUTPUT_PATH = "data/role_family_hierarchy.csv"


# --------------------------------------------------
# ROLE-SPECIFIC FAMILY PRIORITY
#
# Used only to break ties between families.
# The actual family score remains the main factor.
# --------------------------------------------------

ROLE_FAMILY_PRIORITY = {

    # Mobile
    "android developer": [
        "Mobile Development",
        "Software Engineering"
    ],

    "ios developer": [
        "Mobile Development",
        "Software Engineering"
    ],

    "junior ios developer": [
        "Mobile Development",
        "Software Engineering"
    ],

    "mobile developer": [
        "Mobile Development",
        "Software Engineering"
    ],

    "mobile app developer": [
        "Mobile Development",
        "Software Engineering"
    ],

    "mobile application developer": [
        "Mobile Development",
        "Software Engineering"
    ],


    # AI / Research
    "ai researcher": [
        "AI / Machine Learning",
        "Research"
    ],

    "artificial intelligence researcher": [
        "AI / Machine Learning",
        "Research"
    ],

    "machine learning researcher": [
        "AI / Machine Learning",
        "Research"
    ],


    # AI Engineering
    "artificial intelligence engineer": [
        "AI / Machine Learning",
        "Software Engineering"
    ],

    "machine learning engineer": [
        "AI / Machine Learning",
        "Software Engineering"
    ],


    # Cloud / DevOps
    "ansible automation engineer": [
        "Cloud / Infrastructure",
        "DevOps / SRE"
    ],

    "ansible operations engineer": [
        "Cloud / Infrastructure",
        "DevOps / SRE"
    ],

    "aws devops engineer": [
        "Cloud / Infrastructure",
        "DevOps / SRE"
    ],

    "azure devops engineer": [
        "Cloud / Infrastructure",
        "DevOps / SRE"
    ],

    "devops engineer": [
        "DevOps / SRE",
        "Cloud / Infrastructure"
    ],

    "devsecops engineer": [
        "DevOps / SRE",
        "Cybersecurity",
        "Cloud / Infrastructure"
    ],


    # Security
    "cloud security engineer": [
        "Cybersecurity",
        "Cloud / Infrastructure"
    ],


    # Networking
    "cloud network engineer": [
        "Cloud / Infrastructure",
        "Networking"
    ],

    "network and systems administrator": [
        "Networking",
        "IT Operations"
    ],


    # Cloud Administration
    "cloud system administrator": [
        "Cloud / Infrastructure",
        "IT Operations"
    ],


    # API / Integration
    "api developer": [
        "API / Integration",
        "Software Engineering"
    ],

    "mulesoft developer": [
        "API / Integration",
        "Software Engineering"
    ],


    # Web Development
    "web developer": [
        "Web Development",
        "Software Engineering"
    ],

    "front end developer": [
        "Web Development",
        "Software Engineering"
    ],

    "front end web developer": [
        "Web Development",
        "Software Engineering"
    ],

    "javascript developer": [
        "Web Development",
        "Software Engineering"
    ],

    "react developer": [
        "Web Development",
        "Software Engineering"
    ],

    "ui developer": [
        "Web Development",
        "Software Engineering"
    ],


    # Data
    "business intelligence developer": [
        "Data / Analytics",
        "Software Engineering"
    ],

    "data scientist": [
        "Data / Analytics",
        "AI / Machine Learning"
    ],
}


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    role_families = pd.read_csv(
        ROLE_FAMILY_PATH
    )

    role_skills = pd.read_csv(
        ROLE_SKILL_PROFILE_PATH
    )

    role_weights = pd.read_csv(
        ROLE_SKILL_WEIGHT_PATH
    )

    return (
        role_families,
        role_skills,
        role_weights
    )


# --------------------------------------------------
# PREPARE ROLE-FAMILY DATA
# --------------------------------------------------

def prepare_role_families(
    role_families
):

    required_columns = [
        "normalized_title",
        "role_family"
    ]

    missing = [
        column
        for column in required_columns
        if column not in role_families.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns in "
            "role_family_mapping.csv: "
            + str(missing)
        )

    role_families = role_families[
        required_columns
    ].copy()

    role_families[
        "normalized_title"
    ] = (
        role_families[
            "normalized_title"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_families[
        "role_family"
    ] = (
        role_families[
            "role_family"
        ]
        .astype(str)
        .str.strip()
    )

    # Remove unclassified roles
    role_families = role_families[
        role_families[
            "role_family"
        ] != "Unclassified"
    ]

    return (
        role_families
        .drop_duplicates()
    )


# --------------------------------------------------
# PREPARE ROLE-SKILL PROFILE
# --------------------------------------------------

def prepare_role_skills(
    role_skills
):

    required_columns = [
        "normalized_title",
        "canonical_skill",
        "category"
    ]

    missing = [
        column
        for column in required_columns
        if column not in role_skills.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns in "
            "role_skill_profiles.csv: "
            + str(missing)
        )

    role_skills = role_skills[
        required_columns
    ].copy()

    role_skills[
        "normalized_title"
    ] = (
        role_skills[
            "normalized_title"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_skills[
        "canonical_skill"
    ] = (
        role_skills[
            "canonical_skill"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return role_skills


# --------------------------------------------------
# PREPARE ROLE-SKILL WEIGHTS
# --------------------------------------------------

def prepare_role_weights(
    role_weights
):

    required_columns = [
        "normalized_title",
        "canonical_skill",
        "weight"
    ]

    missing = [
        column
        for column in required_columns
        if column not in role_weights.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns in "
            "role_skill_weights.csv: "
            + str(missing)
        )

    role_weights = role_weights[
        required_columns
    ].copy()

    role_weights[
        "normalized_title"
    ] = (
        role_weights[
            "normalized_title"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_weights[
        "canonical_skill"
    ] = (
        role_weights[
            "canonical_skill"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_weights[
        "weight"
    ] = pd.to_numeric(
        role_weights[
            "weight"
        ],
        errors="coerce"
    )

    role_weights = role_weights.dropna(
        subset=["weight"]
    )

    return role_weights


# --------------------------------------------------
# GET TIE-BREAK PRIORITY
# --------------------------------------------------

def get_family_priority(
    role,
    family
):

    role = str(
        role
    ).strip().lower()

    priorities = (
        ROLE_FAMILY_PRIORITY.get(
            role,
            []
        )
    )

    if family in priorities:

        return priorities.index(
            family
        )

    return 999


# --------------------------------------------------
# BUILD FAMILY HIERARCHY
# --------------------------------------------------

def build_family_hierarchy(
    role_families,
    role_skills,
    role_weights
):

    # --------------------------------------------------
    # MERGE SKILLS WITH WEIGHTS
    # --------------------------------------------------

    role_skill_data = role_skills.merge(
        role_weights,
        on=[
            "normalized_title",
            "canonical_skill"
        ],
        how="left"
    )

    # If a skill has no weight,
    # use neutral weight.
    role_skill_data[
        "weight"
    ] = (
        role_skill_data[
            "weight"
        ]
        .fillna(1.0)
    )


    # --------------------------------------------------
    # CONNECT ROLES WITH THEIR FAMILIES
    # --------------------------------------------------

    role_skill_data = role_skill_data.merge(
        role_families,
        on="normalized_title",
        how="inner"
    )


    # --------------------------------------------------
    # CALCULATE FAMILY SKILL WEIGHT
    # --------------------------------------------------

    family_scores = (
        role_skill_data
        .groupby(
            [
                "normalized_title",
                "role_family"
            ],
            as_index=False
        )[
            "weight"
        ]
        .sum()
        .rename(
            columns={
                "weight":
                "family_skill_weight"
            }
        )
    )


    # --------------------------------------------------
    # TOTAL FAMILY WEIGHT PER ROLE
    # --------------------------------------------------

    role_totals = (
        family_scores
        .groupby(
            "normalized_title"
        )[
            "family_skill_weight"
        ]
        .sum()
        .reset_index()
        .rename(
            columns={
                "family_skill_weight":
                "total_family_weight"
            }
        )
    )


    # --------------------------------------------------
    # CALCULATE FAMILY SHARE
    # --------------------------------------------------

    family_scores = family_scores.merge(
        role_totals,
        on="normalized_title",
        how="left"
    )

    family_scores[
        "family_share"
    ] = (
        family_scores[
            "family_skill_weight"
        ]
        / family_scores[
            "total_family_weight"
        ]
        * 100
    )


    # --------------------------------------------------
    # APPLY ROLE-SPECIFIC TIE BREAKING
    # --------------------------------------------------

    family_scores[
        "tie_priority"
    ] = family_scores.apply(
        lambda row: get_family_priority(
            row["normalized_title"],
            row["role_family"]
        ),
        axis=1
    )


    # --------------------------------------------------
    # SORT
    #
    # 1. Higher family score
    # 2. Higher family share
    # 3. Role-specific priority
    # 4. Alphabetical fallback
    # --------------------------------------------------

    family_scores = (
        family_scores
        .sort_values(
            [
                "normalized_title",
                "family_skill_weight",
                "family_share",
                "tie_priority",
                "role_family"
            ],
            ascending=[
                True,
                False,
                False,
                True,
                True
            ]
        )
    )


    # --------------------------------------------------
    # BUILD FINAL RESULTS
    # --------------------------------------------------

    results = []


    for role, role_data in (
        family_scores.groupby(
            "normalized_title"
        )
    ):

        role_data = (
            role_data
            .reset_index(
                drop=True
            )
        )


        # --------------------------------------------------
        # PRIMARY FAMILY
        # --------------------------------------------------

        primary_family = (
            role_data.iloc[0][
                "role_family"
            ]
        )

        primary_score = (
            role_data.iloc[0][
                "family_skill_weight"
            ]
        )

        primary_share = (
            role_data.iloc[0][
                "family_share"
            ]
        )


        # --------------------------------------------------
        # SECONDARY FAMILIES
        # --------------------------------------------------

        secondary_data = (
            role_data.iloc[1:]
        )


        secondary_families = (
            secondary_data[
                "role_family"
            ]
            .tolist()
        )


        secondary_scores = (
            secondary_data[
                "family_skill_weight"
            ]
            .round(2)
            .tolist()
        )


        # --------------------------------------------------
        # SAVE RESULT
        # --------------------------------------------------

        results.append({

            "normalized_title":
                role,

            "primary_family":
                primary_family,

            "primary_family_score":
                round(
                    primary_score,
                    2
                ),

            "primary_family_share":
                round(
                    primary_share,
                    2
                ),

            "secondary_families":
                " | ".join(
                    secondary_families
                ),

            "secondary_family_scores":
                " | ".join(
                    str(score)
                    for score
                    in secondary_scores
                ),

            "family_count":
                len(role_data),

        })


    return pd.DataFrame(
        results
    )


# --------------------------------------------------
# VALIDATE
# --------------------------------------------------

def validate_results(
    hierarchy
):

    print()
    print("=" * 60)
    print(
        "PRIMARY / SECONDARY ROLE FAMILY CLASSIFICATION"
    )
    print("=" * 60)

    print()

    print(
        "Total roles:",
        len(hierarchy)
    )

    print(
        "Roles with multiple families:",
        (
            hierarchy[
                "family_count"
            ] > 1
        ).sum()
    )

    print(
        "Roles with secondary families:",
        (
            hierarchy[
                "secondary_families"
            ].str.len() > 0
        ).sum()
    )

    print()

    print(
        "Primary family distribution:"
    )

    print(
        hierarchy[
            "primary_family"
        ]
        .value_counts()
        .to_string()
    )

    print()

    print(
        "Important role classifications:"
    )

    important_roles = [
        "android developer",
        "ios developer",
        "ai researcher",
        "artificial intelligence researcher",
        "artificial intelligence engineer",
        "machine learning engineer",
        "ansible automation engineer",
        "devops engineer",
        "cloud security engineer",
        "cloud network engineer",
        "api developer",
        "web developer",
        "business intelligence developer",
        "data scientist",
    ]

    sample = hierarchy[
        hierarchy[
            "normalized_title"
        ].isin(
            important_roles
        )
    ]

    print(
        sample[
            [
                "normalized_title",
                "primary_family",
                "primary_family_share",
                "secondary_families"
            ]
        ]
        .to_string(
            index=False
        )
    )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    # --------------------------------------------------
    # LOAD
    # --------------------------------------------------

    (
        role_families,
        role_skills,
        role_weights
    ) = load_data()


    # --------------------------------------------------
    # PREPARE
    # --------------------------------------------------

    role_families = (
        prepare_role_families(
            role_families
        )
    )

    role_skills = (
        prepare_role_skills(
            role_skills
        )
    )

    role_weights = (
        prepare_role_weights(
            role_weights
        )
    )


    # --------------------------------------------------
    # BUILD
    # --------------------------------------------------

    hierarchy = (
        build_family_hierarchy(
            role_families,
            role_skills,
            role_weights
        )
    )


    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    hierarchy.to_csv(
        OUTPUT_PATH,
        index=False
    )


    # --------------------------------------------------
    # VALIDATE
    # --------------------------------------------------

    validate_results(
        hierarchy
    )


    print()

    print(
        "Saved to:",
        OUTPUT_PATH
    )