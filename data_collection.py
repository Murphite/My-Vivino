import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# connecting to the browser
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
# defining the url
url = "https://www.vivino.com/US/en/"
driver.get(url)

# we will have to navigate to the homepage and then click on the wines link to go to the wines pages before scraping
page = driver.find_element(By.CLASS_NAME, 'menuLink_text__nDfIV').click()

# after navigating into the wines page, we then wait for 15 seconds before scraping
time.sleep(10)
# this is where i want to deselect all the types of wines I do not want and leave only the one I need
buttons = driver.find_elements(By.CLASS_NAME, 'filterByWineType__pill--DDMJ3')
not_click = buttons[4]
for button in buttons[:6]:
    if button != not_click:
        button.click()
        time.sleep(3)
# defining the number of files to look for before collecting the data
num_of_items = 100  
result = driver.find_elements(By.CLASS_NAME, 'wineCard__wineCard--2dj2T')
while(len(result) <=num_of_items) :
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    result = driver.find_elements(By.CLASS_NAME, 'wineCard__wineCard--2dj2T')
    time.sleep(5)
result_list = []

# iterating through the collected items and collecting wine informations
for item in result:
    try:
        brand = item.find_element(By.CLASS_NAME, 'wineInfoVintage__truncate--3QAtw').text
    except:
        brand = 'nan'
    try:
        name = item.find_element(By.CLASS_NAME, 'wineInfoVintage__wineInfoVintage--bXr7s').text
    except:
        name = 'nan'
    try:
        location = item.find_element(By.CLASS_NAME, 'wineInfoLocation__wineInfoLocation--BmkcO').text
    except: 
        location = 'nan'
    try:
        rating = item.find_element(By.CLASS_NAME, 'vivinoRating_averageValue__uDdPM').text
    except:
        rating = 'nan'
    try:
        nbr_rating = item.find_element(By.CLASS_NAME, 'vivinoRating_caption__xL84P').text
    except:
        nbr_rating = 'nan'
    try:
        price = item.find_element(By.CLASS_NAME, 'addToCartButton__price--qJdh4 div:nth-child(2)').text
    except:
        price = item.find_element(By.CLASS_NAME, 'addToCart__ppcPrice--ydrd5').text

    # inserting into a diction so it can used to create a pandas dataframe   
    temp_dict = {"Brand":brand, "Name":name, "Location":location, "Rating":rating, "Number of Ratings":nbr_rating, "Price":price}
    result_list.append(temp_dict)
    print(f"Wine No. {len(result_list)} collected")
    
# convert it to a pandas dataframe so it can be saved to a csv file
df = pd.DataFrame(result_list)
df.to_csv('vivino_dataset_fortified.csv', index = False)

# closing the browser
driver.close()

