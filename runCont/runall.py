from os import system
import sys

def Run(ID,File):
    system(f"docker exec -d {ID} {File}")

def runall(File):
    system("docker container ls | tail -n +2 | awk -F' ' '{print $1,$2}' > contls")
    f = open("contls","r")
    txt = f.read().strip()
    f.close()
    lines = txt.split("\n")
    system("rm -f contls")
    for line in lines:
        ID = line.split(" ")[0]
        image = line.split(" ")[1]
        if image == "traffic_gen_box:latest":
            Run(ID,sys.argv[1])

def startNAS():
    system("docker container ls | tial -n +2 | awk -F' ' '{print $1,$2}' > contls")
    f = open("contls","r")
    txt = f.read().strip()
    f.close()
    lines = txt.split("\n")
    system("rm -f contls")
    for line in lines:
        ID = line.split(" ")[0]
        image = line.split(" ")[1]
        if image == "traffic_gen_box:latest":
            Run(ID,".freenas.sh")
            break
