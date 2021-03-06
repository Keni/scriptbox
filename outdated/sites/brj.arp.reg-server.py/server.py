# coding: utf-8
import re
from subprocess import Popen, PIPE
from smtplib import SMTP, SMTPException
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import parseaddr, formataddr

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.config.from_object(__name__)

IP = '0.0.0.0'
PORT = 8000

telegramBotUrl = "https://api.telegram.org/"
roomID = ''

ARP_COMMAND = '/usr/sbin/arp'
ARP_FLAGS = '-n'
MAC_REGEXP = r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})"

MAIL_SERVER = 'localhost'
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

SENDER = 'www@localhost'
RECIPIENTS = ['', '']

message_subject = 'Регистрация'
message_body = u"""
Имя: %s
Отдел: %s
Внутренний телефон: %s
Мобильный телефон: %s
IP: %s
MAC: %s
HOSTNAME: %s
"""


def send_email(name, department, phone_ext, phone, ip, mac, hostname):
    message = message_body % (name ,department, phone_ext, phone, ip, mac, hostname)
    
    send_mess(roomID, message)

    msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')
    msg['From'] = SENDER
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = unicode(message_subject, 'utf-8')

    try:
        smtp = SMTP(MAIL_SERVER)
        if MAIL_USERNAME:
            smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
        smtp.sendmail(SENDER, RECIPIENTS, msg.as_string())
        smtp.quit()
        return message
    except SMTPException as e:
        print 'Не удалось отправить письмо: %s' % str(e)
        return False


def get_mac_by_ip(ip_address):
    pid = Popen(["arp", "-n", ip_address], stdout=PIPE)
    s = pid.communicate()[0]
    try:
        mac = re.search(MAC_REGEXP, s).groups()[0]
    except:
        # mac = u'Не удалось определить'
        mac = u'Unknown'
    return mac

def get_hostname(ip_address):
    pid = Popen(["nbtscan", "-e", ip_address], stdout=PIPE)
    s = pid.communicate()[0]
    try:
        hostname = re.sub(ip_address, '', s)
    except:
        hostname = u'Unknown'
    return hostname

def validate_form(form):
    errors = {}
    if not form['name']:
        errors['name'] = u'Обязательное поле'
    if not form['department']:
        errors['department'] = u'Обязательное поле'
    if not form['phone_ext']:
        errors['phone_ext'] = u'Обязательное поле'
    if not form['phone']:
        errors['phone'] = u'Обязательное поле'
    return errors

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = request.post(telegramBotUrl + 'sendMessage', data=params)
    return response

@app.route("/", methods=['POST', 'GET'])
def index():
    errors = {}
    if request.method == 'POST':
        errors = validate_form(request.form)
        if not errors:
            if send_email(request.form['name'], request.form['department'], request.form['phone_ext'], request.form['phone'],
                request.remote_addr, get_mac_by_ip(request.remote_addr), hostname=get_hostname(request.remote_addr)):
                return render_template('success.html')
            else:
                errors['smtp'] = u'Ошибка отправки письма'
                return render_template('index.html', ip=request.remote_addr, mac=get_mac_by_ip(request.remote_addr), 
                                       hostname=get_hostname(request.remote_addr), errors=errors)
    return render_template('index.html', ip=request.remote_addr, mac=get_mac_by_ip(request.remote_addr), 
                           hostname=get_hostname(request.remote_addr), errors=errors)

if __name__ == "__main__":
    app.run(IP, PORT)
