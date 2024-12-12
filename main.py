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
time.sleep(3)

try:
    # Login process
    login = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-log-reg']//a"))
    )
    login.click()

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
    search_keywords = "Customer Executive"
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
    Location_values = "Delhi, Noida, Gurugram"
    Location_box.send_keys(Location_values)
    print("Location entered")

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='nI-gNb-sb__icon-wrapper']"))
    )
    search_button.click()
    print("Search button clicked, fetching results...")

    # Job application process
    job_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'styles_job-listing-container__OCfZC'))
    )
    print("Job container found")

    job_elements = job_container.find_elements(By.XPATH, "//div[@class='styles_jlc__main__VdwtF']//div[@data-job-id]")
    print(f"Found {len(job_elements)} job elements")

    for index, job in enumerate(job_elements, 1):
        try:
            # Scroll into view to ensure the job is interactable
            driver.execute_script("arguments[0].scrollIntoView(true);", job)

            # Extract visible text for debugging
            job_text = job.text
            print(f"Processing job {index}: {job_text[:50]}...")

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
                time.sleep(5)
                print("Apply button found")
                time.sleep(2)
                apply_button.click()
                time.sleep(3)
                print("Apply button clicked")
            except Exception as e:
                print("No direct Apply button found or other issue:", str(e))

            # Close the current tab and return to the main window
            driver.close()
            print("Closed the new tab")
            driver.switch_to.window(driver.window_handles[0])
            print("Returned to the main window")

        except Exception as e:
            print(f"Error processing job {index}: {e}")
            continue

except Exception as e:
    print("An error occurred:", e)
finally:
    print("Press Enter to close the browser")
    input()
    driver.quit()
