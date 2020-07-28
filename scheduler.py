import numpy as np
from userAgent import userAgent
import time
alive = True
ua = userAgent()
while alive:
    this_action = np.random.uniform()
    wait = np.random.exponential(5)
    if this_action< .5:
        print(f"query google, {wait}")
        ua.random_query()
        time.sleep(5)
        ua.digest()
    elif this_action < .75:
        print(f"send email, {wait}")
    elif this_action < .95:
        print(f"print something, {wait}")
    else:
        print("Done for now")
        alive = False
    time.sleep(wait)


