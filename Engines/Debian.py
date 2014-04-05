import platform
import os
import psutil
import time
import datetime
import subprocess


class General:
    def ping(self):
      return platform.platform()

    def Execute(self,Com):
      if os.system(Com) == 0:
          return "Succesful"
      else:
          return "Failed"


class Config:
    def SetDNS(self,DNS):
      DNS = DNS.split(',')
      Conf = ""
      for each in DNS:
          Conf = Conf+"nameserver  "+each
          Conf = Conf + "\n"

      try:
        ResolvFile = open('/etc/resolv.conf','w')
        ResolvFile.write(Conf)
        ResolvFile.close()
        return "Done"
      except:
         return "ERROR : Could not update resolv file"

class Maintain():
     def Off(self):
       os.system('poweroff')

     def GetStatus(self):
         Response = ""
         Response = Response + "OS->  " + platform.platform() + "\n"
         Response = Response + "TIME->  " + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + "\n"
         Response = Response + "CPU-> CORES:" + str(psutil.cpu_count()) + "  USAGE:"+str(psutil.cpu_percent())
         Response = Response + "%  PROC:" + str(len(psutil.pids())) + "\n"
         Tem = psutil.virtual_memory() 
         Response = Response + "MEMORY->  TOTAL:" + str(Tem.used+Tem.free)+"    USED:" + str(Tem.used) + "   FREE:" + str(Tem.free)
         Response = Response + "    USAGE:" + str(Tem.percent) + "%\n"
         Tem = psutil.disk_usage('/')
         Response = Response + "DISK->  TOTAL:" + str(Tem.total) + "  USED:" + str(Tem.used)  + "  FREE:" + str(Tem.free)
         Response = Response + "  USAGE:" + str(Tem.percent) + "%\n"
         return Response


     def StartService(self,Service):
         Command = "/usr/sbin/service "
         Arg     = Service  + " start"
         Execute = Command + Arg
         if os.system(Execute) == 0:
           return "Executed "
         else:
             return "System returned an error, check the command or use ssh"


     def StopService(self,Service):
         Command = "/usr/sbin/service "
         Arg     = Service  + " stop"
         Execute = Command + Arg
         if os.system(Execute) == 0:
           return "Executed "
         else:
             return "System returned an error, check the command or use ssh"
         

     def ReStartService(self,Service):
         Command = "/usr/sbin/service "
         Arg     = Service  + " restart"
         Execute = Command + Arg
         if os.system(Execute) == 0:
           return "Executed "
         else:
             return "System returned an error, check the command or use ssh"

     def Reboot():
         os.system('reboot')
         return "Rebooting"


class Processes:
    
    def IsRunning(self,Service):
        for each in psutil.process_iter():
            if str(each.name()).lower() == Service.lower():
                return "Running"
        return "Not Running"

    def ListPS(self):
        Procs = ""
        for each in psutil.process_iter():
            Procs = Procs + each.name() + " ........................ " + str(each.pid) + "\n"
        return Procs

    def KillPID(self,Pid):
        for each in psutil.process_iter():
            if each.pid == int(Pid):
                each.kill()
                return "Killed"
        return "No Process Found"
    def KillPS(self,Process):
        for each in psutil.process_iter():
            if each.name().lower() == Process.lower():
                each.kill()
                return "Killed"
        return "No such Process"
