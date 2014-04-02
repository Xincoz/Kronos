def Ping(Kon,Ex,Command):
    Response = Ex.General().ping()
    Kon.send(Response)



def SetDNS(Kon,Ex,Command):
    if len(Command)!=3:
        Kon.send("BAD COMMAND")
    else:
        Response = Ex.SetDNS(Command[1])


def PowerOff(Kon,Ex,Command):
    Kon.send("Initiating Shutdown")
    Kon.close()
    Ex.Maintain().Off()

def GetStat(Kon,Ex,Command):
    Response = Ex.Maintain().GetStatus()
    Kon.send(Response)

def StartS(Kon,Ex,Command):
    print Command,len(Command)
    if len(Command) == 2:
       Response = Ex.Maintain().StartService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")

def StopS(Kon,Ex,Command):
    print Command,len(Command)
    if len(Command) == 2:
       Response = Ex.Maintain().StopService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")

def ReStartS(Kon,Ex,Command):
    print Command,len(Command)
    if len(Command) == 2:
       Response = Ex.Maintain().ReStartService(Command[1])
       Kon.send(Response)
    else:
       Kon.send("BAD REQUEST")


def Reboot(Kon,Ex,Command):
    Response = Ex.Maintain().Reboot()
    Kon.send(Response)

def Execute(Kon,Ex,Command):
    Kon.send("READY")
    Com = Kon.recv(2048)
    if Com is '^*':
        Kon.send('Cancelled')
    else:
        Response = Ex.General().Execute(Com)
        Kon.send(Response)

def IsRun(Kon,Ex,Command):
    Response = Ex.Processes().IsRunning(Command[1])
    Kon.send(Response)

def LisPS(Kon,Ex,Command):
    Response = Ex.Processes().ListPS()
    Kon.send(Response)

def KillPID(Kon,Ex,Command):
    print "lo here"
    Response = Ex.Process0().KillPID(Command[1])
    Kon.send(Response)
