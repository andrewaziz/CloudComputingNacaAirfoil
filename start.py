from worker import start_instance


number_of_workers = raw_input('number of workers: ')
number_of_workers = int(number_of_workers)


def substitute(new, old, file):
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

controller_ip = start_instance('g17control', 'userdata-project.yml', True)


substitute('    - export controller_ip="{}"'.format(controller_ip),
		   '    - export controller_ip', 'userdata-worker.yml')

for x in xrange(1, number_of_workers + 1):
	substitute('    - export worker_id="worker{}"'.format(x),
		   	   '    - export worker_id', 'userdata-worker.yml')


	start_instance('g17worker{}'.format(x), 'userdata-worker.yml', True)
