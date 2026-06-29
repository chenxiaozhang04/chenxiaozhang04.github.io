#!/usr/bin/env python3
"""本地预览个人主页：启动一个静态服务器并自动打开浏览器。

用法：
    python3 serve.py            # 默认端口 8000
    python3 serve.py 8080       # 指定端口

启动后修改 index.html，浏览器刷新即可看到最新效果。按 Ctrl+C 停止。
"""

import http.server
import os
import socketserver
import sys
import threading
import webbrowser

# 关闭缓存，确保每次刷新都拿到最新文件
class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s - %s\n" % (self.address_string(), fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    url = f"http://localhost:{port}/index.html"

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), NoCacheHandler) as httpd:
        print(f"\n本地预览已启动：{url}")
        print("修改 index.html 后，浏览器刷新即可看到最新效果。")
        print("按 Ctrl+C 停止。\n")

        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止预览。")


if __name__ == "__main__":
    main()
