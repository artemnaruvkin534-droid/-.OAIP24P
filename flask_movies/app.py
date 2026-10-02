from flask import Flask, render_template

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "title": "Интерстеллар",
        "year": 2014,
        "rating": 8.7,
        "genre": "Фантастика, драма",
        "description": "Группа астронавтов отправляется через червоточину в поисках новой планеты для человечества."
    },
    {
        "id": 2,
        "title": "Матрица",
        "year": 1999,
        "rating": 8.5,
        "genre": "Фантастика, боевик",
        "description": "Хакер Нео узнаёт, что привычный мир — компьютерная симуляция, и присоединяется к борьбе с машинами."
    },
    {
        "id": 3,
        "title": "Шрек",
        "year": 2001,
        "rating": 8.1,
        "genre": "Мультфильм, комедия",
        "description": "Огр Шрек вместе с говорящим ослом отправляется спасать принцессу, чтобы вернуть себе болото."
    },
    {
        "id": 4,
        "title": "Начало",
        "year": 2010,
        "rating": 8.8,
        "genre": "Фантастика, триллер",
        "description": "Вор, проникающий в сны, получает задание внедрить идею в сознание человека."
    },
    {
        "id": 5,
        "title": "Форрест Гамп",
        "year": 1994,
        "rating": 8.9,
        "genre": "Драма, мелодрама",
        "description": "История простого человека с добрым сердцем, ставшего свидетелем важнейших событий американской истории."
    },
    {
        "id": 6,
        "title": "Тор: Рагнарёк",
        "year": 2017,
        "rating": 7.9,
        "genre": "Фантастика, комедия",
        "description": "Тор попадает на планету-арену и должен вернуться в Асгард, чтобы остановить богиню смерти Хелу."
    }
]


@app.route("/")
def index():
    return render_template("index.html", movies=movies)


@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    for item in movies:
        if item["id"] == movie_id:
            return render_template("movie.html", movie=item)

    return "Фильм не найден", 404


if __name__ == "__main__":
    app.run(debug=True)
