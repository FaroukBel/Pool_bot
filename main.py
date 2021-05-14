from PyQt5.Qt import QMainWindow, QApplication, QPushButton, QLineEdit
from PyQt5.QtCore import *
from PyQt5 import QtCore
import requests
import smtplib
import random
from bs4 import BeautifulSoup as bs
from config import *
import vonage
from datetime import datetime
import pytz
import time
from mainUi import Ui_PoolUi

# CURRENT TIME
tz = pytz.timezone('Africa/Casablanca')
# GLOBAL VARS
PREVIOUS_STATE = ""
# HEADERS
headers = {
    "User-agent": 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J530F) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.105 Mobile Safari/537.36 '
}


class Pool(QMainWindow, Ui_PoolUi):
    def __init__(self):
        super(Pool, self).__init__()
        self.setupUi(self)

        self.close_button.clicked.connect(lambda: self.close())
        self.maxi.clicked.connect(lambda: self.showMinimized())
        urlLink = f" <a href=\"https://candidature.1337.ma/users/sign_in\"> <font face=OCR A Extended size = 3 color=white>1337</font>" \
                  "<STYLE>A {text-decoration: none;} </STYLE></a>"
        urlLink_von = f" <a href=\"https://developer.nexmo.com/messaging/sms/overview\"> <font face=OCR A Extended size = 3 color=white>1. Check-out this website vonage.com and sign-up with your phone number.</font>" \
                  "<STYLE>A {text-decoration: none;} </STYLE></a>"
        self.l1337.setText(urlLink)
        self.vonage.setText(urlLink_von)

        self.sms.clicked.connect(self.sms_clicked)
        self.return_2.clicked.connect(self.return_main)
        self.add.clicked.connect(self.add_recipient)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.title_bar.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def add_recipient(self):
        rec_list = []
        x = 1
        for i in range(x):
            rec_list.append(QLineEdit())
            rec_list[i].setStyleSheet("color: rgb(255, 255, 255);border:none;border-radius:15px;"
                                                      "background-color: rgb(154, 154, 154);")
            rec_list[i].setMinimumHeight(40)
            rec_list[i].setAlignment(QtCore.Qt.AlignCenter)
            font = rec_list[i].font()
            font.setBold(True)
            font.setPointSize(12)
            font.setFamily("OCR A Extended")
            rec_list[i].setFont(font)
            rec_list[i].setPlaceholderText("E-mail")
            self.verticalLay.addWidget(rec_list[i])
        x += 1

    def return_main(self):
        self.stackedWidget.setCurrentIndex(0)

    def sms_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    # ENTER A TELEGRAM TOKEN AND CHAT IS TO BE NOTIFIED OF THE BOT STATUS OR IF ANY PROBLEMS OCCURRED


    def telegram(self, msg, teletoken, chat_id):
        telegram_url = f"https://api.telegram.org/bot{teletoken}/sendMessage?chat_id={chat_id}&text={msg}"
        requests.get(telegram_url, headers)

    # TO BE NOTIFIED AND ALERTED BY THIS BOT VIA SMS SIGN UP FOR FREE IN THE WEBSITE https://www.vonage.com/ ,
    # MAKE AN SMS APPLICATION YOU WILL BE GIVEN API KEY AND A SECRET KEY TO ENTER IN THEIR FIELDS BELOW IN THE FUNCTION sms


    def sms(self, name, message, number, api_key, secret_key):
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

        users_sms = [("Farouk", "The POOL IS HERE CHECK IT OUT", "212624879183", "", ""), ()]
        for users_sms in users_sms:
                self.sms(*users_sms)


    def alert_message(self, tele_msg, email_msg_subject, email_msg_body):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            # CONNECTING GMAIL ACCOUNT
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_address, email_pass)

            # E-MAIL COMPOSITION
            subject = email_msg_subject
            body = email_msg_body
            msg = f'Subject: {subject}\n\n{body}'
            # SENDING ALERT MESSAGE
            smtp.sendmail(email_address, recipients, msg)


    def main(self):
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

                # COMPARING PREVIOUS AND CURRENT STATE
                if PREVIOUS_STATE == '':
                    print('Bot starting...')
                    self.telegram('Bot is starting...', "", "")
                    PREVIOUS_STATE = str_content
                    self.run()
                elif not subs_content:
                    email_msg_subject = "THE POOL IS HERE! CHECK IT OUT!"
                    email_msg_body = f"THE POOL IS LOADING ! PLACES ARE VERY LIMITED!" \
                                     f"Click here {url}"
                    tele_msg = f"THE POOL IS HERE! CHECK IT OUT! Click here {url}"
                    self.alert_message(tele_msg, email_msg_subject, email_msg_body)
                    print("THE POOL IS HERE!!! CHECK IT OUT !!!")

                elif PREVIOUS_STATE != str_content:
                    email_msg_subject = "THE WEBSITE HAS CHANGED! CHECK IT OUT!"
                    email_msg_body = "THE BOT DETECTED A CHANGE IN THE WEBSITE, See for your self!" \
                                     f"{url}"
                    tele_msg = f"THE WEBSITE HAS CHANGED! CHECK IT OUT! Click here! {url}"
                    self.alert_message(tele_msg, email_msg_subject, email_msg_body)
                    print("THE WEBSITE HAS CHANGED! CHECK IT OUT!")
                else:
                    print("No pool yet")
                # ASSIGNING THE CURRENT STATE TO THE PREVIOUS STATE TO BE CHECKED ON THE NEXT LOOP
                PREVIOUS_STATE = str_content

        except Exception as e:
            # RAISING EXCEPTION
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

                # CREATING ERROR MESSAGE
                error_body = str(e)
                error_sub = "Pool bot had an error!"
                error_msg = f'Subject: {error_sub}\n\n{error_body}'
                self.alert_message(str(e))
                # SENDING ERROR E-MAIL
                if str(e) == "'NoneType' object has no attribute 'get'":
                    print(e)
                else:
                    smtp.sendmail(email_address, recipients, error_msg)
                    self.telegram(f"An error occured! Error: {e}", "", "")
                    print("Error message sent!")
                self.run()


    def run(self):
        while True:
            self.main()
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
                self.telegram(random_fromlist, "", "")
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
    import sys
    app = QApplication(sys.argv)
    window = Pool()
    window.show()
    sys.exit(app.exec())