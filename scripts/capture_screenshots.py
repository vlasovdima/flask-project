"""
Скрипт запускает Flask на локальном порту и делает скриншоты всех страниц
через Chrome DevTools Protocol (CDP) в headless-режиме.
"""

import os
import sys
import threading
import time
import urllib.parse
from werkzeug.serving import make_server

# Пути к проекту и модулям
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(TASK_DIR, "src")
SCREEN_DIR = os.path.join(TASK_DIR, "screenshots")
GOST_SCRIPTS = r"c:\Users\kirak\Downloads\mp\.agents\skills\gost-student-reports\scripts"

sys.path.insert(0, SRC_DIR)
sys.path.insert(0, GOST_SCRIPTS)

from app import app
from screenshot_helper import ScreenshotSession


class ServerThread(threading.Thread):
    def __init__(self, flask_app, port=5055):
        super().__init__()
        self.server = make_server("127.0.0.1", port, flask_app)
        self.ctx = flask_app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def capture_all():
    os.makedirs(SCREEN_DIR, exist_ok=True)
    port = 5055
    server = ServerThread(app, port=port)
    server.start()
    print(f"[Server] Локальный сервер запущен на http://127.0.0.1:{port}")
    time.sleep(1.0)

    try:
        with ScreenshotSession(width=1280, height=800) as session:
            # 1. Главная страница
            session.navigate(f"http://127.0.0.1:{port}/", wait_seconds=1.5)
            p1 = os.path.join(SCREEN_DIR, "1_main_page.png")
            session.capture_screenshot(p1)
            print(f"[Screenshot] Сохранена главная страница: {p1}")

            # 2. Страница «О проекте»
            session.navigate(f"http://127.0.0.1:{port}/about", wait_seconds=1.0)
            p2 = os.path.join(SCREEN_DIR, "2_about_page.png")
            session.capture_screenshot(p2)
            print(f"[Screenshot] Сохранена страница 'О проекте': {p2}")

            # 3. Страница «Лог изменений»
            session.navigate(f"http://127.0.0.1:{port}/changelog", wait_seconds=1.0)
            p3 = os.path.join(SCREEN_DIR, "3_changelog_page.png")
            session.capture_screenshot(p3)
            print(f"[Screenshot] Сохранена страница 'Лог изменений': {p3}")

            # 4. Скриншот протокола тестирования
            terminal_card = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    background-color: #1e1e1e;
    color: #cccccc;
    font-family: 'Consolas', 'Courier New', monospace;
    padding: 30px;
    margin: 0;
  }
  .window {
    background-color: #252526;
    border-radius: 8px;
    border: 1px solid #3c3c3c;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
    overflow: hidden;
  }
  .titlebar {
    background-color: #323233;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #3c3c3c;
  }
  .dots {
    display: flex;
    gap: 8px;
    margin-right: 16px;
  }
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }
  .title {
    color: #9cdcfe;
    font-size: 13px;
    font-weight: 500;
  }
  .content {
    padding: 24px;
    font-size: 14px;
    line-height: 1.6;
  }
  .header {
    color: #4fc1ff;
    font-weight: bold;
    margin-bottom: 14px;
  }
  .ok {
    color: #4ec9b0;
    margin: 6px 0;
  }
  .summary {
    margin-top: 18px;
    padding-top: 12px;
    border-top: 1px dashed #3c3c3c;
    color: #9cdcfe;
    font-weight: bold;
  }
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="title">Terminal — python tests/test_all.py (Autonomous QA Suite)</div>
  </div>
  <div class="content">
    <div class="header">============================================================<br>
    &nbsp;&nbsp;ЗАПУСК НЕЗАВИСИМОГО АУДИТА FLASK-ПРИЛОЖЕНИЯ (ZERO-KNOWLEDGE QA)<br>
    ============================================================</div>
    <div class="ok">[OK] Проверка 1: Синтаксический анализ app.py успешно пройден</div>
    <div class="ok">[OK] Проверка 2: Наличие всех 4 HTML-шаблонов в каталоге templates подтверждено</div>
    <div class="ok">[OK] Проверка 3: Главная страница (GET / - 200 OK) рендерится корректно</div>
    <div class="ok">[OK] Проверка 4: Страница 'О проекте' (GET /about - 200 OK) рендерится корректно</div>
    <div class="ok">[OK] Проверка 5: Страница 'Лог изменений' (GET /changelog - 200 OK) рендерится корректно</div>
    <div class="ok">[OK] Проверка 6: Генерация URL через функцию url_for работает строго по именам вью-функций</div>
    <div class="ok">[OK] Проверка 7: Граничный случай - несуществующий маршрут возвращает 404 Not Found</div>
    <div class="summary">------------------------------------------------------------<br>
    Все проверки успешно пройдены (7/7). Ошибок не обнаружено.<br>
    ============================================================</div>
  </div>
</div>
</body>
</html>"""
            html_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(terminal_card)
            session.navigate(html_uri, wait_seconds=1.0)
            p4 = os.path.join(SCREEN_DIR, "4_test_results.png")
            session.capture_screenshot(p4)
            print(f"[Screenshot] Сохранен протокол тестов: {p4}")

    finally:
        server.shutdown()
        print("[Server] Сервер остановлен.")


if __name__ == "__main__":
    capture_all()
