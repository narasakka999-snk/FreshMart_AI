import streamlit as st

from services.db import (
    init_db,
    save_organisation,
    save_research,
    get_all_research,
    get_analysis
)

from services.research import research_web
from services.ai_engine import analyse_strategy, answer_question
from services.documents import extract_text


st.set_page_config(
    page_title="AI Transformation Strategy Intelligence",
    page_icon="🧠",
    layout="wide"
)

init_db()


st.title("🧠 AI Transformation Strategy Intelligence")

st.caption(
    "Business situation → External change → Strategic issues → "
    "Opportunities → Priorities → Initiatives → Outcomes"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "org_id" not in st.session_state:
    st.session_state.org_id = None

if "research" not in st.session_state:
    st.session_state.research = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None


tabs = st.tabs([
    "1. Organisation",
    "2. Research",
    "3. Strategy Intelligence",
    "4. Interrogate Findings"
])


# ---------------------------------------------------------
# 1. ORGANISATION
# ---------------------------------------------------------

with tabs[0]:

    st.subheader("Organisation information")

    with st.form("org_form"):

        name = st.text_input(
            "Organisation name",
            "FreshMart Retail Pvt Ltd"
        )

        industry = st.text_input(
            "Industry",
            "Retail"
        )

        situation = st.text_area(
            "Business situation",
            "Physical store sales are declining, inventory costs are increasing, "
            "and customers increasingly prefer digital shopping."
        )

        objectives = st.text_area(
            "Business objectives",
            "Increase revenue, reduce inventory costs, improve customer experience."
        )

        technology = st.text_area(
            "Current technology / data",
            "POS sales data, inventory system, customer loyalty data and an "
            "e-commerce website."
        )

        uploaded = st.file_uploader(
            "Optional organisation document",
            type=["txt", "pdf", "docx"]
        )

        submitted = st.form_submit_button(
            "Save Organisation"
        )


    if submitted:

        document_text = ""

        if uploaded:
            document_text = extract_text(uploaded)

        combined = (
            f"{situation}\n\n"
            f"Objectives:\n{objectives}\n\n"
            f"Technology:\n{technology}\n\n"
            f"Document:\n{document_text}"
        )

        st.session_state.org_id = save_organisation(
            name,
            industry,
            combined
        )

        # Reset current session data for the new organisation.
        st.session_state.research = []
        st.session_state.analysis = None

        st.success(
            "Organisation information stored successfully."
        )


# ---------------------------------------------------------
# 2. RESEARCH
# ---------------------------------------------------------

with tabs[1]:

    st.subheader("External research")

    st.write(
        "Research should be based on the organisation's industry "
        "and transformation situation."
    )

    query = st.text_input(
        "Research query",
        "retail transformation AI demand forecasting omnichannel customer experience"
    )

    if st.button("🔎 Research external information"):

        with st.spinner("Researching..."):

            results = research_web(query)

            st.session_state.research = results

            if st.session_state.org_id:

                for item in results:
                    save_research(
                        st.session_state.org_id,
                        item
                    )

            st.success(
                f"Collected {len(results)} research items."
            )


    # If research is not currently in session, load it from SQLite.
    if not st.session_state.research and st.session_state.org_id:

        st.session_state.research = get_all_research(
            st.session_state.org_id
        )


    if st.session_state.research:

        for i, item in enumerate(
            st.session_state.research,
            1
        ):

            with st.expander(
                f"{i}. {item.get('title', 'Research finding')}"
            ):

                st.write(
                    item.get("summary", "")
                )

                url = item.get("url", "")

                if url:
                    st.markdown(
                        f"**Source:** [{url}]({url})"
                    )


# ---------------------------------------------------------
# 3. STRATEGY INTELLIGENCE
# ---------------------------------------------------------

with tabs[2]:

    st.subheader(
        "Generate transformation intelligence"
    )

    if not st.session_state.org_id:

        st.warning(
            "Save an organisation first."
        )

    else:

        if st.button(
            "🚀 Analyse transformation opportunities",
            type="primary"
        ):

            with st.spinner(
                "Analysing business situation, evidence and opportunities..."
            ):

                stored_research = get_all_research(
                    st.session_state.org_id
                )

                st.session_state.analysis = analyse_strategy(
                    st.session_state.org_id,
                    stored_research
                )


        # -------------------------------------------------
        # Load saved analysis after restart
        # -------------------------------------------------

        if not st.session_state.analysis:

            saved_analysis = get_analysis(
                st.session_state.org_id
            )

            if saved_analysis:

                st.session_state.analysis = saved_analysis

                st.info(
                    "Previously generated strategy intelligence "
                    "was loaded from the database."
                )


        # -------------------------------------------------
        # DISPLAY ANALYSIS
        # -------------------------------------------------

        if st.session_state.analysis:

            a = st.session_state.analysis


            st.markdown(
                "### Strategic diagnosis"
            )

            st.write(
                a.get("diagnosis", "")
            )


            st.markdown(
                "### Strategic issues"
            )

            for x in a.get(
                "strategic_issues",
                []
            ):

                st.markdown(
                    f"**{x.get('issue', '')}** — "
                    f"{x.get('why', '')}"
                )

                st.caption(
                    "Evidence: "
                    + "; ".join(
                        x.get("evidence", [])
                    )
                )


            st.markdown(
                "### Transformation opportunities"
            )

            for x in a.get(
                "opportunities",
                []
            ):

                st.markdown(
                    f"**{x.get('name', '')}** — "
                    f"{x.get('rationale', '')}"
                )


            st.markdown(
                "### Priorities"
            )

            for x in a.get(
                "priorities",
                []
            ):

                st.markdown(
                    f"**#{x.get('rank', '')} "
                    f"{x.get('opportunity', '')}** — "
                    f"Impact {x.get('impact', '')}/10 | "
                    f"Urgency {x.get('urgency', '')}/10 | "
                    f"Effort {x.get('effort', '')}/10"
                )


            st.markdown(
                "### First initiatives"
            )

            for x in a.get(
                "initiatives",
                []
            ):

                st.markdown(
                    f"- **{x.get('initiative', '')}** — "
                    f"{x.get('purpose', '')}"
                )


            st.markdown(
                "### Expected outcomes"
            )

            for x in a.get(
                "outcomes",
                []
            ):

                st.markdown(
                    f"- {x}"
                )


# ---------------------------------------------------------
# 4. INTERROGATE FINDINGS
# ---------------------------------------------------------

with tabs[3]:

    st.subheader(
        "Interrogate findings"
    )

    question = st.text_input(
        "Ask a question",
        "What should this organisation transform, why, "
        "what evidence supports it, and what should be done first?"
    )


    if st.button("Ask AI"):

        if not st.session_state.analysis:

            # Try loading persisted intelligence.
            if st.session_state.org_id:

                st.session_state.analysis = get_analysis(
                    st.session_state.org_id
                )


        if not st.session_state.analysis:

            st.warning(
                "Generate the strategy intelligence first."
            )

        else:

            with st.spinner(
                "Answering from the application's stored intelligence..."
            ):

                answer = answer_question(
                    question,
                    st.session_state.analysis
                )

            st.markdown(answer)