import qiskit as qk
from qiskit import IBMQ, Aer
import matplotlib.pyplot as plt
from qiskit.circuit.library import MCXGate

def QRAM_circuit(n,m):
    A = qk.QuantumRegister(n,"A")
    D = qk.QuantumRegister(m,"D")
    dq = qk.QuantumRegister(1,"dq")
    qy = qk.QuantumRegister(n+m,"qy")
    r = qk.QuantumRegister(1,"r")   
    QRAM = qk.QuantumCircuit(A,D,dq,qy,r)
    multible_controled_NOT_gate3  = MCXGate(3)

    for i in range(n):
        QRAM.initialize([1,0],A[i])
        QRAM.initialize([1,0],D[i])
    for i in range(n+m):
        QRAM.initialize([1,0],qy[i])
    QRAM.initialize([1,0],dq)
    QRAM.initialize([1,0],r)
    QRAM.h(A)
    QRAM.cx(qy[:n:],A)
    QRAM.x(A)
    QRAM.mct(A,dq)
    QRAM.x(r)
    for i in range(m):
        QRAM.cx(qy[i+n],D[i])
        QRAM.append(multible_controled_NOT_gate3,[1+((n+m)*2),(n+m),n+i,m+i+(m+n+1)])
        QRAM.cx(qy[i+n],D[i])

    QRAM.x(r)
    for i in range(m):    
       QRAM.append(multible_controled_NOT_gate3,[1+((n+m)*2),(n+m),n+i,m+i+(n+m+1)])

       
    QRAM.mct(A,dq)
    for i in range(n):
        QRAM.x(A[i])
        QRAM.cx(qy[i],A[i])
    
    return QRAM


circuit = QRAM_circuit(3,3)
line_colours = {
    "linecolor": "white", 
    "backgroundcolor": "#1F1E2C",
      "textcolor": "white"
}
    

circuit.draw(output="mpl", fold=1, style=line_colours)
