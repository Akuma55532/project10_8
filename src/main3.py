from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import re

COMMON_PATH = r'..\resource\拼音排序\通用_remote.txt'

TECH_PATH = r'..\resource\拼音排序\技术_remote.txt'

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
                line_split = line.strip().split('/')
                words_list.append(line_split)
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
    run()