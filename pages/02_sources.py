import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Intelligence Sources", page_icon="🔍", layout="wide")

colored_header(
    label="Intelligence Sources and Their Limitations",
    description="Exploring various intelligence disciplines",
    color_name="green-70"
)

# Define intelligence sources and their characteristics
sources = {
    "OSINT": {
        "full_name": "Open-Source Intelligence",
        "description": "Collected from publicly available sources",
        "pros": ["Widely accessible", "Cost-effective", "Timely"],
        "cons": ["Information overload", "Reliability concerns", "Deception/misinformation"]
    },
    "HUMINT": {
        "full_name": "Human Intelligence",
        "description": "Gathered from human sources",
        "pros": ["Unique insights", "Context-rich", "Can answer specific questions"],
        "cons": ["Time-consuming", "Risk to sources", "Potential for deception"]
    },
    "SIGINT": {
        "full_name": "Signals Intelligence",
        "description": "Intercepted signals and communications",
        "pros": ["Real-time information", "Wide coverage", "Objective data"],
        "cons": ["Technical challenges", "Legal and ethical concerns", "Encryption barriers"]
    },
    "GEOINT": {
        "full_name": "Geospatial Intelligence",
        "description": "Exploitation and analysis of imagery and geospatial information",
        "pros": ["Visual evidence", "Wide area coverage", "Objective data"],
        "cons": ["Weather dependent", "Limited temporal resolution", "Interpretation challenges"]
    },
    "MASINT": {
        "full_name": "Measurement and Signature Intelligence",
        "description": "Scientific and technical intelligence from sensor data",
        "pros": ["Highly technical data", "Difficult to deceive", "Unique signatures"],
        "cons": ["Specialized equipment needed", "Complex analysis", "Limited applicability"]
    }
}

# Create a dataframe for easier visualization
df = pd.DataFrame.from_dict(sources, orient='index')

# Display each source with an expander
for source, info in sources.items():
    with st.expander(f"{source} - {info['full_name']}"):
        st.write(f"**Description:** {info['description']}")
        st.write("**Pros:**")
        for pro in info['pros']:
            st.write(f"- {pro}")
        st.write("**Cons:**")
        for con in info['cons']:
            st.write(f"- {con}")

# Create a radar chart to compare sources
def create_radar_chart():
    categories = ['Accessibility', 'Reliability', 'Timeliness', 'Cost-Effectiveness', 'Uniqueness']
    fig = go.Figure()

    for source in sources.keys():
        fig.add_trace(go.Scatterpolar(
            r=[4, 3, 5, 4, 2] if source == "OSINT" else  # Example values, adjust as needed
              [2, 4, 3, 2, 5] if source == "HUMINT" else
              [3, 4, 5, 3, 4] if source == "SIGINT" else
              [3, 4, 3, 3, 4] if source == "GEOINT" else
              [2, 5, 3, 2, 5],
            theta=categories,
            fill='toself',
            name=source
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="Comparison of Intelligence Sources"
    )
    return fig

st.plotly_chart(create_radar_chart(), use_container_width=True)

st.markdown("""
The radar chart above provides a visual comparison of different intelligence sources across various attributes. 
This helps in understanding the strengths and weaknesses of each source, emphasizing the importance of 
using multiple sources in All-Source Intelligence.

---

For more information on the principles and practices of All-Source Intelligence, check out the 
[All-Source Intelligence Manifesto](https://medium.com/dead-drop/the-all-source-intelligence-analyst-manifesto-8f19f6e23e7c).
""")

if __name__ == "__main__":
    st.write("Sources page loaded successfully.")
