# trafficGen

## Create session
To create a network, clone this repo and checkout the mono branch. Create a project titled "testtest". type "python3 example-net.py". Four traffic_gen_boxes, one email server, a print server, a NAT cloud, a pfsense router, and a switch will appear. The traffic_gen_boxes, print server, and email server will be connected to the switch, along with the router's em1 port. The router's em0 port will connect to the NAT cloud. All the nodes will be started automatically. Once the router is done booting (the progress of this can be checked by right-clicking the router node and clicking 'console'), the network will be ready to recieve instructions.
