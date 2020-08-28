"""
A module designed to allow the user to run files on containers from the server hosting them within python.

Functions
---------
    Run(ID : str,File: str)->None
        Execute the bash script File in docker container ID.
    runall(File : str)->None
        Execute the bash script File within all docker containers running the traffic_gen_box:latest image.
    startNAS()->None
        Tell one traffic_gen_box:latest container to add a pool and a shared dataset to the FreeNAS network attached storage server.
"""

from os import system
import sys

def Run(ID : str,File : str)->None:
    """
    Take two string arguments, ID and File. If there are no "/" charcters in File, add one to the beginning. If File does not end with ".sh", add ".sh" to the end of File. Run the script File on the docker container of id ID. Return nothing.
    
    args:
        ID (str): The ID of the docker container to run File within.
        File (str): The File to be executed.
    """
    #if there are no slashes in the filename, assume it is within "/".
    if File.count("/") == 0:
        File = "/" + File
    #If the file name does not end with the .sh extension, add .sh to the end of the file name.
    if File[-3:] != ".sh":
        File = File + ".sh"
    #Execute the file File within docker container ID.
    system(f"docker exec -d {ID} {File}")

def runall(File : str)->None:
    """
    Take one string argument File. Execute the shell script named File within every docker container running the traffic_gen_box:latest image. Return nothing.
    
    args:
        File (str): The name of the file to be executed within all traffic_gen_box:latest containers.
    """
    #Get the ID and image of each active docker container and store the result in a file named contls.
    system("docker container ls | tail -n +2 | awk -F' ' '{print $1,$2}' > contls")
    #Open, read, and close contls.
    f = open("contls","r")
    txt = f.read().strip()
    f.close()
    #Seperate the raw text of contls into lines.
    lines = txt.split("\n")
    #Delete contls.
    system("rm -f contls")
    #For each line that was in contls:
    for line in lines:
        #The ID and image are seperated by a space, with the ID coming before the space and the image name after. Read them both from the current line.
        ID = line.split(" ")[0]
        image = line.split(" ")[1]
        #If the container is running the traffic_gen_box:latest image:
        if image == "traffic_gen_box:latest":
            #Call the Run() function to execute File in ID.
            Run(ID,File)
        #Don't return anything.

def startNAS()->None:
    """Take no arguments. Run the bash script /.freenas.sh in a container running the traffic_gen_box:latest image. Return nothing."""
    #Get the ID and image of each active docker container and store the result in a file named contls.
    system("docker container ls | tail -n +2 | awk -F' ' '{print $1,$2}' > contls")
    #Open, read, and close contls.
    f = open("contls","r")
    txt = f.read().strip()
    f.close()
    #Seperate the raw text of contls into lines.
    lines = txt.split("\n")
    #Delete contls.
    system("rm -f contls")
    #For each line that was in contls:
    for line in lines:
        #The ID and image are seperated by a space, with the ID coming before the space and the image name after. Read them both from the current line.
        ID = line.split(" ")[0]
        image = line.split(" ")[1]
        #If the container is running the traffic_gen_box:latest image:
        if image == "traffic_gen_box:latest":
            #Call the Run() function to execute /.freenas.sh in ID and break the loop.
            Run(ID,"/.freenas.sh")
            break
        #Don't return anything.

