import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Define your search keywords
keywords = ["New Grad 2025", "Summer Intern 2025", "Entry Level", "2025", "Co-op", "Coop", "Data engineer", "Data Analyst", "System Analyst", 
            "Business Analyst","Software Engineer","Data Scientist","System Engineer","business intelligence developer","Software Developer"]

# Define websites to scrape (replace with target URLs)
websites = ["https://www.linkedin.com/jobs/search/?currentJobId=3966708624&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&keywords=data%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3931926588&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=data%20analyst&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3960504923&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=data%20scientist&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3949665621&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=business%20analyst&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3960365235&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=system%20analyst&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3958174398&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=business%20data%20analyst&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3937794201&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=system%20engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3920926888&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=business%20intelligence%20developer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3675237694&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=Software%20Developer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&start=25",
            "https://www.linkedin.com/jobs/search/?currentJobId=3902437361&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=solution%20engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3926929924&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=co-op&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3942857107&f_E=1%2C2%2C3&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C2%2C3&geoId=103644278&keywords=intern&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R",
            "https://www.linkedin.com/jobs/search/?currentJobId=3942857107&f_E=1%2C2%2C3&f_F=it%2Ceng%2Canls%2Cmgmt&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C3%2C2&geoId=103644278&keywords=intern&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true",
            "https://www.linkedin.com/jobs/search/?currentJobId=3921489060&f_E=1%2C2%2C3&f_F=it%2Ceng%2Canls%2Cmgmt&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C3%2C2&geoId=103644278&keywords=co-op&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&spellCorrectionEnabled=true",
            "https://www.linkedin.com/jobs/search/?currentJobId=3921489060&f_E=1%2C2%2C3&f_F=it%2Ceng%2Canls%2Cmgmt&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C3%2C2&geoId=103644278&keywords=co-op&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&spellCorrectionEnabled=true",
            "https://www.linkedin.com/jobs/search/?currentJobId=3921489060&f_E=1%2C2%2C3&f_F=it%2Ceng%2Canls%2Cmgmt&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C3%2C2&geoId=103644278&keywords=co-op&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&spellCorrectionEnabled=true",
            "https://www.linkedin.com/jobs/search/?currentJobId=3960514865&f_E=1%2C2%2C3&f_F=it%2Ceng%2Canls%2Cmgmt&f_JT=F%2CP%2CI&f_SB2=2&f_TPR=r2592000&f_WT=1%2C3%2C2&geoId=103644278&keywords=software&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R&spellCorrectionEnabled=true"]

# Define LinkedIn profile URL to scrape
profile_url = "https://www.linkedin.com/in/roshini-p21/"

# Define email details
sender_email = "abc@gmail.com"
sender_password = " Google Sign-in - App Password"
recipient_emails = ["xyz@gmail.com"]

def scrape_jobs(url, keywords, pages=1):
    jobs = []
    for page in range(pages):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        job_listings = soup.find_all("div", class_="base-card")
        
        print(f"Found {len(job_listings)} job listings.")
        
        for listing in job_listings:
            title_element = listing.find("h3", class_="base-search-card__title")
            company_element = listing.find("h4", class_="base-search-card__subtitle")
            location_element = listing.find("span", class_="job-search-card__location")
            application_link_element = listing.find("a", href=True)

            title = title_element.text.strip() if title_element else ""
            company = company_element.text.strip() if company_element else ""
            location = location_element.text.strip() if location_element else ""
            link = application_link_element["href"] if application_link_element else ""

            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    "Title & Summary": title,
                    "Company": company,
                    "Location": location,
                    "Link": link,
                })
        
        next_page_link = soup.find("a", class_="next")
        if next_page_link:
            url = next_page_link["href"]
        else:
            break
    
    return jobs

def wait_for_user_action(driver):
    input("Please complete any manual actions (like MFA) and press Enter when you're on the LinkedIn feed...")

def scrape_profile(driver, profile_url):
    driver.get(profile_url)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge")))
    except TimeoutException:
        print("Profile page did not load as expected. Continuing with limited information.")
    
    profile_data = {}

    try:
        profile_data["Name"] = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").get_attribute("innerText")
    except NoSuchElementException:
        profile_data["Name"] = "Not available"

    try:
        profile_data["Title & Summary"] = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").get_attribute("innerText")
    except NoSuchElementException:
        profile_data["Title & Summary"] = "Not available"

    try:
        profile_data["Location"] = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").get_attribute("innerText")
    except NoSuchElementException:
        profile_data["Location"] = "Not available"

    # Initialize Email as Not available
    profile_data["Email"] = "Not available"
    
    try:
        # Attempt to open the contact info section
        contact_info_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-control-name='contact_info']"))
        )
        driver.execute_script("arguments[0].click();", contact_info_button)
        time.sleep(2)  # Wait for the contact info to be visible
        
        try:
            # Updated CSS selector for the email address
            email_element = driver.find_element(By.CSS_SELECTOR, "a[href^='mailto:']")
            profile_data["Email"] = email_element.get_attribute("innerText")
        except NoSuchElementException:
            print("Email not found in contact info.")
    except TimeoutException:
        print("Could not access contact info. Profile Email will not be available.")
    
    # Adding profile URL to profile data
    profile_data["LinkedIn URL"] = profile_url

    return profile_data

def send_email(sender_email, sender_password, recipient_emails, subject, body, jobs_df, profile_df):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_emails)
    message["Subject"] = subject

    top_3_jobs = jobs_df.head(3)
    jobs_html_table = top_3_jobs.to_html(index=False, justify="left", classes="table table-striped")

    profile_html_table = profile_df.to_html(index=False, justify="left", classes="table table-striped")

    body += f"<p>Total Job Postings: {len(jobs_df)}</p>"
    body += "<h4>Top 3 Job Postings:</h4>"
    body += jobs_html_table
    body += "<h4>Profile Information:</h4>"
    body += profile_html_table

    message.attach(MIMEText(body, "html"))

    excel_file = "linkedin_jobdata.xlsx"
    with pd.ExcelWriter(excel_file) as writer:
        jobs_df.to_excel(writer, sheet_name="Jobs", index=False)
        profile_df.to_excel(writer, sheet_name="Profile", index=False)

    with open(excel_file, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="octet-stream")
        part.add_header('Content-Disposition', 'attachment', filename=excel_file)
        message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, message.as_string())

    print("Email sent successfully!")

def main():
    # Scrape jobs using BeautifulSoup
    all_jobs = []
    for website in websites:
        all_jobs.extend(scrape_jobs(website, keywords, pages=3))

    jobs_df = pd.DataFrame(all_jobs)

    # Scrape profile using Selenium
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    driver.get("https://www.linkedin.com")
    wait_for_user_action(driver)
    
    profile_data = scrape_profile(driver, profile_url)
    profile_df = pd.DataFrame([profile_data])

    driver.quit()

    # Send email with scraped data
    subject = "LinkedIn Job Openings & Profile Data"
    body = f"<p>Hey there, Attached are the scraped job openings from Linkedin matching your keywords:  {', '.join(keywords)}</p><br>"
    send_email(sender_email, sender_password, recipient_emails, subject, body, jobs_df, profile_df)

if __name__ == "__main__":
    main()