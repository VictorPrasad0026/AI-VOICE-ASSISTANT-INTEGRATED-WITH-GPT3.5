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

# Function to generate a question using GPT-3.5
def generate_interview_question(topic):
    prompt = f"Generate an interview question about {topic}"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.7
    )
    print(response.choices[0].text.strip())
    return response.choices[0].text.strip()

# Function to evaluate the user's answer using GPT-3.5
def evaluate_answer(question, user_answer):
    prompt = f"Question: {question}\nUser Answer: {user_answer}\nEvaluate the answer."
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.7
    )
    evaluation = response.choices[0].text.strip()
    return evaluation

# Function to add a command to the database and response.json
def add_command_to_database(commands_data, command, response):
    try:
        # Check if the command already exists in the database
        for entry in commands_data:
            if entry["command"].lower() == command.lower():
                print(f"{assistant_name}: Command '{command}' already exists in the database.")
                speak(f"Command '{command}' already exists in the database.")
                return

        # If the command doesn't exist, add it to the database
        new_entry = {"command": command, "response": response}
        commands_data.append(new_entry)

        # Save the updated database to response.json
        with open("commands.json", "w") as file:
            json.dump({"commands": commands_data}, file, indent=4)

        print(f"{assistant_name}: Command '{command}' added to the database.")
        speak(f"Command '{command}' added to the database.")
    except Exception as e:
        print(f"An error occurred while adding a command to the database: {str(e)}")


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
            elif "check database" in user_input.lower():
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



            # Check if the user wants to add a command
            elif "add command" in user_input.lower():
                print(f"{assistant_name}: Please specify the command you want to add.")
                speak("Please specify the command you want to add.")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                # Use Google Speech Recognition to convert the user's command to text
                new_command = recognizer.recognize_google(audio)
                print(f"{user_name} (Command): {new_command}")

                print(f"{assistant_name}: Please specify the response for the command.")
                speak("Please specify the response for the command.")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                    print("Listening for response...")
                    audio = recognizer.listen(source)

                # Use Google Speech Recognition to convert the user's response to text
                new_response = recognizer.recognize_google(audio)
                print(f"{user_name} (Response): {new_response}")

                # Add the new command and response to the database and response.json
                add_command_to_database(commands, new_command, new_response)

            elif "what is your name" in user_input.lower():
                print(f"{assistant_name}: hey! i'm victor how can i help you")
                speak("hey! i'm victor how can i help you")

            # Check if the user wants to start an interview
            elif "start interview" in user_input.lower():
                print(f"{assistant_name}: Sure, let's start the interview.")
                speak("Sure, let's start the interview. Please specify the topic.")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening for the interview topic...")
                    audio = recognizer.listen(source)

                interview_topic = recognizer.recognize_google(audio)
                print(f"{user_name} (Interview Topic): {interview_topic}")

                print(f"{assistant_name}: Great! We will ask questions about '{interview_topic}'.")
                speak(f"Great! We will ask questions about '{interview_topic}'.")
                print(f"{assistant_name}: You can say 'Please stop interview' to end the interview at any time.")
                speak("You can say 'Please stop interview' to end the interview at any time.")

                # Initialize variables to keep track of questions and answers
                questions = []
                correct_answers = 0

                while True:
                    # Generate an interview question
                    question = generate_interview_question(interview_topic)
                    print(f"{assistant_name}: Question: {question}")
                    speak(f"Question: {question}")
                    questions.append(question)

                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        print("Listening for your answer...")
                        audio = recognizer.listen(source)

                    user_answer = recognizer.recognize_google(audio)
                    print(f"{user_name} (Answer): {user_answer}")

                    # Evaluate the answer
                    evaluation = evaluate_answer(question, user_answer)
                    # print(f"{assistant_name}: Evaluation: {evaluation}")
                    speak(f"Evaluation: {evaluation}")

                    #correct answer
                    correct_answer = generate_response(question)
                    print(f"{assistant_name}: correct_answer: {correct_answer}")
                    speak(f"correct_answer: {correct_answer}")

                    if "stop interview" in user_answer.lower():
                        break

                    if "correct" in evaluation.lower():
                        correct_answers += 1

                print(f"{assistant_name}: Interview completed. You answered {correct_answers} out of {len(questions)} questions correctly.")
                speak(f"Interview completed. You answered {correct_answers} out of {len(questions)} questions correctly.")

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
