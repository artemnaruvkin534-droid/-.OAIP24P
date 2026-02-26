from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    try:
        input_number = float(request.args.get('number', 0))

    except ValueError:

        input_number = 0

    multiplied_number = input_number * 2
    text_message = f"Ваше число {input_number}, умноженное на 2: {multiplied_number}"

    return render_template('index.html',
                           number=multiplied_number,
                           text=text_message)

if __name__ == '__main__':
    app.run(debug=True)