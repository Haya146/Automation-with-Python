# importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to Chrome Driver 
path = "D:\Tutorials\ChromeDriver\chromedriver.exe"

# Create a servic object and pass the chrome driver executable 
service = Service(executable_path= path)

# Intialize the chrome webdriver using the service object
driver = webdriver.Chrome(service=service)

# open the website 
website = "https://www.yalla-kora.plus/"
driver.get(website)

# Wait for the "مباريات اليوم" button and click it 
today_matches_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[1]/ul/li[2]/a"))
)
today_matches_button.click()

# wait for the match to load 
matches_section = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "albaflex"))
)

# Find all match elements in the section 
matches = driver.find_elements(By.CSS_SELECTOR, ".match-container.started, .match-container.commingsoon, .match-container.finshed")

# Intialize lists to store matches details 
Team1 = []
Score = []
Team2 = []
Times = []
Status =[]

# Loop throgh all the atch cards to extract information 
for match in matches :
    try: 
        # Extract team names, score, match time , and status 
        team1 = match .find_element(By.CLASS_NAME, "left-team").text
        team2 = match .find_element(By.CLASS_NAME, "right-team").text
        
        # Extract score or status based on match state 
        if("started")in match .get_attribute("class"):
            score = match.find_element(By.CLASS_NAME, "EventResult").text
            match_time = match.find_element(By.CLASS_NAME, "EventTime").text
            status = "Ongoing"
            
        elif "commingsoon"in match.get_attribute("class"):
            score = "Not Started"
            match_time = match.find_element(By.CLASS_NAME, "EventTime").text
            status = "Upcoming"
            
        elif "finshed" in match.get_attribute("class"):
            score = match.find_element(By.CLASS_NAME, "EventResult").text
            match_time = "Finished"
            status = "Finished"
        
        # Append data to the lists 
        Team1.append(team1)
        Team2.append(team2)
        Score.append(score)
        Times.append(match_time)
        Status.append(status)
        
    except Exception as e :  
        print(f"Error processing match : {e}")

# Create a DataFrame with Scraped data 
df = pd.DataFrame({
    'Team1': Team1,
    'Score': Score,
    'Team2': Team2,
    'Time': Times,
    'Status': Status
})

# Print the dataframe 
print(df)

# save the data to csv files
df.to_csv("today_matches.csv", index= False)

time.sleep(50)
driver.quit()
