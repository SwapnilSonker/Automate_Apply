from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    Thank You
    """
    
    
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



def send_email( your_email , to_email, password, body, subject):
    
    try:
        msg = MIMEMultipart()
        msg["From"] = your_email
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(your_email , password)
            server.sendmail(your_email, to_email, msg.as_string())
            
        print("Email sent successfully")    
    except Exception as e:
        print(f"Error: {e}")
                

# here in the csv there is an error to be fixed that is the column contents are shifted to the right that's why there are different names.
def send_email_from_csv(sender_email, sender_password,csv_file):
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return
    
    for _, row in data.iterrows():
        
        # here ['Company Name'] refers to the email address
        if row['Company Name'] == "N/A" or pd.isna(row['Company Name']):
            # print(f"Error: Email address not found for {row['Company Name']}.")
            continue
        
        # here ['Job Title'] refers to the company name
        if pd.isna(row['Job Title']):
        #    print(f"Skipping row due to missing job title : {row.to_dict()}")
           continue
        try:
            Email = Email_Validation(
                your_email = sender_email,
                to_email = row['Company Name'],
                password = sender_password,
                company_name= row['Job Title'] if row['Company Name'] != "N/A" else "Unknown"
            )
            
            
            # herer ['Page'] refers to the job title 
            job_title = row['Page'].strip()
        
            
            if not pd.isna(row['Company Name']) or row['Company Name'] != "N/A" or not pd.isna(row['Job Title']):
                
                print("job_title" , type(job_title))
                print("sender_email" , type(Email.your_email))
                print("receiver email", type(Email.to_email))
                
                subject =  generate_subject_and_body(job_title, "subject")
                print("subject ->", type(subject))
                
                body = generate_subject_and_body(job_title, "body")
                print("body ->", type(body))
                
                send_email(Email.your_email, Email.to_email, Email.password, body, subject)
            
        except ValidationError as e:
            print(f"Validation Error: {e}")    
        except Exception as e:
            print(e)    
     
   