from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return redirect(url_for('me', name='Гость'))
    else:
        flash('Неверный логин или пароль!')
        return redirect(url_for('login'))


@app.route('/me/<name>')
def me(name):
    return render_template('index.html', name=name)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)