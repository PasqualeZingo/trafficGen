"""
Create, delete, start, and stop nodes in a gns3 project on brass through the gns3 api.

Classes:

    Route
    Star
    Heterogenous

Functions:

    Clear(project_name) -> None
"""

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
    """
    A class representing a router.
    
    ...
    Attributes
    ----------
    NAT : Node
        The NAT node to access the internet
    router : Node
        The router node
    project_id : str
        The id of the project to create nodes in
    router_name : str
        The name of the router node
    router_port : str
        The name of the router port to be linked to the NAT cloud.
    used_links : int
            The number of ports on the router connected to something.
            
    Methods
    -------
    delete(self):
        Delete the router and NAT nodes.
    start(self):
        Start the router node.
    stop(self):
        Stop the router node.
    """
    def __init__(self, name, template):
        """
        Constructor function for the Route class. Take the Route instance and two strings as arguments. Create a router node of name = name argument and template = template argument. Create a NAT node and connect the router's first ethernet port to it. Return nothing.
       
        args
        ----
             self : Route
                the current instance of Route.
             name : str
                the name of the router node.
             template : str
                the template used to create the router node.
        """
        #Declare a gns3fy Node class self.router.
        self.router = Node(
            project_id=lab.project_id,
            connector=server,
            name=name,
            template=template
            )
        #Declare a gns3fy Node class self.NAT.
        self.NAT = Node(project_id=lab.project_id,connector=server,name="NAT-1",template="NAT")
        #Create the router Node.
        self.router.create()
        #Create the NAT node.
        self.NAT.create()
        #Store the project id.
        self.project_id=lab.project_id
        #Store the router name.
        self.router_name=self.router.name
        #Store the router port name.
        self.router_port = self.router.port_name_format
        #a list of dictionaries containing data to create the link between self.NAT and self.router.
        NandR= [dict(node_id=self.NAT.node_id,adapter_number = 0,port_number = 0),dict(node_id=self.router.node_id,adapter_number=0,port_number=0)]
        #Declare a gns3fy Link class between self.router and self.NAT.
        L = Link(project_id=lab.project_id,connector=server,nodes=NandR)
        #Create the link.
        L.create()
        #Store the number of used links as 1.
        self.used_links = 1
    def delete(self):
        """
        Delete the router and NAT cloud created by this Route class. Return nothing.
        
        args
        ----
        self : Route
            The current instance of Route.
        """
        self.router.delete()
        self.NAT.delete()
    def start(self):
        """
        Start the router created by this Route class. Return nothing.
        
        args
        ----
            self : Route
                The current instance of Route.
        """
        self.router.start()
    def stop(self):
        """
        Stop the router created by this Route class. Return nothing.
        
        args
        ----
            self : Route
                The current instance of Route.
        """
        self.router.stop()

def Clear(project_name : str):
    """
    Stop and then delete all nodes within the specified project. Print a confirmation message, and return nothing. The project must be opened before this funciton is called. If the project is closed by a user while this funciton is running, it may lead to undefined behavior.
  
    args
    ----
        project_name : str
            the name of the project to be cleared. 
    """
     #Get the id of the project refered to by project_name.
     project_id = server.get_project(project_name)['project_id']
     #Find all nodes in the project.
     nodes = server.get_nodes(project_id)
     #For each node in the project:
     for node in nodes:
           #Declare a gns3fy Node class with the id of the existing node.
           nd = Node(node_id=node['node_id'],connector=server,project_id=project_id)
           #Delete the node.
           nd.delete()
     #Print a confirmation message.
     print("%s has been cleared of all nodes!" % project_name)
 
          
class Star(Route):
    """
    A class representing a subnet connected to a router.
    
    ...
    Attributes
    ----------
    Nodes : [Node]
        A list of all nodes created in this class.
    project_id : str
        The project id of the project to add nodes to.
    switch_name : str
        The name of the switch connecting the subnet.
    switch_port : str
        The name of the port on the switch connected to the router.
    used_links : int
        The number of links used on the switch.
        
    Methods
    -------
    """
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
                        switch.ports[0].get("name"))
        router.used_links += 1
        
        self.project_id=lab.project_id
        self.switch_name=switch.name
        self.switch_port = switch.port_name_format
        self.used_links = 1
        
    def node_add(self, nnodes, template, name=None):
        if name == None:
           name = template
        for i in range(nnodes):
            self.Nodes.append(Node(
                project_id=self.project_id,
                connector=server,
                template=template,
                name=name
                ))
            self.Nodes[len(self.Nodes) - 1].create()
            lab.get()
            lab.create_link(self.switch_name, 
                            self.switch_port.format(self.used_links), 
                            self.Nodes[len(self.Nodes) - 1].name, 
                            self.Nodes[len(self.Nodes) - 1].ports[0].get("name"))
            self.used_links+=1
    def start(self):
        """
        Start the nodes created by this instance of the Star class. Return nothing.
        
        args
        ----
            self  : Star
                the current instance of Star.
        """
        for n in self.Nodes:
            n.start()
    def stop(self):
        """
        Stop the nodes created by the current instance of the Star class. Return nothing.
        
        args
        ----
            self : Star
                the current instance of Star.
        """
        for n in self.Nodes:
            n.stop()
    def delete(self):
        """
        Delete the nodes created by the current instance of the Star class. Return nothing.
        
        args
        ----
            self : Star
                the current instance of Star.
        """
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
        """
        Start the nodes created by this instance of the Heterogenous class. Return nothing.
        
        args
        ----
            self : Star
                the current instance of Heterogenous.
        """
        for n in self.Nodes:
            n.start()
    def stop(self):
        """
        Stop the nodes created by this instance of the Heterogenous class. Return nothing.
        
        args
        ----
            self : Star
                the current instance of Heterogenous.
        """
        for n in self.Nodes:
            n.stop()
    def delete(self):
        """
        delete the nodes created by this instance of the Heterogenous class. Return nothing.
        
        args
        ----
            self : Star
                the current instance of Heterogenous.
        """
        for n in self.Nodes:
            n.delete()

