import os
from dotenv import load_dotenv
import openai
import streamlit as st

@st.cache_data
def get_response(user_prompt, temperature):
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_output_tokens=100,
    )
    return response.output_text


# load environment variables
load_dotenv(os.environ["dot_env"])

# init openai client
client=openai.OpenAI()

st.title("Hello GenAI!")
st.write("This is your first streamlit appp.")

# add a text input box for the user prompt
user_prompt = st.text_input("Enter your prompt", "Explain generative AI in one sentence.")

# add a slider for temperature
temperature = st.slider(
    "Model temperature:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01,
    help="Controls randomness: 0=deterministic, 1=very creative",
)
with st.spinner("AI is working...."):
    # call the model
    response = get_response(user_prompt, temperature)
    # print the response from openai
    st.write(response)

# => streamlit run M1L2V3_streamlit_chat.py