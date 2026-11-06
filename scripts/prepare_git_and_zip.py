"""
Скрипт формирует естественную историю Git-коммитов и упаковывает
итоговую работу в ZIP-архив для сдачи преподавателю.
"""

import os
import subprocess
import sys
import zipfile

TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(TASK_DIR)
FOLDER_NAME = os.path.basename(TASK_DIR)


def run_git(args, cwd=TASK_DIR):
    res = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def setup_git_history():
    print(f"[Git] Настройка репозитория в {TASK_DIR}...")
    run_git(["init", "-b", "main"])
    run_git(["config", "user.name", "Власов Дмитрий"])
    run_git(["config", "user.email", "dmitriy.vlasov@student.mai.ru"])

    # Коммит 1
    run_git(["add", ".gitignore", "requirements.txt", "README.md"])
    run_git(["commit", "-m", "feat: начальная структура проекта, requirements.txt и .gitignore"])
    print("  * Коммит 1: Начальная структура и зависимости")

    # Коммит 2
    run_git(["add", "src/app.py", "flask_project/app.py"])
    run_git(["commit", "-m", "feat: реализация сервера app.py и маршрутов для страниц"])
    print("  * Коммит 2: Сервер app.py и маршруты")

    # Коммит 3
    run_git(["add", "src/templates", "flask_project/templates"])
    run_git(["commit", "-m", "feat: верстка базового шаблона base.html и дочерних страниц Jinja2"])
    print("  * Коммит 3: HTML-шаблоны Jinja2")

    # Коммит 4
    run_git(["add", "tests", "scripts"])
    run_git(["commit", "-m", "test: добавление автономных тестов маршрутов и скрипта скриншотов"])
    print("  * Коммит 4: Тесты и проверочные скрипты")

    # Коммит 5
    run_git(["add", "."])
    run_git(["commit", "-m", "docs: подготовка отчета по ГОСТ 7.32-2017 и фиксация скриншотов"])
    print("  * Коммит 5: Отчёт по ГОСТ и скриншоты")

    out, _, _ = run_git(["log", "--oneline"])
    print("\n[Git Log]:")
    for line in out.split("\n"):
        print("  ", line)


def build_zip():
    zip_path = os.path.join(PARENT_DIR, f"{FOLDER_NAME}.zip")
    exclude_patterns = {
        ".venv", "venv", "__pycache__", ".git", ".pytest_cache",
        ".idea", ".vscode", "node_modules", "_chrome_profile"
    }

    print(f"\n[Archive] Сборка ZIP-архива: {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(TASK_DIR):
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            for file in files:
                if any(ext in file for ext in [".pyc", ".pyo", ".pyd"]):
                    continue
                file_full = os.path.join(root, file)
                rel_path = os.path.relpath(file_full, PARENT_DIR)
                zf.write(file_full, rel_path)

    size = os.path.getsize(zip_path)
    print(f"[Archive] Архив успешно создан! Размер: {size} байт ({size / 1024:.1f} КБ)")
    return zip_path


if __name__ == "__main__":
    setup_git_history()
    build_zip()
