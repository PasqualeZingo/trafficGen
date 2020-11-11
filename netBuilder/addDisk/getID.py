import requests
import sys

args = sys.argv[1:]

try:
    assert (len(args) == 2 or len(args) == 3)
except:
    print("wrong number of arguments!")
    exit(1)

def getProjectID(name):
    r = requests.get("http://localhost:3080/v2/projects")

    ret = r.json()

    for x in ret:
        if x['name'] == name:
            return x["project_id"]
    return ""

def getNodeID(name,project):
    id = getProjectID(project)
    r = requests.get(f"http://localhost:3080/v2/projects/{id}/nodes")
    ret = r.json()
    for x in ret:
        if x['name'] == name:
            ans = x
            print(x['node_id']) 
            break
    return ans["node_id"]
if args[0].lower().strip() == "project":
    print(getProjectID(args[1]))
    exit(0)
elif args[0].lower().strip() == "node":
    getNodeID(args[2],args[1])
    exit(0)
else:
    ar = args[0]
    print(f"cannot get id of {ar}")
    exit(2)
