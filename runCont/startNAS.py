from os import system

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
        system(f"/usa/lucasd/trafficGen/runCont/run.sh {ID} /.freenas.sh")
        break

