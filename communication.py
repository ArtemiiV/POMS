import numpy as np
from scipy.fft import fftshift, fft
from function import right_shift, find_crc, generate_golds, encode_text_to_binary, plot_graph, decode_binary_to_letters

def main(input_name, N, std_deviation, insertion_key):

    # Кодирование информации
    encoded_data = encode_text_to_binary(input_name)
    plot_graph(encoded_data, "Name and surname", 'Time', 'Bit')

    # Вычисление CRC
    M = len(encoded_data)
    divisor = [1, 0, 1, 0, 0, 1, 1, 1]
    for i in range(len(divisor) - 1):
        encoded_data.append(0)
    crc_result = find_crc(encoded_data)
    print("CRC:", crc_result)
    for i in range(M, len(encoded_data)):
        encoded_data[i] = crc_result[i - M]

    # Генерация последовательности Голда
    sequence_of_golden, G = generate_golds()
    for i in range(G):
        encoded_data.append(0)
        encoded_data = right_shift(encoded_data)
    for i in range(G):
        encoded_data[i] = sequence_of_golden[i]
    plot_graph(encoded_data, "Gold_sequence", 'Time', 'Bit')

    # Преобразования битов в временные отсчёты сигналов
    signal = np.repeat(encoded_data, N)
    plot_graph(signal, "Time_score_graph", 'Time', 'Countdown')
    length = len(signal)

    # Внесение массива информации в массив нулей
    B_sig = [int(0) for i in range(2 * len(signal))]
    while True:
        if 0 < insertion_key < len(signal):
            break
        else:
            print("Недопустимое число, введите ещё раз")
            insertion_key = int(input())
    for i in range(len(B_sig)):
        if insertion_key <= i < insertion_key + len(signal):
            B_sig[i] = signal[i - insertion_key]
        else:
            B_sig[i] = 0

    plot_graph(B_sig, "Radio_info", 'Time', 'Countdown')

    # Генерация шума и передача массива на приёмник
    signal = np.asarray(B_sig)
    create_noise = np.random.normal(0, std_deviation, len(signal))
    noisy_signal = []
    for i in range(len(signal)):
        noisy_signal.append(create_noise[i] + signal[i])
    plot_graph(noisy_signal, "noisy_signal", 'Time', 'Countdown')
    spectre = fftshift(fft(noisy_signal[100:500]))

    # Синхронизация с сигналом и отброс лишних нулей в массиве
    signal = noisy_signal
    sequence_of_golden, G = generate_golds()
    sequence_of_golden = np.repeat(sequence_of_golden, N)
    #autocore = []
    for i in range(len(signal) - len(sequence_of_golden)):
        summation = 0
        for j in range(len(sequence_of_golden)):
            try:
                summation = summation + (sequence_of_golden[j] * signal[i + j])
            except IndexError:
                break
        #autocore.append(summation)
        if i == 0:
            maximum = summation
            pos = 0
        elif maximum < summation:
            maximum = summation
            pos = i
    #print(maximum)
    synchronized_signal = []
    for i in range(pos, pos + length):
        synchronized_signal.append(signal[i])
    #
    #plot_graph(autocore, 'Autocore', 'Corilantion', 'Lag')
    plot_graph(synchronized_signal, "synchronized_signal", 'Time', 'Countdown')


    # Преобразование временных отсчётов в информацию и избавление от шума
# Преобразование временных отсчётов в информацию и избавление от шума
    cipher = []
    for i in range(int(len(synchronized_signal) / N)):
        if synchronized_signal[i * N] > 0.5:
            cipher.append(1)
        else:
            cipher.append(0)
    
    # Удаление последовательности Голда
    cipher_without_gold = []
    for i in range(G, len(cipher)):
        cipher_without_gold.append(cipher[i])
    
    # Проверка CRC
    crc_check = find_crc(cipher_without_gold)
    print("CRC:", crc_check)
    if 1 in crc_check:
        print("Ошибка CRC")
    else:
        # Удаление CRC и декодирование битов информации в буквы
        word = []
        for i in range(len(cipher_without_gold) - 7):
            word.append(cipher_without_gold[i])
        decoded_message = decode_binary_to_letters(word)
        decoded_text = ""
        for i in decoded_message:
            if ord(i) >= 65 and ord(i) < 90:
                decoded_text += " "
            decoded_text += i
        print(decoded_text[1:])
    
    # Исправление спектра
    spectre = np.abs(spectre)
    
    return spectre


#Исправить спект
#понять что
#что такое частота дискртизации
#какое расстояние между двумя отчетами
#откурыть курс экспоненты матлаба
#как длинна символа влияет на длинну символа 
#подписать оси