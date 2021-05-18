from selenium import webdriver
import requests
import smtplib
import random
from bs4 import BeautifulSoup as bs
from config import *
import vonage
from datetime import datetime
import pytz
import time
import telepot

# CURRENT TIME
tz = pytz.timezone('Africa/Casablanca')
# GLOBAL VARS
PREVIOUS_STATE = ""
# HEADERS
headers = {
    "User-agent": 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J530F) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.105 Mobile Safari/537.36 '
}

def screenshot():
    browser= webdriver.Chrome("C:\\Users\\myrdp\\Desktop\\pool_jdid\\webdriver\\chromedriver.exe")
    browser.get("https://candidature.1337.ma/users/sign_in")
    user = ''
    password = ''
    email_box=browser.find_element_by_id("user_email")
    email_box.send_keys(user)
    pass_box=browser.find_element_by_id("user_password")
    pass_box.send_keys(password)
    login_button=browser.find_element_by_name("commit")
    login_button.submit()
    browser.save_screenshot("Capture.png")
    
# ENTER A TELEGRAM TOKEN AND CHAT IS TO BE NOTIFIED OF THE BOT STATUS OR IF ANY PROBLEMS OCCURRED


def send_image(chat_id,image,teletoken):

    bot = telepot.Bot(teletoken)

    # here replace chat_id and test.jpg with real things
    bot.sendPhoto(chat_id, photo=open(image, 'rb'))



def telegram(msg,image):
    teletoken="1791780483:AAH7nR7u0ZWZWqptMTYaOpGZl1jLNYWht-U"
    chat_id="-1001396783230"
    telegram_url=f"https://api.telegram.org/bot{teletoken}/sendMessage?chat_id={chat_id}&text={msg}"
    send=requests.get(telegram_url)
    send_image(chat_id,image,teletoken)


# TO BE NOTIFIED AND ALERTED BY THIS BOT VIA SMS SIGN UP FOR FREE IN THE WEBSITE https://www.vonage.com/ ,
# MAKE AN SMS APPLICATION YOU WILL BE GIVEN API KEY AND A SECRET KEY TO ENTER IN THEIR FIELDS BELOW IN THE FUNCTION sms


