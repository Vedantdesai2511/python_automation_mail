from bs4 import BeautifulSoup
import requests
import pickle
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from _datetime import datetime
import time


def run_code():
    list_ = ["USD Index", "AUDUSD", "EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]

    Dict = {}
    Changed_probability_pairs = {}

    for idx, x in enumerate(list_):
        if x in Dict:
            pass
        else:
            Dict[x] = ""

    print(Dict)
    page1 = requests.get('https://docs.google.com/spreadsheets/d/15Az6QQ5yaGh1giAME-5dKT3YABFqHvF7nqTbQS4bF5Y/edit'
                         '#gid=0')

    soup1 = BeautifulSoup(page1.text, 'html.parser')

    elements = soup1.find('table', attrs={'class': 'waffle'}).find_all(class_="s20")

    for idx, element in enumerate(elements):
        print("1")
        ele = str((element.renderContents()))[2:][:-1]
        if ele == "YES":
            Dict[list_[idx]] = "YES"
        else:
            Dict[list_[idx]] = "NO"

    with open('data.pickle', 'rb') as f:
        list_from_pickle = pickle.load(f)

    for i in Dict:
        print(i)
        if Dict[i] == list_from_pickle[i]:
            Changed_probability_pairs[i] = 'False'
            print("same as before")
        else:
            Changed_probability_pairs[i] = f'True'
            print("different")

    print(list_from_pickle)
    print(Dict)

    with open('data.pickle', 'wb') as f:
        pickle.dump(Dict, f)

    # Send Email

    sender_email = "verdantlee1@gmail.com"
    receiver_email = "verdantlee1@gmail.com"
    password = "VerdantLee@12345"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Probability Sheet"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""

    html = """\
        <table border='1'>
        <tr><th>Symbol</th><th>Old Probability</th><th>New Probability</th><th>Changed?</th></tr>"""
    for sym in Dict:
        html = html + "<tr>"
        html = html + "<td>" + sym + "</td>"
        html = html + "<td>" + list_from_pickle[sym] + "</td>"
        html = html + "<td>" + Dict[sym] + "</td>"
        if Changed_probability_pairs[sym] == "True":
            html = html + "<td> <b>" + Changed_probability_pairs[sym] + "</b> </td>"
        else:
            html = html + "<td>" + Changed_probability_pairs[sym] + "</td>"
        html = html + "</tr>"
    html = html + "</table>"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


run_code()


def start_main_while_loop_exactly_on_time():
    while True:
        a = datetime.now()
        current_time_second_ = int(a.strftime("%S"))
        current_time_minute = int(a.strftime("%M"))
        current_time_hour_ = int(a.strftime("%H"))
        # print(current_time_second_)
        # time.sleep(5)
        if current_time_hour_ == 9 and current_time_minute == 24 and current_time_second_ == 00:
            run_code()


while True:
    a = datetime.now()
    current_time_second = a.strftime("%S")
    current_time_second = float(current_time_second)
    print(current_time_second)
    if current_time_second == 20:
        start_main_while_loop_exactly_on_time()

# credit - https://realpython.com/python-send-email/
