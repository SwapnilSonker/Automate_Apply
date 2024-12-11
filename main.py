from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

load_dotenv()
EMAIL = os.getenv("NAUKRI_MAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")



driver_path = 'C:/Users/91639/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

service = Service(driver_path)

driver = webdriver.Chrome(service=service)


driver.get("https://www.naukri.com/")

driver.maximize_window()
# time.sleep(1)

try:
    login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-log-reg']//a"))
    )
    login.click()
    
    
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='form-row']//input[@type='text']"))
    )
    print("Email input field found.")
    email_input.send_keys(os.getenv("NAUKRI_MAIL"))
    
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='form-row']//input[@type='password']"))
    )
    print("Password input field found.")
    password_input.send_keys(os.getenv("NAUKRI_PASSWORD"))
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div//button[@type='submit']"))
    )
    
    submit_button.click()
    
    print("Login Successful!!!")
    
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-sb__main']"))
    )
    print("found the searchbox")
    search_box.click()
    
    print("Searchbox opened!!")
    
    keyword_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='suggestor-box flex-row flex-wrap bottom ']//input[@type='text' and @placeholder='Enter keyword / designation / companies']"))
    )
    search_keywords = "Customer Executive"
    print("entering the keywords!!!")
    keyword_box.send_keys(search_keywords)
    print("keywords entered")
    
    
    keyword_box.send_keys(Keys.TAB)
    experience_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='dropdownMainContainer focus']"))
    )
    print("experience section found")
    
    experience_box.click()

    
    print("experience section entered")
    
    options= WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[@index='0']"))
    )   
    options.click()
    print("exp entered")
    
    Location_box= WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='suggestor-box flex-row flex-wrap bottom ']//input[@type='text' and @placeholder='Enter location']"))
    )
    Location_box.click()
    Location_values = "Delhi , Noida, Gurugram"
    print("entering location")
    Location_box.send_keys(Location_values)
    print("location entered")
    
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='nI-gNb-sb__icon-wrapper']"))
    )
    print("search button found")
    search_button.click()
    print("search button clicked , queries fetching....")
    
    #Working on the Applyjob part
    job_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'styles_job-listing-container__OCfZC'))
    )
    print("job container found")

    
    job_elements = job_container.find_elements(By.XPATH, "//div[@class='styles_jlc__main__VdwtF']") ##just add //div 
    print("job elements" , len(job_elements))
    
    
    for index, job in enumerate(job_elements, 1):
        # Extract visible text from the job element
        job_text = job.text
        print("job" , len(job_text))
        
        print("index =>" , index)
        
        job.click()
        print("job is clicked")
        
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        
        driver.switch_to.window(driver.window_handles[-1])
        print("switched to a new tab")
        
        try:
            print("Enter apply section")
            apply_button = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='styles_jhc__apply-button-container__5Bqnb']//button[@id='apply-button'and text()='Apply']")) #if things go wrong check here first
            )
            time.sleep(1)
            print("Apply button found")
            apply_button.click()
            print("Apply button clicked, Exiting window")
        except Exception:
            time.sleep(2)
            print("No direct apply button is here!!!!")  
        
        driver.close()
        print("Window exited moving to previous one")
        driver.switch_to.window(driver.window_handles[0])  
        print("In the main window...")    
        
        
    
    
except Exception as e:
    print("an error occured:",e)    
finally:
    print("press enter to close the browser")
    input()
    driver.quit()
    
    

