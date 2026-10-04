import pandas as pd

from services.career_scorer import recommend_roles
from services.career_stage import get_stage_factor


# --------------------------------------------------
# FILE PATH
# --------------------------------------------------

ROLE_FAMILY_PATH = "data/role_family_hierarchy.csv"


# --------------------------------------------------
# RECOMMENDATION FILTER
# --------------------------------------------------
#
# Roles below this suitability score are not useful
# enough to display as recommendations.
#
# Keep this conservative so that legitimate
# low-scoring career paths are not removed.
# --------------------------------------------------

MIN_ROLE_SUITABILITY = 1.0


# --------------------------------------------------
# SECONDARY FAMILY FACTOR
# --------------------------------------------------

SECONDARY_FAMILY_FACTOR = 0.50


# --------------------------------------------------
# LOAD ROLE-FAMILY HIERARCHY
# --------------------------------------------------

def load_role_family_mapping():

    family_mapping = pd.read_csv(
        ROLE_FAMILY_PATH
    )

    required_columns = [
        "normalized_title",
        "primary_family",
        "secondary_families"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in family_mapping.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns in "
            "role_family_hierarchy.csv: "
            + str(missing_columns)
        )

    family_mapping = family_mapping[
        required_columns
    ].copy()

    family_mapping[
        "normalized_title"
    ] = (
        family_mapping[
            "normalized_title"
        ]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    family_mapping[
        "primary_family"
    ] = (
        family_mapping[
            "primary_family"
        ]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    family_mapping[
        "secondary_families"
    ] = (
        family_mapping[
            "secondary_families"
        ]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    return family_mapping


# --------------------------------------------------
# FILTER ROLE RECOMMENDATIONS
# --------------------------------------------------

def filter_role_recommendations(
    role_results
):

    filtered_results = []

    for result in role_results:

        suitability = float(
            result.get(
                "Career Suitability",
                0
            )
        )

        if suitability >= MIN_ROLE_SUITABILITY:

            filtered_results.append(
                result
            )

    return filtered_results


# --------------------------------------------------
# RECOMMEND CAREER FAMILIES
# --------------------------------------------------

def recommend_career_families(
    student_skills,
    student_stage,
    top_families=10,
    roles_per_family=5
):

    # --------------------------------------------------
    # GET ROLE SCORES
    # --------------------------------------------------

    role_results = recommend_roles(
        student_skills
    )

    if not role_results:

        return []


    # --------------------------------------------------
    # CALCULATE CAREER SUITABILITY
    # --------------------------------------------------

    for result in role_results:

        role_level = result.get(
            "Role Level",
            "Unspecified"
        )

        stage_factor = get_stage_factor(
            student_stage,
            role_level
        )

        technical_fitness = float(
            result[
                "Technical Fitness"
            ]
        )

        career_suitability = (
            technical_fitness
            * stage_factor
        )

        result[
            "Stage Factor"
        ] = stage_factor

        result[
            "Career Suitability"
        ] = career_suitability


    # --------------------------------------------------
    # FILTER WEAK / ZERO ROLES
    # --------------------------------------------------

    role_results = filter_role_recommendations(
        role_results
    )

    if not role_results:

        return []


    # --------------------------------------------------
    # LOAD FAMILY HIERARCHY
    # --------------------------------------------------

    family_mapping = (
        load_role_family_mapping()
    )


    # --------------------------------------------------
    # CREATE ROLE → FAMILIES MAPPING
    # --------------------------------------------------

    role_to_families = {}


    for _, row in (
        family_mapping.iterrows()
    ):

        role = str(
            row["normalized_title"]
        ).strip().lower()

        primary_family = str(
            row["primary_family"]
        ).strip()

        secondary_families = str(
            row["secondary_families"]
        ).strip()


        if role not in role_to_families:

            role_to_families[
                role
            ] = []


        # --------------------------------------------------
        # PRIMARY FAMILY
        # --------------------------------------------------

        if primary_family:

            role_to_families[
                role
            ].append({

                "family":
                    primary_family,

                "family_factor":
                    1.00,

                "family_type":
                    "Primary"

            })


        # --------------------------------------------------
        # SECONDARY FAMILIES
        # --------------------------------------------------

        if (
            secondary_families
            and secondary_families.lower()
            != "nan"
        ):

            secondary_list = (
                secondary_families
                .split("|")
            )

            for family in secondary_list:

                family = (
                    family.strip()
                )

                if not family:

                    continue

                if family == primary_family:

                    continue

                role_to_families[
                    role
                ].append({

                    "family":
                        family,

                    "family_factor":
                        SECONDARY_FAMILY_FACTOR,

                    "family_type":
                        "Secondary"

                })


    # --------------------------------------------------
    # BUILD FAMILY → ROLES
    # --------------------------------------------------

    family_roles = {}


    for result in role_results:

        role = str(
            result["Career"]
        ).strip().lower()

        families = (
            role_to_families.get(
                role,
                []
            )
        )


        for family_info in families:

            family = family_info[
                "family"
            ]

            family_factor = (
                family_info[
                    "family_factor"
                ]
            )

            family_type = (
                family_info[
                    "family_type"
                ]
            )


            if family not in family_roles:

                family_roles[
                    family
                ] = []


            role_copy = result.copy()

            role_copy[
                "Family Factor"
            ] = family_factor

            role_copy[
                "Family Type"
            ] = family_type

            role_copy[
                "Family Adjusted Suitability"
            ] = (
                result[
                    "Career Suitability"
                ]
                * family_factor
            )


            family_roles[
                family
            ].append(
                role_copy
            )


    # --------------------------------------------------
    # BUILD FAMILY RESULTS
    # --------------------------------------------------

    family_results = []


    for family, roles in (
        family_roles.items()
    ):

        if not roles:

            continue


        # --------------------------------------------------
        # REMOVE DUPLICATE ROLES
        # --------------------------------------------------

        unique_roles = {}


        for role in roles:

            career = str(
                role["Career"]
            ).strip().lower()


            if career not in unique_roles:

                unique_roles[
                    career
                ] = role

            else:

                existing = unique_roles[
                    career
                ]

                if (
                    role[
                        "Family Adjusted Suitability"
                    ]
                    >
                    existing[
                        "Family Adjusted Suitability"
                    ]
                ):

                    unique_roles[
                        career
                    ] = role


        roles = list(
            unique_roles.values()
        )


        if not roles:

            continue


        # --------------------------------------------------
        # SORT ROLES
        # --------------------------------------------------

        roles = sorted(
            roles,
            key=lambda x: x[
                "Family Adjusted Suitability"
            ],
            reverse=True
        )


        # --------------------------------------------------
        # TOP ROLES
        # --------------------------------------------------

        top_three = roles[:3]


        if not top_three:

            continue


        # --------------------------------------------------
        # FAMILY SCORE
        # --------------------------------------------------

        family_score = (
            sum(
                role[
                    "Family Adjusted Suitability"
                ]
                for role in top_three
            )
            / len(top_three)
        )


        # --------------------------------------------------
        # BEST ROLE
        # --------------------------------------------------

        best_role = roles[0]


        # --------------------------------------------------
        # TOP ROLES FOR DISPLAY
        # --------------------------------------------------

        top_roles = []


        for role in roles[
            :roles_per_family
        ]:

            top_roles.append({

                "Career":
                    role[
                        "Career"
                    ],

                "Technical Fitness":
                    round(
                        role[
                            "Technical Fitness"
                        ],
                        1
                    ),

                "Stage Factor":
                    round(
                        role[
                            "Stage Factor"
                        ],
                        2
                    ),

                "Career Suitability":
                    round(
                        role[
                            "Career Suitability"
                        ],
                        1
                    ),

                "Family Type":
                    role[
                        "Family Type"
                    ],

                "Family Factor":
                    round(
                        role[
                            "Family Factor"
                        ],
                        2
                    ),

                "Family Adjusted Suitability":
                    round(
                        role[
                            "Family Adjusted Suitability"
                        ],
                        1
                    ),

                "Role Level":
                    role[
                        "Role Level"
                    ],

                "Matched Skills":
                    role[
                        "Matched Skills"
                    ],

                "Missing Skills":
                    role[
                        "Missing Skills"
                    ],

            })


        # --------------------------------------------------
        # SAVE FAMILY RESULT
        # --------------------------------------------------

        family_results.append({

            "Role Family":
                family,

            "Family Score":
                round(
                    family_score,
                    1
                ),

            "Best Role":
                best_role[
                    "Career"
                ],

            "Best Role Score":
                round(
                    best_role[
                        "Family Adjusted Suitability"
                    ],
                    1
                ),

            "Roles":
                top_roles,

        })


    # --------------------------------------------------
    # REMOVE EMPTY / ZERO FAMILIES
    # --------------------------------------------------

    family_results = [
        family
        for family in family_results
        if family[
            "Family Score"
        ] >= MIN_ROLE_SUITABILITY
    ]


    # --------------------------------------------------
    # SORT FAMILIES
    # --------------------------------------------------

    family_results.sort(
        key=lambda x: x[
            "Family Score"
        ],
        reverse=True
    )


    # --------------------------------------------------
    # RETURN TOP FAMILIES
    # --------------------------------------------------

    return family_results[
        :top_families
    ]


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


    test_stage = (
        "Student / Fresher"
    )


    recommendations = (
        recommend_career_families(
            test_skills,
            test_stage
        )
    )


    print(
        "=" * 60
    )

    print(
        "CAREER FAMILY RECOMMENDATIONS"
    )

    print(
        "=" * 60
    )

    print(
        f"Student Stage: "
        f"{test_stage}"
    )

    print()


    for index, family in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{index}. "
            f"{family['Role Family']} "
            f"→ "
            f"{family['Family Score']}%"
        )


        print(
            f"   Best Role: "
            f"{family['Best Role']} "
            f"("
            f"{family['Best Role Score']}"
            f"% suitability)"
        )


        print(
            "   Roles:"
        )


        for role in family[
            "Roles"
        ]:

            print(
                f"      - "
                f"{role['Career']} "
                f"(Technical: "
                f"{role['Technical Fitness']}%, "
                f"Suitability: "
                f"{role['Career Suitability']}%, "
                f"Family: "
                f"{role['Family Type']}, "
                f"Adjusted: "
                f"{role['Family Adjusted Suitability']}%) "
                f"[{role['Role Level']}]"
            )


        print()