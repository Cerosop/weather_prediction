from flask import Flask, jsonify, request, render_template
from predict import pre
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def pred():
    if request.method == 'POST':
        y = request.values['sel']
        
        now, p, p2 = pre(int(y))
        
        data = {'now': now, 'p': p, 'p2': p2, 'y': int(y)}
        return jsonify(data)
    else:
        return render_template('main.html')


if __name__ == '__main__':
    app.debug = True
    app.run()