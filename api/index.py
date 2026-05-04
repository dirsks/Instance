from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

KV_URL = os.environ.get('KV_URL') 
r = redis.from_url(KV_URL, decode_responses=True)

@app.route('/api', methods=['GET'])
def handle():
    action = request.args.get('action')
    place_id = request.args.get('placeid')

    if action == 'push' and place_id:
        r.set('current_job', place_id, ex=10)
        return "OK", 200

    if action == 'pull':
        job = r.get('current_job')
        if job:
            r.delete('current_job')
            return jsonify({"placeId": job}), 200
        return jsonify({"placeId": None}), 404

    return "Invalid Action", 400
    
def handler(event, context):
    return app(event, context)
