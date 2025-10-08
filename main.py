import os
import time
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from odds_api import get_live_odds
from arbitrage import detect_arbitrage

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_arbs = []

@app.route('/')
def index():
    return render_template('index.html')

def fetch_and_emit_arbs():
    global latest_arbs
    while True:
        try:
            odds_data = get_live_odds()
            arbs = detect_arbitrage(odds_data)
            if arbs != latest_arbs:  # only emit when new data
                latest_arbs = arbs
                socketio.emit('arbitrage_update', {'arbs': arbs})
            time.sleep(15)  # fetch every 15 seconds
        except Exception as e:
            print("Error:", e)
            time.sleep(30)

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('arbitrage_update', {'arbs': latest_arbs})

if __name__ == '__main__':
    # Start background thread
    thread = threading.Thread(target=fetch_and_emit_arbs)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=5000)
