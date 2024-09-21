from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to the ChromeDriver executable
path = "D:\Tutorials\ChromeDriver\chromedriver.exe"

# Create a Service object and pass the path to the chrome driver executable
service = Service(executable_path=path)

# Initialize the chrome webdriver using the service object 
driver = webdriver.Chrome(service=service)

# Open the website
website = "https://www.adamchoi.co.uk/teamgoals/detailed"
driver.get(website)

# Xpath Syntax  
# //tagName[@AttributeName="value"]

# Wait for the "All Matches" button and click it
all_matches_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[text()='All matches']"))
)
all_matches_button.click()

# Gather all the tables on the page
tables = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//table"))
)

# Initialize lists to store match details
date = []
home_team = []
score = []
away_team = []

# Iterate over each table and extract rows from them
for table in tables:
    # Get all the rows (tr elements) inside the current table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        # Get all the columns (td elements) inside the row
        columns = row.find_elements(By.TAG_NAME, 'td')
        
        if len(columns) < 4:
            print("Skipping row due to insufficient data.")
            continue

        try:
            # Check if any of the elements are missing or empty
            row_data = [columns[0].text, columns[1].text, columns[2].text, columns[3].text]
            if all(row_data):  # Ensure all elements in the row have data
                date.append(columns[0].text)  # Date
                home_team.append(columns[1].text)  # Home Team
                score.append(columns[2].text)  # Score
                away_team.append(columns[3].text)  # Away Team
            else:
                print(f"Skipping row due to missing data: {row_data}")
        except Exception as e:
            print(f"Error processing row: {e}")

# Check if all lists are of the same length before creating the DataFrame
if len(date) == len(home_team) == len(score) == len(away_team):
    # Create a DataFrame from the collected data
    df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
    print(df)
else:
    print("Error: Lists are not of the same length!")

# Close the browser after a short delay
time.sleep(5)
driver.quit()

df.to_csv('Football_data.csv',index= False)