import os
from sys import argv
import time
from novaclient.client import Client

config = {'username':os.environ['OS_USERNAME'],
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

nc = Client('2',**config)
ubuntu = 'Ubuntu Server 14.04 LTS (Trusty Tahr)'
image = nc.images.find(name='g17-airfoil')
flavor = nc.flavors.find(name='m1.medium')
network = nc.networks.find(label='ACC-Course-net')
userdata = open('userdata-project.yml', 'r')
name = argv[1]

try:
    server = nc.servers.create(name=name, image=image.id, flavor=flavor.id,
                               network=network.id, key_name='AndrewKeyPair',
                               userdata=userdata, security_groups=None)
finally:
    userdata.close()

floating_ips = nc.floating_ips.list()
state = server.status

while(state == 'BUILD'):
    time.sleep(4)
    server = nc.servers.get(server.id)
    state = server.status

for ip in floating_ips:
    if ip.instance_id == None:
        server.add_floating_ip(ip)
        print 'Ubuntu Server running at: {}'.format(ip.ip)
        break
else:
    print 'No available floating IPs in the pool'
