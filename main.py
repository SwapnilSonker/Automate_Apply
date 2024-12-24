from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import csv
import re

from customs.email_sender import send_email_from_csv

load_dotenv()
EMAIL = os.getenv("NAUKRI_MAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

job_location = os.getenv("job_location")
keyword = os.getenv("search_keyword")

driver_path = 'C:/Users/91639/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://www.naukri.com/")
driver.maximize_window()
time.sleep(3)

while True:
    def next_page(driver):
            try:
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='styles_btn-secondary__2AsIP']"))
                )
                next_page.click()
                print("Moving to the next page")
                time.sleep(1)  # Allow time for the page to load
            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                raise
    
    def get_page_count(driver):
        try:
            pages_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='styles_pages__v1rAK']"))
            )
            print("Pages container located")

            # Retrieve all the <a> tags within the container
            pages = pages_container.find_elements(By.XPATH, ".//a")
            return len(pages)
        except Exception as e:
            print("Error in page count" , e)
            return 0   
    
    def fetch_job_elements(driver):
        try:
            job_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'styles_job-listing-container__OCfZC'))
            )
            print("Job container found")
            job_elements = job_container.find_elements(By.XPATH, "//div[@class='styles_jlc__main__VdwtF']//div[@data-job-id]")
            print(f"Found {len(job_elements)} job elements")
            return job_elements
        except Exception as e:
            print(f"Error fetching job elements: {e}")
            return []
    
    def process_jobs(driver, job_elements):
        for index, job in enumerate(job_elements, 1):
            try:
                # Scroll into view to ensure the job is interactable
                driver.execute_script("arguments[0].scrollIntoView(true);", job)

                # Extract visible text for debugging
                job_text = job.text
                print(f"Processing job {index}: {job_text[:50]}...")

                # Click the job
                job.click()
                print("Job clicked")

                # Wait for a new tab to open
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                print("Switched to the new tab")

                try:
                    print("Looking for the Apply button...")
                    apply_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='styles_jhc__apply-button-container__5Bqnb']//button[@id='apply-button' and text()='Apply']")
                        )
                    )
                    apply_button.click()
                    print("Apply button clicked")
                except Exception as e:
                    print("No Apply button found:", str(e))

                try:
                    details_div = driver.find_element(By.CLASS_NAME, "styles_JDC__dang-inner-html__h0K4t")
                    details_text = details_div.text

                    # Extract email and phone using regex
                    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', details_text)
                    phone_match = re.search(r'\b\d{10}\b', details_text)

                    # Extract values or set as "N/A" if not found
                    email = email_match.group(0) if email_match else "N/A"
                    phone = phone_match.group(0) if phone_match else "N/A"

                    # Extract the company name (adjust the selector as needed)
                    company_name = driver.find_element(By.XPATH, "//div[@class='styles_jd-header-comp-name__MvqAI']//a").text
                    print(f"Company Name: {company_name}")
                    job_title = driver.find_element(By.XPATH, "//h1[@class='styles_jd-header-title__rZwM1']").text
                    print(f"Job Title: {job_title}")
                    # Save to CSV
                    writer.writerow([job_title, company_name, email, phone])
                    print(f"Saved: {job_title} | {company_name} | Email: {email} | Phone: {phone}")

                except Exception as e:
                    print(f"Error extracting details for job {index}: {e}")

                # Close the current tab and return to the main window
                driver.close()
                print("Closed the new tab")
                driver.switch_to.window(driver.window_handles[0])
                print("Returned to the main window")

            except Exception as e:
                print(f"Error processing job {index}: {e}")
                continue
   
 
    try:
        # Login process
        login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-log-reg']//a"))
        )
        login.click()
        time.sleep(4)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='form-row']//input[@type='text']"))
        )
        print("Email input field found.")
        email_input.send_keys(EMAIL)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='form-row']//input[@type='password']"))
        )
        print("Password input field found.")
        password_input.send_keys(PASSWORD)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div//button[@type='submit']"))
        )
        submit_button.click()
        print("Login Successful!!!")

        # Search process
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-sb__main']"))
        )
        print("Found the search box")
        search_box.click()

        keyword_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='suggestor-box flex-row flex-wrap bottom ']//input[@type='text' and @placeholder='Enter keyword / designation / companies']"))
        )
        search_keywords = keyword
        keyword_box.send_keys(search_keywords)
        print("Keywords entered")

        keyword_box.send_keys(Keys.TAB)

        experience_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dropdownMainContainer focus']"))
        )
        experience_box.click()
        print("Experience section opened")

        options = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@index='0']"))
        )
        options.click()
        print("Experience level selected")

        Location_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='suggestor-box flex-row flex-wrap bottom ']//input[@type='text' and @placeholder='Enter location']"))
        )
        Location_values = job_location
        Location_box.send_keys(Location_values)
        print("Location entered")

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='nI-gNb-sb__icon-wrapper']"))
        )
        search_button.click()
        print("Search button clicked, fetching results...")

        # Job application process
        page_count = get_page_count(driver)
        print("page count", page_count)
        
        current_page = 1
        
    
        with open("jobs_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write CSV header
            writer.writerow(["Page", "Job Title", "Company Name", "Email", "Phone Number"])        
            while True:  # Loop through all pages
                try:
                    print(f"\nProcessing Page {current_page} of {page_count}")

                    # Fetch job elements on the current page
                    job_elements = fetch_job_elements(driver)
                    if not job_elements:
                        print(f"No job elements found on page {current_page}. Skipping.")
                    else:
                        # Process the jobs
                        process_jobs(driver, job_elements)

                    if current_page >= page_count:
                        print("There are no more pages to browse.")
                        break

                    # Navigate to the next page
                    next_page(driver)
                    current_page += 1  # Increment page counter
                except Exception as e:
                    print(f"Error in processing page {current_page}: {e}")
                    break  # Exit on unexpected error                       
    except Exception as e:
        print("An error occurred:", e)
    finally:
        send_email_from_csv(EMAIL, EMAIL_PASSWORD, "jobs_data.csv")
        print("Press Enter to close the browser")
        input()
        driver.quit()
