import requests


def send_to_telegram(message, id):

  apiToken = '5911694475:AAF66cTb5AS9plYubGzEQTrqx7LbaYtT0_A'
  chatID = id
  apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

  try:
    response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    # print(response.text)
    print("Message sent to Telegram")
  except Exception as e:
    print("Error sending message to Telegram")
    print(e)


def send(message):
  send_to_telegram(message, "5237588830")
  send_to_telegram(message, "591873121")
