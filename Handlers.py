
#Kronos - 0.1 [Abstract Anion] - Alpha
#Copyright Blaise M Crowly 2014 - All rights reserved
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

#Handler to handle PING request
def Ping(Kon,Ex,Command):
    #Engine call
    Response = Ex.General().ping()
    Kon.send(Response)


#Handler to handle SETDNS request
def SetDNS(Kon,Ex,Command):
    if len(Command)!=2:
        #Cehck to see if DNS list is passed
        Kon.send("BAD COMMAND")
    else:
        #Engine call
        Response = Ex.Config().SetDNS(Command[1])
        Kon.send(Response)

#Handler to handle PWROFF request
def PowerOff(Kon,Ex,Command):
    Kon.send("Initiating Shutdown")
    Kon.close()
    #Engine call
    Ex.Maintain().Off()

#Handler to handle GETSTAT request
def GetStat(Kon,Ex,Command):
    #Engine Call
    Response = Ex.Maintain().GetStatus()
    Kon.send(Response)

#Handler to handle STASERV request
def StartS(Kon,Ex,Command):
    if len(Command) == 2:
       #Engine call
       Response = Ex.Maintain().StartService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")


#Handler to handle STOSERV
def StopS(Kon,Ex,Command):
    print Command,len(Command)
    if len(Command) == 2:
       #Engine call
       Response = Ex.Maintain().StopService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")

#Handler to handle RESSERV request
def ReStartS(Kon,Ex,Command):
    print Command,len(Command)
    if len(Command) == 2:
       #Engine call
       Response = Ex.Maintain().ReStartService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")

#Handler to handle REBOOT request
def Reboot(Kon,Ex,Command):
    #Engine call
    Response = Ex.Maintain().Reboot()
    Kon.send(Response)

#Handler to handle EXECUT request
def Execute(Kon,Ex,Command):
    #Send redy and recieve the command to execute
    Kon.send("READY")
    Com = Kon.recv(2048)
    if Com is '^*':
        Kon.send('Cancelled')
    else:
        #Engine call
        Response = Ex.General().Execute(Com)
        Kon.send(Response)

#Handler to handle ISRUN request
def IsRun(Kon,Ex,Command):
    #Engine call
    Response = Ex.Processes().IsRunning(Command[1])
    Kon.send(Response)

#Handler to handle LISPS
def LisPS(Kon,Ex,Command):
    #Engine call
    Response = Ex.Processes().ListPS()
    Kon.send(Response)


#Handler to handle KILLPID
def KillPID(Kon,Ex,Command):
    print "lo here"
    #Engine call
    Response = Ex.Processes().KillPID(Command[1])
    print Response
    Kon.send(Response)

#Handler to handle KILLPS
def KillPS(Kon,Ex,Command):
    #Engine call
    Response = Ex.Processes().KillPS(Command[1])
    Kon.send(Response)
