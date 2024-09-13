import streamlit as st
from streamlit_extras.colored_header import colored_header
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real-Time Intelligence", page_icon="🔄", layout="wide")

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

# Function to create a word cloud
def create_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# Initialize session state variables
if 'api_calls' not in st.session_state:
    st.session_state.api_calls = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'cached_data' not in st.session_state:
    st.session_state.cached_data = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Main layout
st.sidebar.title("Controls")
dark_mode = st.sidebar.checkbox("Dark Mode")
if dark_mode:
    st.markdown("<style>body {color: white; background-color: #1E1E1E;}</style>", unsafe_allow_html=True)

search_term = st.sidebar.text_input("Search Reports")

# Display API call information
st.sidebar.write(f"API calls made today: {st.session_state.api_calls}")
if st.session_state.last_update:
    st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Manual refresh button
if st.sidebar.button("Refresh Data"):
    st.session_state.cached_data = None
    st.experimental_rerun()

colored_header(
    label="Real-Time Intelligence Data Integration",
    description="Live feed of global events and potential intelligence reports",
    color_name="blue-70"
)

col1, col2 = st.columns([3, 2])

with col1:
    colored_header(label="Live Intelligence Feed", description="Real-time updates of global events", color_name="blue-70")
    live_feed = st.empty()

with col2:
    colored_header(label="Data Analysis", description="Insights from intelligence reports", color_name="green-70")
    analysis_section = st.empty()

# Fetch and display data
with st.spinner("Fetching real-time intelligence data..."):
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

    # Filter data based on search term
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False) | df['description'].str.contains(search_term, case=False)]

    # Display live feed
    with live_feed.container():
        for _, row in df.iterrows():
            with st.expander(row['title'], expanded=True):
                st.markdown(f"**Source:** {row['source']['name']}")
                st.markdown(f"**Description:** {row['description']}")
                st.markdown(f"**Published:** {row['publishedAt'].strftime('%Y-%m-%d %H:%M:%S')}")
                if st.button("⭐ Favorite", key=row['title']):
                    if row['title'] not in st.session_state.favorites:
                        st.session_state.favorites.append(row['title'])
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")

    # Display data analysis
    with analysis_section.container():
        st.metric("Total Reports", len(df))
        
        # Source distribution (Updated as requested)
        source_counts = df['source'].apply(lambda x: x['name']).value_counts().reset_index()
        source_counts.columns = ['source', 'count']
        fig_sources = px.bar(source_counts, x='source', y='count', title="Top Sources")
        st.plotly_chart(fig_sources, use_container_width=True)

        # Report frequency over time
        fig_timeline = px.line(df.groupby(df['publishedAt'].dt.date).size().reset_index(name='count'), 
                               x='publishedAt', y='count', title="Report Frequency")
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Word cloud
        if len(df) > 0:
            word_cloud_text = ' '.join(df['title'])
            st.pyplot(create_word_cloud(word_cloud_text))

else:
    st.write("No data available. Please check your API connection and ensure the API key is set up correctly.")

# Display warning when approaching API limit
if st.session_state.api_calls > 90:  # Assuming a limit of 100 calls per day
    st.warning("Warning: Approaching daily API call limit. Please use the refresh button sparingly.")

# Display favorites
st.sidebar.subheader("Favorites")
for favorite in st.session_state.favorites:
    st.sidebar.write(favorite)

if __name__ == "__main__":
    st.sidebar.success("Real-Time Intelligence page loaded successfully.")
