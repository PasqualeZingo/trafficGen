from gns3fy import Node, Link, Gns3Connector
import gns3fy

server = Gns3Connector("http://brass.ece.udel.edu:3080")
lab = gns3fy.Project(name="testtest", connector=server)
lab.get()

#This creates a star top with 0-7 nodes of any arbatrary end device template
#TODO: make star a subclass of a larger class that makes the whole network.

#{Star(name='Developer').addnode(nnodes=16, image='debian')
# Star(name='Office').addnode(nnodes=4, image='ubuntu')
# Star(name='Management' ...)
# Heterogenous(MailServer(), WebServer(), Storage(), etc...)
#}
#server = Gns3Connector("http://brass.ece.udel.edu:3080")
#lab = gns3fy.Project(name="testtest", connector=server)
#star(name='Mamagement').addnode(nnodes=4, image='ubuntu')

class Route():
    def __init__(self, name, template):
        router = Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            )
        router.create()
        
        self.project_id=lab.project_id
        self.router_name=router.name
        self.router_port = router.port_name_format
        self.used_links = 0
           
            
class Star(Route):
    def __init__(self, router, name, template):
        switch = Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            )
        switch.create()
        lab.get()
        lab.create_link(router.router_name, 
                        router.router_port.format(router.used_links), 
                        switch.name, 
                        switch.ports[0].get("name"))
        router.used_links += 1
        
        self.project_id=lab.project_id
        self.switch_name=switch.name
        self.switch_port = switch.port_name_format
        self.used_links = 1
        
    def node_add(self, nnodes, template):
        ndsFile = ".%s.nodes" % self.project_id
        try:
                f=open(ndsFile,'x')
                f.close()
                f=open(ndsFile,'w')
                f.write('0')
                f.close()
        except:
                pass
        for i in range(nnodes):
            node = Node(
                project_id=self.project_id,
                connector=server,
                template=template
                )
            if(template=='traffic_gen_box'):
                 f=open(ndsFile,'r')
                 n = int(f.read().strip())
                 n += nnodes
                 f.close()
                 f=open(ndsFile,'w')
                 f.write(str(n))
                 f.close()
            node.create()
            lab.get()
            lab.create_link(self.switch_name, 
                            self.switch_port.format(self.used_links), 
                            node.name, 
                            node.ports[0].get("name"))
            self.used_links+=1
            
class Heterogenous(Route):
    def __init__(self, router, name, template):
        node = Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            )
        node.create()
        lab.get()
        lab.create_link(router.router_name, 
                        router.router_port.format(router.used_links), 
                        node.name, 
                        node.ports[0].get("name"))
        router.used_links += 1
        
        self.project_id=lab.project_id
        self.node_name=node.name
        self.node_port = node.port_name_format
        self.used_links = 1
            

