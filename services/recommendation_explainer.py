from collections import Counter


# --------------------------------------------------
# SKILL GROUPS
# --------------------------------------------------
#
# These groups are used only for presentation.
# They DO NOT change scoring or recommendation logic.
# --------------------------------------------------

SKILL_GROUPS = {

    "Algorithms & Algorithm Design": {
        "algorithms",
        "algorithm design",
        "ai/ml algorithms",
        "nlp algorithms",
    },

    "Data Analysis": {
        "data analysis",
        "data analytics",
        "data wrangling",
    },

    "Statistics": {
        "statistics",
        "statistical analysis",
        "statistical modeling",
    },

    "Machine Learning": {
        "machine learning",
        "deep learning",
        "neural networks",
        "computer vision",
        "natural language processing",
    },

    "Cloud Computing": {
        "cloud computing",
        "cloud platforms",
        "aws",
        "azure",
        "gcp",
    },

    "DevOps & CI/CD": {
        "ci/cd",
        "ci/cd pipelines",
        "automation",
        "scripting",
        "jenkins",
        "docker",
        "kubernetes",
        "terraform",
        "ansible",
    },

    "Software Development": {
        "software development",
        "software design",
        "programming",
        "data structures",
        "git",
        "java",
        "python",
        "javascript",
        "c++",
    },

    "Model Deployment": {
        "model deployment",
        "deployment",
        "model serving",
        "mlops",
    },

    "Research": {
        "research methods",
        "scientific writing",
        "publications",
        "research",
    },

    "Database & Data Engineering": {
        "database development",
        "database design",
        "data modeling",
        "etl",
        "etl processes",
        "sql",
        "sql server",
        "oracle database",
    },

}


# --------------------------------------------------
# NORMALIZE SKILL LIST
# --------------------------------------------------

def normalize_skill_list(skills):
    """
    Convert a skill value into a clean unique list.

    Supports:
        - list
        - tuple
        - comma-separated string
        - pipe-separated string
    """

    if skills is None:
        return []


    if isinstance(
        skills,
        (list, tuple)
    ):

        values = skills

    else:

        text = str(
            skills
        ).strip()


        if (
            not text
            or text.lower() == "nan"
        ):

            return []


        if "|" in text:

            values = text.split("|")

        elif "," in text:

            values = text.split(",")

        else:

            values = [text]


    cleaned = []
    seen = set()


    for skill in values:

        skill = str(
            skill
        ).strip()


        if not skill:

            continue


        key = skill.lower()


        if key in seen:

            continue


        seen.add(key)

        cleaned.append(
            skill
        )


    return cleaned


# --------------------------------------------------
# FIND SKILL GROUP
# --------------------------------------------------

def find_skill_group(
    skill
):
    """
    Return the presentation group for a skill.

    If no group exists, return None.
    """

    skill_key = (
        str(skill)
        .strip()
        .lower()
    )


    for group_name, group_skills in (
        SKILL_GROUPS.items()
    ):

        if skill_key in group_skills:

            return group_name


    return None


# --------------------------------------------------
# COLLECT MATCHED SKILLS
# --------------------------------------------------

def collect_matched_skills(
    roles
):
    """
    Collect unique skills that the student already has.
    """

    matched = []
    seen = set()


    for role in roles:

        skills = normalize_skill_list(
            role.get(
                "Matched Skills",
                []
            )
        )


        for skill in skills:

            key = skill.lower()


            if key not in seen:

                seen.add(key)

                matched.append(
                    skill
                )


    return matched


# --------------------------------------------------
# COLLECT RAW MISSING SKILLS
# --------------------------------------------------

def collect_missing_skill_data(
    roles
):
    """
    Collect missing skills from recommended roles.

    Each skill stores:
        - frequency
        - role relevance
        - original display name
    """

    skill_data = {}


    for role_index, role in enumerate(
        roles
    ):

        missing = normalize_skill_list(
            role.get(
                "Missing Skills",
                []
            )
        )


        # Higher-ranked roles receive more weight.
        role_factor = (
            1.0 /
            (role_index + 1)
        )


        for skill in missing:

            key = skill.lower()


            if key not in skill_data:

                skill_data[key] = {

                    "display":
                        skill,

                    "count":
                        0,

                    "relevance":
                        0.0,

                }


            skill_data[
                key
            ][
                "count"
            ] += 1


            skill_data[
                key
            ][
                "relevance"
            ] += role_factor


    return skill_data


# --------------------------------------------------
# GROUP MISSING SKILLS
# --------------------------------------------------

