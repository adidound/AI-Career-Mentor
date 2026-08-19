import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career Mentor",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# LOAD CAREER DATA
# --------------------------------------------------

@st.cache_data
def load_career_data():
    return pd.read_csv("data/career_data.csv")


career_data = load_career_data()


# --------------------------------------------------
# CAREER RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend_careers(student_skills, career_data):

    student_skills = {
        skill.strip().lower()
        for skill in student_skills
        if skill.strip()
    }

    results = []

    for career in career_data["career"].unique():

        career_skills = set(
            career_data[
                career_data["career"] == career
            ]["skill"]
            .str.strip()
            .str.lower()
        )

        matched_skills = student_skills.intersection(career_skills)

        missing_skills = career_skills - student_skills

        if len(career_skills) > 0:
            match_percentage = (
                len(matched_skills) / len(career_skills)
            ) * 100
        else:
            match_percentage = 0

        results.append({
            "Career": career,
            "Match": round(match_percentage, 1),
            "Matched Skills": sorted(matched_skills),
            "Missing Skills": sorted(missing_skills)
        })

    results = sorted(
        results,
        key=lambda x: x["Match"],
        reverse=True
    )

    return results


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎓 AI Career Mentor")

st.markdown(
    """
    ### Personalized Career Guidance System

    Discover suitable career roles based on your **skills and interests**,
    identify your **skill gaps**, and understand what you should learn next.
    """
)

st.divider()


# --------------------------------------------------
# STUDENT PROFILE
# --------------------------------------------------

st.header("👤 Student Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    education = st.text_input(
        "Education",
        placeholder="e.g. B.Tech Computer Engineering"
    )


with col2:

    interests = st.text_input(
        "Career Interests",
        placeholder="e.g. Artificial Intelligence, Data Science"
    )

    skills_input = st.text_input(
        "Your Skills",
        placeholder="e.g. Python, SQL, Machine Learning, Pandas"
    )


st.divider()


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button(
    "🚀 Analyze My Career Profile",
    use_container_width=True
):

    if not name:
        st.warning("Please enter your name.")

    elif not skills_input:
        st.warning("Please enter at least one skill.")

    else:

        student_skills = skills_input.split(",")

        recommendations = recommend_careers(
            student_skills,
            career_data
        )


        # --------------------------------------------------
        # PROFILE SUMMARY
        # --------------------------------------------------

        st.success(
            f"Profile analyzed successfully for {name}!"
        )

        st.subheader("📋 Profile Summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.metric(
                "Skills",
                len([
                    s for s in student_skills
                    if s.strip()
                ])
            )

        with summary_col2:
            st.metric(
                "Career Areas",
                len(career_data["career"].unique())
            )

        with summary_col3:
            st.metric(
                "Top Match",
                f"{recommendations[0]['Match']}%"
            )


        # --------------------------------------------------
        # CAREER RECOMMENDATIONS
        # --------------------------------------------------

        st.divider()

        st.header("🎯 Recommended Career Paths")

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            career = recommendation["Career"]
            match = recommendation["Match"]

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.subheader(
                        f"{index}. {career}"
                    )

                with col2:

                    st.metric(
                        "Career Fit",
                        f"{match}%"
                    )


                # Matched skills
                matched = recommendation["Matched Skills"]

                if matched:

                    st.write(
                        "✅ **Matching Skills:** "
                        + ", ".join(
                            skill.title()
                            for skill in matched
                        )
                    )

                else:

                    st.write(
                        "✅ **Matching Skills:** None"
                    )


                # Missing skills

                missing = recommendation["Missing Skills"]

                if missing:

                    st.write(
                        "❌ **Skill Gaps:** "
                        + ", ".join(
                            skill.title()
                            for skill in missing
                        )
                    )


        # --------------------------------------------------
        # TOP CAREER ANALYSIS
        # --------------------------------------------------

        top_career = recommendations[0]

        st.divider()

        st.header(
            f"🔍 Detailed Analysis — {top_career['Career']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Skills You Already Have")

            for skill in top_career["Matched Skills"]:

                st.write(
                    f"✓ {skill.title()}"
                )


        with col2:

            st.subheader("📚 Skills You Need")

            for skill in top_career["Missing Skills"]:

                st.write(
                    f"→ {skill.title()}"
                )


        # --------------------------------------------------
        # EXPLANATION
        # --------------------------------------------------

        st.divider()

        st.header("💡 Why This Career?")

        st.write(
            f"**{top_career['Career']}** is currently the "
            f"highest-ranked career based on your existing "
            f"skill coverage."
        )

        st.write(
            f"You currently match "
            f"**{len(top_career['Matched Skills'])}** "
            f"of the required skills."
        )

        st.write(
            f"There are "
            f"**{len(top_career['Missing Skills'])}** "
            f"identified skills that you can develop "
            f"to improve your career fit."
        )