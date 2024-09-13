import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go

st.set_page_config(page_title="All-Source Intelligence", page_icon="🕵️", layout="wide")

# Add logo (replace with actual logo URL when available)
add_logo("https://example.com/logo.png", height=100)

# Main page header
colored_header(
    label="All-Source Intelligence Dashboard",
    description="Comprehensive analysis and insights",
    color_name="red-70"
)

# Introduction
st.markdown("""
Welcome to the All-Source Intelligence Dashboard. This application provides an in-depth look into the world of intelligence analysis, offering comprehensive insights and tools for analysts and policymakers.
""")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Active Sources", value="5", delta="1")
col2.metric(label="Reports Analyzed", value="1,234", delta="23")
col3.metric(label="Threat Level", value="Moderate", delta="↓")
col4.metric(label="Confidence Score", value="85%", delta="3%")
style_metric_cards()

# Intelligence Overview
st.subheader("Intelligence Overview")
fig = go.Figure(data=[go.Pie(labels=['OSINT', 'HUMINT', 'SIGINT', 'GEOINT', 'MASINT'],
                             values=[30, 20, 25, 15, 10])])
fig.update_layout(title="Distribution of Intelligence Sources")
st.plotly_chart(fig, use_container_width=True)

# Recent Alerts
st.subheader("Recent Alerts")
alerts = [
    {"severity": "High", "message": "Cybersecurity threat detected in financial sector"},
    {"severity": "Medium", "message": "Political unrest reported in Region A"},
    {"severity": "Low", "message": "Economic indicators show positive growth in target market"}
]
for alert in alerts:
    st.warning(f"**{alert['severity']}:** {alert['message']}")

# Quick Navigation
st.subheader("Quick Navigation")
col1, col2, col3 = st.columns(3)

def navigate_to_page(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

with col1:
    if st.button("View Detailed Reports"):
        navigate_to_page("Overview")
with col2:
    if st.button("Run ML Analysis"):
        navigate_to_page("ML Analysis")
with col3:
    if st.button("Access Real-Time Intel"):
        navigate_to_page("Real-Time Intelligence")

st.sidebar.success("Select a page above for detailed analysis.")

if __name__ == "__main__":
    st.write("Main dashboard loaded successfully.")