def sms():
    def sms_sender1():
        client = vonage.Client(key="", secret="")
        sms_client = vonage.Sms(client)

        responseData = sms_client.send_message(
            {
                "from": "Pool_Bot",
                "to": "",
                "text": "The pool is here! check it out. ",
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully to User 1.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    def sms_sender2():
        client = vonage.Client(key="", secret="")
        sms_client = vonage.Sms(client)

        responseData = sms_client.send_message(
            {
                "from": "Pool_Bot",
                "to": "",
                "text": "The pool is here! check it out. ",
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully to User 2.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    # YOU CAN ALWAYS ADD A NEW USER SMS FUNCTION

    # SEND NOW
    sms_sender1()
    sms_sender2()


def main():
    try:
        global PREVIOUS_STATE

        url = 'https://candidature.1337.ma/users/sign_in'
        with requests.session() as session:
            # GETTING HTML LOGIN PAGE AS LXML FORMAT
            response = session.post(url)
            soup_login = bs(response.text, 'lxml')

            # FINDING THE AUTH TOKEN
            auth = soup_login.find('meta', attrs={'name': 'csrf-token'}).get('content')
            data = {
                'authenticity_token': auth,
                'user[email]': user,
                'user[password]': password
            }

            # LOGGING IN AND GETTING MAIN HTML AS LXML FORMAT
            r_post = session.post(url, data=data)
            soup_check = bs(r_post.text, 'lxml')

            # FINDING A SPECIFIC VARIABLE IN THE UI TO NOTIFY THE USER IF CHANGED
            subs_content = soup_check.findAll('div', attrs={"id": "subs-content"})

            nav = soup_check.find("li", class_="disabled")
            no_pool = '''<li class="disabled"><a href="#">Piscine !</a></li>'''
            li_after = soup_check.find("li", class_="active").getText()
            d = str(nav)

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                # CONNECTING GMAIL ACCOUNT
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(email_address, email_pass)

                # E-MAIL COMPOSITION
                subject = "WA RAH L POOL (maybe) TLA7!!"
                body = "THE POOL IS LOADING !!!"
                msg = f'Subject: {subject}\n\n{body}'

                # COMPARING PREVIOUS AND CURRENT STATE
                if PREVIOUS_STATE == '':
                    print('Bot starting...')
                    telegram('Bot is starting...')
                    PREVIOUS_STATE = str(subs_content)[1249:1388]
                    run()
                elif str(subs_content)[1249:1388] != PREVIOUS_STATE or d != no_pool or li_after == "Piscine!":
                    # SENDING ALERT MESSAGE
                    screenshot()
                    smtp.sendmail(email_address, recipients, msg)
                    telegram("Rah lpool tla7 maybe","Capture.png")
                    sms()
                else:
                    print("No pool yet")
                # ASSIGNING THE CURRENT STATE TO THE PREVIOUS STATE TO BE CHECKED ON THE NEXT LOOP
                PREVIOUS_STATE = str(subs_content)[1249:1388]
    except Exception as e:
        # RAISING EXCEPTION
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            # LOGGING IN WITH THE SAME ACCOUNT
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_address, email_pass)

            # CREATING ERROR MESSAGE
            error_body = str(e)
            error_sub = "Pool bot had an error!"
            error_msg = f'Subject: {error_sub}\n\n{error_body}'

            # SENDING ERROR E-MAIL
            if str(e) == "'NoneType' object has no attribute 'get'":
                print(e)
            else:
                smtp.sendmail(email_address, recipients, error_msg)
                screenshot()
                telegram(f"An error occured! Error: {e}","Capture.png")
                print("Error message sent!")
            run()


def run():
    while True:
        main()
        # PAUSING THE SCRIPT FOR A RANDOM AMOUNT OF TIME TO AVOID 1337 STAFF ;)
        # 3s-10s

        def timer_func():
            timeout = random.randint(3, 10)
            while timeout:
                # CREATING A TIMER AND PRINTING TIME LEFT
                mins, secs = divmod(timeout, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print("\r", end='')
                print(f"Script is checking again in: {timer}", end="")
                time.sleep(1)
                timeout -= 1
            print('\nChecking again...')

        timer_func()

        # STATUS NOTIFIER
        h = datetime.now(tz).hour
        m = datetime.now(tz).minute
        s = datetime.now(tz).second

        phrases = ["Bot talking: Don't worry I'm working...", "Bot talking: Aghh! I'm working shut up...",
                   "Bot talking: I'm working! do you ?", "Bot talking: Do something else, I'm working!",
                   "Bot talking: Are you gonna watch me all day? Leave me alone, I'm working!",
                   "Bot talking: I'm doing my job!", "Bot talking: Working on it! so you don't have to dumbass"]
        random_fromlist = random.choice(phrases)

        def status():
            print("Getting bot status...")
            screenshot()
            telegram(random_fromlist,"Capture.png")
            print("Bot status sent.")

        if (h == 23 and m == 6 and s >= 0) and (h == 23 and m == 6 and s <= 10):
            status()
        elif (h == 7 and m == 1 and s >= 0) and (h == 7 and m == 1 and s <= 10):
            status()
        elif (h == 8 and m == 1 and s >= 0) and (h == 8 and m == 1 and s <= 10):
            status()
        elif (h == 9 and m == 1 and s >= 0) and (h == 9 and m == 1 and s <= 10):
            status()
        elif (h == 10 and m == 1 and s >= 0) and (h == 10 and m == 1 and s <= 10):
            status()
        elif (h == 11 and m == 1 and s >= 0) and (h == 11 and m == 1 and s <= 10):
            status()
        elif (h == 12 and m == 1 and s >= 0) and (h == 12 and m == 1 and s <= 10):
            status()
        elif (h == 13 and m == 1 and s >= 0) and (h == 13 and m == 1 and s <= 10):
            status()
        elif (h == 14 and m == 1 and s >= 0) and (h == 14 and m == 1 and s <= 10):
            status()
        elif (h == 15 and m == 1 and s >= 0) and (h == 15 and m == 1 and s <= 10):
            status()
        elif (h == 16 and m == 1 and s >= 0) and (h == 16 and m == 1 and s <= 10):
            status()
        elif (h == 17 and m == 1 and s >= 0) and (h == 17 and m == 1 and s <= 10):
            status()
        elif (h == 18 and m == 1 and s >= 0) and (h == 18 and m == 1 and s <= 10):
            status()
        elif (h == 19 and m == 1 and s >= 0) and (h == 19 and m == 1 and s <= 10):
            status()
        elif (h == 20 and m == 1 and s >= 0) and (h == 20 and m == 1 and s <= 10):
            status()
        elif (h == 21 and m == 1 and s >= 0) and (h == 21 and m == 1 and s <= 10):
            status()


if __name__ == '__main__':
    run()
