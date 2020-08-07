from gns3fy import *
from gns3_api import *

server = Gns3Connector("http://brass.ece.udel.edu:3080")
lab = gns3fy.Project(name="testtest", connector=server)
lab.get()

lab.open()

Clear("testtest")

pf = Route(name="pfsense", template="pfSense 2.4.5-ready-to-go")
gp1 = Star(router=pf, name="office", template="Ethernet switch")
gp1.node_add(nnodes=4, template="traffic_gen_box")

pf.start()
gp1.start()

gp2 = Heterogenous(router=pf, name="single", template="sfcal-sfcal")

gp2.start()

