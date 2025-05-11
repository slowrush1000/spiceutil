
.subckt pkg 1 2
r1 n1 n2 100
c1 n3 n4 1u
l1 n5 n6 1n
l2 n7 n8 100n
k1 l1 l2 0.1
v1 n9 n10 0
e1 n1 n2 n9 n10 0.01
g1 n3 n4 n9 n10 0.01
h1 n11 n12 v1 1
f1 n13 n14 v1 100
.ends