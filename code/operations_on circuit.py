import qiskit as qk
from qiskit import Aer
import matplotlib.pyplot as plt
from qiskit.circuit.library import MCXGate


    
def simulate_circute(circuit):
    backend = Aer.get_backend("statevector_simulator")
    job = backend.run(circuit, shots=8192)
    result = job.result()
    counts = result.get_counts(circuit)
    total_counts = sum(counts.values())
    probabilities = {state: count / total_counts for state, count in counts.items()}
    ax = plt.axes()
    ax.set_facecolor("#1F1E2C")
    plt.bar(probabilities.keys(), probabilities.values(), color="#b587f8", edgecolor="#1F1E2C")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel('Probability', color="black")
    plt.xlabel('state', color="black")
    plt.show()
   
    
def user_interface_write():
    print("input data in binary representation :")
    data = input()
    data = data[::-1]
    size_of_data = len(data)
    print("input address in binary representation :")
    address = input()
    address = address[::-1]
    size_of_address = len(address)
    return size_of_address, size_of_data, address, data

def QRAM_circuit():
    size_of_address, size_of_data, address, data = user_interface_write()
    A = qk.QuantumRegister(size_of_address)
    D = qk.QuantumRegister(size_of_data)
    dq = qk.QuantumRegister(1)
    qy = qk.QuantumRegister(size_of_data+size_of_address)
    r = qk.QuantumRegister(1)
    QRAM = qk.QuantumCircuit(A, D, dq, qy, r)
    multible_controled_NOT_gate3  = MCXGate(3)
    

    QRAM.initialize([1,0],r) # the Qubir r use to determine the operation is read or write and it takes that value from quantum processor 
    QRAM.h(A) #make address register in superposition to generate all possible combinations of addresses
    
    QRAM.cx(qy[:size_of_address:], A)
    QRAM.x(A)
    QRAM.mct(A, dq)
     # the controled NOT and NOT gate is equavilant to the S gate that determines the needed address by make dq qubit equale 1 when the adsress find in the address register 

    QRAM.x(r)
    
    # input the address from QY1 to QYn and data from QYn+1 to QYn+m where n is the size of addres and m is size of data 
    for i in range(size_of_address):
        if address[i] == '1':
            QRAM.initialize([0, 1], qy[i])
        else:
            QRAM.initialize([1, 0], qy[i])
    for j in range(size_of_data):
        if data[j] == '1':
            QRAM.initialize([0, 1], qy[j+size_of_data])
        else:
            QRAM.initialize([1, 0], qy[j+size_of_data])
    

    # the implementation of swap gate with 3 CNOT gate and and two control bit and swap gate use to transfer data form data bus to data register      
    for i in range(size_of_address):
        QRAM.cx(qy[i+size_of_address],D[i])
        QRAM.append(multible_controled_NOT_gate3,[1+((size_of_address+size_of_data)*2),(size_of_data+size_of_address),size_of_address+i,size_of_address+i+(size_of_data+size_of_address+1)])
        QRAM.cx(qy[i+size_of_address],D[i])

         
   

    
       
    QRAM.x(r)
# the toffoli gate copy values for data register to data bus  
    for i in range(size_of_address):
        QRAM.append(multible_controled_NOT_gate3,[1+((size_of_address+size_of_data)*2),(size_of_data+size_of_address),size_of_address+i,size_of_address+i+(size_of_data+size_of_address+1)])
      
# Remove the entanglement between qubit dq and register A by applying the Toffoli gate to disentangle it
    QRAM.mct(A,dq)
#Remove the effect of the first step by applying a set of n CNOT gates between each qubit of the bus register qy as a control qubit and the corresponding qubit in the register A as a target qubit. Then, a set of n quantum-NOT gates are applied on the qubits of register A individually.


    for i in range(size_of_address):
        QRAM.x(A[i])
        QRAM.cx(qy[i],A[i])
        
        

    simulate_circute(QRAM)
    return QRAM
   
    




QRAM_circuit()











