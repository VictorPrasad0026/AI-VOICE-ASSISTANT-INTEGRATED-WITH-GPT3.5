import json
import smtplib
import ssl
import openai

# Set up OpenAI API credentials
openai.api_key = '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'

# Function to generate a rephrased sentence using OpenAI GPT-3
def generate_rephrased_sentence(sentence):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt="Rephrase the following sentence: " + sentence,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to send an email
def send_email(sender_email, sender_password, receiver_email, subject, body):
    smtp_server = "smtp.gmail.com"  # Update with the appropriate SMTP server
    smtp_port = 587  # Update with the appropriate SMTP port

    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)

# Configure the sender's email credentials
sender_email = "your_email@gmail.com"  # Update with the sender's email address
sender_password = "your_password"  # Update with the sender's email password



# Read the recipient's email ID from the JSON file
with open("recipients.json") as file:
    recipients_data = json.load(file)

# Extract the recipient's name and email ID
recipient_name = recipients_data["name"]
recipient_email = recipients_data["email"]

# Input the sentence
sentence = input("Enter a sentence: ")

# Generate the rephrased sentence
rephrased_sentence = generate_rephrased_sentence(sentence)

# Set the subject and body based on the rephrased sentence
subject = "Rephrased Sentence"
body = rephrased_sentence

# Send the email
send_email(sender_email, sender_password, recipient_email, subject, body)

print(f"Email sent successfully to {recipient_name} ({recipient_email})!")
