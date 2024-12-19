from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from openai import OpenAI
import time
import re

filter_path = r'..\resource\result_ful2\filter.txt'

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

def readfile_frompath(filepath):
    words_list = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line_split = line.strip().split()  # 去除行末的换行符并分割
            if len(line_split) == 3:
                word, count, idf = line_split[0], int(line_split[1]), float(line_split[2])
                words_list.append(word)

    return words_list


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # 在这里添加任何自定义的初始化代码
        super().__init__(*args, **kwargs)

        first_input = "词语：保护 (bǎo hù)\n" \
                     "1.动词，用于防止损害或危险，如：保护环境、保护文化遗产。\n" \
                     "2.名词，指防护措施或行为，如：动物保护、环境保护措施。\n" \
                     "3.高频搭配：环境保护、文化遗产保护、消费者保护、野生动植物保护。\n" \
                     "根据上面格式回复我下面说的词语"

        self.qianwen_back(first_input)

    def _set_headers(self):
        # 设置响应头，允许所有来源的请求（生产环境中应更具体）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        # 处理 OPTIONS 请求
        self.send_response(200)
        self._set_headers()

    def do_GET(self):
        if self.path == '/get-common-words':
            # 设置响应码为200 OK
            self.send_response(200)
            # 设置响应头
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # 允许所有来源的跨域请求
            self.end_headers()
            # 发送响应体
            words = readfile_frompath(filter_path)  # 这里可以替换为你想要返回的任何词语列表
            response = json.dumps(words)
            print(f"Returning words: {response}")  # 打印返回的词语列表
            self.wfile.write(response.encode('utf-8'))
        if self.path == '/get-profess-words':
            # 设置响应码为200 OK
            self.send_response(200)
            # 设置响应头
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # 允许所有来源的跨域请求
            self.end_headers()
            # 发送响应体
            words = ['系统', '电压', '电流', '保护', '运行', '控制', '进行', '设备', '工作', '线路', '电路', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好', '你好']  # 这里可以替换为你想要返回的任何词语列表
            response = json.dumps(words)
            print(f"Returning words: {response}")  # 打印返回的词语列表
            self.wfile.write(response.encode('utf-8'))


    def do_POST(self):
        if self.path == '/word_info':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                words_response = self.qianwen_back(data['data'])
                words_response_list = words_response.split('\n')

                # 定义正则表达式模式
                word_pattern = r'词语：([\u4e00-\u9fa5]{1,10})\s'
                dapei_pattern = r'高频搭配：([\u4e00-\u9fa5])'

                word_title, word_dapei, word_atitude_lines = '', '', []
                found_word = False

                for line in words_response_list:
                    if not found_word:
                        match = re.search(word_pattern, line)
                        if match:
                            word_title = line

                            found_word = True
                            continue
                        else:
                            continue

                    match = re.search(dapei_pattern, line, re.MULTILINE)
                    if match:
                        word_dapei = line

                        break
                    else:
                        print(f"{word_atitude_lines}")
                        word_atitude_lines.append(line)

                word_atitude = '\n'.join(word_atitude_lines).strip()

                response = {
                    'status': 'success',
                    'word_title': word_title,
                    'word_dapei': word_dapei,
                    'word_atitude': word_atitude
                }

                self.send_response(200)
                self._set_headers()  # 确保此方法已定义并正确设置响应头
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

            except json.JSONDecodeError as e:
                self.send_error(400, f"Invalid JSON: {e}")
            except Exception as e:
                # 捕获所有其他异常并发送服务器错误响应
                self.send_error(500, f"Server Error: {e}")

        else:
            self.send_error(404, "Not Found")

    def qianwen_back(self, prompt):
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

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()




if __name__ == "__main__":
    run()