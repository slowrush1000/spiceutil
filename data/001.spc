$ 001.spc

.model n nmos 
+ vth=0.7
+ vth0 = '34*45' $ aaa

.model p pmos vth=0.7

.model nt.0 nmos vth=0.7 vth0 = 1
.model nt.1 nmos vth=0.8 vth0 = 1
.model nt.2 nmos vth=0.9 vth0 = 1

.model pt.0 pmos vth=0.7 vth0 = 1
.model pt.1 pmos vth=0.8 vth0 = 1
.model pt.2 pmos vth=0.9 vth0 = 1

.subckt s_n d g s b l=l w=w
.model s_n nmos vht0=10 vth=20
main d g s b s_n l=l w=w
.ends

.subckt s_p d g s b l=l w=w
.model s_p nmos vht0=10 vth=20
main d g s b s_p l=l w=w
.ends
.model d d

.subckt s_n_binning d g s b l=l w=w
.model s_n_binning.0 nmos vth=0.7 vth0 = 1
.model s_n_binning.1 nmos vth=0.8 vth0 = 1
.model s_n_binning.2 nmos vth=0.9 vth0 = 1
main d g s b s_n_binning l=l w=w
.ends

.subckt s_p_binning d g s b l=l w=w
.model s_p_binning.0 pmos vth=0.7 vth0 = 1
.model s_p_binning.1 pmos vth=0.8 vth0 = 1
.model s_p_binning.2 pmos vth=0.9 vth0 = 1
main d g s b s_p_binning l=l w=w
.ends

.subckt inv_normal in out $ comment
mp out in vdd vdd p l=1u w=4u
mn out in vss vss n l=1u w=2u
d1 in  vdd d
.ends

.subckt inv_normal_binning in out $ comment
mp out in vdd vdd pt l=1u w=4u
mn out in vss vss nt l=1u w=2u
d1 in  vdd d
.ends

.subckt s_inv_normal in out $ comment
xs_mp out in vdd vdd s_p l=1u w=4u
xs_mn out in vss vss s_n l=1u w=2u
d1 in vdd d
r1 in 1 100
l1 1  2 1n
l2 2  3 0.001n
c1 3  4 1u
k1 l1 l2 0.1
vs1 5 6 100
is1 6 7 1m 
e1  7 8 5 6 10
g1  8 9 6 7 20
h1  9 10 vs1 100 
f1  10 11 vs1 200
.ends

.subckt s_inv_normal_binning in out $ comment
xs_mp_binning out in vdd vdd s_p_binning l=1u w=4u
xs_mn_binning out in vss vss s_n_binning l=1u w=2u
r1 in 1 100
r2 1 out 200
d2 in  vdd d
.ends

xinv_normal in out inv_normal
xinv_normal_binning in out inv_normal_binning
xs_inv_normal in out s_inv_normal
xs_inv_normal_binning in out s_inv_normal_binning

.global vdd