import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Source Blending", page_icon="🔀", layout="wide")

colored_header(
    label="Matrix of Source Blending",
    description="Analyzing pros and cons of combining intelligence sources",
    color_name="orange-70"
)

st.markdown("""
Source blending is a critical aspect of All-Source Intelligence. By combining different intelligence sources, 
analysts can overcome the limitations of individual sources and create a more comprehensive understanding of 
complex situations. However, this process also comes with its own set of challenges.

Below is a matrix showcasing the pros and cons of blending different intelligence sources:
""")

# Define source blending matrix
blending_matrix = {
    "OSINT + HUMINT": {
        "pros": ["Enhanced context", "Verification of open-source data", "Cost-effective insights"],
        "cons": ["Potential bias reinforcement", "Overreliance on easily accessible information"]
    },
    "SIGINT + GEOINT": {
        "pros": ["Comprehensive situational awareness", "Corroboration of electronic and visual data"],
        "cons": ["Technical complexities", "High resource requirements"]
    },
    "HUMINT + SIGINT": {
        "pros": ["Validation of human source information", "Deeper insights into communications"],
        "cons": ["Ethical concerns", "Potential for conflicting information"]
    },
    "OSINT + GEOINT": {
        "pros": ["Improved geographical context", "Rapid initial assessments"],
        "cons": ["Misinterpretation of visual data", "Overemphasis on publicly visible features"]
    },
    "MASINT + SIGINT": {
        "pros": ["Advanced technical intelligence", "Unique signature identification"],
        "cons": ["Highly specialized analysis required", "Limited applicability in some scenarios"]
    }
}

# Create an interactive table
def create_blending_table():
    df = pd.DataFrame.from_dict(blending_matrix, orient='index')
    df['pros'] = df['pros'].apply(lambda x: '<br>'.join(x))
    df['cons'] = df['cons'].apply(lambda x: '<br>'.join(x))
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Source Combination', 'Pros', 'Cons'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.index, df.pros, df.cons],
                   fill_color='lavender',
                   align='left',
                   height=30))
    ])
    
    fig.update_layout(title="Source Blending Matrix")
    return fig

st.plotly_chart(create_blending_table(), use_container_width=True)

st.markdown("""
The matrix above illustrates some common source blending combinations and their associated pros and cons. 
It's important to note that the effectiveness of source blending depends on various factors, including:

1. The specific intelligence requirements
2. The availability and quality of sources
3. The expertise of analysts in integrating diverse information
4. The temporal and geographical context of the intelligence problem

Effective All-Source Intelligence requires a thoughtful approach to source blending, considering both the 
strengths and limitations of each combination to produce the most accurate and actionable intelligence products.
""")

if __name__ == "__main__":
    st.write("Source Blending page loaded successfully.")
