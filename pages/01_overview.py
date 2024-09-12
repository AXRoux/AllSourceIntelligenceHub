import streamlit as st
from streamlit_extras.colored_header import colored_header
import plotly.graph_objects as go

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

colored_header(
    label="Overview of All-Source Intelligence",
    description="Understanding the fundamentals",
    color_name="blue-70"
)

st.markdown("""
All-Source Intelligence is a comprehensive approach to intelligence analysis that combines information from multiple sources to provide a more complete and accurate picture of a situation or threat.

Key aspects of All-Source Intelligence include:
- Integration of various intelligence disciplines
- Critical thinking and analysis
- Consideration of diverse perspectives
- Identification of patterns and trends
""")

# Create a simple Sankey diagram to visualize the flow of information in All-Source Intelligence
def create_sankey_diagram():
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = ["OSINT", "HUMINT", "SIGINT", "GEOINT", "MASINT", "Analysis", "All-Source Intelligence"],
          color = "blue"
        ),
        link = dict(
          source = [0, 1, 2, 3, 4, 5],
          target = [5, 5, 5, 5, 5, 6],
          value = [1, 1, 1, 1, 1, 5]
      ))])

    fig.update_layout(title_text="Flow of Information in All-Source Intelligence", font_size=10)
    return fig

st.plotly_chart(create_sankey_diagram(), use_container_width=True)

st.markdown("""
The diagram above illustrates how different intelligence sources feed into the analysis process, 
which then culminates in All-Source Intelligence. This integrated approach allows for a more 
comprehensive understanding of complex situations and threats.
""")

if __name__ == "__main__":
    st.write("Overview page loaded successfully.")
