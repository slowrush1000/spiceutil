$ 001.spc
.subckt a 1 2 l=100u w=200u $ aaa
r1  1   aaa 100
r2  aaa 2   200
r3  1   2   resStar r=100
c1  1   2   10
l1  1   2   1n
.ends

.subckt b 1 2 l='aaa + 1000u * 200' w = bbbb * bbb
m1  1 2 3 4 n l=100u w=200u
m2  4 3 2 1 p l=100u w=400u
.ends

.subckt c 1 2 $ ccc
d1  1   2   ddd
.ends

xa 1 2 a l='xa' w='xb'
xb 3 4 b l=xa w=xb
xc 5 6 c l='xa' w='xb'

.include "./0011.spc"

.model n nmos
.model p pmos
.model d d