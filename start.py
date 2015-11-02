from instance import start_instance, substitute

number_of_workers = raw_input('number of workers: ')
number_of_workers = int(number_of_workers)

controller_ip = start_instance('g17control', 'userdata-controller.yml', True)


substitute('    - export controller_ip="{}"'.format(controller_ip),
           '    - export controller_ip', 'userdata-worker.yml')

for x in xrange(1, number_of_workers + 1):

	start_instance('g17worker{}'.format(x), 'userdata-worker.yml', False)
