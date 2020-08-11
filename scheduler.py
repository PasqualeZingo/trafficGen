import time
import numpy as np
import os

alive = True
run = True # Get from docker run signal
scale = 1
while alive:
    nxt = np.random.uniform()
    if not run:
        time.sleep(10)
        continue
    if nxt < .5:
        print("Call random google query")
        os.system("/usa/lucasd/runCont/runall.sh /.query.sh")
    elif nxt < .75:
        print("Call send Email")
        os.system("/usa/lucasd/runCont/runall.sh /.email.sh")
    elif nxt < .95:
        print("Print a dummy file")
        os.system("/usa/lucasd/runCont/runall.sh /.print.sh")
    elif nxt >= 0.95:
        print("Done for now")
        alive = False
    wait = np.random.exponential(scale)
    time.sleep(wait)
    time.sleep(10)

