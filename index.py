import datetime
import wget
import smtplib
import os
import re

url = "http://www.estofex.org/cgi-bin/polygon/showforecast.cgi?listvalid=yes"

no_alert_string = "<P> No valid Storm Forecast available.</P>"

to_email = 'tamaskelemen.kt@gmail.com'

file_name = 'index.html'
old_file_name = 'old_index.html'
file_exists = os.path.isfile(file_name)


def delete_old_file():
    if os.path.isfile(old_file_name):
        os.remove(old_file_name)


def send_email(to, msg):
    try:
        # email kuldes az eredmenyrol
        sender = 'tomizulu@gmail.com'
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('tomizulu@gmail.com', 'praclin18')
        server.sendmail(sender, to, msg)

    except Exception as e:
        print(e)
        print("Something went wrong while sending email...")


# megnezi, van e kulonbseg az elozo allapotjelenteshez kepest.
# returns bool
def kulonbseg_checker():
    try:
        info_table = re.search('<DIV CLASS="title">Forecasts</DIV>', file_content)

        print("VERJEM", )

    except AttributeError:
        print("The table, containing the information was not found in file")
        info_table = ''

    return True


delete_old_file()

if file_exists:
    os.rename(file_name, 'old_' + file_name)

wget.download(url, out=file_name)

if os.path.isfile(file_name):
    print(datetime.datetime.now())
    print("Filedownload OK -- " + file_name)
else:
    print("File download ERROR")
    exit(404)


# open the file
f = open('index.html', 'r')
file_content = f.read()


if no_alert_string in file_content:
    # ha nincs riasztas, akkor a regit is toroljuk, es csak a legfrissebb allapot marad
    print("There is no storm activity right now")
    # delete_old_file()
else:
    # ha van riasztas, megnezzuk, van e kulonbseg az eggyel elozo allapothoz kepest
    print("RIASZTAAAS")


van_e_kulonbseg = kulonbseg_checker()

if van_e_kulonbseg:
    msg = 'van kulonbseg az elozo riasztashoz kepes'
    # send_email(to_email, msg)
else:
    # nincs kulonbseg
    delete_old_file()


# send_email('tamaskelemen.kt@gmail.com', 'Sikeresen lefutott a cron. Ne felejstd el ezt az emailt kiszedni!')


