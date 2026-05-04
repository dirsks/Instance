from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Conexão segura com Redis
KV_URL = os.environ.get('KV_URL')
r = redis.from_url(KV_URL, decode_responses=True) if KV_URL else None

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if r is None:
        return "Erro: KV_URL não configurada", 500
        
    action = request.args.get('action')
    place_id = request.args.get('placeid')

    if action == 'push' and place_id:
        r.set('current_job', place_id, ex=10)
        return f"OK: {place_id}", 200

    if action == 'pull':
        job = r.get('current_job')
        if job:
            r.delete('current_job')
            return jsonify({"placeId": job}), 200
        return jsonify({"placeId": None}), 404

    return "Ação Inválida ou API Ativa", 200
