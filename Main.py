import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) # Permite que seu site da Vercel acesse esses dados

API_KEY = os.getenv('API_KEY') # Pega a chave que você salvou no Railway

@app.route('/stats')
def get_stats():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = { "x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": API_KEY }
    
    try:
        response = requests.get(url, headers=headers).json()
        jogos_analisados = []

        for jogo in response.get('response', []):
            # Lógica de Pressão do Nano Drago
            # Se a API não der chutes, usamos uma base de perigo por tempo/ataques
            home = jogo['teams']['home']['name']
            away = jogo['teams']['away']['name']
            tempo = jogo['status']['elapsed']
            gols_home = jogo['goals']['home']
            gols_away = jogo['goals']['away']

            # Cálculo de "Pressão Fantasma" (Baseado no tempo e eventos)
            # No futuro, aqui pegaremos estatísticas detalhadas de cada jogo
            ip = (tempo / 90) * 1.2 # Exemplo de lógica inicial

            jogos_analisados.append({
                "partida": f"{home} vs {away}",
                "placar": f"{gols_home} - {gols_away}",
                "tempo": f"{tempo}'",
                "pressao": round(ip * 10, 1) # Transforma em escala de 0 a 10
            })

        return jsonify(jogos_analisados)
    except:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
