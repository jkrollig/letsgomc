import os
from together import Together

together_client = Together(api_key="c884f94a32de7e896e1e0eba832db42c421273f4fdd1562472719c55bac0d8fe")

import json

topics = [
    'Wealth'
]

base_prompt = (
    "You are a helpful assistant who gives facts about the given topics. You are very specialized in the given topics and you can provide really interesting facts that cannot be known by an average human. "
    "Now, your topic is '{topic}'. Write a transcript for a video that will last around 40 seconds. Remember you are highly specialized in this topic and you will provide deeply fascinating, helpful interesting facts. "
    "Don't use any starting sentences like 'ladies and gentlemen' get straight into the point. Start each transcript with sentences similar to 'Only 1 percent of people know this are you one of them?'. "
    "Ask the viewer questions at the start of the transcript to engage with them and end it with a question to add mystery and tell them to comment down below. Give only 1 fact about the topic. Remove the starting sentence 'Here is the transcript' "
)

prompts = [base_prompt.format(topic=topic) for topic in topics for _ in range(1)]

# Generating responses for each prompt
responses = []

for i, prompt in range(100):
    response = together_client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
                
    )
    print(f"Response {i+1}:")
    response_content = response.choices[0].message.content
    print(response_content)
    responses.append(response_content)

# Write all responses to a file
with open('ai_responses.txt', 'w') as file:
    for response in responses:
        file.write(response + "\n\n")
