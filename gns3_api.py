from gns3fy import Node, Link, Gns3Connector
import gns3fy
import os
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
        self.router = Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            )
        self.NAT = Node(project_id=lab.project_id,connector=server,name="NAT-1",template="NAT")
        self.router.create()
        self.NAT.create()
        self.project_id=lab.project_id
        self.router_name=self.router.name
        self.router_port = self.router.port_name_format
        lab.create_link(self.NAT.name,self.NAT.port_name_format,self.router_name,self.router.ports[0].get("name"))
        self.used_links = 1
    def delete(self):
        self.router.delete()
    def start(self):
        self.router.start()
    def stop(self):
        self.router.stop()

def Clear(project_name):
     project_id = server.get_project(project_name)['project_id']
     nodes = server.get_nodes(project_id)
     for node in nodes:
           nd = Node(node_id=node['node_id'],connector=server,project_id=project_id)
           nd.delete()
     print("%s has been cleared of all nodes!" % project_name)
 
          
class Star(Route):
    def __init__(self, router, name, template):
        self.Nodes = []
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
                        switch.ports[1].get("name"))
        router.used_links += 1
        
        self.project_id=lab.project_id
        self.switch_name=switch.name
        self.switch_port = switch.port_name_format
        self.used_links = 1
        
    def node_add(self, nnodes, template):
        for i in range(nnodes):
            self.Nodes.append(Node(
                project_id=self.project_id,
                connector=server,
                template=template
                ))
            self.Nodes[len(self.Nodes) - 1].create()
            lab.get()
            lab.create_link(self.switch_name, 
                            self.switch_port.format(self.used_links), 
                            self.Nodes[len(self.Nodes) - 1].name, 
                            self.Nodes[len(self.Nodes) - 1].ports[0].get("name"))
            self.used_links+=1
    def start(self):
        for n in self.Nodes:
            n.start()
    def stop(self):
        for n in self.Nodes:
            n.stop()
    def delete(self):
        for n in self.Nodes:
            n.delete()

class Heterogenous(Route):
    def __init__(self, router, name, template):
        self.Nodes = []
        self.Nodes.append(Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            ))
        self.Nodes[0].create()
        lab.get()
        lab.create_link(router.router_name, 
                        router.router_port.format(router.used_links), 
                        self.Nodes[0].name, 
                        self.Nodes[0].ports[0].get("name"))
        
        router.used_links += 1
        
        self.project_id=lab.project_id
        self.node_name=self.Nodes[0].name
        self.node_port = self.Nodes[0].port_name_format
        self.used_links = 1
    def start(self):
        for n in self.Nodes:
            n.start()
    def stop(self):
        for n in self.Nodes:
            n.stop()
    def delete(self):
        for n in self.Nodes:
            n.delete()

