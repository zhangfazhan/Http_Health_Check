# -*- coding: utf-8 -*-


import sys
import time
import requests
import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header
from config import config

# 邮件参数
my_sender = config['from_email']
my_pass = config['password']
mail_host = config['mail_host']
to_email = config['to_email']
subject = config['subject']
mail_port = config['mail_port']


# http参数
url = config['url']
data = config['data']
method = config['method']
server_name = config['server_name']


# 检查参数
check_Intervals = config['check_Intervals']
check_total = config['check_total']
error_num = config['error_num']


def sent_email(email_content):
    msg = MIMEText(email_content, 'plain', 'utf-8')
    msg['From'] = Header('HEALTH CHECKER', 'utf-8')
    msg['To'] = Header('USER', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP()
    server.connect(mail_host, mail_port)
    server.login(my_sender, my_pass)
    server.sendmail(my_sender, to_email, msg.as_string())
    server.quit()


def get_response_code():
    if method == 'post':
        response = requests.post(url=url, data=json.dumps(data))
        return response.status_code
    if method == 'get':
        response = requests.get(url=url, data=json.dumps(data))
        return response.status_code


def health_cheak():
    while True:
        counter = 0
        error_code_counter = {}
        content = """
         SERVER: {} ERROR !!!
         
         SERVER URL:  {}
         TOTAL CHECK: {}
         ERROR NUM:   {}
         ERROR CODE:  {}
    
         ^_^  Please confirm as soon as possible ^_^
        """
        for i in range(check_total):
            error_code = get_response_code()

            if error_code not in error_code_counter:
                error_code_counter[error_code] = 1
            else:
                error_code_counter[error_code] += 1

            if error_code != 200:
                counter += 1

        if counter >= error_num:
            sent_email(content.format(server_name, url, check_total, counter, str(error_code_counter)))
            sys.exit()

        time.sleep(check_Intervals)


if __name__ == '__main__':
    health_cheak()