def group_missing_skills(
    roles
):
    """
    Convert individual missing skills into
    higher-level learning targets.

    Example:

        algorithms
        algorithm design
        ai/ml algorithms

    becomes:

        Algorithms & Algorithm Design
    """

    skill_data = (
        collect_missing_skill_data(
            roles
        )
    )


    grouped = {}


    # --------------------------------------------------
    # PROCESS KNOWN GROUPS
    # --------------------------------------------------

    for group_name, group_skills in (
        SKILL_GROUPS.items()
    ):

        group_count = 0
        group_relevance = 0.0
        source_skills = []


        for skill_key, data in (
            skill_data.items()
        ):

            if skill_key in group_skills:

                group_count += (
                    data["count"]
                )

                group_relevance += (
                    data["relevance"]
                )

                source_skills.append(
                    data["display"]
                )


        if group_count > 0:

            grouped[
                group_name
            ] = {

                "count":
                    group_count,

                "relevance":
                    group_relevance,

                "source_skills":
                    source_skills,

            }


    # --------------------------------------------------
    # KEEP UNGROUPED SKILLS
    # --------------------------------------------------

    grouped_skill_keys = set()


    for group_skills in (
        SKILL_GROUPS.values()
    ):

        grouped_skill_keys.update(
            group_skills
        )


    for skill_key, data in (
        skill_data.items()
    ):

        if skill_key in grouped_skill_keys:

            continue


        grouped[
            data["display"]
        ] = {

            "count":
                data["count"],

            "relevance":
                data["relevance"],

            "source_skills":
                [
                    data["display"]
                ],

        }


    return grouped


# --------------------------------------------------
# PRIORITIZE LEARNING TARGETS
# --------------------------------------------------

def collect_missing_skills(
    roles,
    max_skills=8
):
    """
    Return prioritized learning targets.

    Priority is based on:
        1. How often the skill/group is missing.
        2. How relevant it is across recommended roles.
    """

    grouped = group_missing_skills(
        roles
    )


    ranked = sorted(
        grouped.items(),
        key=lambda item: (
            -item[1]["count"],
            -item[1]["relevance"],
            item[0].lower()
        )
    )


    return [
        group_name
        for group_name, _
        in ranked[:max_skills]
    ]


# --------------------------------------------------
# BUILD ONE FAMILY EXPLANATION
# --------------------------------------------------

def explain_family(
    family_result,
    max_development_skills=8
):
    """
    Convert one family recommendation into
    UI-ready explanation data.
    """

    family_name = (
        family_result.get(
            "Role Family",
            ""
        )
    )


    family_score = float(
        family_result.get(
            "Family Score",
            0
        )
    )


    best_role = (
        family_result.get(
            "Best Role",
            ""
        )
    )


    best_role_score = float(
        family_result.get(
            "Best Role Score",
            0
        )
    )


    roles = (
        family_result.get(
            "Roles",
            []
        )
    )


    # --------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------

    matched_skills = (
        collect_matched_skills(
            roles
        )
    )


    # --------------------------------------------------
    # PRIORITIZED SKILL GAPS
    # --------------------------------------------------

    skills_to_develop = (
        collect_missing_skills(
            roles,
            max_development_skills
        )
    )


    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    return {

        "Role Family":
            family_name,

        "Skill Alignment":
            round(
                family_score,
                1
            ),

        "Best Role":
            best_role,

        "Best Role Score":
            round(
                best_role_score,
                1
            ),

        "Why It Fits":
            matched_skills,

        "Skills To Develop":
            skills_to_develop,

    }


# --------------------------------------------------
# BUILD ALL EXPLANATIONS
# --------------------------------------------------

def explain_recommendations(
    family_results,
    max_development_skills=8
):
    """
    Convert recommendation-engine output
    into user-facing explanation data.
    """

    if not family_results:

        return []


    explanations = []


    for family_result in family_results:

        explanation = explain_family(
            family_result,
            max_development_skills
        )


        explanations.append(
            explanation
        )


    return explanations


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

def print_explanations(
    explanations
):

    print(
        "=" * 60
    )

    print(
        "CAREER RECOMMENDATION EXPLANATIONS"
    )

    print(
        "=" * 60
    )


    for index, explanation in enumerate(
        explanations,
        start=1
    ):

        print()

        print(
            f"{index}. "
            f"{explanation['Role Family']} "
            f"→ "
            f"{explanation['Skill Alignment']}%"
        )


        print(
            f"   Best Role: "
            f"{explanation['Best Role']} "
            f"("
            f"{explanation['Best Role Score']}%"
            f")"
        )


        print()

        print(
            "   Why It Fits:"
        )


        for skill in explanation[
            "Why It Fits"
        ]:

            print(
                f"      ✓ {skill}"
            )


        print()

        print(
            "   Skills To Develop:"
        )


        for skill in explanation[
            "Skills To Develop"
        ]:

            print(
                f"      → {skill}"
            )


        print()


# --------------------------------------------------
# TEST WITH REAL RECOMMENDATION ENGINE
# --------------------------------------------------

if __name__ == "__main__":

    from services.recommendation_engine import (
        recommend_career_families
    )


    # --------------------------------------------------
    # TEST STUDENT
    # --------------------------------------------------

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


    # --------------------------------------------------
    # GET REAL RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = (
        recommend_career_families(
            test_skills,
            test_stage
        )
    )


    # --------------------------------------------------
    # GENERATE EXPLANATIONS
    # --------------------------------------------------

    explanations = (
        explain_recommendations(
            recommendations
        )
    )


    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    print(
        f"Student Stage: "
        f"{test_stage}"
    )

    print()


    print_explanations(
        explanations
    )