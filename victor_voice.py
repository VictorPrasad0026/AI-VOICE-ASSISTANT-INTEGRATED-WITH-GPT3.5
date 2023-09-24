
# import speech_recognition as sr
# import pyttsx3
# import openai

# # Initialize the speech recognition engine
# recognizer = sr.Recognizer()

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Set up OpenAI API credentials
# openai.api_key = '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'

# # Function to speak the given text
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Function to generate a response using GPT-3.5
# def generate_response(input_text):
#     response = openai.Completion.create(
#         engine='text-davinci-003',  # Use GPT-3.5 engine
#         prompt=input_text,
#         max_tokens=100,  # Adjust as per your preference
#         n=1,  # Generate a single response
#         stop=None,  # Stop generating when the model reaches a stopping condition
#         temperature=0.7  # Controls the randomness of the generated response
#     )
#     return response.choices[0].text.strip()

# # Main loop
# while True:
#     try:
#         # Continuously listen for user input
#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
#             print("Listening...")
#             audio = recognizer.listen(source)

#         # Use Google Speech Recognition to convert speech to text
#         user_input = recognizer.recognize_google(audio)
#         print("You:", user_input)

#         # Check if user wants to end the conversation
#         if "bye" in user_input.lower():
#             print("Victor: Goodbye!")
#             speak("Goodbye!")
#             break

#         # Generate a response using GPT-3.5
#         response = generate_response(user_input)
#         print("Victor:", response)

#         # Speak the response
#         speak(response)

#     except sr.UnknownValueError:
#         print("Sorry, I couldn't understand your speech.")

#     except sr.RequestError as e:
#         print("Error occurred during speech recognition:", str(e))
import speech_recognition as sr
import pyttsx3
import openai
import json

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set up OpenAI API credentials
openai.api_key = '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'

# Set your name and voice assistant's name
user_name = "Your Name"
assistant_name = "Victor"

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to generate a response using GPT-3.5
def generate_response(input_text):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Use GPT-3.5 engine
        prompt=input_text,
        max_tokens=100,  # Adjust as per your preference
        n=1,  # Generate a single response
        stop=None,  # Stop generating when the model reaches a stopping condition
        temperature=0.7  # Controls the randomness of the generated response
    )
    return response.choices[0].text.strip()

# Load commands from JSON file
def load_commands_from_file(file_path):
    with open(file_path) as file:
        commands_data = json.load(file)
    return commands_data["commands"]

# Main loop
def main():
    # Load commands from JSON file
    commands = load_commands_from_file("commands.json")

    # Continuously listen for user input
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                print("Listening...")
                audio = recognizer.listen(source)

            # Use Google Speech Recognition to convert speech to text
            user_input = recognizer.recognize_google(audio)
            print(f"{user_name}: {user_input}")

            # Check if user wants to end the conversation
            if "bye" in user_input.lower():
                print(f"{assistant_name}: Goodbye!")
                speak("Goodbye!")
                break

            # Check if the user input matches any command
            matched_command = None
            for command in commands:
                if command["command"].lower() in user_input.lower():
                    matched_command = command
                    break

            if matched_command:
                response = matched_command["response"]
            else:
                # Generate a response using GPT-3.5
                response = generate_response(user_input)

            print(f"{assistant_name}: {response}")

            # Speak the response
            speak(response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")

        except sr.RequestError as e:
            print("Error occurred during speech recognition:", str(e))

if __name__ == "__main__":
    main()
