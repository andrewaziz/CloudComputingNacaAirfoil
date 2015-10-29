import os
import sys
import time
from novaclient.client import Client

def start_instance(name, userdata, floating_ip):
    ''' start_instance starts a virtual machine
    Args:
        name (str) : name assigned to the virtual machine
        userdata (str) : userdata file
        floating_ip (bool) : if True the start_instance will try to assign a
            floating ip to the instance.

    Returns:
        The floating ip assigned to the virtual machine if no floating ip it
        will return 0.
    '''

    config = {'username':os.environ['OS_USERNAME'],
              'api_key':os.environ['OS_PASSWORD'],
              'project_id':os.environ['OS_TENANT_NAME'],
              'auth_url':os.environ['OS_AUTH_URL']}

    nc = Client('2',**config)

    image = nc.images.find(name='g17-airfoil')
    flavor = nc.flavors.find(name='m1.medium')
    network = nc.networks.find(label='ACC-Course-net')
    userdata = open(userdata, 'r')

    try:
        server = nc.servers.create(name=name, image=image.id,
                                   flavor=flavor.id, network=network.id,
                                   userdata=userdata, security_groups=None,
                                   key_name='g17key')
    finally:
        userdata.close()

    floating_ips = nc.floating_ips.list()
    state = server.status

    while(state == 'BUILD'):
        time.sleep(4)
        server = nc.servers.get(server.id)
        state = server.status

    if floating_ip:
        for ip in floating_ips:
            if ip.instance_id == None:
                server.add_floating_ip(ip)
                print 'Ubuntu Server running at: {}'.format(ip.ip)
                return ip.ip
        else:
            print 'No available floating IPs in the pool'
            return 0


def substitute(new, old, file):
	''' substitues one line for another in a file

	Args:
		new (str) : the line you want to insert into file
		old (str) : the line you want to replace
		file (str) : file you want to modify

	Returns:
		None

	'''

	f = open(file, "r")
	lines = f.readlines()
	f.close()

	f = open(file, "w")
	for line in lines:
		if not old in line:
			f.write(line)
		else:
			f.write(new + '\n')
	f.close()



if __name__ == '__main__':
	start_instance(sys.argv[1], sys.argv[2], True)
