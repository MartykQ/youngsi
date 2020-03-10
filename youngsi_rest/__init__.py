from flask import Flask, request, jsonify, render_template
from youngsi_rest.markov_model.model import SongWriter
from flask_cors import CORS
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

path_n1 = os.path.join(THIS_FOLDER, '..', 'data', 'youngsi_n1.pkl')
path_n2 = os.path.join(THIS_FOLDER, '..', 'data', 'youngsi_n2.pkl')


model_n1 = SongWriter.load_raper(path_n1)
model_n2 = SongWriter.load_raper(path_n2)
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/song', methods=['GET'])
def return_a_song():
    base = request.args.get('n_base')

    if int(base) == 1:
        song = model_n1.sing_a_song()
    else:
        song = model_n2.sing_a_song()

    return jsonify({
        'lyrics': song
    })


@app.route('/api/chat', methods=['POST'])
def response_chat():
    data = request.get_json()
    mes = data['message']
    response = model_n1.get_message_response(mes)
    return jsonify({
        'mes': str(response)
    })


@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')
