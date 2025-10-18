from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Получаем путь к директории, где находится server.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Формируем полный путь к index.html
        html_path = os.path.join(current_dir, 'index.html')

        # Все GET-запросы возвращают страницу контактов
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Чтение HTML-файла
        try:
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        # Обработка POST-запросов
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # Вывод данных в консоль
        print("Получены POST-данные:")
        try:
            # Пытаемся распарсить JSON
            data = json.loads(post_data.decode('utf-8'))
            print("JSON данные:", data)
        except:
            # Если не JSON, выводим как есть
            print("Данные формы:", post_data.decode('utf-8'))

        # Ответ клиенту
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write('Данные получены сервером'.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Запуск сервера на порту {port}...')
    print('Откройте http://localhost:8000 в браузере')
    httpd.serve_forever()


if __name__ == '__main__':
    run()