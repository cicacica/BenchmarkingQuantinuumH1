from pytket.extensions.nexus import Nexus, QuantinuumConfig
from pytket.extensions.nexus.backends import NexusBackend
from pytket.backends.resulthandle import ResultHandle
from pytket import Circuit
from pytket.unit_id import BitRegister
from pytket.circuit.display import render_circuit_jupyter
import networkx as nx
import matplotlib.pyplot as plt
import math as ma 
import numpy as np
import random as rm
import pandas as pd
import re
import copy
import warnings
import sympy as sy
import helper_functions as hf

# Set to generate randomness each shot
def circuit_01():
    # Set up qircuit and registers
    c = Circuit()
    quantum_register = c.add_q_register(name="quantum_reg", size=1)
    classic_register = c.add_c_register(name="classical_reg", size=1)
    conditional_register_z_gate = c.add_c_register(name='z_condition_gate_reg', size=1)
    conditional_register_z_value = c.add_c_register(name='z_condition_reg', size=1)
    conditional_register_x_value = c.add_c_register(name='x_condition_reg', size=1)

    # Set index at 0 for single qubit circuit
    index = 0
    # Create random bits
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_z_value[index])
    c.Reset(quantum_register[index])
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_x_value[index])
    c.Reset(quantum_register[index])
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_z_gate[index])
    c.Reset(quantum_register[index])

    # Run actual circuit
    c.H(qubit=quantum_register[index])
    c.Z(qubit=quantum_register[index], condition=conditional_register_z_gate[index])

    # Adjust to basis based on conditional gates
    c.Sdg(quantum_register[index], condition=conditional_register_z_value[index] & conditional_register_x_value[index])
    c.H(quantum_register[index], condition=conditional_register_x_value[index])

    # Measure
    c.Measure(qubit=quantum_register[index], bit=classic_register[index])

    return c



def circuit_02():

    
    # Set up qircuit and registers
    c = Circuit()
    quantum_register = c.add_q_register(name="quantum_reg", size=1)
    classic_register = c.add_c_register(name="classical_reg", size=1)

    
    # Rotation conditions
    conditional_register_pi_rotation = c.add_c_register(name='pi_rotation_condition', size=1)
    conditional_register_half_pi_rotation = c.add_c_register(name='half_pi_rotation_condition', size=1)
    conditional_register_quarter_pi_rotation = c.add_c_register(name='quarter_pi_rotation_condition', size=1)

    
    # Basis conditions
    conditional_register_z_value = c.add_c_register(name='z_condition_reg', size=1)
    conditional_register_x_value = c.add_c_register(name='x_condition_reg', size=1)

    
    # Set index at 0 for single qubit circuit
    index = 0

    
    # Full pi rotation condition
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_pi_rotation[index])
    c.Reset(quantum_register[index])

    
    # Half pi rotation condition
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_half_pi_rotation[index])
    c.Reset(quantum_register[index])

    
    # Quarter pi rotation condition
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_quarter_pi_rotation[index])
    c.Reset(quantum_register[index])

    
    # Z basis condition
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_z_value[index])
    c.Reset(quantum_register[index])

    
    # X basis condition
    c.H(qubit=quantum_register[index])
    c.Measure(qubit=quantum_register[index], bit=conditional_register_x_value[index])
    c.Reset(quantum_register[index])

    
    # Full pi rotation condition
    c.X(quantum_register[index], condition = conditional_register_pi_rotation[index])

    
    # Half pi rotation condition
    c.V(quantum_register[index], condition = conditional_register_half_pi_rotation[index])

    
    # Quarter pi rotation condition
    c.Rx(0.25, quantum_register[index], condition = conditional_register_quarter_pi_rotation[index])


    # Adjust to basis based on conditional gates
    c.Sdg(quantum_register[index], condition=conditional_register_z_value[index] & conditional_register_x_value[index])
    c.H(quantum_register[index], condition=conditional_register_x_value[index])

    # Measure
    c.Measure(qubit=quantum_register[index], bit=classic_register[index])

    return c

def circuit_03(num_qubits: int):
    # Set up qircuit and registers
    c = Circuit()
    qr = c.add_q_register(name="quantum_reg", size=num_qubits)
    cr = c.add_c_register(name="classical_reg", size=num_qubits)
    con_reg = c.add_c_register(name='condition_reg', size=num_qubits)

    # Prepare a random vector of bits for use as
    # conditions
    # need to apply to conditional gates
    for q in range(num_qubits):
        c.H(qr[q])
        c.Measure(qubit=qr[q], bit=con_reg[q])
        c.Reset(qr[q])

    # Entangle
    [hf.XCX(c, qr[index], qr[index+1]) for index in range(num_qubits-1)]
    
    for q in range(num_qubits):
        if q == 0:
            c.Sdg(qr[q], condition=con_reg[q] & con_reg[q+1])
            c.H(qr[q], condition=con_reg[q+1])
        elif q < num_qubits-1:
            c.Sdg(qr[q], condition=con_reg[q] & (con_reg[q-1] ^ con_reg[q+1]))
            c.H(qr[q], condition=con_reg[q-1] ^ con_reg[q+1])
        elif q == num_qubits-1:
            c.Sdg(qr[q], condition=con_reg[q] & con_reg[q-1])
            c.H(qr[q], condition=con_reg[q-1])
        else:
            raise ValueError("Qubits is outside range.")
        c.Measure(qubit=qr[q], bit=cr[q])


    return c



def circuit_04(num_qubits: int, graph):
    

    random_bits = gen_n_rand_bits(num_qubits)
    # Set up qircuit and registers
    c = Circuit()
    qr = c.add_q_register("q", num_qubits)
    cr = c.add_c_register("c", num_qubits)



    [XCX(c, e[0], e[1]) for e in graph.edges()]

    basis_strings = list()
    for index in range(num_qubits):
        basis = get_basis_from_graph(graph,random_bits, index)
        basis(c,qr,index)
        basis_str = func_2_str_basis_letter(basis)
        basis_strings.append(basis_str)
        c.Measure(qr[index], cr[index]) 

    
    return {'circuit':c, 'random_bits':random_bits,'basis':basis_strings}


def circuit_05(num_qubits: int, graph):

    random_bits_for_basis = gen_n_rand_bits(num_qubits)
    random_bits_for_r_bit_U_V_gate = gen_n_rand_bits(num_qubits)
    random_bits_for_theta_int_U_V_gate = gen_k_theta_rand_bits(num_qubits)
    
    # Set up qircuit and registers
    c = Circuit()
    qr = c.add_q_register("q", num_qubits)
    cr = c.add_c_register("c", num_qubits)


    # Apply U gate
    for q in range(num_qubits):
        basis_func = get_basis_from_graph(graph, random_bits_for_basis, q)
        basis_str = func_2_str_basis_letter(basis_func)
        U_gate(c, basis_str, q, random_bits_for_r_bit_U_V_gate[q], random_bits_for_theta_int_U_V_gate[q])

    # Apply entanglgin X controlled X: X-X
    [XCX(c, e[0], e[1]) for e in graph.edges()]

    [V_gate(c, q, random_bits_for_theta_int_U_V_gate[q]) for q in range(num_qubits)]

    results = {'circuit':c,
              'random_bits_for_basis':random_bits_for_basis,
              'random_bits_for_r_bit_U_V_gate':random_bits_for_r_bit_U_V_gate,
              'random_bits_for_theta_int_U_V_gate':random_bits_for_theta_int_U_V_gate}
    return results













    