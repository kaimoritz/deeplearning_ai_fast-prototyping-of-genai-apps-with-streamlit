import os
from dotenv import load_dotenv
import openai
import streamlit as st

# load environment variables
load_dotenv(os.environ["dot_env"])

# init openai client
client=openai.OpenAI()

st.title("Hello GenAI!")
st.write("This is your first streamlit appp.")


response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": "Explain generative AI in one sentence"}
    ],
    temperature=0.7,
    max_output_tokens=100,
)

st.write(response.output_text)

# => streamlit run M1L2V3_streamlit_chat.py