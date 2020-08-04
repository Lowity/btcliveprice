import smtplib
import requests
import json
import time
import locale

sender_email = ""
rec_email = ""
password = ""
text = ""
subject = "Alert"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, password)
print("Login success")

api = 'https://blockchain.info/ticker'
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def get_value():
    response =  requests.get(api)
    data = json.loads(response.content)
    value = data['CHF']['last']
    brl = locale.currency(value, grouping=True, symbol=None)
    return brl

def view():
    value = get_value()
    new_price = True
    print("1 BTC = %s CHF"%value)
    text = "1 BTC = %s CHF"%value
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server.sendmail(sender_email, rec_email, message)
    while True:
        current_value = get_value()
        if current_value < value:
            print("[-] DOWN, 1 BTC = %s CHF [-]"%current_value)
            text = "[-] DOWN, 1 BTC = %s CHF [-]"%current_value
            message = 'Subject: {}\n\n{}'.format(subject, text)
            server.sendmail(sender_email, rec_email, message)
            new_price = True
        elif current_value > value:
            print("[+] UP, 1 BTC = %s [+]"%current_value)
            text = "[+] UP, 1 BTC = %s [+]"%current_value
            message = 'Subject: {}\n\n{}'.format(subject, text)
            server.sendmail(sender_email, rec_email, message)
            new_price = True
        else:
            if new_price == True:
                print("[=] Waiting new price [=]\n")
                text = "[=] Waiting new price [=]\n"
                #message = 'Subject: {}\n\n{}'.format(subject, text)
                #server.sendmail(sender_email, rec_email, message)
                new_price = False
        value = current_value
        time.sleep(300)

view()