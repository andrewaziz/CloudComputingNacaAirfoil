# CloudComputingNacaAirfoil

instance g17-airfoil including fenics-dolfin, gmsh, including packages


##example

make directories to save output from runme.sh

mkdir /home/ubuntu/msh
mkdir /home/ubuntu/geo

./runme.sh 0 30 10 200 3

convert file to dolfin xml format
dolfin-convert r1a18n200.msh r1a18n200.xml 

./airfoil  10 0.0001 10. 1 cloudnaca/msh/r1a18n200.xml
