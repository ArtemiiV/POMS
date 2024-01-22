from communication import main
import matplotlib.pyplot as plt


Name = input("Введите имя и фамилию: ")
key = int(input("Введите число для вставки в массив: "))
std_dev = float(input("Введите стандартное отклонение: "))
spectre_1 = main(Name, 2, std_dev, key)
spectre_2 = main(Name, 4, std_dev, key)
spectre_3 = main(Name, 8, std_dev, key)

plt.figure()
plt.title('Spectre_OF_signal')
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.plot(spectre_1)
plt.plot(spectre_2)
plt.plot(spectre_3)
plt.show()

