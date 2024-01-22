# encoding.py
import numpy as np
import matplotlib.pyplot as plt

def decode_binary_to_letters(code):
    sim = ""
    decoded = []
    j = 0
    for i in code:
        if j == 7:
            decoded.append(chr(int(sim, 2)))
            j = 0
            sim = ""
        sim += str(i)
        j += 1
    decoded.append(chr(int(sim, 2)))
    return decoded

def encode_text_to_binary(text):
    mas = []
    for i in text:
        if i != " ":
            mas.append(ord(i))

    code = []
    for j in mas:
        binary_representation = str(bin(j))
        for i in range(2, len(binary_representation)):
            code.append(int(binary_representation[i]))

    return code

def plot_graph(data, title, xlabel, ylabel):
    graf = np.asarray(data)
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(graf)
    

def find_crc(packet):
    divisor = [1, 0, 1, 0, 0, 1, 1, 1]
    remainder = [i for i in range(len(divisor))]
    for i in range(len(divisor) - 1):
        remainder[i] = packet[i + 1] ^ divisor[i + 1]
    remainder[len(divisor) - 1] = packet[len(divisor)]

    for i in range(len(divisor) + 1, len(packet)):
        if remainder[0] != 0:
            for j in range(len(divisor) - 1):
                remainder[j] = remainder[j + 1] ^ divisor[j + 1]
        else:
            for j in range(len(divisor) - 1):
                remainder[j] = remainder[j + 1]
        remainder[len(divisor) - 1] = packet[i]

    if remainder[0] != 0:
        for j in range(len(divisor)):
            remainder[j] = remainder[j] ^ divisor[j]
    result = []
    for i in range(1, len(remainder)):
        result.append(remainder[i])
    return result

def right_shift(data):
    tmp = data[len(data) - 1]
    for i in range(len(data) - 1, 0, -1):
        data[i] = data[i - 1]
    data[0] = tmp
    return data

def generate_golds():
    x = [1, 1, 1, 1, 0]
    y = [0, 1, 1, 0, 1]
    G = 31
    result = []
    for i in range(G):
        summ_x = x[2] ^ x[3]
        summ_y = y[2] ^ y[1]
        result.append(x[4] ^ y[4])
        x = right_shift(x)
        y = right_shift(y)
        x[0] = summ_x
        y[0] = summ_y
    return result, G


