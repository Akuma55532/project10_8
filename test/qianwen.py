import os
from openai import OpenAI

# 确保环境变量已设置
if not os.getenv("DASHSCOPE_API_KEY"):
    raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

# 初始化API客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def get_response(prompt):
    try:
        # 调用API
        completion = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ],
            response_format=[
                "type": "json_object"
            ]
        )

        # 获取API的回复
        response_content = completion.choices[0].message.content

        return response_content
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return None




# 初步对话
def preinput():
    ready_to_process = False
    while not ready_to_process:
        user_input = input("请输入您的问题或指令（输入'可以'结束初步对话）：")
        if user_input.lower() == '可以':
            ready_to_process = True
            print("初步对话结束，准备进行词汇处理。")
        else:
            response = get_response(user_input)
            print("模型回复：", response)

# 词汇数据
vocabulary_data = [
    ('系统', 35626, 0.8),
    ('电压', 34314, 0.75),
    ('电流', 31931, 0.7),
    ('保护', 29069, 0.65),
    ('运行', 23335, 0.6),
    ('控制', 19802, 0.55),
    ('进行', 19120, 0.5),
    ('设备', 18686, 0.45),
    ('工作', 16704, 0.4),
    ('线路', 16254, 0.35),
    ('电路', 16071, 0.3),
    ('电力', 14814, 0.25),
    ('装置', 14275, 0.2),
    ('变压器', 13880, 0.15),
    ('可以', 13612, 0.1),
    ('采用', 12641, 0.05),
    ('故障', 12602, 0.04),
    ('技术', 12384, 0.03)
]

input_prompt = ""

for word, freq, idf in vocabulary_data:
    input_prompt += f"{word} {freq} {idf}\n"

print(input_prompt)


if __name__ == "__main__":

    preinput()    #预输入，调节参数

    test()

    main_process()

    json_process()