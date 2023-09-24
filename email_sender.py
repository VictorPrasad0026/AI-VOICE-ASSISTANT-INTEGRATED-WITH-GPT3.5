import smtplib
import ssl

def send_email(recipient_email, subject, body):
    sender_email = "dasarboss7@gmail.com"  # Update with the sender's email address
    sender_password = "xljqalzmgkacngab"  # Update with the sender's email password

    smtp_server = "smtp.gmail.com"  # Update with the appropriate SMTP server
    smtp_port = 587  # Update with the appropriate SMTP port

    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message)
        #print("done")



#send_email('rishabhvctor@gmail.com',"heloo","whatsapp")
