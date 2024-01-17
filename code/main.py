import qiskit as qk

def QRAM_circuit(n,m):
    A = qk.QuantumRegister(n,"A")
    D = qk.QuantumRegister(m,"D")
    dq = qk.QuantumRegister(1,"dq")
    qy = qk.QuantumRegister(n+m,"qy")
    r = qk.QuantumRegister(1,"r")   
    QRAM = qk.QuantumCircuit(A,D,dq,qy,r)

    address_A = [int (i) for i in range(n)]
    
    for i in range(n):
        QRAM.initialize([1,0],A[i])
        QRAM.initialize([1,0],D[i])

    for i in range(n+m):
        QRAM.initialize([1,0],qy[i])
     
    QRAM.initialize([1,0],dq)
    QRAM.initialize([1,0],r)
    QRAM.h(address_A)
    QRAM.cx(qy[:n:],A)
    QRAM.x(A)
    QRAM.mct(A,dq)
    QRAM.x(r)
    
    for i in range(m):
        QRAM.cswap(dq,D[i],qy[i+n])
        QRAM.cswap(r,D[i],qy[i+n])
        QRAM.cswap(dq,D[i],qy[i+n])

    QRAM.x(r)

    for i in range(m):    
        QRAM.ccx(D[i],dq[0],qy[i+n])
        QRAM.cx(r,qy[i+n])
        QRAM.ccx(D[i],dq[0],qy[i+n])
       
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