
.subckt a 1 2
r1  1   aaa 100
r2  aaa 2   200
.ends

.subckt b 1 2
m1  1 2 3 4 n l=100u w=200u
m2  4 3 2 1 p l=100u w=400u
.ends

.subckt c 1 2
d1  1   2   100
.ends

xa 1 2 a
xb 3 4 b
xc 5 6 c

.include "./0011.spc"

.model n nmos
.model p pmos
.model d d