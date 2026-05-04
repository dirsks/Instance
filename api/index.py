from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Tentativa de conexão robusta
def get_redis_client():
    kv_url = os.environ.get('KV_URL')
    if not kv_url:
        return None
    try:
        return redis.from_url(kv_url, decode_responses=True)
    except:
        return None

r = get_redis_client()

@app.route('/', methods=['GET'])
def handle():
    # ... resto do código igual ...
    # Se o Redis não estiver configurado, avisa o erro de forma clara
    if r is None:
        return jsonify({"error": "KV_URL não configurada ou Redis offline"}), 500

    action = request.args.get('action')
    place_id = request.args.get('placeid')

    # WEBSITE envia o ID
    if action == 'push' and place_id:
        try:
            r.set('current_job', place_id, ex=10)
            return "OK", 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # PYTHON local busca o ID
    if action == 'pull':
        try:
            job = r.get('current_job')
            if job:
                r.delete('current_job')
                return jsonify({"placeId": job}), 200
            return jsonify({"placeId": None}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return "Invalid Action", 400

# Export para a Vercel
def handler(event, context):
    return app(event, context)
