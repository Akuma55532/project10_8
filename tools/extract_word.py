import re
import os


input_filepath = '../resource/result_retry/end.txt'
output_folder = '../resource/result_retry'

def main(input_filepath,output_folder = None):
    words_list = []
    with open(input_filepath,'r',encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()

            if len(line_split) == 4:
                word, freq = line_split[1], line_split[2]
                words_list.append((word,freq))
            else:
                print(line_split)
                break

    print(words_list)

    output_filepath = os.path.join(output_folder, 'enen.txt')

    with open(output_filepath,'w',encoding='utf-8') as output_file:
        for word,freq in words_list:
            output_file.write(f'{word} {freq}' + '\n')

    print(words_list)


main(input_filepath,output_folder)
