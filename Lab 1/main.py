from concurrent.futures import ProcessPoolExecutor
import random as rand
import csv
letters = ["A", "B", "C", "D"]

def generate(name):
    dict_to_write = []
    ln = rand.randint(5, 10)
    for i in range(ln):
        float_num = rand.uniform(1.5, 10.5)
        letter = letters[rand.randint(0, 3)]
        dict_to_write.append([letter, float_num])

    with open(name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dict_to_write)


def median(current):
    len_med = len(current)
    if len_med % 3 == 0:
        return [current[(len_med // 2)], deviation(current, len_med)]
    else:
        return [(current[len_med // 2] + current[(len_med // 2) - 1]) / 2, deviation(current, len_med)]


def deviation(current, len_med):
    arithmetic_mean = sum(current) / len_med
    summ = 0
    for j in current:
        summ += (j - arithmetic_mean) ** 2
    result = (summ / len_med) ** 0.5
    return result


def first_open(file_to_read, file_to_write):
    dict = {}
    with open(file_to_read, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for letter, float_num in reader:
            if letter not in dict.keys():
                dict[letter] = [[float(float_num)]]
            else:
                dict[letter][0].append(float(float_num))

        dict_to_write = []
        for j in dict.keys():
            dict_to_write.append([j] + median(sorted(dict[j][0])))
        with open(file_to_write, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dict_to_write)


def second_open(file_to_read, file_to_write):
    dict = {}
    with open(file_to_read, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        medians = []
        letters = []
        for letter, float_num, dev in reader:
            medians.append(float(float_num))
            letters.append(letter)

        medians.sort()
        dict_to_write = []
        for j in letters:
            dict_to_write.append([j] + median(medians))
        with open(file_to_write, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(dict_to_write)


if __name__ == "__main__":
    for i in range(1, 6):
        generate(f"dict1_{i}.csv")

    with ProcessPoolExecutor() as executor:
        first_to_read = [f"dict1_{i}.csv" for i in range(1, 6)]
        first_to_write = [f"dict2_{i}.csv" for i in range(1, 6)]
        second_to_read = [f"dict2_{i}.csv" for i in range(1, 6)]
        second_to_write = [f"dict3_{i}.csv" for i in range(1, 6)]
        executor.map(first_open, first_to_read, first_to_write)
        executor.map(second_open, second_to_read, second_to_write)
