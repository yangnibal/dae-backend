import smtplib
from email.mime.text import MIMEText

def send_id(email, username, receiver):
    send = 'lsy4255@gmail.com'
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    #import pdb; pdb.set_trace()
    smtp.login(send, '0462love@@')

    msg = MIMEText(receiver+"님의 아이디는 "+username+"입니다.")
    msg['To'] = email
    msg['Subject'] = "대외비 아이디 확인"
    smtp.sendmail(send, email, msg.as_string())
 
    smtp.quit()

def init_pw(email, username, receiver, password):
    send = 'lsy4255@gmail.com'
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    #import pdb; pdb.set_trace()
    smtp.login(send, '0462love@@')

    msg = MIMEText(receiver+"님의 비밀번호가 "+password+"로 초기화 되었습니다.")
    msg['To'] = email
    msg['Subject'] = "대외비 비밀번호 초기화"
    smtp.sendmail(send, email, msg.as_string())

    smtp.quit()