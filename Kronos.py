# -*- coding: utf-8 -*-
import sys
import os
import platform
from OpenSSL import SSL
import socket
ossupport= True
OS = platform.version()
import Handlers as H


if 'Debian' in OS:
    import Engines.Debian as Ex
    ossupport = False
if 'Ubuntu' in OS:
    import Engine.Ubuntu as Ex
    ossupport = False

LINKS = {
       'PING':H.Ping,
       'SETDNS':H.SetDNS
        }
     


class Security:

    def KeyCheck(self):
        print "Checking for key.......",
        if os.path.isfile('Kronos.key'):
            print "[FOUND]"
        else:
            print "[NOT FOUND]\nCreating one...........",
            if os.system('openssl genrsa 1024 > Kronos.key') is 0:
                print "Created!"
            else:
                print "CRITICAL ERROR: Key Creation failed."
                print "Check if Openssl is installed and you have permission"
                exit()
        print "Checking for Certificate.......",
        if os.path.isfile('Kronos.cert'):
            print "[FOUND]"
        else:
            print "[NOT FOUND]\nCreating one...........",
            if os.system('openssl req -new -x509 -nodes -sha1 -days 365 -key Kronos.key > Kronos.cert') is 0:
                print "Created!"
            else:
                print "CRITICAL ERROR: Certificate Creation Failed."
                exit()

class Kronos:


    def ServerOn(self):
        print "Starting Kronos Manager Server on port"
        from Config import Server,Secret
        Kset = SSL.Context(SSL.SSLv23_METHOD)
        Kset.use_privatekey_file('Kronos.key')
        Kset.use_certificate_file('Kronos.cert')
        KServ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        KServ = SSL.Connection(Kset, KServ)
        print "Binding to",Server
        KServ.bind(Server)
        print "Listening..."
        while True:
            KServ.listen(1)
            (Kon, address) = KServ.accept()
            print "We have connection.....",
            print address
            while True:
                try:
                  Command = Kon.recv(2048)
                except:
                  break
                Command = Command.strip()
                Command = Command.split(' ')
                if Command[0] != Secret:
                    Kon.send('AUTHFAIL')
                    Kon.close()
                    break
                else:
                    print LINKS[Command[1]]
                    try:
                        LINKS[Command[1]](Kon,Ex)
                    except:
                      Kon.send('BAD COMMAND')



    def Start(self):
        os.system('clear')
        print "Kronos - Manager Alpha 0.1 By Blaise M Crowly.\n Copyright  Xincoz 2014. All Rights Reserved | xincoz.com"
        print "Running SSL/TLS test"
        Security().KeyCheck()
        self.ServerOn()
    

if __name__ == '__main__':
    Kronos().Start()


