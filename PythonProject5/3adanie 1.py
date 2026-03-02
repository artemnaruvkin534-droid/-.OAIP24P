from flask import Flask, render_template, request, session, flash, url_for
from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = 'arbuz123'

VALID_USER = "student"
VALID_PASS = "Cerber666"

@app.route('/')
def index():
    if "username" in session:
        return f"Привет, {session['username']}!"
    else:
        return "У вас нет доступа к этому ресурсу"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')


        if user == VALID_USER and password == VALID_PASS:
            session['username'] = user
            flash("Вы успешно вошли", "success")
            return redirect(url_for("profile"))
        else:
            flash("Данные неверны", "danger")

    return render_template('login.html')

@app.route('/profile')
def profile():
    if "username" not in session:
        flash("Сначала войдите в систему!", "warning")
        return redirect(url_for("login"))

    return render_template('profile.html', name=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из системы", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug = True)
