# -*- coding: utf-8 -*-
#Kronos - 0.1 [Abstract Anion] - Alpha
#Copyright (C) 2014 Blaise M Crowly  - All rights reserved
#Created at Xincoz [xincoz.com]
#GPL v3

"""This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.)"""

"""This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details."""

########################################################################
# The main program that starts a TCP server and listens for incoming   #
# Connections and  requests are sorted and call for the right handler  #
# is made depending on the request. The secret is also checked with the#
# hash in the config file.                                             #
########################################################################



#Import necessary modules
import sys
import os
import platform
from OpenSSL import SSL
import socket
import hashlib

#Importing handler module that contain classes to handle the incoming messages.

import Handlers as H 

#Flag to check if the Operating system is supported by the engine
ossupport= True
#Get the platform information
OS = platform.version()

#Check if OS is Debian based and import Debian Engine
if 'Debian' in OS:
    import Engines.Debian as Ex
    ossupport = False #Set OS support flag to false

#Check if OS is Ubuntu based and import Ubuntu Engine
if 'Ubuntu' in OS:
    import Engines.Ubuntu as Ex
    ossupport = False #Set OS support flag to false

#If OS support flag is still true the Os is not supported
if ossupport:
    print "OS not supported"
    exit()

#Link dictionary links incoming request to the handler function
LINKS = {
       'PING':H.Ping,       #Ping function 
       'SETDNS':H.SetDNS,   #Set DNS reques
       'PWROFF':H.PowerOff, #Power Off system
       'GETSTAT':H.GetStat, #Get the machine status of this system
       'STASERV':H.StartS,  #Start a service
       'STOSERV':H.StopS,    #Stop a service
       'RESSERV':H.ReStartS,#Restart a service
       'REBOOT':H.Reboot,   #Reboot system
       'EXECUT':H.Execute,  #Execute a command
       'ISRUN':H.IsRun,     #Check is a process is running
       'LISPS':H.LisPS,     #List all running processes
       'KILLPID':H.KillPID, #Kill  a given process by PID
       'KILLPS':H.KillPS    #Kill all process by name
        }
     

#Security class to take care of communication security
class Security:
    #Check if a key exists
    def KeyCheck(self):
        print "Checking for key.......",
        if os.path.isfile('Kronos.key'):
            print "[FOUND]"
        else:
            #Creating new key if one does not exist
            print "[NOT FOUND]\nCreating one...........",
            if os.system('openssl genrsa 1024 > Kronos.key') is 0:
                print "Created!"
            else:
                print "CRITICAL ERROR: Key Creation failed."
                print "Check if Openssl is installed and you have permission"
                exit()
        #Check if a certificate with the given key exist
        print "Checking for Certificate.......",
        if os.path.isfile('Kronos.cert'):
            print "[FOUND]"
        else:
            #If one does not exist a new one is created
            print "[NOT FOUND]\nCreating one...........",
            if os.system('openssl req -new -x509 -nodes -sha1 -days 365 -key Kronos.key > Kronos.cert') is 0:
                print "Created!"
            else:
                print "CRITICAL ERROR: Certificate Creation Failed."
                exit()

#Main class to handle the server
class Kronos:
    #Start the server
    def ServerOn(self):
        print "Starting Kronos Manager Server on port"
        from Config import Server,Secret
        #Create socket and apply SSL wrapper
        Kset = SSL.Context(SSL.SSLv23_METHOD)
        Kset.use_privatekey_file('Kronos.key')
        Kset.use_certificate_file('Kronos.cert')
        KServ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        KServ = SSL.Connection(Kset, KServ)
        print "Binding to",Server
        KServ.bind(Server)
        print "Listening..."
        while True:
          #Listen for connection
            KServ.listen(5)
            (Kon, address) = KServ.accept()
            print "We have connection.....",
            print address
            while True:
                try:
                  #Receive  the incoming request
                  Command = Kon.recv(2048)
                except:
                  break
                #Strip and Split the request sting for easy processing
                Command = Command.strip()
                Command = Command.split()
                #check if the secret send is right
                if hashlib.sha256(Command[0]).hexdigest() != Secret:
                    Kon.send('BAD SECRET')
                    Kon.close()
                    break
                else:
                    try:
                        #Invoke handler using the Link dictionary
                        LINKS[Command[1]](Kon,Ex,Command[1:])
                    except Exception,e:
                        print e
                        #Respond bad command if the send request do not fit
                        Kon.send('BAD COMMAND')


#Start function to start up the server
    def Start(self):
        os.system('clear')
        print "Kronos - Manager Alpha 0.1 By Xincoz.\nCopyright   2014 Blaise M Crowly. All Rights Reserved | xincoz.com"
        print "This program is distributed in the hope that it will be useful,"
        print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
        print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
        print "GNU General Public License (v3.0) for more details.\n\n"
        
        print "\n\n []ATTENTION : If you are running this for the first time make sure you deleted the Kronos.key and Kronos.cert files provided for testing. They are not safe. ]\n\n"
        print "Running SSL/TLS test"
        Security().KeyCheck()
        self.ServerOn()
    
#starts here
if __name__ == '__main__':
    if len(sys.argv) > 1:
      if sys.argv[1] == '--gen-secret':
        if len(sys.argv) == 3:
          print "Secret Hash : " + hashlib.sha256(sys.argv[2]).hexdigest() + "  - Replace the hash in Config.py with this"
          exit()
        else:
            print "Usage : --gen-secret <secret>"
            exit()
    Kronos().Start()


