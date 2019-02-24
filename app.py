
from flask import  Flask
from flask import render_template, request
import MarkovModel

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':

        order = int(request.form['order'])
        numZwrot = int(request.form['zwrotki'])
        numVerse = int(request.form['wersy'])
        with open("final.txt", "r") as plik:
            model = MarkovModel.MarkovModel(order, plik)
        xd = model.dropThatBeat(numZwrot, numVerse)
        return render_template("generated.html", xd = xd)

    return render_template("index.html")

@app.route('/generate')
def generate():
    if request.method == 'GET':
        order = request.args.get('order')
    return order

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug= True)



