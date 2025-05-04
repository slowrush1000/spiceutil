# spice syntax

[SPICE - A Brief Tutorial](https://www.seas.upenn.edu/~jan/spice/spice.overview.html)

# spice netlist format

* independent source
```
Vname N1 N2 Value -> Vname N1 N2 dc=value
Iname N1 N2 Value -> Iname N1 N2 dc=value
```
* PWL source
```
Vname N1 N2 PWL (T1 V1 T2 V2 ... TN VN)
Iname N1 N2 PWL (T1 V1 T2 V2 ... TN VN)
```
* Pulse source
```
Vname N1 N2 PULSE (V1 V2 Tr Tf PW Period)
Iname N1 N2 PULSE (V1 V2 Tr Tf PW Period)
```

* Dependent source
```
* VCVS
Ename N1 N2 NC1 NC2 value   -> Ename N1 N2 NC1 NC2 e=value
* VCCS
Gname N1 N2 NC1 NC2 value   -> Gname N1 N2 NC1 NC2 g=value
* CCVS
Hname N1 N2 Vcontrol value  -> Hname N1 N2 Vcontrol h=value
* CCCS
Fname N1 N2 VControl value  -> Fname N1 N2 Vcontrol f=value
```

* element
* Resistor
```
Rname n1 n2 value ...
Rname n1 n2 model r=value ...
```
* Capacitor and Inductor
```
Cname n1 n2 value
Lname n1 n2 value
```
* Mutual Inductor
```
Kname L1 L2 value
```
* subckts
```
.SUBCKT SUBNAME N1 N2 N3 ... NN
.ENDS SUBNAME
```
* Semiconductor Devices
* diode
```
.MODEL MODname D (IS=V N=V RS=V CJ0=V TT=V IBV=V)
Dname N+ N- MODName ...
```

* Bipolar transistors 
```
.MODEL MODname NPN (BF=val IS=val VAF=val)
.MODEL MODname PNP (BF=val IS=val VAF=val)

Qname C B E BJT_modelNAme ...
```

* MOSFET
```
.MODEL MODname NMOS (KP=val VT0=val lambda=val gamma=val)
.MODEL MODname PMOS (KP=val VT0=val lambda=val gamma=val)

Mname ND NG NS NB ModName L=VAL W=VAL AD=VAL AS=VAL PD=VAL PS=VAL NRD=VAL ...
```

* JFET
```
.MODEL MODname NJF (parameter= ...)
.MODEL MODname PJF (parameter= ...)

Jname ND NG NS ModName
```