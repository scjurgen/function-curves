set terminal pngcairo size 500, 400 linewidth 1
set size ratio 1
set output '{filename}'
set title "{title}"
set view equal xy
set key outside
set mxtics 10
set mytics 10
set xtics 1
set ytics 1
set style line 12 lc rgb 'blue' lt 1 lw 1
set style line 13 lc rgb 'grey' lt 1 lw 1
set grid mxtics mytics xtics ytics ls 12, ls 13
set xrange [{minrange}:1.1]
set yrange [{minrange}:1.1]
plot {plot}
