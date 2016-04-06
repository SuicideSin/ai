set terminal png
set output "swaps.png"
set title "Swaps"
set xlabel "n"
set ylabel "Number of swaps"
plot "swaps.txt" u 1:2 w l notitle


set terminal png
set output "shuffles.png"
set title "Shuffles"
set xlabel "n"
set ylabel "Number of shuffles"
plot "shuffles.txt" u 1:2 w l notitle