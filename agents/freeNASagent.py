from os import system #To enter commands into bash for mounting and unmounting /mnt.
import random #To randomly select a file from the local or remote storage, and to randomly choose between copying from local to remote or vice-versa.

class Connection(object):
    """
    A class representing a connection to a FreeNAS server.
    
    Attrubutes
    ----------
    hostname : str
        The hostname of the server.
    domain : str
        The domain of the server.
    mountPoint : str
        The directory where shared files will appear. Copying files to this directory will store them on the server.
    local : str
        The directory where files are copied to the server from and from the server to.
    poolName : str
        The name of the pool containing the desired dataset.
    shareName : str
        The name of the desired dataset, shared via nfs.

    Methods
    -------
    __init__(self: Connection,hostname : str,domain : str, mountPoint : str, local : str, poolName : str, shareName : str)
        Constructor function. Copies the string arguments into the attributes of the same names. Returns nothing.
    localToNet(self: Connection)
        Copies a random file from self.local to self.mountPoint.
    netToLocal(self: Connection)
    TBD
    """
    def __init__(self,hostname,domain,mountPoint,local,poolName,shareName):
        """
        Constructor funciton. store the hostname and domain in self.url, the mountPoint in self.mountPoint, local in self.local, poolName in self.poolName, and shareName in self.shareName. Return nothing.
        
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
        local : str
            A directory containing files to be copied to and from mountPoint.
        poolName : str
            The name of the pool containing the desired share
        shareName : str
            The name of the desired share.
        """
        #Store the url used to access the server.
        self.url = "%s.%s" % (hostname,domain)
        #Store the point where the remote storage will be mounted.
        self.mountPoint = mountPoint
        #Store the name of the pool containing the desired dataset.
        self.poolName = poolName
        #Store the name of the shared dataset.
        self.shareName = shareName
        #Store the location to look for local files.
        self.local = local
        #Create a command to mount the remote storage.
        cmd = "mount " + self.url + ":/mnt/" + self.poolName + "/" + self.shareName + " " + self.mountPoint
        #Mount the remote storage.
        system(cmd)
    def localToNet(self)->str:
        """
        Take a Connection object as an input. Copy a randomly selected file from self.local to self.mountPoint. Return the command run through bash to copy the file as a string.
        
        args:
            self (Connection): A Connection object.
        
        returns:
            str: The command run by os.system to copy the randomly selected file.
        """
        #Create a command to copy from the local storage to the mounted network storage through bash.
        cmd = "cp %s/%s %s" % (self.local,self._getRandLocalFile(),self.mountPoint)
        #Execute the command in bash.
        system(cmd)
        #return the command as a string.
        return cmd
    def netToLocal(self)->str:
        #If _getRandNetFile() returns a filename:
        if self._getRandNetFile():
            #Create a command to copy from the mounted remote storage to the local storage
            cmd = "cp %s/%s %s" % (self.mountPoint,self._getRandNetFile(),self.local)
        else:
            #Otherwise, terminate the function and return the string below.
            return "No remote files."
        #Execute the command to copy from the remote to local storage.
        system(cmd)
        #Return the executed command.
        return cmd
    def umount(self)->str:
        """
        Take a Connection as an argument. Unmount the remote storage. Return the shell command used to do so as a string.
        
        args:
            self (Connection): An instance of Connection
        
        returns:
            str: The command run to unmount the remote storage.
        """
        #Create the bash command to unmount the remote storage.
        cmd = "umount " + self.mountPoint
        #Unmount the storage through bash.
        system(cmd)
        #Return the command run.
        return cmd
    def _getRandLocalFile(self)->str:
        """
        Take a Connection as an argument. Return the name of a randomly selected file in self.local. Throws a ValueError if no files are found in self.local.

        args:
            self (Connection): an instance of Connection.
        
        returns:
            str: The name of a randomly-selected file in self.local.
        """
        #Store a list of files in self.local in the file .dat.
        system('echo "$(ls %s)" > .dat' % self.local)
        #Open, read, close, and remove .dat.
        f = open(".dat","r")
        files = f.read().strip()
        f.close()
        system("rm -f .dat")
        #Split the data from .dat into seperate lines. If no files were found, this will be a list consisting of a single empty string.
        files = files.split("\n")
        #Randomly select a valid index of files.
        fileno = random.randint(0,len(files) - 1)
        #Set the name of the file to the appropriate file name.
        file = files[fileno]
        #If the file name is not empty:
        if file:
            #Return it as a string.
            return file
        else:
            #Otherwise, raise a ValueError.
            raise ValueError("Attempted to retrieve locally stored files from an empty or nonexistent directory! If the directory is not empty, make sure you have rwx permissions.")
    def _getRandNetFile(self)->str:
        """
        Take a Connection as an argument. Return the name of a randomly selected file in self.mountPoint as a string. If no files are found, an empty string is returned.
        
        args:
            self (Connection): an instance of the Connection class.
        
        returns:
            str: The name of a random file within self.mountPoint. If no files are found, this will be an empty string.
        """
        #Store a list of files in self.mountPoint in the file .dat.
        system('echo "$(ls %s)" > .dat' % self.mountPoint) 
        #Open, read, close, and delete .dat.
        f = open(".dat","r")
        files = f.read().strip()
        f.close()
        system("rm -f .dat")
        #Seperate the raw data from .dat into seperate lines. If self.mountPoint is empty, this will be a list containing only an empty string.
        files = files.split("\n")
        #Select a random valid index of files.
        fileno = random.randint(0,len(files) - 1)
        #Return the appropriate file.
        file = files[fileno]
        return file

#Declare an instance of Connection with settings tailored to the default hostname and domain of a network attached storage server template. traffic_gen_box containers will come with 10 empty files in /root, named file1-10. 
C = Connection("FreeNAS","luked.com","/mnt","/root","tank","MyShare")

#Pick 0 or 1 at random.
todo = random.randint(0,1)

#If 1 was picked:
if todo:
    #Copy a random file from remote storage to local storage.
    C.netToLocal()
else:
    #Copy a random file from local storage to the server.
    C.localToNet()

#Unount the mountPoint when the program is complete.
C.umount()

