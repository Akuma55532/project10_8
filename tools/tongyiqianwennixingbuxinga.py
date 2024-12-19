import os
from openai import OpenAI
import time


input_file = r"..\resource\ful2\hebing.txt"
output_file = r"..\resource\ful2\response.txt"

def read_file(input_file):
    all_words_list = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()  # 去除行末的换行符并分割
            if len(line_split) == 3:
                word, count, idf = line_split[0], int(line_split[1]), float(line_split[2])
                temp_wordset = (word, count, idf)
                all_words_list.append(temp_wordset)

    return tuple(all_words_list[:1000])


def preinput():
    ready_to_process = False
    while not ready_to_process:
        user_input = input("输入('run'结束对话):")
        if user_input.lower() == 'run':
            ready_to_process = True
            print("初步对话结束，准备进行词汇处理。")
        else:
            response = get_response(user_input)
            print("模型回复：", response)


def get_response(prompt,max_retries=5, retry_delay=2):
    conversation_history.append({'role': 'user', 'content': prompt})
    for attempt in range(max_retries + 1):
        try:
            # 调用API
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=conversation_history,
                timeout=1200  # 设置超时时间为30秒
            )

            if completion is None:
                print("API 调用返回 None，可能是由于网络问题或其他错误。")
                return None

            # 获取API的回复
            response_content = completion.choices[0].message.content

            conversation_history.append({'role': 'assistant', 'content': response_content})

            return response_content
        except Exception as e:
            if attempt < max_retries:
                print(f"尝试 {attempt + 1}/{max_retries} 失败，将在 {retry_delay} 秒后重试: {e}")
                time.sleep(retry_delay)
            else:
                print(f"所有尝试均失败: {e}")
                print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
                return None

def main_process(allwords):
    batch_size = 100

    batches = [allwords[i:i + batch_size] for i in range(0, len(allwords), batch_size)]

    response = ""

    for batch in batches:
        input_prompt = ""

        for word, freq, idf in batch:
            input_prompt += f"{word} {freq} {idf}\n"

        response_temp = get_response(input_prompt).__str__()

        print(batch[-1])

        print(response_temp)

        response += response_temp

        response += "\n----------------------------------------------------------------------\n\n"

    return response


if __name__ == "__main__":


    all_words = read_file(input_file)

    # 确保环境变量已设置
    if not os.getenv("DASHSCOPE_API_KEY"):
        raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

    # 初始化API客户端
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    user_input = "保护 （“bǎo hù”）\n" \
                 "1.动词，用于防止损害或危险，如：保护环境、保护文化遗产。\n" \
                 "2.名词，指防护措施或行为，如：动物保护、环境保护措施。\n" \
                 "3.高频搭配：环境保护、文化遗产保护、消费者保护、野生动植物保护。\n" \
                 "根据上面格式回复我下面说的词语"

    response_end = main_process(all_words)

    with open(output_file,'w',encoding='utf-8') as file:
        file.write(response_end)
#
#
# 下面我将输入大量词汇数据,格式为(词汇 词汇在文本的出现频率 词汇在文本中的idf值)
# 我需要你帮我根据“词频，idf值(idf越小词语越普遍)和词汇的专业性(电气专业)”三个因素来进行对词汇进行划分为"高频专业性词汇，低频专业性词汇，高频非专业性词汇，低频非专业性词汇"四个等级
# 注意：词频大于100且idf小于3.5属于高频词，其他的属于低频词。专业性靠你来判断
# 一定要精准按照我给的要求划分高频和低频词，即使没有低频词也没关系
# 请每一次输出都保持相同的格式，以便我之后对其进行数据统计



