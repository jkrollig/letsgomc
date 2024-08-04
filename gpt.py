from g4f.client import Client
from g4f.Provider import You, Bing


client = Client()

response = client.chat.completions.create(
    
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "You are a helpful assistant who gives fascinating facts about the given topics. You are very specialized in the given topics and you can provide really interesting facts that cannot be known by an average human. Now, your topic is ### Personal Finance ###. Write a transcript for a talk that will last around 40 seconds. Remember you are highly specialized in this topic and you will provide deeply fascinating, helpful interesting facts."}],
    
)


print(response.choices[0].message.content)