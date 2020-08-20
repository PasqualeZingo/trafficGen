import requests, json
class Startup(object):
  def __init__(self, hostname, user, secret):
       self._hostname = hostname
       self._user = user
       self._secret = secret
       self._ep = 'http://%s/api/v1.0' % hostname
  def request(self, resource, method='GET', data=None):
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
       print(r.text)
       raise ValueError(r)

  def _get_disks(self):
       disks = self.request('storage/disk')
       return [disk['disk_name'] for disk in disks]

  def create_pool(self):
       disks = self._get_disks()
       print(self.request('storage/volume', method='POST', data={
           'volume_name': 'tank',
           'layout': [
               {'vdevtype': 'stripe', 'disks': "ada1"},
           ]
}))
  def create_dataset(self):
       self.request('storage/volume/tank/datasets', method='POST', data={
           'name': 'MyShare',
       })

  def create_nfs_share(self):
       self.request('sharing/nfs', method='POST', data={
           'nfs_name': 'My Test Share',
           'nfs_paths': ['/mnt/tank/MyShare'],
           'nfs_guestonly': True
})
  def service_start(self, name):
       self.request('services/services/%s' % name, method='PUT', data={
           'srv_enable': True,

})

S = Startup("FreeNAS.luked.com","root","toor")

S.create_nfs_share()

S.service_start("nfs")
