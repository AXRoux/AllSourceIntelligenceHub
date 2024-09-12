import streamlit as st
from streamlit_extras.colored_header import colored_header
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="ML Analysis", page_icon="🤖", layout="wide")

# Sample data (in a real scenario, this would be loaded from a database)
intelligence_reports = [
    ("Increased military activity observed near the border", "Threat"),
    ("Successful diplomatic talks concluded with neighboring country", "Opportunity"),
    ("Economic indicators show stable growth in the region", "Opportunity"),
    ("Cybersecurity threats on the rise in financial sector", "Threat"),
    ("New trade agreement signed, expected to boost exports", "Opportunity"),
    ("Environmental disaster affecting local communities", "Threat"),
    ("Peaceful protests lead to policy changes", "Neutral"),
    ("Tensions escalate in disputed territory", "Threat"),
    ("Breakthrough in renewable energy research announced", "Opportunity"),
    ("Food shortages reported in conflict-affected areas", "Threat"),
    ("Artificial intelligence advancements in defense sector", "Neutral"),
    ("International cooperation on climate change initiatives", "Opportunity"),
    ("Rise in cross-border smuggling activities", "Threat"),
    ("Medical research breakthrough in infectious diseases", "Opportunity"),
    ("Political instability following contested elections", "Threat")
]

# Prepare data
reports, classifications = zip(*intelligence_reports)

# Text preprocessing and vectorization
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(reports)
y = np.array(classifications)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Get feature importance
feature_importance = model.feature_importances_
feature_names = vectorizer.get_feature_names_out()

# Sort feature importance
sorted_idx = np.argsort(feature_importance)
sorted_features = feature_names[sorted_idx]
sorted_importance = feature_importance[sorted_idx]

# Streamlit interface
colored_header(
    label="Advanced Machine Learning Analysis for Intelligence",
    description="Random Forest classification and feature importance analysis",
    color_name="violet-70"
)

st.write("Enter an intelligence report for classification:")

# Text input for intelligence report
report = st.text_area("Intelligence Report", height=150)

# Classify button
if st.button("Classify"):
    if report:
        # Vectorize the input
        report_vec = vectorizer.transform([report])
        
        # Make prediction
        prediction = model.predict(report_vec)[0]
        probabilities = model.predict_proba(report_vec)[0]
        
        st.write(f"Predicted Classification: **{prediction}**")
        st.write("Probabilities:")
        for cls, prob in zip(model.classes_, probabilities):
            st.write(f"- {cls}: {prob:.2f}")
    else:
        st.write("Please enter a report to classify.")

# Feature Importance Visualization
st.subheader("Feature Importance Analysis")

top_n = 20  # Show top 20 features
top_features = sorted_features[-top_n:]
top_importance = sorted_importance[-top_n:]

fig = go.Figure(go.Bar(
    x=top_importance,
    y=top_features,
    orientation='h'
))

fig.update_layout(
    title="Top 20 Most Important Features",
    xaxis_title="Importance",
    yaxis_title="Feature",
    height=600
)

st.plotly_chart(fig)

st.write("""
The bar chart above shows the top 20 most important features (words or terms) that the Random Forest model 
uses to classify intelligence reports. Longer bars indicate higher importance in the classification process.

This analysis helps identify key terms that are most influential in determining whether a report is classified 
as a Threat, Opportunity, or Neutral.
""")

if __name__ == "__main__":
    st.write("ML Analysis page loaded successfully.")
