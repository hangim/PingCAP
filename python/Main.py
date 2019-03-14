#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time

INPUT_FILE = "/data/1.txt"
TEMP_DIR = "/data/tmp"

word_pattern = re.compile(r"[a-zA-Z0-9]+")
alpha_list = "abcdedfhijklmnopqrstuvwxyzABCDEDFHIJKLMNOPQRSTUVWXYZ0123456789"


def solve():
    answer_word, answer_index = None, None  # final answer

    # open tmp files, total 62 files
    tmp_file = []
    for it in alpha_list:
        temp_filename = "{}.tmp".format(it)
        temp_filepath = os.path.join(TEMP_DIR, temp_filename)
        tmp_file.append(open(temp_filepath, "w+"))

    # step 1, read input file and split to 62 files, write (word, index, count=1)
    with open(INPUT_FILE, "r") as input_file:
        index = 0
        line_index = 0
        for line in input_file:
            # for word in word_pattern.findall(line):  # Use Regular Expression will be better, but very slow
            for word in line.strip().split(" "):
                if not word or word[0] not in alpha_list or ',' in word:
                    continue
                # print(word, index)  # debug
                index += 1
                tmp_file[alpha_list.find(word[0])].write("{},{},1\n".format(word, index))
            line_index += 1
            if line_index % 100000 == 0:
                print("process {} lines...".format(line_index))

    # step 2, process each tmp file, (word, index, count) --> (word, index.min, count.sum)
    # step 3, filter count.sum == 1 and only save first word
    file_index = 0
    for file in tmp_file:
        file.seek(0)
        word_index_count_dict = {}

        for line in file:
            tmp = line.rstrip().split(",")
            word, index, count = tmp[0], int(tmp[1]), int(tmp[2])
            if word not in word_index_count_dict:
                word_index_count_dict[word] = [index, count]  # {word: [index, count=1]}
            else:
                it = word_index_count_dict[word]  # {word: [index.min, count.sum]}
                it[0] = min(it[0], index)
                it[1] = it[1] + count
        # print(word_index_count_dict)  # debug

        for word, (index, count) in word_index_count_dict.items():
            # print(word, index, count)  # debug
            if count == 1 and (not answer_index or index < answer_index):  # filter and compare
                answer_word = word
                answer_index = index
        del word_index_count_dict

        file_index += 1
        print("process {}/62 files...".format(file_index))

    for it in tmp_file:
        it.close()
    print("---> The answer word is '{}'".format(answer_word))


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print("Error: INPUT_FILE dos not exist.")
        exit(0)
    if not os.path.exists(TEMP_DIR):
        print("Error: TEMP_DIR file dos not exist.")
        exit(0)
    if len(os.listdir(TEMP_DIR)) > 0:
        print("Error: TEMP_DIR is not empty, please delete old files by manual.")
        exit(0)
    print(time.strftime("start time: %Y-%m-%d %H:%M:%S", time.localtime()))
    solve()
    print(time.strftime("end time: %Y-%m-%d %H:%M:%S", time.localtime()))
