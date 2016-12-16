set terminal postscript eps enhanced "Times-Roman" 20
set output 'a.eps'
set title "Radial distribution functions in molten LiF (Python)"
set xlabel "r(r_B)"
set ylabel "g(r)"
plot 'lili.rdf' using 1:2  with lines title "Li-Li",\
'ff.rdf' using 1:2  with lines title "F-F",\
'lif.rdf' using 1:2 with lines title "Li-F", 
