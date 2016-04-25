set terminal png
set output "hc.png"
set title "Local Min using swapping"
plot 'hcdata.txt' using 1:2 t 'data points', \
  "hcdata.txt" using 1:2 t "lines" with lines

set terminal png
set output "g.png"
set title "Greedy Algorithm (Best of 5)"
plot 'gdata.txt' using 1:2 t 'data points', \
  "gdata.txt" using 1:2 t "lines" with lines