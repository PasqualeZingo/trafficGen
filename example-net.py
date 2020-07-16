import gns3fy
import gns3-api.py

server = Gns3Connector("http://brass.ece.udel.edu:3080")
lab = gns3fy.Project(name="testtest", connector=server)
lab.get()

pf = Route(name="pfsense", template="pfSense 2.4.4")
gp1 = Star(router=pf, name="office", template="Ethernet switch")
gp1.node_add(nnodes=4, template="sfcal-sfcal")

gp2 = Star(router=pf, name="managment", template="Ethernet switch")
gp2.node_add(nnodes=2, template="sfcal-sfcal")
gp2.node_add(nnodes=2, template="sfcal-sfcal")

gp3 = Heterogenous(router=pf, name="single", template="sfcal-sfcal")
