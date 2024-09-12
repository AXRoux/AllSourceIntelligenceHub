import streamlit as st
from streamlit_extras.colored_header import colored_header
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Real-Time Intelligence", page_icon="🔄", layout="wide")

colored_header(
    label="Real-Time Intelligence Data Integration",
    description="Live feed of global events and potential intelligence reports",
    color_name="blue-70"
)

st.info('To enable real-time data fetching, please set up your NEWS_API_KEY in the secrets.toml file. You can get a free API key from https://newsapi.org/')

# Initialize session state variables
if 'api_calls' not in st.session_state:
    st.session_state.api_calls = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'cached_data' not in st.session_state:
    st.session_state.cached_data = None

# Function to fetch news data (simulating intelligence reports)
@st.cache_data(ttl=900)  # Cache for 15 minutes
def fetch_news_data():
    api_key = st.secrets.get('NEWS_API_KEY')
    if not api_key:
        st.warning('NEWS_API_KEY not found in secrets. Please set it up to enable real-time data fetching.')
        return None
    url = f"https://newsapi.org/v2/top-headlines?category=general&language=en&pageSize=10&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        st.session_state.api_calls += 1
        st.session_state.last_update = datetime.now()
        return response.json()['articles']
    else:
        st.error("Failed to fetch real-time data. Please check your API key and try again.")
        return None

# Display API call information
st.sidebar.write(f"API calls made today: {st.session_state.api_calls}")
if st.session_state.last_update:
    st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Manual refresh button
if st.sidebar.button("Refresh Data"):
    st.session_state.cached_data = None
    st.experimental_rerun()

# Fetch and display real-time data
st.subheader("Live Intelligence Feed")

if st.session_state.cached_data is None:
    data = fetch_news_data()
    if data:
        st.session_state.cached_data = data
else:
    data = st.session_state.cached_data

if data:
    df = pd.DataFrame(data)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df = df.sort_values('publishedAt', ascending=False)

    for _, row in df.iterrows():
        st.write(f"**Source:** {row['source']['name']}")
        st.write(f"**Title:** {row['title']}")
        st.write(f"**Description:** {row['description']}")
        st.write(f"**Published:** {row['publishedAt'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("---")

    # Analysis of data
    st.subheader("Data Analysis")
    st.write(f"Total number of reports: {len(df)}")
    st.write(f"Timespan of reports: {df['publishedAt'].min().strftime('%Y-%m-%d %H:%M:%S')} to {df['publishedAt'].max().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Source distribution
    source_counts = df['source'].apply(lambda x: x['name']).value_counts()
    st.write("Top Sources:")
    st.bar_chart(source_counts)

else:
    st.write("No data available. Please check your API connection and ensure the API key is set up correctly.")

# Display warning when approaching API limit
if st.session_state.api_calls > 90:  # Assuming a limit of 100 calls per day
    st.warning("Warning: Approaching daily API call limit. Please use the refresh button sparingly.")

if __name__ == "__main__":
    st.write("Real-Time Intelligence page loaded successfully.")
