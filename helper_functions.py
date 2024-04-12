from pytket.extensions.nexus import Nexus, QuantinuumConfig
from pytket.extensions.nexus.backends import NexusBackend
from pytket.backends.resulthandle import ResultHandle
from pytket import Circuit
from pytket.unit_id import BitRegister
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
import ast


def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")


def circuit_dict_to_data_frame(circuit_dict):
    keys = [str(key[0]) for key in circuit_dict.keys()]
    assert all([isinstance(l,tuple) for l in circuit_dict.keys()]), "All types of keys representing a circuit result must be tuples, they are not."
    assert all([len(l) == 1 for l in circuit_dict.keys()]), "All types of keys representing a circuit result must each have length one, they are not."
    values = list(circuit_dict.values())
    return pd.DataFrame({'state': keys, 'probability': values})

def compute_expected_value(df):
    outputs_diff = []
    for row in range(len(df)):
        #data_dict = ast.literal_eval(df.outcomes[row])
        data_dict = df.outcomes[row]
        if len(data_dict) == 2:
            outputs_diff.append(list(data_dict.values())[0] - list(data_dict.values())[1])
        elif len(data_dict) == 1:
            if list(data_dict.keys())[0][0] == 0:
                outputs_diff.append(list(data_dict.values())[0])
            elif list(data_dict.keys())[0][0] == 1:
                outputs_diff.append(-list(data_dict.values())[0])
            else:
                raise ValueError("The result tested is either 0 or 1. Check.")

    df['expected_value'] = outputs_diff
    return df

def concatenate_dictionary_results_to_dataframe(df):
    len_df = len(df)
    list_df = []
    for row in range(len(df)):
        row_df = df.iloc[row].to_frame().transpose()
        #data_dict = ast.literal_eval(row_df.outcomes[row])
        outcome_df = circuit_dict_to_data_frame(row_df.outcomes[row])
        row_df['experiment_id'] = row
        repeated_one_row_df = pd.concat([row_df] * len(outcome_df), ignore_index=True)
        joined_df = pd.concat([repeated_one_row_df,outcome_df], axis=1, join='outer')
        joined_df.drop(columns = ['outcomes'],inplace = True)
        list_df.append(joined_df)

    
    concatenated_df = pd.concat(list_df, axis=0, ignore_index=True)
    first_col = 'circuit_num'
    column_to_move = 'experiment_id'
    new_order = [first_col,column_to_move] + [col for col in concatenated_df.columns if col != first_col and col != column_to_move]
    
    return concatenated_df[new_order]


def gen_watts_strogatz_random_connected_graph(num_vertices: int, initial_node_nearest_neigh: int, prob_rewire_edge: float):
    
    # Number of nodes
    n = num_vertices
    
    # Each node is connected to k nearest neighbors in ring topology
    k = initial_node_nearest_neigh
    
    # The probability of rewiring each edge
    p = prob_rewire_edge
    
    # Ensure the graph is connected
    while True:
        G = nx.connected_watts_strogatz_graph(n, k, p)
        if nx.is_connected(G):
            break
    return G


def create_grid_graph(rows, cols):
    # Create a new graph
    G = nx.Graph()

    # Add nodes to the graph
    for i in range(rows):
        for j in range(cols):
            node_id = i * cols + j  # Convert 2D coordinates to 1D
            G.add_node(node_id)

    # Add edges between adjacent nodes
    for i in range(rows):
        for j in range(cols):
            node_id = i * cols + j
            if i > 0:
                G.add_edge(node_id, (i - 1) * cols + j)  # Connect to node above
            if i < rows - 1:
                G.add_edge(node_id, (i + 1) * cols + j)  # Connect to node below
            if j > 0:
                G.add_edge(node_id, i * cols + j - 1)  # Connect to node on the left
            if j < cols - 1:
                G.add_edge(node_id, i * cols + j + 1)  # Connect to node on the right

    return G

def get_x_bit_from_graph(random_bits: list, vertex: int):
    return random_bits[vertex]


def get_z_bit_from_graph(graph, random_bits: list, vertex: int):
    neighbors_list = list(graph.neighbors(vertex))
    bits_corresonding_to_neighbors = [random_bits[i] for i in neighbors_list]
    return direct_sum_on_list_bits(bits_corresonding_to_neighbors)
    


def adjust_to_X_basis(circuit, quantum_register, index):
    circuit.H(quantum_register[index])
    return circuit


