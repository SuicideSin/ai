'''
An introduction to neural networks

{} denotes a neuron

x1 -> {f(x)} -> out

f(x) = 1/(1+e^(-wx+b)) -- sigmoid function

b - bias or offset

Implement a NOT

In  Out
1       0
0       1


x1 -> {f(x)} -> out
        ^
        |
        x2

f(x) = 1/(1+e^(-c*x+b)) 
= 
f(x) = 1/(1+e^(-(w1x1+w2x2)+b))
=
f(x) = 1/(1+e^(-w(x1+x2)+b))

OR

In      Out
0 0     0
1 0     1
0 1     1
1 1     1

AND

In      Out
0 0     0
0 1     0
1 0     0
1 1     1


NOT

Find values for w and b for which these results occur

'''