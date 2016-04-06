set terminal png
set xtics nomirror
set ytics nomirror
set xlabel "n"
set grid ytics

set output "swaps.png"
set title "Swaps (lateral algorithm)"
set ylabel "Number of swaps"
plot "swaps.txt" u 1:2 w l notitle

set output "shuffles.png"
set title "Shuffles (lateral algorithm)"
set ylabel "Number of shuffles"
plot "shuffles.txt" u 1:2 w l notitle