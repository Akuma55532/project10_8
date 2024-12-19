import os
import re

input_folder = r"..\resource\dict"
output_folder = r"..\resource\dict"


pattern_1 = r'\d+\.\s*\d+摇(.*?)摇[a-zA-Z\s]+'

pattern_2 = r'(.*?)摇'

pattern_feizhong = r'[^\u4e00-\u9fff]'



def main(input_folder,output_folder):
    for filename in os.listdir(input_folder):
        if filename == "电力dict.txt":
            file_path = os.path.join(input_folder,filename)
            words = []
            with open(file_path,'r',encoding='utf-8') as file:
                for line in file:
                    match = re.search(pattern_1, line)
                    if match:
                        word = match.group(1)
                        if word == '':
                            continue
                        matches = re.search(pattern_feizhong, word)
                        if matches:
                            continue

                        words.append(word)

                    match = re.search(pattern_2, line)
                    if match:
                        word = match.group(1)
                        if word == '':
                            continue
                        matches = re.search(pattern_feizhong, word)
                        if matches:
                            continue

                        words.append(word)

            output_path = os.path.join(output_folder,'end.txt')
            with open(output_path,'w',encoding='utf-8') as outputfile:
                for word in words:
                    outputfile.write(f"{word}\n")




if __name__ == "__main__":
    main(input_folder,output_folder)
    print("finished")