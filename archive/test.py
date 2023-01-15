from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service_log_path='NULL', options=chrome_options)
depart_city = "MDW"
arrive_city = "PHX"
depart_date = "2023-03-03"
url = "https://www.southwest.com/air/booking/select.html?adultPassengersCount=1&adultsCount=1&clk=GSUBNAV-AIR-BOOK&departureDate="+depart_date+"&departureTimeOfDay=ALL_DAY&destinationAirportCode="+arrive_city+"&fareType=USD&originationAirportCode="+depart_city+"&passengerType=ADULT&returnDate=&returnTimeOfDay=ALL_DAY&tripType=oneway"
driver.get(url)
driver.implicitly_wait(20)

non_stop = driver.find_element(By.XPATH, "//*[@id='air-booking-product-0']/div[4]/div/fieldset/label/button")
non_stop.click()

results_table = driver.find_element(By.XPATH, "//li[@class='air-booking-select-detail']")
flights = results_table.find_elements(By.XPATH, "//span[@class='actionable--text']")
dtime = results_table.find_elements(By.XPATH, "//span[@class='time--value']")

time_data = ""
for i in dtime:
    time_data += i.text + "\n"
time_date = time_data.replace(" ", "")
time_date = time_date.split("\n")
new_time_date = []
#combine 1st and 2nd element, 3rd and 4th element, etc.
result = []
for i in range(0, len(time_date)-1, 2):
    result.append(str(time_date[i]+"~"+time_date[i+1]))

print (result)