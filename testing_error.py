import requests
import datetime
import time

url = 'https://funpay.com/chips/16/'

def getDataFromURL():
    global count
    try:
        response = requests.get(url, headers={'accept-language': 'en-US,en;q=0.5',
                                              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

        print("status: " + str(response.status_code) + ", count requests: " + str(count))
        count = count + 1
    except Exception:
        print("End scan at " + str(datetime.datetime.now()))
        time.sleep(15)
        getDataFromURL()

print("Start scan at " + str(datetime.datetime.now()))
count = 1
while True:
    getDataFromURL()
