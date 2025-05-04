$ 001.spc

.global vdd vss

.model dd d
.model qqn npn
.model qqp pnp
.model jn njf
.model jp pjf
.model n nmos
.model p pmos

.subckt inv in out
mn0 out in vss vss n l=100u w=200u
mp0 out in vdd vdd p l=200u w=400u
.ends

r1 1 2 1
r2 2 3 resStar r=2
c1 3 4 1u
l1 4 5 2u
l2 5 6 4u
k1 l1 l2 0.5
vdd vdd 0 1
idd vdd 0 100n
e1 6 7 1 2  100
g1 7 8 2 3  1000
h1 8 9 vdd 10000
f1 9 10 vdd 100000
d1 10 11 dd l=100u w=200u
qn1 11 12 vss qqn l=100u w=200u
qp1 14 15 vdd qqp l=200u w=400u
jn1 20 21 vss jn l=10u w=20u
jp1 22 23 vdd jp l=30u w=40u
mn0 100 101 vss vss n l=100u w=200u
mp0 out in vdd vdd p l=200u w=400u

xinv in out inv

.end