import time
import numpy as np
import os

os.system("python3 /usa/lucasd/trafficGen/runCont/startNAS.py")
time.sleep(10)
alive = True
run = True # Get from docker run signal
scale = 1
while alive:
    nxt = np.random.uniform()
    if not run:
        time.sleep(10)
        continue
    if nxt < .35:
        print("Call random duckduckgo query")
        #Executes userAgent.py on all traffic_gen_boxes.
        os.system("python3 /usa/lucasd/trafficGen/runCont/runall.py /.query.sh")        
    elif nxt < .5:
        print("Interact with storage")
        os.system("python3 /usa/lucasd/trafficGen/runCont/runall.py /.freenasagent.sh")
    elif nxt < .75:
        print("Call send Email")
        #Executes emailSender.py on all traffic_gen_boxes.
        os.system("python3 /usa/lucasd/trafficGen/runCont/runall.py /.email.sh")
    elif nxt < .95:
        print("Print a dummy file")
        #Executes printFile.py on all traffic_gen_boxes.
        os.system("python3 /usa/lucasd/trafficGen/runCont/runall.py /.print.sh")
    elif nxt >= 0.95:
        print("Done for now")
        #Terminates the program.
        alive = False
    wait = np.random.exponential(scale)
    time.sleep(wait)
    #wait an extra 10 seconds to make sure the executed script is complete before attempting to run another.
    time.sleep(10)

