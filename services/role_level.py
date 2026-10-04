import pandas as pd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

ROLE_WEIGHTS_PATH = "data/role_skill_weights.csv"

OUTPUT_PATH = "data/role_level_mapping.csv"


# --------------------------------------------------
# ROLE LEVEL CLASSIFICATION
# --------------------------------------------------
def classify_role_level(role_title):

    title = str(role_title).strip().lower()

    # --------------------------------------------------
    # EXECUTIVE
    # --------------------------------------------------

    executive_titles = {
        "chief technology officer",
        "chief technology officer (cto)",
        "chief information officer",
        "chief information officer (cio)",
    }

    if title in executive_titles:
        return "Executive"

    # --------------------------------------------------
    # DIRECTOR
    # --------------------------------------------------

    # Organizational/business directors
    # Technical/artistic "director" titles are not
    # automatically considered executive.
    director_keywords = [
        "director business systems",
        "director of engineering",
        "director of security",
        "information management systems director",
        "implementation director",
        "integration director",
        "it director",
        "it program engagement director",
        "it sales director",
    ]

    if title in director_keywords:
        return "Director"

    # --------------------------------------------------
    # PRINCIPAL
    # --------------------------------------------------

    if (
        title.startswith("principal ")
        or title.startswith("principle ")
    ):
        return "Principal"

    # --------------------------------------------------
    # MANAGER
    # --------------------------------------------------

    if "manager" in title:
        return "Manager"

    # --------------------------------------------------
    # LEAD
    # --------------------------------------------------

    if "lead" in title:
        return "Lead"

    # --------------------------------------------------
    # SENIOR
    # --------------------------------------------------

    if (
        title.startswith("senior ")
        or title.startswith("sr. ")
        or title.startswith("sr ")
    ):
        return "Senior"

    # --------------------------------------------------
    # ENTRY LEVEL
    # --------------------------------------------------

    if (
        title.startswith("entry level ")
        or title.startswith("new grad ")
    ):
        return "Entry"

    # --------------------------------------------------
    # JUNIOR
    # --------------------------------------------------

    if (
        title.startswith("junior ")
        or title.startswith("jr ")
        or title.startswith("jr. ")
    ):
        return "Junior"

    # --------------------------------------------------
    # UNSPECIFIED
    # --------------------------------------------------

    return "Unspecified"
# --------------------------------------------------
# LOAD ROLES
# --------------------------------------------------

df = pd.read_csv(
    ROLE_WEIGHTS_PATH
)


# --------------------------------------------------
# GET UNIQUE ROLES
# --------------------------------------------------

roles = (
    df[
        ["normalized_title"]
    ]
    .drop_duplicates()
    .copy()
)


# --------------------------------------------------
# CLASSIFY ROLE LEVEL
# --------------------------------------------------

roles["role_level"] = (
    roles["normalized_title"]
    .apply(classify_role_level)
)


# --------------------------------------------------
# SAVE
# --------------------------------------------------

roles.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("=" * 60)
print("ROLE LEVEL CLASSIFICATION")
print("=" * 60)

print(
    f"Total normalized roles : "
    f"{len(roles)}"
)

print()

print(
    roles["role_level"]
    .value_counts()
    .to_string()
)

print()

print(
    f"Saved to: {OUTPUT_PATH}"
)