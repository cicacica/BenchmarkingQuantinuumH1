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

def circuit_01(basis):
    # Set up qircuit and registers
    c = Circuit()
    qr = c.add_q_register("q", 1)
    cr = c.add_c_register("c", 1)
    con_reg = c.add_c_register("con_reg",1) 
    # Determine index
    index = 0

    # Generate a random bit
    c.H(index)
    c.Measure(qr[index], con_reg[index])
    c.Reset(qr[index])

    # Init H gate
    c.H(index)

    # Condition gate X on random bit
    c.Z(qr[index], condition = con_reg[index])

    # Adjust to apropriate basis
    basis(c, qr, index)

    # Measure in computational basis
    c.Measure(qr[index], cr[index])

    return c



def circuit_02(theta_integer: int, basis):
    # Set up qircuit and registers
    c = Circuit()
    qr = c.add_q_register("q", 1)
    cr = c.add_c_register("c", 1)

    # Determine index
    index = 0


    # Apply theta rotation
    #theta = (theta_integer % 8) * ma.pi / 4.0 pyket adds pi inro Rx gate
    theta = (theta_integer % 8) / 4.0 # mod 8 to ensure integers are 0...7
    c.Rx(theta,qr[index])

    # Adjust to apropriate basis
    basis(c,qr,index)

    # Measure in computational basis
    c.Measure(qr[index], cr[index])

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













    