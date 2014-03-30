def Ping(Kon,Ex):
    Response = Ex.General().ping()
    Kon.send(Response)



def SetDNS(Kon,Ex,Command):
    if len(Command)!=3:
        Kon.send("BAD COMMAND")
    else:
        Response = Ex.SetDNS(Command[2])
    
