import tkinter as tk
from tkinter import ttk

import requests
from bs4 import BeautifulSoup
from Seller import Seller
from SellersSet import SellersSet

url = 'https://funpay.ru/en/chips/16/'

server_labels = {}
window = tk.Tk()
combobox_servers = None
server_name = tk.StringVar()
is_send_telegram = tk.BooleanVar()

# EDITABLE
chat_id = "820834588"
time_refresh = 1000
input_in_stock = 32
input_price = 7.27
server_id = None

pattern_message = "Price:%20{price}%0AAmount:%20{amount}%0ALink:%20{link}"

RUNNING = True  # Global flag -> when app is starting then it is alredy running

sellers = SellersSet()


def getDataFromURL():
    response = requests.get(url, headers={"accept-language": "en-US,en;q=0.5"})
    root = BeautifulSoup(response.text, 'lxml')
    return root


def get_servers(root):
    for servers in root.find_all("select", attrs={"name": "server"}):
        for server in servers.find_all('option'):
            if server['value'] and server.text:
                server_labels[server.text] = server['value']


def get_online_sellers(root):
    for s in root.find_all(class_="tc-item", attrs={"data-server": server_id}):
        seller = Seller(s['href'], int(s.find(class_="tc-amount").text.replace(" ", "")),
                        float(s.find(class_="tc-price").div.text.replace(" ₽", "")))
        # print(seller)

        if s.has_attr('data-online'):
            sellers.add(seller)
        else:
            sellers.remove(seller)


def get_best_sellers(root):
    get_online_sellers(root)
    cheapest_sellers = SellersSet()
    # get cheapest
    for s in sellers.set:
        if s.price <= input_price:
            # if we have define amount of items in stock then filtering
            if input_in_stock != 0:
                if s.amount >= input_in_stock:
                    cheapest_sellers.add(s)
            else:
                cheapest_sellers.add(s)
    return cheapest_sellers


def send_telegram(msg):
    requests.get(
        'https://api.telegram.org/bot1650132772:AAFKhBoYLpdfkzDlKmsFyN7aEbb930MQx8s/sendMessage?chat_id=' + chat_id + '&text=' + msg)


def scanning():
    if RUNNING:
        best_sellers = get_best_sellers(getDataFromURL())
        print(len(best_sellers.set))
        # how to make best seller affect to sellers
        for best_seller in best_sellers.set:
            if not best_seller.isSend:
                msg = pattern_message.format(price=str(best_seller.price),
                                             amount=str(best_seller.amount),
                                             link=best_seller.link)
                if is_send_telegram.get():
                    send_telegram(msg)
                    best_seller.sended()

    window.after(time_refresh, scanning)


def start_scan():
    global RUNNING, server_id
    if start_scan['text'] == "Start scannning...":
        RUNNING = True
        start_scan.configure(text="Stop!")
        status_label.config(text="Running..")
        server_id = server_labels.get(combobox_servers.get())
    else:
        RUNNING = False
        start_scan.configure(text="Start scannning...")
        status_label.config(text="has stopped...")
        server_id = None
        sellers.clear()


def stop_scan():
    global RUNNING, server_id
    RUNNING = False
    start_scan.configure(text="Start scannning...")
    status_label.config(text="has stopped...")
    server_id = None
    sellers.clear()


# Define here buttons to use global
# GUI Buttons
start_scan = ttk.Button(window, text="Stop!", command=start_scan)
status_label = tk.Label(window, text="Running..")


def main():
    global combobox_servers, server_id
    is_send_telegram.set(False)
    get_servers(getDataFromURL())

    window.title("Quick helper")
    tk.Label(window, text='Choose server', bd=3).grid(row=0, column=0)

    combobox_servers = ttk.Combobox(window, values=list(server_labels.keys()), justify="center",
                                    textvariable=server_name, state="readonly")
    combobox_servers.bind('<<ComboboxSelected>>', lambda event: stop_scan())
    combobox_servers.grid(row=0, column=1)
    # 3 == PC(STANDART)
    combobox_servers.current(3)
    server_id = server_labels.get(combobox_servers.get())

    checkButtonSendTelegram = ttk.Checkbutton(window, text="Send Telegram ", var=is_send_telegram)
    checkButtonSendTelegram.grid(row=0, column=2)
    start_scan.grid(row=1, column=1)
    status_label.grid(row=2, column=0)

    window.after(time_refresh, scanning)  # After 1 second, call scanning
    window.mainloop()


if __name__ == '__main__':
    main()
