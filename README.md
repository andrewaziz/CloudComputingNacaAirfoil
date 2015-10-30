# CloudComputingNacaAirfoil
This project lets you start up virtual machines in a openstack environment to comput drag lift force with naca airfoil: https://github.com/TDB-UU/naca_airfoil/tree/master/navier_stokes_solver. 

## Prerequisite
You need access to an openstack environment with your own public container. You also need to install python novaclient. It would be nice to be able to use a private container but is currently not implemented.
- pip install python-novaclient

## Run
git clone https://github.com/andrewaziz/CloudComputingNacaAirfoil.git  
You need to configure userdata-controller.yml and userdata-worker with your own credentials. 

    - export OS_AUTH_URL=http://smog.uppmax.uu.se:5000/v2.0
    - export OS_TENANT_NAME= 
    - export OS_USERNAME= 
    - export OS_PASSWORD=
    - export OS_IMAGE="g17airfoil"
    - export OS_FLAVOR= 
    - export OS_NETWORK=
    - export OS_SECURITY_KEY=
    - export OS_CONTAINER=

We used a snapshot based on Ubuntu Server 14.04 LTS if this isn't available you need to add following lines right after runcmd: in both userdata files.
The system will only work with Ubuntu images and is only tested on Ubuntu Server 14.04 LTS.

    - git clone https://github.com/TDB-UU/naca_airfoil.git /home/ubuntu/
    - add-apt-repository ppa:fenics-packages/fenics
    - apt-get update
    - sudo apt-get install fenics
    - sudo apt-get dist-upgrade

## REST-API
The REST api have 2 endpoints one for xml files and another for drag_lift.m files.  
To download a xml file for example r0a60n100.xml with curl:  
- curl yourfloatingip:5000/api/v1.0/r0a60n100.xml  

To download the drag_lift.m for r0a60n100.xml with airfoil with folling settings:  
number of samples 4, viscocity 10, speed 20,  total time 2 with curl:  
- curl yourfloatingip:5000/api/v1.0/r0a60n100.xml/s4v10s20t2/drag_lift.m

