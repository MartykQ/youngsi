from flask import Flask, request, jsonify
from youngsi_rest.markov_model.model import SongWriter
from flask_cors import CORS
import os

model_n1 = SongWriter.load_raper(r'data\youngsi_n1.pkl')
model_n2 = SongWriter.load_raper(r'data\youngsi_n2.pkl')
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

    song_string = ""
    for segment in song:
        for sentence in segment:
            song_string = f"{song_string}\n {sentence} "

    return jsonify({
        'lyrics': song_string
    })
