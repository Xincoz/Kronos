import platform

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


