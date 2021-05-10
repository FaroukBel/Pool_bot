import requests
import time
import smtplib
import random
from bs4 import BeautifulSoup as bs
from config import *
import vonage

headers={"User-agent":'Mozilla/5.0 (Linux; Android 8.1.0; SM-J530F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36'}

def telegram(msg):
    teletoken=""
    chat_id=""
	telegram_url=f'https://api.telegram.org/bot{teletoken}/sendMessage?chat_id={chat_id}&text={msg}'
	send=requests.get(telegram_url,headers)
    
def Sms():
  def sms_senderyounes():
    client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Pool_Bot",
            "to": "",
            "text": "rah tla7 lpool azaml ",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully to younes.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
  

  def sms_sendermohamed():
    client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Pool_Bot",
            "to": "",
            "text": "rah tla7 lpool azaml    ",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully to mohamed .")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


  def sms_sendersaid():
    client = vonage.Client(key="", secret="")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Pool_Bot",
            "to": "",
            "text": "rah tla7 lpool azaml    ",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully to mohamed .")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

  #sendnow 
  sms_senderyounes()
  sms_senderoussama()
  sms_sendersaid()

# GLOBAL VARS
PREVIOUS_STATE = ""


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
            nav=soup_check.find("li",class_="disabled")
            poolmakaynx='''<li class="disabled"><a href="#">Piscine!</a></li>'''
            li_after=soup_check.find("li",class_="active").getText()
            d=str(nav)
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
                    PREVIOUS_STATE = str(subs_content)[1249:1388]
                    run()
                elif str(subs_content)[1249:1388] != PREVIOUS_STATE or d != poolmakaynx or li_after =="Piscine!" :
                    # SENDING ALERT MESSAGE
                    smtp.sendmail(email_address, email_address, msg)
                    telegram("rah lpool tla7 maybe")
                    Sms()
                    print("Message sent!")
                else:
                    print("no pool yet")
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
            smtp.sendmail(email_address, email_address, error_msg)
            telegram("dok wlad l97ab ma3tawnix token")
            print("Error message sent!")
            print(e)
            run()


def run():
    while True:
        main()
        # PAUSING THE SCRIPT FOR A RANDOM AMOUNT OF TIME TO AVOID 1337 STAFF ;)
        # 2min-10min

        def timer_func():
            timeout = random.randint(5, 20)
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


if __name__ == '__main__':
    run()