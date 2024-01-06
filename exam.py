from qiskit import *
    
def QRAM_circuit(n,m):
    A=QuantumRegister(n,"A")
    D=QuantumRegister(n,"D")
    dq=QuantumRegister(1,"dq")
    qy=QuantumRegister(n+m,"qy")
    r=QuantumRegister(1,"r")   
    QRAM=QuantumCircuit(A,D,dq,qy,r)
    adress_A= [int (i) for i in range(n)]
    for i in range(n):
     QRAM.initialize([1,0],A[i])
     QRAM.initialize([1,0],D[i])
    for i in range(n+m):
        QRAM.initialize([1,0],qy[i])
     
    QRAM.initialize([1,0],dq)
    QRAM.initialize([1,0],r)
 
    QRAM.h(adress_A)
    QRAM.cx(qy[:n:],A)
    QRAM.x(A)
    QRAM.mct(A,dq)
    for i in range(m):
        QRAM.cswap(dq,D[i],qy[i+n])
    for i in range(m):    
       QRAM.ccx(D[i],dq[0],qy[i+n])
       QRAM.cx(r,qy[i+n])
       QRAM.ccx(D[i],dq[0],qy[i+n])
       
    QRAM.mct(A,dq)
    for i in range(n):
        QRAM.x(A[i])
        QRAM.cx(qy[i],A[i])
        
        
   
    return QRAM
vico=QRAM_circuit(3,3)
vico.draw(output="mpl")