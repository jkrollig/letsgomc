from together import Together
from science_topics import get_science_topic
from tts import generate_video_from_answer
from sbtnew import executor


together_client = Together(api_key="c884f94a32de7e896e1e0eba832db42c421273f4fdd1562472719c55bac0d8fe")


def update_cache(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Get the last number from the file
    if lines:
        last_number = int(lines[-1].strip())
    else:
        last_number = 0
    
    # Increment the last number by one
    new_number = last_number + 1
    
    # Write the new number to the file
    with open(file_path, 'a') as file:
        file.write(f"{new_number}\n")
        
    print(f"Added {new_number} to {file_path}")
    return new_number

# Usage
def main():
        
    file_path = 'cache_science.txt'
    day_number = update_cache(file_path)
    day_number = f"science/{day_number}"

    MAX_RETRIES = 4  # Define a maximum number of retries

    for number in range(1, 7):
        attempt = 0  # Initialize the retry attempt counter
        
        while attempt < MAX_RETRIES:
            selected_topic = get_science_topic()

            prompt = f"""You are a helpful assistant who gives facts about the given topics. You are very specialized in the given topics and you can provide really interesting facts that cannot be known by an average human. Now, your topic is {selected_topic}. Write a transcript for a video that will last around 40 seconds (maximum 140words). Remember you are highly specialized in this topic and you will provide deeply fascinating, helpful interesting facts.Dont use any starting sentences like "ladies and gentlemen" get straight into the point.start each transcript with a question thats both engaging and mysterius about the topic.Ask the viewer questions at the start of the transcript to engage with them and end it with a question to add mystery and tell them to comment down below. Avoid phrases like Here is the transcript or [transcript]"""

            response = together_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7,
                top_p=0.7,
                top_k=50,
                repetition_penalty=1,
            )

            transcript = response.choices[0].message.content
            print(f"Response {number} (Attempt {attempt + 1}):")
            print(transcript)

            if generate_video_from_answer(transcript, number, day_number):  # if it executes successfully
                executor(number, transcript, day_number)
                print(transcript)
                break  # Exit the while loop if successful
            else:
                print(transcript)
                print("1.25x Audio longer than 1min or shorter than 30s aborted mission")
                attempt += 1  # Increment the retry attempt counter

        if attempt == MAX_RETRIES:
            print(f"Failed to generate video for response {number} after {MAX_RETRIES} attempts.")

if __name__ == "__main__":
    main()