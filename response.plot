set terminal pngcairo size 350, 350 fontscale 0.8
set output '{filename}'
set title "{title}"
set view equal xy
set mxtics 10
set mytics 10
unset key
set xtics 1
set ytics 1
set style line 12 lc rgb 'blue' lt 1 lw 1
set style line 13 lc rgb 'grey' lt 1 lw 1
set grid mxtics mytics xtics ytics ls 12, ls 13
set xrange [-1.1:1.1]
set yrange [-1.1:1.1]
set style line 2 linetype 1 linewidth 3 linecolor rgb "{color}"
plot 'curve.csv' using 1:2 smooth mcspline ls 2 title "y"
