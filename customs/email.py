import pandas as pd
import smtplib
from pydantic import BaseModel , EmailStr

class Email_Validation(BaseModel):
    your_email: EmailStr
    to_email: EmailStr
    password: str
    company_name: str



def send_email(self, your_email , to_email, password, body, subject):
    self.your_email = your_email
    self.to_email = to_email
    self.password = password
    self.subject = subject
    self.body = body
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(self.your_email , self.password)
        server.sendmail(self.your_email, self.to_email,self.subject, self.body)

def send_email_from_csv(sender_email, sender_password,csv_file):
    data = pd.read_csv(csv_file)
    
    for _, row in data.iterrows():
        job_title = row['Job Title']
        try:
            Email = Email_Validation(
                your_email = sender_email,
                to_email = row['Email'],
                password = sender_password,
                company_name= row['Company Name']
            )
            # subject to be added on the basis of job title
            # body to be added on the basis of job title
            # for subject & body use huggingface model to generate subject 
        except Exception as e:
            print(e)    
        