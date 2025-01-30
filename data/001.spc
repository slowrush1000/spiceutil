$ 001.spc
.subckt a 1 2 l=100u w=200u $ aaa
r1  1   aaa 100
r2  aaa 2   200
r3  1   vdd   resStar r=100
c1  1   vdd   10
l1  1   vss   1n
.ends

.subckt b 1 2 l='aaa + 1000u * 200' w = bbbb * bbb
m1  1 2 vss vss n l=100u w=200u
m2  1 2 vdd vdd p l=100u w=400u
xaaa 1 2 aaa
.ends

.subckt c 1 2 $ ccc
d1  1   vdd   ddd
.ends

xa 1 2 a l='xa' w='xb'
xb 3 4 b l=xa w=xb
xc 5 6 c l='xa' w='xb'

.include "./0011.spc"

.model n nmos
.model p pmos
.model d d