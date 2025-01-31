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

.subckt s_inv_normal in out $ comment
xmp out in vdd vdd s_p l=1u w=4u
xmn out in vss vss s_n l=1u w=2u
d1 in  vdd d
.ends

.subckt s_sinv_normal_binning in out $ comment
xmp out in vdd vdd s_p_binning l=1u w=4u
xmn out in vss vss s_n_binning l=1u w=2u
d2 in  vdd d
.ends

xinv_normal in out inv_normal
xinv_normal_binning in out inv_normal_binning
xs_inv_normal in out s_inv_normal
xs_inv_normal_binning in out s_sinv_normal_binning