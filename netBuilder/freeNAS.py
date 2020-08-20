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
  Makes a request where method=method and data=data of the FreeNAS api with the url stored in self._ep plus resource. Returns the response as a json if possible or a string otherwise. Raises a valueError if the response contains an error code.
  Copied from https://www.ixsystems.com/documentation/freenas/11.3-RELEASE/api.html#a-more-complex-example
  args:
       self (Startup): The current instance of Startup.
       resource (str): a string appended to the api's url stored in self._ep. The request is made to this concatenated string.
       method (str): a string representing the method of the request. Default value is "GET".
       data (str): a string representing the data to be sent to the api. Default value is None.
  returns:
       str: The text of the response from the server.
       
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

  def create_pool(self):
  """
  
  """
       return self.request('storage/volume', method='POST', data={
           'volume_name': 'tank',
           'layout': [
               {'vdevtype': 'stripe', 'disks': "ada1"},
           ]
})
  def create_dataset(self):
       return self.request('storage/volume/tank/datasets', method='POST', data={
           'name': 'MyShare',
       })

  def create_nfs_share(self):
       return self.request('sharing/nfs', method='POST', data={
           'nfs_name': 'My Test Share',
           'nfs_paths': ['/mnt/tank/MyShare'],
           'nfs_guestonly': True,
           'nfs_mapall_user': 'root',
})
  def service_start(self, name):
       return self.request('services/services/%s' % name, method='PUT', data={
           'srv_enable': True,

})

S = Startup("FreeNAS.luked.com","root","toor")

print(S.create_pool())
print("----------")
print(S.create_dataset())
print("----------")
print(S.create_nfs_share())
print("----------")
print(S.service_start("nfs"))
print("----------")
print(S.request("sharing/nfs"))
