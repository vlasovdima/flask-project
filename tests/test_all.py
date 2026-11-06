"""
Автономный скрипт тестирования приложения на Flask (Zero-knowledge QA).
Проверяет синтаксис, структуру файлов, корректность отдачи HTTP-ответов,
работу шаблонизатора Jinja2 и генерацию динамических URL через url_for.
"""

import os
import py_compile
import sys
import unittest

# Добавляем путь к каталогу src для импорта Flask-приложения
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(CURRENT_DIR)
SRC_DIR = os.path.join(TASK_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from app import app


class FlaskAppTestCase(unittest.TestCase):
    """Набор тестов для проверки многостраничного приложения Flask."""

    def setUp(self):
        # Создаем тестовый клиент Flask
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_syntax_and_compilation(self):
        """Проверка 1: Компиляция исходных файлов Python без синтаксических ошибок."""
        app_file = os.path.join(SRC_DIR, "app.py")
        self.assertTrue(os.path.exists(app_file), "Файл app.py не найден!")
        compiled = py_compile.compile(app_file, doraise=True)
        self.assertIsNotNone(compiled)
        print("[OK] Проверка 1: Синтаксический анализ app.py успешно пройден")

    def test_02_template_files_structure(self):
        """Проверка 2: Проверка наличия и структуры обязательных HTML-шаблонов."""
        templates_dir = os.path.join(SRC_DIR, "templates")
        expected_templates = ["base.html", "index.html", "about.html", "changelog.html"]
        for t in expected_templates:
            tpl_path = os.path.join(templates_dir, t)
            self.assertTrue(os.path.exists(tpl_path), f"Шаблон {t} отсутствует в {templates_dir}!")
        print("[OK] Проверка 2: Наличие всех 4 HTML-шаблонов в каталоге templates подтверждено")

    def test_03_index_route(self):
        """Проверка 3: Главная страница (маршрут /)."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200, "Главная страница вернула код отличный от 200")
        html = response.get_data(as_text=True)
        self.assertIn("Главная", html, "Заголовок 'Главная' не найден на странице")
        self.assertIn("Мой Flask-проект", html, "Базовый заголовок из base.html не найден")
        self.assertIn("Это главная страница учебного Flask-приложения", html)
        self.assertIn("Flask Project", html, "Подвал из base.html не отобразился")
        print("[OK] Проверка 3: Главная страница (GET / - 200 OK) рендерится корректно")

    def test_04_about_route(self):
        """Проверка 4: Страница 'О проекте' (маршрут /about)."""
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200, "Страница /about вернула код отличный от 200")
        html = response.get_data(as_text=True)
        self.assertIn("О проекте", html)
        self.assertIn("Цель проекта заключается в изучении базовых принципов", html)
        self.assertIn("Мой Flask-проект", html)
        print("[OK] Проверка 4: Страница 'О проекте' (GET /about - 200 OK) рендерится корректно")

    def test_05_changelog_route(self):
        """Проверка 5: Страница 'Лог изменений' (маршрут /changelog)."""
        response = self.client.get("/changelog")
        self.assertEqual(response.status_code, 200, "Страница /changelog вернула код отличный от 200")
        html = response.get_data(as_text=True)
        self.assertIn("Лог изменений", html)
        self.assertIn("Версия 0.1", html)
        self.assertIn("Версия 0.5", html)
        print("[OK] Проверка 5: Страница 'Лог изменений' (GET /changelog - 200 OK) рендерится корректно")

    def test_06_url_for_resolution(self):
        """Проверка 6: Корректность разрешения маршрутов через url_for."""
        with app.test_request_context():
            from flask import url_for
            self.assertEqual(url_for("index"), "/")
            self.assertEqual(url_for("about"), "/about")
            self.assertEqual(url_for("changelog"), "/changelog")
        print("[OK] Проверка 6: Генерация URL через функцию url_for работает строго по именам вью-функций")

    def test_07_not_found_edge_case(self):
        """Проверка 7: Обработка несуществующего маршрута (404 Not Found)."""
        response = self.client.get("/non_existent_page_12345")
        self.assertEqual(response.status_code, 404, "Несуществующий URL не вернул код 404")
        print("[OK] Проверка 7: Граничный случай - несуществующий маршрут возвращает 404 Not Found")


if __name__ == "__main__":
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 60)
    print("  ЗАПУСК НЕЗАВИСИМОГО АУДИТА FLASK-ПРИЛОЖЕНИЯ (ZERO-KNOWLEDGE QA)")
    print("=" * 60)

    suite = unittest.TestLoader().loadTestsFromTestCase(FlaskAppTestCase)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print("-" * 60)
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors

    if result.wasSuccessful():
        print(f"Все проверки успешно пройдены ({passed}/{total}). Ошибок не обнаружено.")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"ОБНАРУЖЕНЫ ОШИБКИ: {failures} провалов, {errors} сбоев!")
        sys.exit(1)
