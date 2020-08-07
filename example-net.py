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
gp1.node_add(nnodes=1,template="printer",name="cups_pdf")
gp1.node_add(nnodes=1,template="studio.lrd.com",name="studio.lrd.com")

pf.start()
gp1.start()


