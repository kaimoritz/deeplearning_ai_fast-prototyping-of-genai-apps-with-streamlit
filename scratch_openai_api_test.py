import os
from dotenv import load_dotenv
import openai

load_dotenv(os.environ["dot_env"])

client=openai.OpenAI()
response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "user", "content": "Explain generative AI in one sentence"}
    ],
    temperature=0.7,
    max_output_tokens=100,
)

print(response)

print(response.output[0].content[0].text)
#print(response.output_text)

