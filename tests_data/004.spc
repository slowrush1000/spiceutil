$ 004.spc

.global vdd vss

.model n nmos
.model p pmos

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