from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = 'arbuz123'
VALID_USER = "admin"
VALID_PASS = "123"

materials = [
    {
        "id": 1,
        "title": "Flask для начинающих",
        "category": "Книга",
        "author": "Иванов",
        "description": "Введение во Flask"
    },
    {
        "id": 2,
        "title": "Python для профессионалов",
        "category": "Статья",
        "author": "Петров",
        "description": "Продвинутые техники Python"
    },
    {
        "id": 3,
        "title": "JavaScript основы",
        "category": "Видеоурок",
        "author": "Сидоров",
        "description": "Базовые концепции JavaScript"
    }
]

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/materials')
def materials_list():
    return render_template('materials.html', materials=materials)

@app.route('/materials/<int:material_id>')
def material_detail(material_id):
    for material in materials:
        if material["id"] == material_id:
            return render_template('material_detail.html', material=material)
    return "Материал не найден", 404




@app.route('/stats')
def stats():

    total_materials = len(materials)
    categories = {}
    authors = {}

    for material in materials:

        if material['category'] in categories:
            categories[material['category']] += 1
        else:
            categories[material['category']] = 1

        if material['author'] in authors:
            authors[material['author']] += 1
        else:
            authors[material['author']] = 1

    return render_template('stats.html',
                           total_materials=total_materials,
                           categories=categories,
                           authors=authors)

@app.route('/add', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':

        new_id = len(materials) + 1
        new_material = {
            "id": new_id,
            "title": request.form['title'],
            "category": request.form['category'],
            "author": request.form['author'],
            "description": request.form['description']
        }
        materials.append(new_material)
        return redirect(url_for('materials_list'))

    return render_template('add_material.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')


        if user == VALID_USER and password == VALID_PASS:
            session['username'] = user
            flash ("Вы успешно вошли", "success")
            return redirect(url_for("profile"))
        else:
            flash("Данные неверны", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)