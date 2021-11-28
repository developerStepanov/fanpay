import tkinter as tk
import requests
from tkinter import ttk
from bs4 import BeautifulSoup

# EDITABLE
chat_id = "820834588"
time_refresh = 1000

url = 'https://funpay.ru/en/chips/16/'
response = requests.get(url, headers={"accept-language":"en-US,en;q=0.5"})
root = BeautifulSoup(response.text, 'lxml')

server_labels = {}
window = tk.Tk()
server_name = tk.StringVar()
sellers = []

input_in_stock = 0
input_price = 6.98

cache_sellers = []

is_send_telegram = tk.BooleanVar()

pattern_message = "Price:%20{price}%0AAmount:%20{amount}%0ALink:%20{link}"

RUNNING = True # Global flag -> when app is starting then it is alredy running

def get_servers():
    for servers in root.find_all("select", attrs={"name" : "server"}):
        for server in servers.find_all('option'):
            if server['value'] and server.text:
                server_labels[server.text] = server['value']

def get_best_sellers():
    sellers = []
    sellers_ = root.find_all(class_ = "tc-item")
    cheapest_sellers = []

    for seller in sellers_:
        if seller.has_attr('data-online'):
            sellers.append(
                            {
                                "link":     seller['href'],
                                "amount":   int(seller.find(class_ = "tc-amount").text.replace(" ", "")),
                                "price":    float(seller.find(class_ = "tc-price").div.text.replace(" ₽", "")),
                                "sent":     False
                            }
            )
        else:
            # 1. if person in cache is offline remove him
            for cache_seller in cache_sellers[:]:
                if seller['href'] == cache_seller['link']:
                    cache_sellers.remove(cache_seller)

    # get cheapest
    for seller in sellers:
        if seller['price'] <= input_price:
            # if we have define amount of items in stock then filtering
            if input_in_stock != 0:
                if seller['amount'] >= input_in_stock:
                    cheapest_sellers.append(seller)
            else:
                cheapest_sellers.append(seller)
    # print(cheapest_sellers)
    return cheapest_sellers

def send_telegram(msg):
    requests.get('https://api.telegram.org/bot1650132772:AAFKhBoYLpdfkzDlKmsFyN7aEbb930MQx8s/sendMessage?chat_id=' + chat_id + '&text=' + msg)

def scanning():
    global cache_sellers
    if RUNNING:
        best_sellers = get_best_sellers()

        # to do
        # for cache_seller in cache_sellers:
        #     for best_seller in best_sellers:
        #         if cache_seller['link'] == best_seller['link'] and cache_seller['price'] == best_seller['price'] and cache_seller['amount'] == best_seller['amount']:
        #             cache_sellers.remove(cache_seller)

        for best_seller in best_sellers:
            cache = False
            for cache_seller in cache_sellers:
                if cache_seller['link'] == best_seller['link']:
                    if cache_seller['price'] == best_seller['price'] and cache_seller['amount'] == best_seller['amount']:
                        cache = True
                        print("2")
                    # 2. check if sellers in cache are still the best sellers if not remove it from the cache !!!!! not update
                    else:
                        cache = False
                        cache_sellers.remove(cache_seller)
                        print("4")
            # for new ones
            if not cache:
                cache_sellers.append(best_seller)
                print("3")

        print(cache_sellers)

        for cache_seller in cache_sellers:
            if not cache_seller['sent']:
                msg = pattern_message.format(price=str(cache_seller['price']), amount=str(cache_seller['amount']), link=cache_seller['link'])
                if is_send_telegram.get():
                    send_telegram(msg)
                    cache_seller['sent'] = True

    window.after(time_refresh, scanning)

def start_scan():
    global RUNNING
    if start_scan['text'] == "Start scannning...":
        RUNNING = True
        start_scan.configure(text="Stop!")
        status_label.config(text="Running..")
    else:
        RUNNING = False
        start_scan.configure(text="Start scannning...")
        status_label.config(text="has stopped...")


# Define here buttons to use global
# GUI Buttons
start_scan = ttk.Button(window, text="Stop!", command=start_scan)
status_label = tk.Label(window, text="Running..")

def main():
    is_send_telegram.set(False)

    get_servers()

    window.title("Quick helper")
    tk.Label(window, text='Choose server', bd=3).grid(row=0, column=0)

    combobox_servers = ttk.Combobox(window, values=list(server_labels.keys()), justify="center", textvariable=server_name, state="readonly")
    # combobox_servers.bind('<<ComboboxSelected>>', lambda event: print(server_labels[server_name.get()]))
    combobox_servers.grid(row=0, column=1)
    combobox_servers.current(0)

    checkButtonSendTelegram = ttk.Checkbutton(window, text="Send Telegram ", var=is_send_telegram)

    checkButtonSendTelegram.grid(row=0, column=2)
    start_scan.grid(row=1, column=1)
    status_label.grid(row=2, column=0)

    window.after(time_refresh, scanning)  # After 1 second, call scanning
    window.mainloop()

if __name__ == '__main__':
    main()
