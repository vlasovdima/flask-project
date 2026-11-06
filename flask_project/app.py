"""
Практическое занятие №1: Создание простого веб-проекта на Flask.
Студент: Власов Дмитрий (группа М3О-236БВ-25)

В приложении настроены три маршрута:
- / - главная страница
- /about - страница с описанием проекта
- /changelog - лог изменений версий
Все страницы наследуют структуру base.html.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # Отображаем главную страницу
    return render_template("index.html")


@app.route("/about")
def about():
    # Отображаем страницу "О проекте"
    return render_template("about.html")


@app.route("/changelog")
def changelog():
    # Отображаем журнал версий
    return render_template("changelog.html")


if __name__ == "__main__":
    # Запускаем локальный веб-сервер в режиме отладки
    app.run(debug=True)
