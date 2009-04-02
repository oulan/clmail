# -*- coding: cp936 -*-
#
#

import smtplib, datetime
import sys, getopt
import mimetypes

from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email import Utils, encoders

class CLMailer:
    def __init__(self):
        self.server = None
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
        self.mailMsg['Date'] = Utils.formatdate(localtime = 1)

    def mailMessage(self, message):
        textBody = MIMEText(message, _subtype = 'plain')
        self.mailMsg.attach(textBody)
                
    def prepareAttachs(self, attachFiles):
        for att in attachFiles:
            try:
                attFile = file(att, 'rb')
                mimeType, mimeEncoding = mimetypes.guess_type(att)
                if mimeEncoding or (mimeType is None):
                    mimeType = "application/octet_stream"

                mainType, subType = mimeType.split("/")
                if "text" == mainType:
                    print "attaching(text): %s" % att
                    attText = MIMEText(attFile.read(), _subtype=subType)
                else:
                    print "attaching(binary): %s(%s,%s)" % (att, mainType, subType)
                    attText = MIMEBase(mainType, subType)
                    attText.set_payload(attFile.read())
                    encoders.encode_base64(attText)
                attText.add_header("Content-Disposition", "attachment", filename=att)
                print attText.as_string()
                attFile.close()                
                self.mailMsg.attach(attText)
            except:
                pass
                
    def startTask(self):
        print "starting send mail..."
        #print self.mailMsg.as_string()
        self.server.sendmail(self.mailMsg['from'], self.mailMsg['to'],
                             self.mailMsg.as_string())
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
        self.serverPort = 25
        self.mailMsg = ''
        self.mailMsgTextFile = ''
        self.encode = 'gb2312'
        self.enableSSL = False
        self.subject = ''
        self.attachFiles = []

    def doMailTask(self):
        mailer = CLMailer()
        try:
            mailer.bindServer(self.serverAddr, self.serverPort, self.enableSSL)
            okToSend = True
            print "authenticating..."
            if self.userName <> "":
                okToSend = mailer.checkLogin(self.userName, self.password)
            if okToSend:
                print "mail setting..."
                print "from:"
                mailer.fromUser(self.fromAddr)
                print "to:"
                mailer.toUser(self.toAddr, self.ccAddr, self.bccAddr)
                print "subject:%s" % self.subject
                mailer.mailSubject(self.subject, self.encode)
                print "date"
                mailer.mailDate()
                print "body:%s" % self.mailMsg
                mailer.mailMessage(self.mailMsg)
                print "attachments:%d" % len(self.attachFiles)
                mailer.prepareAttachs(self.attachFiles)
                print "start mail:"
                mailer.startTask()
            else:
                print "authentication error"
        except:
            pass
        
    def testArgs(self):
        mailTask = True
        opts, args = getopt.getopt(sys.argv[1:],'u:p:f:t:C:B:H:s:P:ea:m:Th')

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
                print "attachment = %s" % optParam
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
clmail.py -u �û��� -p ���� -H smtp������ -s Hello -t
 Ŀ������ -f ������� -a wx.txt -m alllow -a wow.gif

�磺
clmail.py -u abc@163.com -p 123 -H smtp.163.com -s ���� -t abc@163.com -f abc@163.com -a wx.txt -m �������� -a wow.gif

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
