import time #For sleeping between script executions
import numpy as np #For generating random numbers between 0 and 1. To randomly decide which traffic type to generate and when to stop the script.
from runall import startNAS, runall #For starting scripts on the traffic_gen_box containers and adding a pool and a dataset to the FreeNAS server. See runall.__doc__ for more details.

#Add a pool and a dataset to the freenas storage server on the network.
startNAS()
#Wait for the script activated by the previous command to finish.
time.sleep(10)
alive = True
run = True # Get from docker run signal
scale = 1
while alive:
    #Generate a random number between 0 and 1.
    nxt = np.random.uniform()
    if not run:
        time.sleep(10)
        continue
    if nxt < .35:
        print("Call random duckduckgo query")
        #Executes userAgent.py on all traffic_gen_boxes.
        runall(".query")
        #Wait an extra 5 seconds, since this script is particularly slow.
        time.sleep(5)        
    elif nxt < .5:
        print("Interact with storage")
        #Executes freeNASagent.py on all traffic_gen_boxes.
        runall(".freenasagent.sh")
    elif nxt < .75:
        print("Call send Email")
        #Executes emailSender.py on all traffic_gen_boxes.
        runall(".email")
    elif nxt < .95:
        print("Print a dummy file")
        #Executes printFile.py on all traffic_gen_boxes.
        runall(".print.sh")
    elif nxt >= 0.95:
        print("Done for now")
        #Terminates the while loop.
        alive = False
    #Wait for a random number of seconds.
    wait = np.random.exponential(scale)
    time.sleep(wait)
    #wait an extra 10 seconds to make sure the executed script is complete before attempting to run another.
    time.sleep(10)

