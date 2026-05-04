from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Configuração do Vercel KV (Redis)
# Pegue essas variáveis no painel da Vercel
KV_URL = os.environ.get('KV_URL') 
r = redis.from_url(KV_URL, decode_responses=True)

@app.route('/api', methods=['GET'])
def handle():
    action = request.args.get('action')
    place_id = request.args.get('placeid')

    # Ação do WEBSITE: Cria uma requisição que dura 10 segundos
    if action == 'push' and place_id:
        r.set('current_job', place_id, ex=10)
        return "OK", 200

    # Ação do PYTHON: Lê e limpa a requisição imediatamente
    if action == 'pull':
        job = r.get('current_job')
        if job:
            r.delete('current_job') # Garante que só processe uma vez
            return jsonify({"placeId": job}), 200
        return jsonify({"placeId": None}), 404

    return "Invalid Action", 400