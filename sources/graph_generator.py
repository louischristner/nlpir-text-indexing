import os
import sys
import random

import matplotlib.pyplot as plt
from wordcloud import WordCloud



# graphs

def generate_bar_graph(file_index: dict, folder_name: str):
    words = list(file_index.keys())
    values = list(file_index.values())

    plt.figure(figsize=(15, 10))
    plt.title(folder_name)
    plt.bar(words, values)
    plt.xticks(rotation=60)
    plt.xlabel("Words")
    plt.ylabel("Occurences")
    plt.show()


def generate_wordcloud_graph(file_index: dict, folder_name: dict):
    words = []

    for word in file_index:
        for _i in range(file_index[word]):
            words.append(word)

    # if not shuffle the words appear twice on the graph
    random.shuffle(words)

    wordcloud = WordCloud().generate(' '.join(words))
    wordcloud.to_file("results/" + folder_name + "_wordcloud.png")

    plt.figure()
    plt.title(folder_name)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()



# information retrieval

def get_file_content_string(file_path: str) -> str:
    file_content_line = ""
    file = open(file_path, "r")

    for line in file.readlines():
        clean_line = line.lstrip().rstrip()
        if len(clean_line) > 0:
            if clean_line.upper() != clean_line:
                file_content_line += " " + clean_line

    file.close()

    file_content_line = file_content_line.lower()

    for symbol in [ ".", ",", ":", ";", "!", "?", "(", ")", "\"", " - ", "--", "'", "*" ]:
        file_content_line = file_content_line.replace(symbol, ' ')
    return file_content_line


def get_file_index(file_path: str, stopwords: list[str]) -> dict:
    file = open(file_path, "r")
    file_content = []
    file_index = {}

    file_content_line = get_file_content_string(file.readlines())

    for word in file_content_line.split(' '):
        if len(word) > 0 and not word in stopwords:
            file_content.append(word)

    for word in file_content:
        if not word in file_index:
            file_index[word] = file_content.count(word)
    return file_index


def get_highest_values_file_index(file_index: dict, amount: int) -> dict:
    tmp_key = ""
    tmp_amount = 0
    tmp_file_index = {}

    for _i in range(amount):
        for key in file_index.keys():
            if file_index[key] > tmp_amount and not key in tmp_file_index.keys():
                tmp_amount = file_index[key]
                tmp_key = key
        tmp_file_index[tmp_key] = tmp_amount
        tmp_amount = 0
        tmp_key = ""
    return tmp_file_index


def get_folder_file_index(folder_name: str, stopwords: list[str]):
    files_index = {}

    for file_name in sorted(os.listdir(folder_name)):
        print(file_name)

        file_content_line = get_file_content_string(folder_name + "/" + file_name)
        file_content_list = file_content_line.split(' ')
        file_index = {}

        for word in file_content_list:
            if len(word) > 0 and not word in stopwords and not word in file_index:
                file_index[word] = file_content_list.count(word)

        for word in file_index:
            if not word in files_index:
                files_index[word] = 0
            files_index[word] += file_index[word]

    return files_index


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        first_folder_name = sys.argv[1]
        second_folder_name = sys.argv[2]

        stopwords_file = open("stopwords.txt")
        stopwords = [ word.replace('\n', '') for word in stopwords_file.readlines() ]

        # first folder
        first_folder_file_index = get_folder_file_index(first_folder_name, stopwords)
        first_folder_highest_values_index = get_highest_values_file_index(first_folder_file_index, 60)

        generate_bar_graph(first_folder_highest_values_index, first_folder_name)
        generate_wordcloud_graph(first_folder_highest_values_index, first_folder_name)

        # second folder
        second_folder_file_index = get_folder_file_index(second_folder_name, stopwords)
        second_folder_highest_values_index = get_highest_values_file_index(second_folder_file_index, 60)

        generate_bar_graph(second_folder_highest_values_index, second_folder_name)
        generate_wordcloud_graph(second_folder_highest_values_index, second_folder_name)

    else: print("USAGE: requires two folder names as argument")
