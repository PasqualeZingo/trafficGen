import requests, json
class Startup(object):
  def __init__(self, hostname, user, secret):
       """
       Constructor function. Stores the appropriate arguments as properties of self. Returns nothing. Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
       args:
           self (Startup): The current instance of Startup.
           hostname (str): the hostname of the storage server, including the domain.
           user (str): the username to send requests as.
           secret (str): the password of user.
       """
       self._hostname = hostname
       self._user = user
       self._secret = secret
       self._ep = 'http://%s/api/v1.0' % hostname
  def request(self, resource, method='GET', data=None):
       """
       Takes the current instance of Startup and three strings as arguments. Makes a request where method=method argument and data=data argument of the FreeNAS api with the url
       stored in self._ep + resource. Returns the response as a json if possible or a string otherwise. Raises a valueError if the response contains an error code.
       Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
       args:
            self (Startup): The current instance of Startup.
            resource (str): a string appended to the api's url stored in self._ep. The request is made to this concatenated string.
            method (str): a string representing the method of the request. Default value is "GET".
            data (str): a string representing the data to be sent to the api. Default value is None.
        returns:
            str/dict: The response from the server. If it can be returned as a dict, the function will do so. Otherwise, it will be returned as a string.      
  """
       if data is None:
           data = ''
       r = requests.request(
           method,
           '%s/%s/' % (self._ep, resource),
           data=json.dumps(data),
           headers={'Content-Type': "application/json"},
           auth=(self._user, self._secret),
       )
       if r.ok:
           try:
               return r.json()
           except:
               return r.text
       raise ValueError(r)

  def create_pool(self)->str:
       """
      Takes the current instance of Startup as an argument. Creates a pool on the appropriate FreeNAS server. Returns the response from the server as a string or dictionary.
  Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
      args:
          self (Startup): the current instance of the Startup class.
      returns:
          str/dict: the response from the server. Type is selected in Startup.requests().
       """
       #Makes a POST request of the api to add the pool. volume_name represents the name of the pool, while the layout represents which disk to use, and the way the data is stored.
       return self.request('storage/volume', method='POST', data={
           'volume_name': 'tank',
           'layout': [
               {'vdevtype': 'stripe', 'disks': "ada1"},
           ]
})
  def create_dataset(self):
       """
        Takes the current instance of Startup as an argument. Creates a dataset on the appropriate FreeNAS server. Returns the response from the server as a string or dictionary.
        Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
        args:
            self (Startup): The current instance of the Startup class.
        returns:
            str/dict: The response from the server. Type is selected within Startup.requests().
       """
       #Makes a POST request of the api to create a dataset. 'name' reperesents the name of the new dataset.
       return self.request('storage/volume/tank/datasets', method='POST', data={
           'name': 'MyShare',
       })

  def create_nfs_share(self):
       """
        Takes the current instance of Startup as an argument. Creates an nfs share on the appropriate FreeNAS server. Returns the response from the server as a string or dictionary.
    Adapted from create_cifs_share found at https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
        args:
             self (Startup): The current instance of the Startup class.
        returns:
             str/dict: the response from the server. The type is selected within Startup.requests().
       """
       #Makes a POST request of the server to create a new nfs share. nfs_name is the name of the share. nfs_paths is a list of paths to share over nfs.
       #nfs_guestonly's purpose is unclear. It does not appear as a setting within the online ui.
       #nfs_mapall_user represents a user whose permissions will be granted to anyone who mounts the share.
       return self.request('sharing/nfs', method='POST', data={
           'nfs_name': 'My Test Share',
           'nfs_paths': ['/mnt/tank/MyShare'],
           'nfs_guestonly': True,
           'nfs_mapall_user': 'root',
})
  def service_start(self, name):
       """
      Takes the current instance of Startup and a string as arguments. Starts a service on the server with the name matching the name argument given. Returns the response from the
  server as a string or a dictionary. Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
      args:
           self (Startup): The current instance of the Startup class.
       	   name (str): the name of the service to be started.
      returns:
           str/dict: The response from the server. The type is selected within Startup.requests().
       """
       #Makes a PUT request to enable a service. srv_enable represents whether the service should be started or stopped.
       return self.request('services/services/%s' % name, method='PUT', data={
           'srv_enable': True,

})

#Declare S as an instance of the Startup class.
S = Startup("FreeNAS.luked.com","root","toor")

if len(S.request("storage/volume")) >= 2:
	raise ValueError("Pool is already present!") 


#Create a pool on the server.
print(S.create_pool())
#Seperate the json objects for ease of reading
print("----------")
#Create a dataset on the server.
print(S.create_dataset())
print("----------")
#Share the dataset through nfs.
print(S.create_nfs_share())
print("----------")
#Start the nfs service.
print(S.service_start("nfs"))
#As a hold-over from earlier attempts to automate this process, the server may contain a pool already that is not functional. This may appear in the output from these print statements.

