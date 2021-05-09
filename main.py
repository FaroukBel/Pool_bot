from config import user, password
import requests
import time
from bs4 import BeautifulSoup as bs
import smtplib


def main():

    url = "https://candidature.1337.ma/users/sign_in"
    with requests.session() as session:
        response = session.post(url)

        soup_login = bs(response.text, 'lxml')
        auth = soup_login.find('meta', attrs={'name':'csrf-token'}).get('content')

        data = {
            'authenticity_token': auth,
            'user[email]': user,
            'user[password]': password
        }
        r_post = session.post(url, data=data)

        soup_check = bs(r_post.text, 'lxml')
        subs_content = soup_check.findAll('div', attrs={"id": "subs-content"})

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

            # EMAIL FIN AYTSAFT LIK NOTIFICATION
            email_address = ""
            # PASSWORD DYALO
            email_pass = ""

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email_address, email_pass)

            # Email composition
            subject = "WA RAH L POOL (maybe) TLA7!!"
            body = "THE POOL IS LOADING !!!"
            msg = f'Subject: {subject}\n\n{body}'

            # The equal sign in if statement just for checking if the code is working, for future use it will be =!
            if str(subs_content)[1249:1388] == "Aucune piscine n'est actuellement disponible. Pour être au courant dès qu'une nouvelle piscine s'ouvrira, tu peux nous follow sur twitter :":
                print('maaazal')
                smtp.sendmail(email_address, email_address, msg)


if __name__ == '__main__':
    for _ in range(10):
        main()
        time.sleep(5)