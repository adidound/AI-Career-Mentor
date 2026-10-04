# --------------------------------------------------
# CAREER STAGE DEFINITIONS
# --------------------------------------------------

CAREER_STAGES = [
    "Student / Fresher",
    "Early Career",
    "Experienced Professional",
]


# --------------------------------------------------
# GET STAGE FACTOR
# --------------------------------------------------

def get_stage_factor(
    student_stage,
    role_level
):

    # --------------------------------------------------
    # STUDENT / FRESHER
    # --------------------------------------------------

    if student_stage == "Student / Fresher":

        factors = {
            "Entry": 1.00,
            "Junior": 1.00,
            "Unspecified": 0.95,
            "Senior": 0.80,
            "Lead": 0.70,
            "Manager": 0.60,
            "Director": 0.50,
            "Principal": 0.45,
            "Executive": 0.35,
        }

        return factors.get(
            role_level,
            0.95
        )


    # --------------------------------------------------
    # EARLY CAREER
    # --------------------------------------------------

    if student_stage == "Early Career":

        factors = {
            "Entry": 0.95,
            "Junior": 1.00,
            "Unspecified": 1.00,
            "Senior": 0.90,
            "Lead": 0.80,
            "Manager": 0.70,
            "Director": 0.60,
            "Principal": 0.55,
            "Executive": 0.40,
        }

        return factors.get(
            role_level,
            1.00
        )


    # --------------------------------------------------
    # EXPERIENCED PROFESSIONAL
    # --------------------------------------------------

    if student_stage == "Experienced Professional":

        factors = {
            "Entry": 0.85,
            "Junior": 0.90,
            "Unspecified": 1.00,
            "Senior": 1.00,
            "Lead": 1.00,
            "Manager": 1.00,
            "Director": 0.95,
            "Principal": 0.95,
            "Executive": 0.90,
        }

        return factors.get(
            role_level,
            1.00
        )


    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    return 1.00