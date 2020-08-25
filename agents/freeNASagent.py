import requests
from os import system
import random

class Connection(object):
    def __init__(self,hostname,domain,mountPoint,localStorage,poolName,shareName):
        self.url = "%s.%s" % (hostname,domain)
        self.mountPoint = mountPoint
        self.poolName = poolName
        self.shareName = shareName
        self.local = localStorage
        cmd = "mount " + self.url + ":/" + self.poolName + "/" + self.shareName + " " + self.mountPoint
        system(cmd)
    def localToNet(self):
        cmd = "cp %s/%s %s" % (self.local,self._getRandLocalFile(),self.mountPoint)
        system(cmd)
        return cmd
    def netToLocal(self):
        if self._getRandNetFile():
            cmd = "cp %s/%s %s" % (self.mountPoint,self._getRandNetFile(),self.local)
        else:
            return "No remote files."
        system(cmd)
        return cmd
    def umount(self):
        cmd = "umount " + self.mountPoint
        system(cmd)
        return cmd
    def _getRandLocalFile(self):
        system('echo "$(ls %s)" > .dat' % self.local)
        f = open(".dat","r")
        files = f.read().strip()
        f.close()
        system("rm -f .dat")
        files = files.split("\n")
        fileno = random.randint(0,len(files) - 1)
        file = files[fileno]
        if file:
            return file:
        else:
            raise ValueError("Attempted to retrieve locally stored files from an empty directory!")
    def _getRandNetFile(self):
        system('echo "$(ls %s)" > .dat' % self.mountPoint) 
        f = open(".dat","r")
        files = f.read().strip()
        f.close()
        system("rm -f .dat")
        files = files.split("\n")
        fileno = random.randint(0,len(files) - 1)
        file = files[fileno]
        return file

C = Connection("FreeNAS","luked.com","/mnt","/root","tank","MyShare")
todo = random.randint(0,1)
if todo:
    C.netToLocal()
else:
    C.localToNet()
C.umount()

