from flask import Flask, jsonify, render_template, request
import sqlite3
import vlc
import threading
import time

app = Flask(__name__)

def stream_audio():
    time.sleep(5)  # Wait for Icecast
    mp3_path = "file:///D:/my-portfolio/music/Various Artists - country songs to scream in the car (2025) Mp3 320kbps [PMEDIA] ⭐️/03. Luke Combs - Ain't No Love in Oklahoma (From Twisters The Album).mp3"
    instance = vlc.Instance('--no-video', '--verbose=2', '--loop')  # Add --loop
    player = instance.media_player_new()
    media = instance.media_new(mp3_path)
    player.set_media(media)
    sout = "#transcode{vcodec=none,acodec=mp3,ab=128,channels=2}:standard{access=shout,mux=mp3,dst=source:hackme@localhost:8000/mystream}"
    media.add_option(f"sout={sout}")
    result = player.play()
    if result == 0:
        print("Streaming started successfully!")
    else:
        print(f"Failed to start streaming: Error code {result}")
    # Keep thread alive
    while True:
        time.sleep(1)  # Prevent thread from exiting

threading.Thread(target=stream_audio, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/streets')
def get_streets():
    lat = float(request.args.get('lat', 24.7136))
    lon = float(request.args.get('lon', 46.6753))
    radius = float(request.args.get('radius', 1000))
    conn = sqlite3.connect('speedradio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, coords, maxspeed FROM streets WHERE abs(lat - ?) < 0.01 AND abs(lon - ?) < 0.01", (lat, lon))
    streets = cursor.fetchall()
    conn.close()
    result = [{'name': row[0], 'coords': eval(row[1]), 'maxspeed': row[2]} for row in streets]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)