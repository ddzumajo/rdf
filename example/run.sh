#!/bin/bash

#Take the LAMMPS output, dump.production, in which there are position and energy files for each particle. Then, it generates two files, datoslili and datosff, with the dessired format to run properly the python scripts rdf_xx.py and rdf_yy.py

awk '/NUMBER/{n=2}; n {n--;next}; 1' dump.production > output
awk '/[0-517]+/      {
        if (NF==1) { time = $1 }
        if (NF==7) { print $1, $2, $3, $4, $5, $6, $7, time }
    }' output > data
rm output
awk '{if ($2==1) {print; }}' data > datalili

awk '{if ($2==2) {print; }}' data > dataff

# Run python scripts in order to obtain the rdf of Li-Li, F-F and Li-F. Then it sorts the outputs to draw them later. Finally, it deletes the useless files. 

python rdf_xx.py datalili > lilirdf
sort -nk 1 lilirdf > lili.rdf
rm lilirdf 

python rdf_xx.py dataff > ffrdf
sort -nk 1 ffrdf > ff.rdf
rm ffrdf

python rdf_xy.py datalili datosff > lifrdf
sort -nk 1 lifrdf > lif.rdf
rm lifrdf datalili dataff data
