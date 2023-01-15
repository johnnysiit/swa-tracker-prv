###Test on 2023-01-01, working
#    pkgs.chromium
#    pkgs.chromedriver
def get_price(depart_city, arrive_city, depart_date):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    import time
    import pandas as pd
    import datetime

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("window-size=1000,600")
    #chrome_options.add_argument("user-agent= chrome on mac os newest
    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.3729.169 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service_log_path='NULL', options=chrome_options)

    url = "https://www.southwest.com/air/booking/select.html?adultPassengersCount=1&adultsCount=1&clk=GSUBNAV-AIR-BOOK&departureDate="+depart_date+"&departureTimeOfDay=ALL_DAY&destinationAirportCode="+arrive_city+"&fareType=USD&originationAirportCode="+depart_city+"&passengerType=ADULT&returnDate=&returnTimeOfDay=ALL_DAY&tripType=oneway"

    driver.get(url)
    driver.implicitly_wait(20)
    # try:
    #     driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[2]/div/div/section/div[2]/div[2]/div/form/div[2]/div[9]/button").click()
    #     driver.implicitly_wait(20)
    # except:
    #     pass
    
    non_stop = driver.find_element(By.XPATH, "//*[@id='air-booking-product-0']/div[4]/div/fieldset/label/button")
    non_stop.click()

    results_table = driver.find_element(By.XPATH, "//li[@class='air-booking-select-detail']")
    flights = results_table.find_elements(By.XPATH, "//span[@class='actionable--text']")
    dtime = results_table.find_elements(By.XPATH, "//span[@class='time--value']")

    all_data = ""
    for flight in flights:
        if flight.text.startswith("$") or flight.text.startswith("#"):
            all_data = all_data + flight.text + "\n"

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

    

    #remove element endling with "left"
    all_data = all_data.split("\n")
    all_data = [i for i in all_data if not i.endswith("left")]
    all_data = "\n".join(all_data)

    driver.close()

    all_data = all_data[all_data.find("#"):]
    all_data = all_data.split("#")[1:]

    price_all = {}
    price_list = []
    for i in all_data:
        index = all_data.index(i)
        splited_price = i.split("\n")
        splited_price = list(filter(None, splited_price))
        airline = splited_price[0].replace(" ", "")
        airline = airline + ":" + depart_date
        price = float(splited_price[-1].replace("$", ""))
        price_all[splited_price[0]] = price

        now = datetime.datetime.now()
        output = airline + "," + str(price) + "," + str(now) + "," + depart_city + "," + arrive_city + "," + result[index]
        price_list.append(output)
    return price_list
