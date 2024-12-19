import os
from openai import OpenAI
import time

# 确保环境变量已设置
if not os.getenv("DASHSCOPE_API_KEY"):
    raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

# 初始化API客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 初始化对话历史
conversation_history = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
]


def qianwen_back(prompt):
    # 更新对话历史
    conversation_history.append({'role': 'user', 'content': prompt})

    try:
        # 调用API
        response = client.chat.completions.create(
            model="qwen-max",  # 使用适当的模型名称
            messages=conversation_history
        )

        if response.choices:
            # 获取API的回复
            response_content = response.choices[0].message.content

            # 更新对话历史
            conversation_history.append({'role': 'assistant', 'content': response_content})

            return response_content
        else:
            print("API 调用返回无有效响应，可能是由于网络问题或其他错误。")
            return None

    except Exception as e:
        print(f"调用失败: {e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return None


# 示例调用
if __name__ == "__main__":
    user_input = "保护 （“bǎo hù”）\n" \
                 "1.动词，用于防止损害或危险，如：保护环境、保护文化遗产。\n" \
                 "2.名词，指防护措施或行为，如：动物保护、环境保护措施。\n" \
                 "3.高频搭配：环境保护、文化遗产保护、消费者保护、野生动植物保护。\n" \
                 "根据上面格式回复我下面说的词语"
    response = qianwen_back(user_input)
    if response:
        print(f"{response}")
    while True:
        user_input = input()
        response = qianwen_back(user_input)
        if response:
            print(f"{response}")