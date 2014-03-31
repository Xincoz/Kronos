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

