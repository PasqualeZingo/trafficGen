"""
This script will return the id of a project or node with the name supplied through command-line arguments. This allows it to be accessed through the gns3 api, and makes it easier to find the directory containing its disk.

Functions
---------
getProjectID(name: str)->str
    Make a GET request to the gns3 api to retrieve the ID of a project with a given name.
getNodeID(name: str,project: str)
    Makes a GET request to the gns3 api to retrieve the ID of a node of a given name within a given project.
"""

import requests #For contacting the gns3 api. should be run on the server hosting the gns3 network
import sys #For reading arguments from the command line.

#Store the arguments supplied through the command line.
args = sys.argv[1:]

#Make sure that the user has made a valid request.
try:
    assert (len(args) == 2 or len(args) == 3)
except:
    print("wrong number of arguments!")
    exit(1)

def getProjectID(name: str)->str:
    """
    Make a GET http request to the gns3 api to retrieve a list of all projects. Record the response as a list of dictionaries, ret. for each dictionary in ret, check if the dictionary's 'name' field matches the name argument. If it does, return the 'project_id' field of the dictionary. If no dictionary in ret matches the name, return an empty string.
    
    args:
        name (str): The name of the project the user wants the ID of. Supplied via the second command-line argument to the script.
    """
    #Make a GET request to the GNS3 api, requesting data on all the projects.
    r = requests.get("http://localhost:3080/v2/projects")
    
    #Save this data as a list of dictionaries.
    ret = r.json()

    #For each dictionary in the response...
    for x in ret:
        #If the project's name matches the argument supplied...
        if x['name'] == name:
            #Return the project's id.
            return x["project_id"]
    #If no project with the appropriate name is available, return an empty string.
    return ""

def getNodeID(name: str,project: str)->str:
    """
    Make a GET http request to the gns3 api to retrieve a list of all nodes in the project given by the project argument. Record the response as a list of dictionaries, ret. For each dictionary in ret, check if the dictionary's 'name' field matches the name argument. If it does, return the node_id field of the dictionary. If no match is found, return an empty string.
    
    args:
        name (str): The name of the node being searched for. Supplied via the third comamnd-line argument.
        project (str): The name of the project being searched through for the node. Supplied via the second command-line argument.
    """
    
    #Get the id of the project
    id = getProjectID(project)
    #Make a GET http request to the gns3 API for all nodes in the requested project.
    r = requests.get(f"http://localhost:3080/v2/projects/{id}/nodes")
    #Store the response in ret.
    ret = r.json()
    #for each dictionary in ret:
    for x in ret:
        #If the name matches the requested name:
        if x['name'] == name:
            #return the ID of the requested node.
            return x["node_id"]
    #If no match is found, return an empty string.
    return ""
   

#If the first command line argument is "project":
if args[0].lower().strip() == "project":
    #get the id of the requested project.
    pid = getProjectID(args[2])
    #If the id is not empty:
    if pid:
        #Print it out and exit.
        print(pid)
        exit(0)
    else:
        #Otherwise, print an error message and exit with an error code.
        print("Requested project was not found!")
        exit(3)
#If the first command line argument is "node":
elif args[0].lower().strip() == "node":
    #Get the ID of the requested node.
    nid = getNodeID(args[2],args[1])
    #If the id is not empty:
    if nid:
        #print it out and exit.
        print(nid)
        exit(0)
    #Otherwise:
    else:
        #Print out an error message and exit with an error code.
        print("Requested node was not found!")
        exit(4)
    #Exit with exit code zero.
    exit(0)
else:
    #If the first argument is neither node or project...
    ar = args[0]
    #Inform the user of what went wrong
    print(f"cannot get id of {ar}")
    #Exit with code 2.
    exit(2)
