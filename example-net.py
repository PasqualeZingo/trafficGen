from gns3fy import *
from gns3_api import *

#Tell the program what url to use to contact the gns3 api on brass. If this script is to be used on a different server, this line will need to be modified.
server = Gns3Connector("http://brass.ece.udel.edu:3080")
#Decalres an instance of the project class with the name "testtest" and "server" as its connector. 
lab = gns3fy.Project(name="testtest", connector=server)
lab.get()

#open the project
lab.open()

#Clear all nodes from the project.
Clear("testtest")

#Create the router.
pf = Route(name="pfsense", template="pfSense 2.4.5-ready-to-go")
#Start the router.
pf.start()

#Declare an instance of the Star class from gns3_api.
gp1 = Star(router=pf, name="office", template="Ethernet switch")

#Add 4 traffic_gen_boxes to the network.
gp1.node_add(nnodes=4, template="traffic_gen_box")

#Add a printer server named "cups_pdf" to the network.
gp1.node_add(nnodes=1,template="printer",name="cups_pdf")

#Add an email server named "studio.lrd.com" to the printer server.
gp1.node_add(nnodes=1,template="studio.lrd.com",name="studio.lrd.com")

#Start the nodes created with the Star class.
gp1.start()


