# import packages
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import openai
from dotenv import load_dotenv
import string

st.set_page_config(layout="wide")
load_dotenv(os.environ["dot_env"])
client = openai.OpenAI()

def get_dataset_path():
    """
    Returns the absolute path to the customer_reviews.csv dataset file.

    This function calculates the path relative to the current script location,
    navigating three directories up and then into the 'data' folder.

    Returns:
        str: The absolute file path to the dataset 'customer_reviews.csv'.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "..", "..", "data", "customer_reviews.csv")
    return csv_path

@st.cache_data
def get_sentiment(text):
    """
    Classify the sentiment of a given text using an LLM API.

    This function sends a request to the LLM client to classify the sentiment
    of the input text as one of three categories: Positive, Negative, or Neutral.
    It caches the result to avoid unnecessary API calls for repeated inputs.

    Args:
        text (str): The input text to classify the sentiment of.

    Returns:
        str: The sentiment classification ("Positive", "Negative", or "Neutral").

    Raises:
        Exception: Handles general exceptions during API call and returns "Neutral" on failure.
    """
    if not text or pd.isna(text):
        return "Neutral"
    try:
        response = client.responses.create(
            model="gpt-4o",  # Use the latest chat model
            input=[
                {"role": "system", "content": "Classify the sentiment of the following review as exactly one word: Positive, Negative, or Neutral."},
                {"role": "user", "content": f"What's the sentiment of this review? {text}"}
            ],
            temperature=0,  # Deterministic output
            max_output_tokens=100  # Limit response length
        )
        return response.output[0].content[0].text.strip()
    except Exception as e:
        st.error(f"API error: {e}")
        return "Neutral"

#if "df" not in st.session_state:
#    st.session_state.df = pd.DataFrame()

st.header("☕ GenAI Sentiment Analysis Dashboard")
st.write("This is your GenAI-powered data processing app.")

col1, col2, col3 = st.columns([1,1,5])
with col1:
    if st.button("📥 Load Dataset"):
        try:
            df = pd.read_csv(get_dataset_path())
            # st.session_state["df"] = df
            st.session_state["df"] = df.head(20) # for testing: reduce to 20 rows
            st.toast(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

        except FileNotFoundError:
            st.error("Dataset not found.")

with col2:
    if st.button("🔍 Analyze Sentiment"):
        if "df" in st.session_state:
            try:
                with st.spinner("Analyzing sentiment..."):
                    st.session_state["df"].loc[:, "Sentiment"] = st.session_state["df"]["SUMMARY"].apply(get_sentiment)
                    st.success("Sentiment analysis completed!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
        else:
            st.warning("Please ingest the dataset first.")

# Display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    st.subheader(f"📁 Reviews for {product}")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    # Visualization using Plotly if sentiment analysis has been performed
    if "Sentiment" in st.session_state["df"].columns:
        st.subheader(f"📊 Sentiment Breakdown for {product}")

        # Create Plotly bar chart for sentiment distribution using filtered data
        sentiment_counts = filtered_df["Sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']

        # Define custom order and colors
        sentiment_order = ['Negative', 'Neutral', 'Positive']
        sentiment_colors = {'Negative': 'red', 'Neutral': 'lightgray', 'Positive': 'green'}

        # Only include sentiment categories that actually exist in the data
        existing_sentiments = sentiment_counts['Sentiment'].unique()
        filtered_order = [s for s in sentiment_order if s in existing_sentiments]
        filtered_colors = {s: sentiment_colors[s] for s in existing_sentiments if s in sentiment_colors}

        # Reorder the data according to our custom order (only for existing sentiments)
        sentiment_counts['Sentiment'] = pd.Categorical(sentiment_counts['Sentiment'], categories=filtered_order,
                                                       ordered=True)
        sentiment_counts = sentiment_counts.sort_values('Sentiment')

        fig = px.bar(
            sentiment_counts,
            x="Sentiment",
            y="Count",
            title=f"Distribution of Sentiment Classifications - {product}",
            labels={"Sentiment": "Sentiment Category", "Count": "Number of Reviews"},
            color="Sentiment",
            color_discrete_map=filtered_colors
        )
        fig.update_layout(
            xaxis_title="Sentiment Category",
            yaxis_title="Number of Reviews",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)