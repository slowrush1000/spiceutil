$ 002.spc

.model n nmos
.model p pmos
.model dd d
.model qn npn
.model qp pnp
.model jn njf
.model jp pjf
.model resstar r

.subckt ns d g s b
.model ns nmos
main d g s g ns l=10 w=10
.ends

.subckt ps d g s b
.model ps pmos
main d g s g ps l=10 w=10
.ends

.subckt inv in out
mn out in vss vss n l=1 w=2
mp out in vdd vdd p l=1 w=2
.ends

.subckt inv_s in out
xmn out in vss vss ns l=1 w=2
xmp out in vdd vdd ps l=1 w=2
.ends

xinv in out inv
xinv_s in out inv_s

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
qn1 11 12 vss qn l=100u w=200u
qp1 14 15 vdd qp l=200u w=400u
jn1 20 21 vss jn l=10u w=20u
jp1 22 23 vdd jp l=30u w=40u
mn0 100 101 vss vss n l=100u w=200u
mp0 out in vdd vdd p l=200u w=400u