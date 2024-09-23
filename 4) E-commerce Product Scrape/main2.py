# Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to Chrome Driver 
path = "D:\Tutorials\ChromeDriver\chromedriver.exe"

# Create a service object and pass the chrome driver executable 
service = Service(executable_path= path)

# Initialize the chrome webdriver using the service object
driver = webdriver.Chrome(service=service)

# Open the website 
website = "https://www.ulta.com/brand/dior"
driver.get(website)

# Find all products elements
products = driver.find_elements(By.CLASS_NAME,"ProductListingResults__productCard")

# Initialize lists to store product details
name = []
description = []
msrp = []
image = []

# Loop through all the product cards to extract information 
for product in products:
    try:
        # Extract product details
        name1 = product.find_element(By.CLASS_NAME, "Text-ds--body-2").text
        desc1 = product.find_element(By.CLASS_NAME, "ProductCard__heading").text
        msrp1 = product.find_element(By.CLASS_NAME, "ProductCard__price").text
        img1  = product.find_element(By.TAG_NAME, "img").get_attribute('src')
        
        # Append data to the lists 
        name.append(name1)
        description.append(desc1)
        msrp.append(msrp1)
        image.append(img1)
        
    except Exception as e:  
        print(f"Error processing product: {e}")

# Create a DataFrame with Scraped data 
df = pd.DataFrame({
    'Name': name,
    'Description': description,
    'MSRP': msrp,
    'Image': image
})

# Print the dataframe 
print(df)

# Save the data to CSV file
df.to_csv("ulta_dior_products.csv", index=False)

time.sleep(50)
driver.quit()
