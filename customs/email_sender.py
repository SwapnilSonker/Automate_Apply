import pandas as pd
import smtplib
from pydantic import BaseModel , EmailStr
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from typing import Literal
from langchain.schema.runnable import RunnableSequence
from pydantic_core import ValidationError



# loading the huggingface api key
load_dotenv()

os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# function to generate email subject and body
def generate_subject_and_body(job_title:str, prompt_type:Literal['subject', 'body']) -> str:
    chat_memory = ConversationBufferMemory(input_key="job_title" , memory_key="chat_memory")
    
    example_subject = "Exciting Opportunity for a Frontend Engineer with React and JavaScript Expertise"
    example_body = """Dear Hiring Manager,

    I am writing to express my interest in the Frontend Engineer position at your company. With expertise in skills and measures required in this domain, I am confident that my skills will be a valuable asset to your team. I am particularly drawn to your company's commitment to innovation, and I would love the opportunity to contribute to your dynamic team.

    Sincerely,
    [Your Name]"""
    
    
    if prompt_type == "subject":
        detailed_prompt = f"""You are an expert email subject generator. Your task is to generate an attractive, concise, and engaging email subject for a {job_title} job position. The subject should be relevant to the job title, including key skills such as, and it should be compelling enough for an employer to open the email.

                        Example Subject: {example_subject}

                        Generate a similar subject for the job title "{job_title}"."""
    else:  # for 'body'
        detailed_prompt = f"""You are an expert email body generator. Write a detailed and persuasive email body for a {job_title} job application. The body should highlight key skills such as , express enthusiasm about the role, and be unique and professional.

                        Example Body:
                        {example_body}

                        Generate a similar body for the job title "{job_title}"."""
  
    
    prompt = PromptTemplate(
        input_variables={"job_title": job_title},
        template= detailed_prompt,
    )
    
    llm = HuggingFaceHub(repo_id = "google/flan-t5-large", model_kwargs = {"temperature": 0.7 , "max_length": 500})
    
    chain = LLMChain(llm=llm, memory=chat_memory, prompt=prompt, verbose=True)
    
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
        
        try:
            Email = Email_Validation(
                your_email = sender_email,
                to_email = row['Email'],
                password = sender_password,
                company_name= row['Company Name']
            )
            
            job_title = row['Job Title'].strip()
            
            print("job_title" , job_title)
            print("sender_email" , Email.your_email)
            print("receiver email", Email.to_email)
            # subject to be added on the basis of job title
            # subject =  generate_subject_and_body(job_title, "subject")
            
            # body to be added on the basis of job title
            # body = generate_subject_and_body(job_title, "body")
            
            # send_email(Email.your_email, Email.to_email, Email.password, body, subject)
            # for subject & body use huggingface model to generate subject 
            
        except ValidationError as e:
            print(f"Validation Error: {e}")    
        except Exception as e:
            print(e)    
     
if __name__ == "__main__":
    send_email_from_csv("swapnilsonker04@gmail.com", "Swapnil@0406", "jobs_data.csv")     