from os import system
import sys

def Run(ID,File):
    print(f"docker exec -d {ID} {File}")
    system(f"docker exec -d {ID} {File}")

def runall(File):
    if File.count("/") == 0:
        File = "/" + File
    if File[-3:-1] != ".sh":
        File = File + ".sh"
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
            Run(ID,File)

def startNAS():
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
            Run(ID,"/.freenas.sh")
            break

