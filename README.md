# LinkedIn Job Postings Scraper and Profile Extractor using Selenium and BeautifulSoup libraries

## Overview

This project provides a Python script to scrape job postings from LinkedIn and extract profile information. It uses the Selenium and BeautifulSoup libraries for scraping and data extraction, and sends an email with the results in an Excel file.

## Features

- **Job Scraping:** Fetches job listings based on specific keywords from LinkedIn job search URLs.
- **Profile Scraping:** Extracts profile information from a LinkedIn profile URL, including name, title, location, and LinkedIn profile URL.
- **Email Notification:** Sends an email with the top 3 job postings and profile information attached as an Excel file.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- Pandas
- `webdriver-manager`
- `requests`
- `smtplib` (standard library)
- `email` (standard library)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   
2. **Navigate to the project directory:**
    ```bash
   cd yourrepository

3. **Install the required packages:**
   ```bash  
   pip install selenium beautifulsoup4 pandas webdriver-manager requests

## Configuration

**Update the Email Credentials**

1. **Edit the script to include your email credentials in the send_email function:**


```python 
sender_email = "your_email@gmail.com" 
sender_password = "your_email_password"
recipient_emails = ["recipient@example.com"]

```

## Set LinkedIn Profile URL
 **Update the profile_url variable with the LinkedIn profile URL you wish to scrape:**

```python

profile_url = "https://www.linkedin.com/in/your-profile/"

```

## Modify Job Search URLs
**Update the websites list with the LinkedIn job search URLs you want to scrape:**

```
websites = [
    "https://www.linkedin.com/jobs/search/?keywords=data%20engineer",
    ...
]
```

## Usage
**Run the Script using the following command:**

```bash
python your_script_name.py
```
This will scrape job listings and profile data, and send an email with the results.

## Script Breakdown of Functions

1. scrape_jobs(url, keywords, pages=1) : Scrapes job postings from the given URL and filters them based on the provided keywords.
2. scrape_profile(driver, profile_url) : Extracts profile information including the LinkedIn profile URL.
3. send_email(sender_email, sender_password, recipient_emails, subject, body, jobs_df, profile_df) : Sends an email with the job postings and profile data attached as an Excel file.
4. main() : Coordinates the scraping process and sends the email with the collected data.


## Troubleshooting
- NoSuchElementException: This error occurs if the element cannot be found on the page. Ensure that the LinkedIn profile is fully loaded and that the element selectors are correct.
- TimeoutException: May occur if the page takes too long to load. Consider increasing the wait times if you experience this issue frequently.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
LinkedIn for providing a platform to scrape job postings and profile information.
Selenium for the web automation framework.
BeautifulSoup for parsing HTML and XML documents.



## Instructions for Adding Images:

Take screenshots of the output or intermediate steps in your script.
Save these images in a directory within your project, such as /images.
Update the ![Description](path/to/image) lines in the README to point to the correct paths.
For example:

![Job Listings Output](images/job_listings_output.png)
![Profile Data Output](images/profile_data_output.png)


