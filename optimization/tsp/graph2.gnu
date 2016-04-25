set terminal png
set output "reversal.png"
set title "Greedy + Local Min using reversal"
plot 'reversaldata.txt' using 1:2 t 'data points', \
  "reversaldata.txt" using 1:2 t "lines" with lines
