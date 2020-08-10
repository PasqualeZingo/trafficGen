import time
import numpy as np

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
    elif nxt < .75:
        print("Call send Email")
    elif nxt < .95:
        print("Do something else")
    elif nxt >= 0.95:
        print("Done for now")
        alive = False
    wait = np.random.exponential(scale)
    time.sleep(wait)

