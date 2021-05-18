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
    telegram_info = [["", ""],
                     ["", ""]]
    for teletoken, chat_id in telegram_info:
        telegram_url = f"https://api.telegram.org/bot{teletoken}/sendMessage?chat_id={chat_id}&text={msg}"
        send=requests.get(telegram_url)
        send_image(chat_id,image,teletoken)
   
# TO BE NOTIFIED AND ALERTED BY THIS BOT VIA SMS SIGN UP FOR FREE IN THE WEBSITE https://www.vonage.com/ ,
# MAKE AN SMS APPLICATION YOU WILL BE GIVEN API KEY AND A SECRET KEY TO ENTER IN THEIR FIELDS BELOW IN THE FUNCTION sms


def sms(name, message, number, api_key, secret_key):
    client = vonage.Client(key=api_key, secret=secret_key)
    sms_client = vonage.Sms(client)

    responseData = sms_client.send_message(
        {
            "from": "Pool Bot",
            "to": number,
            "text": message,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print(f"Message sent successfully to {name}.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    # ADD YOUR INFORMATIONS HERE
    users_sms = [("NAME", "The POOL IS HERE CHECK IT OUT", "NUMBER", "API_KEY", "SECRET_KEY"), ()]
    for users_sms in users_sms:
        sms(*users_sms)

        
def alert_message(email_msg_subject, email_msg_body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # CONNECTING GMAIL ACCOUNT
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_address, email_pass)

        # E-MAIL COMPOSITION
        msg = f'Subject: {email_msg_subject}\n\n{email_msg_body}'
        # SENDING ALERT MESSAGE
        smtp.sendmail(email_address, recipients, msg)
      
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
            str_content = str(subs_content)
            content_list = [str_content[1249:1388]]
            
            if PREVIOUS_STATE == '':
                print('Bot starting...')
                telegram('Bot is starting...', "Capture.png")
                PREVIOUS_STATE = str_content
                run()
            elif not content_list:
                screenshot()
                email_msg_subject = "THE POOL IS HERE! CHECK IT OUT!"
                email_msg_body = f"THE POOL IS LOADING ! PLACES ARE VERY LIMITED!" \
                                 f"Click here {url}"
                tele_msg = f"THE POOL IS HERE! CHECK IT OUT! Click here {url}"
                telegram(tele_msg, "Capture.png")
                alert_message(email_msg_subject, email_msg_body)
                print("THE POOL IS HERE!!! CHECK IT OUT !!!")
            elif not subs_content or PREVIOUS_STATE != str_content:
                screenshot()
                email_msg_subject = "THE WEBSITE HAS CHANGED! CHECK IT OUT!"
                email_msg_body = "THE BOT DETECTED A CHANGE IN THE WEBSITE, See for your self!" \
                                 f"{url}"
                tele_msg = f"THE WEBSITE HAS CHANGED! CHECK IT OUT! Click here! {url}"
                telegram(tele_msg, "Capture.png")
                alert_message(email_msg_subject, email_msg_body)
                print("THE WEBSITE HAS CHANGED! CHECK IT OUT!")
            else:
                print("No pool yet")
            # ASSIGNING THE CURRENT STATE TO THE PREVIOUS STATE TO BE CHECKED ON THE NEXT LOOP
            PREVIOUS_STATE = str(subs_content)[1249:1388]
                
    except Exception as e:
        # RAISING EXCEPTION
        
        # CREATING ERROR MESSAGE
        error_body = str(e)
        error_sub = "Pool bot had an error!"
        error_msg = f'Subject: {error_sub}\n\n{error_body}'

        # SENDING ERROR E-MAIL
        if str(e) == "'NoneType' object has no attribute 'get'":
            print(e)
        else:
            alert_message(error_sub, error_body)
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
