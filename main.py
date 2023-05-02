import datetime
import time
import price_detect
import pandas as pd
import tele_bot as tb
#read in the check file
#check the current price from check file
#compare the current price with the record price
#write the record in the record file


def get_price():
  #read the trip_list
  trip_list = open("trip_list", "r")
  trip_list = trip_list.read()
  trip_list = trip_list.split("\n")
  for i in trip_list:
    trip_info = i.split(":")
    depart_city = trip_info[0]
    arrive_city = trip_info[1]
    depart_date = trip_info[2]
    try:
      print("Scraping Started", depart_city, arrive_city, depart_date)
      price_list = price_detect.get_price(depart_city, arrive_city,
                                          depart_date)
      #add the price_list to price database
      price_database = open("price_database", "a")
      for g in price_list:
        price_database.write(g + "\n")
      price_database.close()
      print("Scraping Success", depart_city, arrive_city, depart_date)
    except:
      print("Error Scraping", depart_city, arrive_city, depart_date)


def price_compare():
  print("Price Compare Started")
  price_database = open("price_database", "r")
  price_database = price_database.read()
  price_database = price_database.split("\n")
  price_database = price_database[:-1]
  all_data = []
  for i in price_database:
    i = i.split(",")
    all_data.append(i)

  df = pd.DataFrame(all_data,
                    columns=[
                      "Airline", "Price", "Time", "Departure", "Arrival",
                      "Flight Time"
                    ])
  df["Time"] = pd.to_datetime(df["Time"])
  airline_list = df["Airline"].unique()
  for i in airline_list:
    airline_df = df[df["Airline"] == i]
    #sort by time, newest time on top
    airline_df = airline_df.sort_values(by="Time", ascending=False)
    #get the latest price
    latest_price = airline_df["Price"].iloc[0]
    #get the lowest price
    lowest_price = airline_df["Price"].min()
    #is lowest_price unique value?
    if len(airline_df[airline_df["Price"] == lowest_price]) == 1:
      if latest_price == lowest_price and len(airline_df) > 1:
        isplit = i.split(":")
        code = "WN" + isplit[0]
        depart_time = isplit[1]
        previous_price = airline_df["Price"].iloc[1]
        message = ("[Price Alert]\n" + code + " " + depart_time + "\n" +
                   "Lowest Price Hit $" + str(lowest_price) +
                   "\nPrevious Price $" + previous_price + "\n" +
                   airline_df["Departure"].iloc[0] + " -> " +
                   airline_df["Arrival"].iloc[0] + "\nFlight Time: " +
                   airline_df["Flight Time"].iloc[0])
        tb.send(message)
  now = datetime.datetime.now()
  print("Price Compare Ended at", now)


def price_summary():
  print("Price Summary Started")
  price_database = open("price_database", "r")
  price_database = price_database.read()
  price_database = price_database.split("\n")
  price_database = price_database[:-1]
  all_data = []
  for i in price_database:
    i = i.split(",")
    all_data.append(i)

  df = pd.DataFrame(all_data,
                    columns=[
                      "Airline", "Price", "Time", "Departure", "Arrival",
                      "Flight Time"
                    ])
  df["Time"] = pd.to_datetime(df["Time"])
  airline_list = df["Airline"].unique()
  summmary_message = "====Daily Summary====\n"
  for i in airline_list:
    airline_df = df[df["Airline"] == i]
    #sort by time, newest time on top
    airline_df = airline_df.sort_values(by="Time", ascending=False)
    #get the latest price
    latest_price = airline_df["Price"].iloc[0]
    #get the lowest price
    lowest_price = airline_df["Price"].min()
    isplit = i.split(":")
    code = "WN" + isplit[0]
    depart_time = isplit[1]
    if latest_price == lowest_price:
      summmary_message += ("[**Lowest Price] " + depart_time + " " +
                           airline_df["Departure"].iloc[0] + " -> " +
                           airline_df["Arrival"].iloc[0] + " $" +
                           latest_price + "\n")
    else:
      summmary_message += depart_time + " " + airline_df["Departure"].iloc[
        0] + " -> " + airline_df["Arrival"].iloc[0]
      summmary_message += " CP: $" + latest_price + " LP: $" + lowest_price + "\n"
    summmary_message += airline_df["Flight Time"].iloc[0] + " " + code + " \n\n"
  tb.send(summmary_message)
  now = datetime.datetime.now()
  print("Price Summary Ended at", now)

if __name__ == "__main__":
  # while True:
  now = datetime.datetime.now()
  get_price()
  price_compare()
  if now.hour == 14:
    price_summary()
    # time.sleep(3600)
