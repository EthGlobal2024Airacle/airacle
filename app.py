from flask import Flask, send_from_directory, request, redirect
import os
import random


app = Flask(__name__)

@app.before_request
def before_request():
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/claimCheck')
def get_claim_bot_check():
    return random.randint(0, 100)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)