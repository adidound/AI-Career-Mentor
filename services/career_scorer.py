import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

ROLE_WEIGHTS_PATH = "data/role_skill_weights.csv"
ROLE_FAMILY_PATH = "data/role_family_mapping.csv"
ROLE_LEVEL_PATH = "data/role_level_mapping.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_role_data():

    role_weights = pd.read_csv(
        ROLE_WEIGHTS_PATH
    )

    role_families = pd.read_csv(
        ROLE_FAMILY_PATH
    )

    role_levels = pd.read_csv(
        ROLE_LEVEL_PATH
    )

    # --------------------------------------------------
    # NORMALIZE ROLE WEIGHTS COLUMNS
    #
    # Actual file:
    # role | skill | weight
    #
    # Internally we use:
    # normalized_title | canonical_skill | weight
    # --------------------------------------------------

    role_weights = role_weights.rename(
        columns={
            "role": "normalized_title",
            "skill": "canonical_skill"
        }
    )

    # --------------------------------------------------
    # NORMALIZE TEXT
    # --------------------------------------------------

    role_weights["normalized_title"] = (
        role_weights["normalized_title"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_weights["canonical_skill"] = (
        role_weights["canonical_skill"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_families["normalized_title"] = (
        role_families["normalized_title"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_levels["normalized_title"] = (
        role_levels["normalized_title"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return (
        role_weights,
        role_families,
        role_levels
    )


# --------------------------------------------------
# NORMALIZE STUDENT SKILLS
# --------------------------------------------------

def normalize_student_skills(student_skills):

    return {
        str(skill).strip().lower()
        for skill in student_skills
        if str(skill).strip()
    }


# --------------------------------------------------
# GET ROLE FAMILY
# --------------------------------------------------

def get_role_family(
    role,
    role_families
):

    matches = role_families[
        role_families[
            "normalized_title"
        ] == role
    ]

    if len(matches) == 0:

        return "Unclassified"

    return matches[
        "role_family"
    ].iloc[0]


# --------------------------------------------------
# GET ROLE LEVEL
# --------------------------------------------------

def get_role_level(
    role,
    role_levels
):

    matches = role_levels[
        role_levels[
            "normalized_title"
        ] == role
    ]

    if len(matches) == 0:

        return "Unspecified"

    return matches[
        "role_level"
    ].iloc[0]


# --------------------------------------------------
# SCORE ONE ROLE
# --------------------------------------------------

def score_role(
    student_skills,
    role_data,
    role_families,
    role_levels
):

    student_skills = (
        normalize_student_skills(
            student_skills
        )
    )

    # --------------------------------------------------
    # ROLE NAME
    # --------------------------------------------------

    role = (
        str(
            role_data[
                "normalized_title"
            ].iloc[0]
        )
        .strip()
        .lower()
    )

    # --------------------------------------------------
    # ROLE SKILLS
    # --------------------------------------------------

    role_skill_names = (
        role_data[
            "canonical_skill"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    role_skills = set(
        role_skill_names
    )

    # --------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------

    matched_skills = (
        student_skills
        .intersection(
            role_skills
        )
    )

    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    missing_skills = (
        role_skills
        - student_skills
    )

    # --------------------------------------------------
    # WEIGHTED COVERAGE
    # --------------------------------------------------

    matched_mask = (
        role_skill_names.isin(
            matched_skills
        )
    )

    matched_weight = (
        role_data.loc[
            matched_mask,
            "weight"
        ].sum()
    )

    total_weight = (
        role_data[
            "weight"
        ].sum()
    )

    if total_weight > 0:

        weighted_coverage = (
            matched_weight
            / total_weight
        ) * 100

    else:

        weighted_coverage = 0.0

    # --------------------------------------------------
    # SKILL COUNT COVERAGE
    # --------------------------------------------------

    total_role_skills = len(
        role_skills
    )

    matched_skill_count = len(
        matched_skills
    )

    if total_role_skills > 0:

        skill_coverage = (
            matched_skill_count
            / total_role_skills
        ) * 100

    else:

        skill_coverage = 0.0

    # --------------------------------------------------
    # FINAL TECHNICAL FITNESS
    # --------------------------------------------------

    technical_fitness = (
        0.70 * weighted_coverage
        +
        0.30 * skill_coverage
    )

    # --------------------------------------------------
    # ROLE FAMILY
    # --------------------------------------------------

    role_family = get_role_family(
        role,
        role_families
    )

    # --------------------------------------------------
    # ROLE LEVEL
    # --------------------------------------------------

    role_level = get_role_level(
        role,
        role_levels
    )

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    return {

        "Career": role,

        "Match": round(
            technical_fitness,
            1
        ),

        "Technical Fitness": round(
            technical_fitness,
            1
        ),

        "Weighted Coverage": round(
            weighted_coverage,
            1
        ),

        "Skill Coverage": round(
            skill_coverage,
            1
        ),

        "Role Family": role_family,

        "Role Level": role_level,

        "Matched Skills": sorted(
            matched_skills
        ),

        "Missing Skills": sorted(
            missing_skills
        ),

    }


# --------------------------------------------------
# RECOMMEND ROLES
# --------------------------------------------------

def recommend_roles(
    student_skills,
    role_skill_weights=None,
    role_families=None,
    role_levels=None
):

    # --------------------------------------------------
    # LOAD DATA IF NOT PROVIDED
    # --------------------------------------------------

    if (
        role_skill_weights is None
        or role_families is None
        or role_levels is None
    ):

        (
            loaded_weights,
            loaded_families,
            loaded_levels
        ) = load_role_data()

        if role_skill_weights is None:

            role_skill_weights = (
                loaded_weights
            )

        if role_families is None:

            role_families = (
                loaded_families
            )

        if role_levels is None:

            role_levels = (
                loaded_levels
            )

    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------

    required_columns = {
        "normalized_title",
        "canonical_skill",
        "weight"
    }

    missing_columns = (
        required_columns
        - set(
            role_skill_weights.columns
        )
    )

    if missing_columns:

        raise ValueError(
            "role_skill_weights is missing "
            f"columns: {missing_columns}"
        )

    # --------------------------------------------------
    # SCORE EVERY ROLE
    # --------------------------------------------------

    results = []

    roles = (
        role_skill_weights[
            "normalized_title"
        ]
        .dropna()
        .unique()
    )

    for role in roles:

        role_data = (
            role_skill_weights[
                role_skill_weights[
                    "normalized_title"
                ] == role
            ]
        )

        result = score_role(
            student_skills,
            role_data,
            role_families,
            role_levels
        )

        results.append(
            result
        )

    # --------------------------------------------------
    # SORT BY TECHNICAL FITNESS
    # --------------------------------------------------

    results.sort(
        key=lambda x: x[
            "Technical Fitness"
        ],
        reverse=True
    )

    return results


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_skills = [

        "python",
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "sql",

    ]

    recommendations = (
        recommend_roles(
            test_skills
        )
    )

    print("=" * 60)
    print(
        "CAREER SCORING TEST"
    )
    print("=" * 60)

    for recommendation in (
        recommendations[:10]
    ):

        print(
            f"{recommendation['Career']}: "
            f"{recommendation['Match']}%"
        )

        print(
            f"Role Family: "
            f"{recommendation['Role Family']}"
        )

        print(
            f"Role Level: "
            f"{recommendation['Role Level']}"
        )

        print(
            f"Weighted Coverage: "
            f"{recommendation['Weighted Coverage']}%"
        )

        print(
            f"Skill Coverage: "
            f"{recommendation['Skill Coverage']}%"
        )

        print(
            "Matched:",
            ", ".join(
                recommendation[
                    "Matched Skills"
                ]
            )
        )

        print(
            "Missing:",
            ", ".join(
                recommendation[
                    "Missing Skills"
                ]
            )
        )

        print()