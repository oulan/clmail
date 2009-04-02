# -*- coding: cp936 -*-
#
#

import smtplib, datetime
import sys, getopt
import mimetypes

from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Utils, Encoders

class CLMailer:
    def __init__(self):
        self.server = Null
        self.mailMsg = MIMEMultipart()

    def bindServer(self, server, port, SSL):
        if not SSL:
            self.server = smtplib.SMTP(server, port)
        else:
            self.server = smtplib.SMTP_SSL(server, port)

    def checkLogin(self, user, password):
        try:
            self.server.login(user, password)
            return True
        except:
            return False

    def fromUser(self, fromAddr):
        self.mailMsg['from'] = fromAddr

    def toUser(self, toAddr, ccAddr, bccAddr):
        self.mailMsg['to'] = toAddr
        self.mailMsg['cc'] = ccAddr
        self.mailMsg['bcc'] = bccAddr

    def mailSubject(self, subject, encode):
        self.mailMsg['subject'] = Header(subject, encode)
                
    def mailDate(self):
        self.mailMsg['Date'] = utils.formatdate(localtime = 1)

    def mailMessage(self, message):
        textBody = MIMEText(message, _subtype = 'plain')
        self.mailMsg.attach(textBody)
                
    def prepareAttachs(self, attachFiles):
        for att in attachFiles:
            try:
                attFile = open(att, 'rb')
                mimeType, mimeEncoding = mimetypes.guess_type(att)
                if mimeEncoding or (mimeType is None):
                    mimeType = "application/octet_stream"

                mainType, subType = mimeType.split('/')
                if 'text' == mainType:
                    attText = MIMEText(attFile.read(), _subtype = subtype)
                else:
                    attText = MIMEBase(mainType, subtype)
                    attText.set_payload(attFile.read())
                    Encoders.encode_base64(attText)
                    
                attText.add_header("Content-Disposition", "attachment", filename=att)
                attFile.close()
            except:
                attText = ''
            if attText <> '':
                self.mailMsg.attach(attText)
                
    def startTask(self):
        print "starting send mail..."
        self.server.sendmail(self.mailMsg['from'], self.mailMsg['to'],
                             self.mailMsg.as_string())
        print "preparing attachments..."
        print "mail sent."

class CLMailApp:
    def __init__(self, argv):
        self.argv = argv
        self.userName = ''
        self.password = ''
        self.fromAddr = ''
        self.toAddr = ''
        self.ccAddr = ''
        self.bccAddr = ''
        self.serverAddr = 'localhost'
        self.serverPort = 110
        self.mailMsg = ''
        self.mailMsgTextFile = ''
        self.encode = 'gb2312'
        self.enableSSL = False
        self.subject = ''
        self.attachFiles = []

    def doMailTask(self):
        print self.attachFiles
        print self.mailMsg
        print "-----------------------"
        mailer = CLMailer()
        try:
            mailer.bindServer(self.serverAddr, self.serverPort, self.enableSSL)
            okToSend = True
            if self.userName <> "":
                okToSend = mailer.checkLogin(self.userName, self.password)
            mailer.fromUser(self.fromAddr)
            mailer.toUser(self.toAddr, self.ccAddr, self.bccAddr)
            mailer.mailSubject(self.subject, self.encode)
            mailer.mailDate()
            mailer.mailMessage(self.mailMsg)
            mailer.prepareAttachs(attachFiles)
            if okToSend:
                mailer.startTask()
            else:
                print "authentication error"
        except:
            pass
        
    def testArgs(self):
        mailTask = True
        opts, args = getopt.getopt(sys.argv[1:],'u:p:a:h:m:H:e', ['user', 'password'])

        if 0 == len(opts):
            return False
        
        for optSwitch, optParam in opts:
            if optSwitch == '-u':
                self.userName = optParam
            elif optSwitch == '-p':
                self.password = optParam
            elif optSwitch == '-f':
                self.fromAddr = optParam
            elif optSwitch == '-t':
                self.toAddr = optParam
            elif optSwitch == '-C':
                self.ccAddr = optParam
            elif optSwitch == '-B':
                self.bccAddr = optParam
            elif optSwitch == '-H':
                self.serverAddr = optParam
            elif optSwitch == '-s':
                self.subject = optParam
            elif optSwitch == '-P':
                self.serverPort = optParam
            elif optSwitch == '-e':
                self.enableSSL = True
                if self.serverPort == '':
                    self.serverPort = 995
            elif optSwitch == '-a':
                self.attachFiles.append(optParam)
            elif optSwitch == '-m':
                self.mailMsg += optParam
            elif optSwitch == '-T':
                try:
                    textFile = open(optParam, 'r')
                    textMsg  = textFile.read()
                except:
                    textMsg = ''
                self.mailMsg += textMsg
            elif optSwitch == '-h':
                mailTask = False

        #if mailTask:
        return mailTask

    def printUsage(self):
        self.printUsageCn()
            
    def printUsageCn(self):
        print """clmail - �����ʼ����͹���
�����ʽ��
clmail -[u|p|a|s|p|h]

˵����
--help, -h:       ��ʾ������
--from, -f:       �ʼ����͵�ַ
--to, -t:         �ʼ�Ŀ���ַ
--cc, -C:         ���͵�ַ
--bcc, -B:        ���س��͵�ַ
--user, -u:       ָ�������ʼ����û���
--password, -p:   ָ�������ʼ����û�����
--host,-H:        ָ�������ʼ��ķ�����
--subject, -s:    �ʼ�����
--message, -m:    ָ�������ʼ�������
--textfile, -T:   �����ʼ��������ı�����
--attachfile, -a: �ʼ�����

���磺
clmail -u u01 -p u01pwd -s smtp.163.com -o 110 -m "test message"

�����ߣ�ŷ����(ouland@fairybeans.com)
���°汾����ʣ�http://www.oulan.com/clmail/
        """
        
    def run(self):
        if self.testArgs():
            self.doMailTask()
        else:
            self.printUsage()
    
if __name__ == "__main__":
    app = CLMailApp(sys.argv)
    app.run()
