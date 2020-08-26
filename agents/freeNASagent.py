import requests
from os import system
import random

class Connection(object):
    def __init__(self,hostname,domain,mountPoint,localStorage,poolName,shareName):
        """
        Constructor funciton. store the hostname and domain in self.url, the mountPoint in self.mountPoint, localStorage in self.local, poolName in self.poolName, and shareName in self.shareName. Return nothing.
        
        args
        ----
        self : Connection
            the current instance of Connection.
        hostname : str
            The hostname of the FreeNAS server.
        domain : str
            The domain used to locate the FreeNAS server.
        mountPoint : str
            The directory where share files will appear.
        localStorage : str
            A directory containing files to be copied to and from mountPoint.
        poolName : str
            The name of the pool containing the desired share
        shareName : str
            The name of the desired share.
        """
        self.url = "%s.%s" % (hostname,domain)
        self.mountPoint = mountPoint
        self.poolName = poolName
        self.shareName = shareName
        self.local = localStorage
        cmd = "mount " + self.url + ":/mnt/" + self.poolName + "/" + self.shareName + " " + self.mountPoint
        system(cmd)
    def localToNet(self):
        """
        Take a Connection object as an input. Copy a randomly selected file from self.local to self.mountPoint. Return the command run through bash to copy the file as a string.
        
        args
        ----
        self : Connection
            A Connection object.
        
        returns
        -------
        str
            The command run by os.system to copy the randomly selected file.
        """
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
            return file
        else:
            raise ValueError("Attempted to retrieve locally stored files from an empty or nonexistent directory! If the directory is not empty, make sure you have rwx permissions.")
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

