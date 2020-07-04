set terminal pngcairo size 300, 300 fontscale 0.8
set output '{filename}'
set title "{title}"
set xlabel 'x'
set ylabel 'y'
set xtics 0.1
set ytics 0.1
set xrange [-0.1:1.1]
set yrange [-0.1:1.1]
set grid
set style line 2 linetype 1 linewidth 1 linecolor rgb "#004000"
plot 'curve.csv' using 1:2 smooth mcspline ls 2 title "y"
