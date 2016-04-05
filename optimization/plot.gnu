#
# Torbert, 2 November 2012
#
# gnuplot demo1.gnu
#
set terminal png
set output "shuffles.png"
plot "shuffles.txt" u 1:2 w l notitle
#
# end of file
#