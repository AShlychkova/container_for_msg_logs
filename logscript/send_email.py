#!/Users/alexandrashlychkova/anaconda2/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import platform
import json
import time, calendar
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import urllib2, smtplib, sys, os

def parseConfig (configFileName):
    configFile = open (configFileName, 'r')
    configText=""
    for line in configFile:
        configText += line #[:-1] #delete /n in the end
    config = json.loads(configText,encoding='utf-8')

    global emailSubject
    emailSubject=config["mailSubject"]
    
    global emailServer
    emailServer=config["mailServerAddsress"]
    
    global emailPort
    emailPort=int(config["mailServerPort"])
    
    global receiverEmail
    receiverEmail=config["receiverEmail"]
    
    global emailUsername
    emailUsername=config["senderEmail"]
    
    global emailPassword
    emailPassword=config["senderPassword"]
    
    global emailText
    emailText=config["mailText"]

    global zipFile
    zipFile=config["zipFile"]

    global zipFilePDF
    zipFilePDF=config["zipFilePDF"]

def sendEmail():
    msg = MIMEMultipart()
    text_email = "\n----\n"
    att = MIMEBase('zip_archive', "zip_archive")
    with open( zipFile, "rb") as fh:
        data = fh.read()
    att.set_payload(data)
    Encoders.encode_base64(att)
    att.add_header("Content-Disposition", "attachment", filename='output.zip')
    msg.attach(att)
    att = MIMEBase('zip_archive', "zip_archive")
    with open( zipFilePDF, "rb") as fh:
        data = fh.read()
    att.set_payload(data)
    Encoders.encode_base64(att)
    att.add_header("Content-Disposition", "attachment", filename='output_pdf.zip')
    msg.attach(att)
    msg['Subject'] = emailSubject
    msg['From'] = emailUsername
    msg['To'] = ', '.join(receiverEmail)
    s = smtplib.SMTP(emailServer, emailPort)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(emailUsername, emailPassword)
    s.sendmail(emailUsername, receiverEmail, msg.as_string())
    s.quit()
    return 0

try:
    configFileName = sys.argv[1]
except Exception:
    configFileName = 'config.json'


parseConfig (configFileName)
sendEmail()
