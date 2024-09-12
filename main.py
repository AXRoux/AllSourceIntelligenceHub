import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="All-Source Intelligence", page_icon="🕵️", layout="wide")

# Add logo (replace with actual logo URL when available)
add_logo("https://example.com/logo.png", height=100)

# Main page header
colored_header(
    label="All-Source Intelligence Dashboard",
    description="Exploring the world of intelligence analysis",
    color_name="red-70"
)

st.markdown("""
Welcome to the All-Source Intelligence Dashboard. This application provides an in-depth look into the world of intelligence analysis, focusing on:

- Overview of All-Source Intelligence
- Various intelligence sources and their limitations
- Source blending techniques and their pros and cons
- Bridging the gap between analysts and policymakers
- Advanced machine learning analysis for intelligence reports, including Random Forest classification and feature importance

Navigate through the pages using the sidebar to explore each topic in detail.
""")

st.sidebar.success("Select a page above.")

if __name__ == "__main__":
    st.write("Main page loaded successfully.")
