import random
import smtplib #can used Flask.Mail too
from email.mime.text import MIMEText

# Generate a random 6-digit code
def generate_verification_code():
    return str(random.randint(100000, 999999))

## solution 1
# Function to send verification code to the user's email
def send_verification_email(user_email, code):
    sender = 'cancer webapp' 
    password = 'cancer123'

    # context of the Email text, Although can render html too.
    message = MIMEText(f'Your verification code is: {code}')
    message['Subject'] = 'Email Verification Code'
    message['From'] = sender
    message['To'] = user_email
    
    # Send the email using SMTP
    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, user_email, message.as_string())



# with outlook
import getpass
import smtplib , ssl

Host = "smtp.office365.com"
Port = 587
From_mail = "outlook_d7b4ef6926778bd3@outlook.com"  # Your Outlook email
To_mail = "a_arabi@yahoo.com"  # Recipient email
Password = "$123456$" #getpass.getpass("Enter your Outlook App Password: ")  

Message = """\
Subject: This is a test mail

Hi Arman,
Many thanks.
"""

context = ssl.create_default_context()

# Initialize SMTP connection
with smtplib.SMTP(host=Host, port=Port) as server:

    # Perform EHLO and StartTLS
    response_code, status = server.ehlo()
    print(f"[*] Ehlo to server : {response_code} & {status}")

    response_code, status = server.starttls(context)
    print(f"[*] TLS server : {response_code} & {status}")

    # Log in to the server with your App Password
    try:
        response_code, status = server.login(user=From_mail, password=Password)
        print(f"[*] Logged in : {response_code} & {status}")
        
        # Send the email
        server.sendmail(From_mail, To_mail, Message)
        print("[*] Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()
        
        
        
# with email
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path # Help us to access to the html file

email = EmailMessage() #creates the email object
#html = Template(Path("index.html").read_text()) # Path become a Template Object

email["from"] = "arman.arabi.456@gmail.com"
email["to"] = "a_arabi@yahoo.com" 
email["subject"] = "Notification from home"

#email.set_content(html.substitute({"name" : "Caca"}), "html")
email.set_content("Hello, this is a notification from home.")

with smtplib.SMTP(host = "smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("a_arabi@yahoo.com", "zldx icmd cbsc mkqu")
    smtp.send_message(email)
    print("Email Sent")
    
    
# yagmail :
import yagmail

receiver = "arman.arabi.456@gmail.com"
body = "Hello there from Yagmail"
#filename = "document.pdf"

yag = yagmail.SMTP("a_arabi@yahoo.com","$123456$")
try:
    yag.send(
    to=receiver,
    subject="Yagmail test with attachment",
    contents=body, 
    #attachments=filename,
    )
    print('succesfully sent')
except Exception as e:
    print(f'Error: {e}')      