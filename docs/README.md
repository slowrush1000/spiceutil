spice netlist format

.subckt name pin1 pin2 ... pinN
Rname n1 n2 value
Rname n1 n2 model r=value ...
Cname n1 n2 value
Lname n1 n2 value
Mname n1 n2 n3 n4 model l=l1 w=w1
Qname n1 n2 n3 model l=l1 w=w1
Jname n1 n2 n3 model ...
Kname Inductor1 Inductor2 value
Ename N1 N2 NC1 NC2 value
Gname N1 N2 NC1 NC2 value
Hname N1 N2 Vcontrol value
Fname N1 N2 VControl value
.ends

.model name[.#] d ...
.model name[.#] npn ...
.model name[.#] pnp ...
.model name[.#] nmos ...
.model name[.#] pmos ...
.model name[.#] njf ...
.model name[.#] pjf ...

.inc "aaa"
.include "bbb"
.inc 'aaa'
.include 'bbb'