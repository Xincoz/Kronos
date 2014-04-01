import platform
import os
import psutil
import time
import datetime

class General:
    def ping(self):
      return platform.platform()


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


         

