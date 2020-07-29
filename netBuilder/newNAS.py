import requests
import json
class Startup(object):
	def __init__(self,hostname,user,secret):
		self._hostname = hostname
		self._user = user
		self._secret = secret
		self._ep = 'http://%s/api/v1.0' % hostname
		print(self._ep)
	def request(self, resource, method='GET', data=''):
		r = requests.request(
		method,
		'%s/%s' % (self._ep, resource),
		data=json.dumps(data),
		headers={'Content-Type': "application/json"},
		auth=(self._user,self._secret)
	)
		if r.ok:
			try:
				return r.json()
			except:
				return r.text
		raise ValueError(r)
	def _get_disks(self):
		disks = self.request('storage/disk')
		return disks
	def create_pool(self):
		disks = self._get_disks()
		self.request('storage/volume',method='POST',data={
			'volume_name': 'tank',
			'layout': [
				{'vdevtype': 'stripe', 'disks': disks},
			],
})

	def create_dataset(self):
		self.request('storage/volume/tank/datasets', method='POST', data={'name': 'mydata'})
	def create_nfs_share(self):
		self.request('sharing/nfs', method='POST', data={
			'nfs_name': 'mynfs',
			'nfs_path': 'mnt/tank/mydata',
			'nfs_guestonly': True
})
St = Startup('FreeNAS.luked.com','root','toor')
print(St._get_disks())
