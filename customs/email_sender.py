import pandas as pd
import smtplib
from pydantic import BaseModel , EmailStr
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from typing import Literal


# loading the huggingface api key
load_dotenv()

os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')

def generate_subject(job_title: str, prompt_type: Literal['subject', 'body']) -> str:
    llm_memory = ConversationBufferMemory(input_key="job_title", memory_key="chat_memory")
    prompt = f"Generate a {prompt_type} for a email for the topic: {job_title} within 20 words"
    prompt = PromptTemplate(
        input_variables={"job_title": job_title},
        template= prompt,
    )
    
    llm = HuggingFaceHub(repo_id = "google/flan-t5-large", model_kwargs = {"temperature": 0.7 , "max_length": 500})
    chain = LLMChain(llm, memory=llm_memory, prompt=prompt , verbose=True)
    
    result = chain.run({"job_title": job_title})
    
    return result
    
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
     
if __name__ == "__main__":
    generate_subject("Data Scientist", "subject")        