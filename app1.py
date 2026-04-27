import streamlit as st

st.set_page_config(
    page_title="Churn Pattern",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

pg = st.navigation(
    [
        st.Page(
            "pages/dashboard1.py",
            title="Showcase",
            icon=":material/dashboard:",
            default=True,
        )
    ]
)
pg.run()
