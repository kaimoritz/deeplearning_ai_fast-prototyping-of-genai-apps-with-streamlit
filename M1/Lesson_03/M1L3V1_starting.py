# import packages
import streamlit as st
import pandas as pd
import re
import os
import string

from matplotlib import pyplot as plt


# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "..", "..", "data", "customer_reviews.csv")
    return csv_path

def clean_text(text):
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    # Lowercase
    text = text.lower()
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

# Layout two buttons side by side
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Ingest Dataset"):
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.toast("Dataset loaded successfully!", icon="✅")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the path.")
with col2:
    if st.button("🧹 Parse  Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.toast("Dataset parsed and cleaned successfully!")
        else:
            st.warning("Pleas ingest the dataset first.")

# display the dataset if it exists in the session state
if "df" in st.session_state:
    st.subheader("Dataset Preview")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]

    st.dataframe(filtered_df)

    # visualisation
    # built-in
    st.subheader("Sentiment Score by Product (built-in streamlit plotting)")
    grouped = st.session_state["df"].groupby(["PRODUCT"])["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)


