import os
from glob import glob
current_dir="/clhome/TOMO1/CMU/krause_jul19/"
dirn="s1400_110_1_nf"
outputdir=dirn+"_reduced/"
inputdir="/s1c/krause_jul19/nf/"+dirn+"/"
configfn=dirn+".config"
scriptfn=dirn+".sh"
#zs=range(0,11)
Ls=2
rots=720

NFile = len(glob(inputdir+'*'))
NZ = NFile//(Ls*rots)
zs = range(NZ)
print(f'fileNumber: {NFile}, layer: {NZ}')


import numpy as np


os.mkdir(outputdir)

script="""#!/bin/csh
#$ -S /bin/csh
#$ -N {0:s}
#$ -pe sec1_reg 120
#$ -j y
### Export these environmental variables
#$ -v LOG_NAME,HOSTNAME,PWD,HOME
#### job starts in current working directory
#$ -cwd
# to submit a job, run:
echo $LOG_NAME
echo $HOSTNAME
echo $PWD
echo $HOME
#########################################################################

#LD_LIBRARY_PATH=/clhome/aps_tools/shared/lib/
# put ITK on the path bash shell
# LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/clhome/aps_tools/shared/lib/InsightToolkit
setenv LD_LIBRARY_PATH /clhome/aps_tools/shared/lib:/clhome/aps_tools/shared/lib/InsightToolkit

echo "Start at : "
date
cd {2:s}
sleep 1
echo $TMPDIR
ls $TMPDIR
head -100 $TMPDIR/machines
echo "Starting binary call..."
/clhome/aps_tools/mpich-1.2.6/bin/mpirun -np 120 -machinefile $TMPDIR/machines /clhome/TOMO1/CMU/ParallelReduction.TestedBinary {1:s} 0 0
echo "Cleaning up..."
echo "End at : "
date
sleep 1
#/clhome/aps_tools/mpich2-1.0.6p1/bin/mpdallexit
#########################################################################

""".format(dirn,configfn,current_dir)

with open(scriptfn,'w') as f:
    f.write(script)

firstfile=os.listdir(inputdir)[0]
fileprefix=firstfile[:-10]
firstnumb=firstfile[-10:-4]

configheader="""DataRoot        {0:s}
PrefixIn        {1:s}
Rotations       720
Extension       tif
ImageSize       2048
Digits          6
BlanketSubtraction      5
PeakHeightRatio         0.1
NumberMinPixels         4
MedFiltSize             1
NumberStartingPoints    {2:d}
OutputRoot              {5:s}{3:s}
OutputPrefix            {4:s}
StartingPoints""".format(inputdir,fileprefix,Ls*len(zs),outputdir,dirn,current_dir)

#layers=len(os.listdir(inputdir))//(rots*Ls)



whole=[]
for z in zs:
    for l in range(Ls):
        numb=int(firstnumb)+z*Ls*rots + l*rots
        whole.append([z,l,numb])
#second=np.array(range(Ls)*layers,dtype='int')
#third=np.arange(start,start+layers*Ls*rots,rots,dtype='int')
#first=np.empty(Ls*layers,dtype='int')
#for ii in range(Ls):
#    first[np.arange(0,layers*Ls,Ls)+ii]=np.arange(layers)
#
#
#whole=np.transpose(np.vstack([first,second,third]))
np.savetxt(configfn,whole, fmt='%d', delimiter=' ',header=configheader,comments='')
