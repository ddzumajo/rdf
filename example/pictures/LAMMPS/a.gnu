set terminal postscript eps enhanced "Times-Roman" 20
set output 'a.eps'
set title "Radial distribution functions in molten LiF (LAMMPS)"
set xlabel "r(r_B)"
set ylabel "g(r)"
plot 'lili.rdf(L)' using 2:3 with lines title "Li-Li" , \
'ff.rdf(L)' using 2:3 with lines title "F-F", \
'lif.rdf(L)' using 2:3 with lines title "Li-F", 

