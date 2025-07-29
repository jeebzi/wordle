# app.py

from flask import Flask, request, jsonify, send_from_directory
from wordle_api import full_round

app = Flask(__name__, static_folder='static')

app.route('/')
def index():
    # renvoie static/index.html
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/round', methods=['POST'])
def api_round():
    """
    POST JSON attendu :
    {
      "path": "five_letter_words.txt",
      "historique": [
        { "choix": "arose", "couleurs": "02010" },
        { "choix": "prune", "couleurs": "00201" }
      ]
    }
    Réponse :
    {
      "mots_restants": [...],
      "reco": "soare",
      "round": 2
    }
    """
    data = request.get_json()
    path = data.get('path', "five_letter_words.txt")
    historique = data.get('historique', [])
    try:
        result = full_round(path, historique)
        return jsonify(status="ok", **result), 200
    except Exception as e:
        return jsonify(status="error", message=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

