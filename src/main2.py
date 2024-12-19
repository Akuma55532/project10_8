from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from openai import OpenAI
import re

# 定义过滤词文件路径
COMMON_PATH = r'..\resource\拼音排序\通用_拼音.txt'

TECH_PATH = r'..\resource\拼音排序\技术_拼音.txt'
# 确保环境变量已设置
if not os.getenv("DASHSCOPE_API_KEY"):
    raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

# 初始化 OpenAI API 客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 初始化对话历史
conversation_history = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
]

def read_words_from_file(filepath):
    """
    从文件中读取词语列表
    :param filepath: 文件路径
    :return: 词语列表
    """
    words_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line_split = line.strip().split()
                if len(line_split) == 1:
                    word = line_split  # 提取词语部分
                    words_list.append(word)
                if len(line_split) == 3:
                    word, _, _ = line_split  # 提取词语部分
                    words_list.append(word)
    except FileNotFoundError:
        print(f"文件未找到: {filepath}")
    return words_list

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        """
        设置通用响应头
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """
        处理 OPTIONS 请求
        """
        self.send_response(200)
        self._set_headers()

    def do_GET(self):
        """
        处理 GET 请求
        """
        if self.path == '/get-common-words':
            self._handle_get_common_words()
        elif self.path == '/get-profess-words':
            self._handle_get_profess_words()
        else:
            self.send_error(404, "路径未找到")

    def _handle_get_common_words(self):
        """
        返回过滤词列表
        """
        self.send_response(200)
        self._set_headers()
        words = read_words_from_file(COMMON_PATH)
        response = json.dumps(words)
        print(f"返回通用词: {response}")
        self.wfile.write(response.encode('utf-8'))

    def _handle_get_profess_words(self):
        """
        返回专业词汇列表
        """
        self.send_response(200)
        self._set_headers()
        words = read_words_from_file(TECH_PATH)
        response = json.dumps(words)
        print(f"返回专业词: {response}")
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        """
        处理 POST 请求
        """
        if self.path == '/word_info':
            self._handle_word_info()
        else:
            self.send_error(404, "路径未找到")

    def _handle_word_info(self):
        """
        处理词语信息查询
        """
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            words_response = self._fetch_word_info(data.get('data', ''))
            response = self._parse_word_response(words_response)

            self.send_response(200)
            self._set_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except (json.JSONDecodeError, KeyError):
            self.send_error(400, "无效的 JSON 数据")
        except Exception as e:
            self.send_error(500, f"服务器错误: {e}")

    def _fetch_word_info(self, prompt):
        """
        调用 API 获取词语信息
        :param prompt: 用户输入
        :return: API 响应
        """
        conversation_history.append({'role': 'user', 'content': prompt})
        try:
            response = client.chat.completions.create(
                model="qwen-max",
                messages=conversation_history
            )
            if response.choices:
                response_content = response.choices[0].message.content
                conversation_history.append({'role': 'assistant', 'content': response_content})
                return response_content
        except Exception as e:
            print(f"API 调用失败: {e}")
        return ""

    def _parse_word_response(self, response):
        """
        解析 API 响应内容
        :param response: API 响应
        :return: 解析后的字典
        """
        word_title, word_dapei, word_atitude_lines = '', '', []
        word_pattern = r'词语：([\u4e00-\u9fa5]{1,10})\s'
        dapei_pattern = r'高频搭配：([\u4e00-\u9fa5])'
        found_word = False

        for line in response.split('\n'):
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
                word_atitude_lines.append(line.strip())
        print(f"response:{response}")
        print(f"words_title:{word_title}")
        print(f"words_dapei:{word_dapei}")
        print(f"words_atitude:{word_atitude_lines}")

        return {
            'status': 'success',
            'word_title': word_title,
            'word_dapei': word_dapei,
            'word_atitude': '\n'.join(word_atitude_lines).strip()
        }

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    """
    启动 HTTP 服务器
    :param server_class: HTTP 服务器类
    :param handler_class: 请求处理类
    :param port: 端口号
    """
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f'HTTP 服务器已启动，端口号: {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    user_input = "词语：保护 （“bǎo hù”）\n" \
                 "1.动词：用于防止损害或危险，如：保护环境、保护文化遗产。\n" \
                 "2.名词：指防护措施或行为，如：动物保护、环境保护措施。\n" \
                 "高频搭配：环境保护、文化遗产保护、消费者保护、野生动植物保护。\n" \
                 "根据上面格式回复我下面说的词语。"
    conversation_history.append({'role': 'user', 'content': user_input})
    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=conversation_history
        )
        if response.choices:
            response_content = response.choices[0].message.content
            conversation_history.append({'role': 'assistant', 'content': response_content})
    except Exception as e:
        print(f"API 调用失败: {e}")
    run()