def adjust_to_Y_basis(circuit, quantum_register, index):
    circuit.Sdg(quantum_register[index])
    circuit.H(quantum_register[index])
    return circuit


def adjust_to_Z_basis(circuit, quantum_register, index):
    return circuit


def direct_sum_on_list_bits(list_bits: list):
    return sum(list_bits) % 2

def gen_n_rand_bits(n: int):
    return [rm.randint(0, 1) for i in range(n)]

def gen_k_theta_rand_bits(n: int):
    return [rm.randint(0, 7) for i in range(n)]

def divisor_pairs(n):
    divisors = []
    for i in range(1, int(ma.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append((i, n // i))
    return divisors

def sample_random_grid_dims_no_path(list_pairs:list):
    pairs =  [pair for pair in list_pairs if 1 not in pair]
    return rm.choice(pairs)


def either_side_index(random_bits: list, index: int):
    if len(random_bits) < 2:
        raise ValueError("Random bits vector must be greater than 1 qubit, it is currently strictly less than 2.")
    if index == 0:
        return list([random_bits[index], random_bits[index+1]])
    elif index + 1 == len(random_bits):
        return list([random_bits[index], random_bits[index-1]])
    elif index > 0 and index < len(random_bits):
        index_2 = random_bits[index-1]^random_bits[index+1]
        return list([random_bits[index], index_2])
    else:
        raise ValueError("index is in at 0, nor the size of the random bits, nor in the middle. Check index and random bits list.")

# Version 1 is not in use hence I appended "_version_01" so as to not have to change
# other functions that rely on that same name for the updated version
def generate_basis_from_two_bits_version_01(bit1: int, bit2: int):
    if bit1 == 1 and bit2 == 0:
        return adjust_to_X_basis
    elif bit1 == 1 and bit2 == 1:
        return adjust_to_Y_basis
    elif bit1 == 0 and bit2 == 1:
        return adjust_to_Z_basis
    elif bit1 == 0 and bit2 == 0:
        warnings.warn("X and Y bits are both 0, no basis change", Warning)
        return adjust_to_Z_basis
    else:
        raise ValueError("None of the bit options were supplied")


def generate_basis_from_two_bits(bit1: int, bit2: int):
    if bit1 == 1 and bit2 == 0:
        return adjust_to_Z_basis
    elif bit1 == 1 and bit2 == 1:
        return adjust_to_Y_basis
    elif bit1 == 0 and bit2 == 1:
        return adjust_to_X_basis
    elif bit1 == 0 and bit2 == 0:
        warnings.warn("X and Y bits are both 0, no basis change", Warning)
        return adjust_to_Z_basis
    else:
        raise ValueError("None of the bit options were supplied")


def get_basis(random_bits: list, index: int):
    bit1, bit2 = either_side_index(random_bits, index)
    return generate_basis_from_two_bits(bit1, bit2)

def get_basis_from_graph(graph,random_bits: list, index: int):
    x_bit = get_x_bit_from_graph(random_bits,index)
    z_bit = get_z_bit_from_graph(graph, random_bits, index)
    return generate_basis_from_two_bits(x_bit, z_bit)

def normalise_single_qubit_results(result):
    values = result.get_counts().values()
    values_array = np.array(list(values))
    total = np.sum(values_array)
    data = values_array / total
    return data

def validated_normalise_single_qubit_results(result):
    if (0,) in list(result.get_counts().keys()) and (1,) in list(result.get_counts().keys()):
        new_result = normalise_single_qubit_result(result)
    elif (0,) in list(result.get_counts().keys()) and not (1,) in list(result.get_counts().keys()):
        pre_result = normalise_single_qubit_result(result)
        new_result = [pre_result[0],0.0]
    elif not (0,) in list(result.get_counts().keys()) and (1,) in list(result.get_counts().keys()):
        pre_result = normalise_single_qubit_result(result)
        new_result = [0.0,pre_result[0]]
    elif not (0,) in list(result.get_counts().keys()) and not (1,) in list(result.get_counts().keys()):
        new_result = [0.0,0.0]
        warnings.warn("There was no outcome in either 0 or 1", Warning)
    else:
        raise ValueError("Outcome indices not correct check")
    return new_result


def compile_run_result_circuit(circuit,n_shots):
    compiled_circuit = backend.get_compiled_circuit(circuit)
    result = backend.run_circuit(
        circuit=compiled_circuit,
        n_shots=n_shots)
    return validated_normalise_single_qubit_results(result)


def compile_and_submit_job_return_handle(backend,circuit, n_shots):
    backend.default_compilation_pass().apply(circuit)
    handle = backend.process_circuit(comp_circuit, n_shots=n_shots)
    return handle


def func_2_str_basis_letter(basis_function):
    func_str = basis_function.__name__
    if re.compile(r'X').search(func_str):
        basis = 'X'
    elif re.compile(r'Y').search(func_str):
        basis = 'Y'
    elif re.compile(r'Z').search(func_str):
        basis = 'Z'
    else:
        raise ValueError("Invalid: basis is only defined on X,Y or Z Paulie basis")
    return basis

def add_data(df,circuit_num,num_shots,input_param,pauli_basis,zero_outcome,one_outcome):
    d = {'circuit_num':circuit_num,'num_shots':num_shots,'input_param':input_param, 'pauli_basis':pauli_basis, 'zero_outcome':zero_outcome,'one_outcome': one_outcome}
    new_df = pd.DataFrame([d])
    df = pd.concat([df, new_df], axis=0, ignore_index=True)
    return df


def add_data_for_circuit(df,circuit_num,num_shots,num_qubits,input_param,pauli_basis,outcomes):
    d = {'circuit_num':circuit_num,'num_shots':num_shots,'num_qubits':num_qubits,'input_param':input_param, 'pauli_basis':pauli_basis, 'outcomes':outcomes}
    new_df = pd.DataFrame([d])
    df = pd.concat([df, new_df], axis=0, ignore_index=True)
    return df


def add_data_for_circuit_03(df,circuit_num,num_shots,num_qubits,bit_basis,num_draws_per_bit_basis,pauli_basis,outcomes):
    d = {'circuit_num':circuit_num,'num_shots':num_shots,'num_qubits':num_qubits,'bit_basis':bit_basis,'num_draws_per_bit_basis':num_draws_per_bit_basis,'pauli_basis':pauli_basis, 'outcomes':outcomes}
    new_df = pd.DataFrame([d])
    df = pd.concat([df, new_df], axis=0, ignore_index=True)
    return df


def read_res_from_handle(backend,df_file: str):
    df = pd.read_csv(df_file)

    if 'outcomes' not in df.columns:
        raise ValueError('The column \'outcomes\' needs to be a column in the data frame, it is not')
        
    ress = list()
    for h in range(len(df)):
        handle = ResultHandle.from_str(df.outcomes[h])
        res = backend.get_result(handle).get_distribution()
        ress.append(res)
    
    df['outcome_res'] = ress
    del df['outcomes']
    df.rename(columns = {'outcome_res':'outcomes'},inplace=True)
    return df
    

def XCX(circuit, bit1: int, bit2: int):
    circuit.H(bit1)
    circuit.CX(bit1, bit2)
    circuit.H(bit1)
    return circuit


def U_gate(circuit, basis_str: str, qubit: int, random_bit: int, theta_int: int):
    theta = (theta_int % 8) * ma.pi / 4.0
    if basis_str == 'X':
        if random_bit == 1:
            circuit.Z(qubit)
        circuit.H(qubit)
    elif basis_str == 'Y':
        rotation_angle = theta + random_bit * ma.pi + ma.pi / 2.0
        circuit.Rx(rotation_angle, qubit)
    elif basis_str == 'Z':
        rotation_angle = theta + random_bit * ma.pi
        circuit.Rx(rotation_angle, qubit)
    else:
        raise ValueError("Invalid: basis is only defined on X,Y or Z Paulie basis, thus U gate not defined")
    return circuit


def V_gate(circuit, qubit: int, theta_int: int):
    theta = (theta_int % 8) * ma.pi / 4.0
    return circuit.Rx(-theta,qubit)

    
"""
Need to work this function out
def select_U_V_gates_randomisation(basis_function, circuit):
    func_str = basis_function.__name__
    if re.compile(r'X').search(func_str):
        r = rm.randint(0, 1)
        theta_int = rm.randint(0, 7)
        theta = (theta_integer % 8) * ma.pi / 4.0
        if r == 1:
            U(bit) = circuit.Z(bit)

        U(bit) = circuit
        V(bit) = circuit.Rz(theta,bit)
    elif re.compile(r'Y').search(func_str):
        basis = 'Y'
    elif re.compile(r'Z').search(func_str):
        basis = 'Z'
    else:
        raise ValueError("Invalid: basis is only defined on X,Y or Z Paulie basis")
    return basis
"""

