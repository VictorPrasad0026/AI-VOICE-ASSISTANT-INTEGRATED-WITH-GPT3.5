import speech_recognition as sr
import pyttsx3
import openai
import json
from email_sender import send_email  # Import the function from your other Python file

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set up OpenAI API credentials
openai.api_key = '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'

# Set your name and voice assistant's name
user_name = "Rishabh Prasad"
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

# Function to search for recipient's email based on their name
def get_recipient_email(name):
    with open("recipients.json") as file:
        recipients_data = json.load(file)
    recipients = recipients_data["recipients"]
    for recipient in recipients:
        if recipient["name"].lower() == name.lower():
            return recipient["email"]
    return None


# Function to get a response from the database (commands.json)
def get_response_from_database(user_command, commands_data):
    try:
        # Search for a response based on the user's command
        for entry in commands_data:
            if entry["command"].lower() == user_command.lower():
                return entry["response"]
        
        # Return None if the command is not found
        return None
    except Exception as e:
        print(f"An error occurred while fetching response from the database: {str(e)}")
        return None

    

# Load commands from JSON file
def load_commands_from_file(file_path):
    with open(file_path) as file:
        commands_data = json.load(file)
    return commands_data["commands"]


# Main loop
def main():
    # Load commands from JSON file
    commands = load_commands_from_file("commands.json")

    # Main loop
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

            # Check if the user wants to send an email
            if "send mail to" in user_input.lower():
                name = user_input.lower().replace("send mail to", "").strip()
                recipient_email = get_recipient_email(name)
                if recipient_email:
                    # Ask for the body of the email using voice
                    speak("Please provide the body of the email.")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                        print("Listening...")
                        audio = recognizer.listen(source)
                    body = recognizer.recognize_google(audio)

                    # Send the email using the function from your other Python file
                    send_email(recipient_email, "Automatic Email", body)

                    print(f"{assistant_name}: Email sent successfully to {name}!")
                    speak(f"Email sent successfully to {name}!")
                else:
                    print(f"{assistant_name}: Recipient {name} not found.")
                    speak(f"Recipient {name} not found.")

            # Check if the user explicitly requests to check the database
            if "check database" in user_input.lower():
                print(f"{assistant_name}: OK, tell me.")
                speak("OK, tell me.")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                # Use Google Speech Recognition to convert the user's command to text
                command = recognizer.recognize_google(audio)
                print(f"{user_name} (Command): {command}")

                # Look for a response in the 'response.json' file based on the user's command
                response = get_response_from_database(command,commands)
                if response:
                    print(f"{assistant_name}: {response}")
                    speak(response)
                else:
                    print(f"{assistant_name}: Response not found in the database.")
                    speak("Response not found in the database.")
            
            else:
                # Generate a response using GPT-3.5
                response = generate_response(user_input)

                print(f"{assistant_name}: {response}")

                # Speak the response
                speak(response)
            speak("Please tell me.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
            speak("Sorry, I couldn't understand your speech.")

        except sr.RequestError as e:
            print("Error occurred during speech recognition:", str(e))
            speak("Sorry, an error occurred during speech recognition.")

if __name__ == "__main__":
    main()
