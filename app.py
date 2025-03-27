from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.environ.get('DB_PATH', 'speedradio.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            lat REAL,
            lon REAL,
            coords TEXT,
            maxspeed INTEGER
        )
    ''')
    # Existing streets
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('King Fahd Road', 24.7136, 46.6753, '[[24.7136, 46.6753], [24.7236, 46.6853]]', 80))
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('King Abdullah Road', 24.6877, 46.7219, '[[24.6877, 46.7219], [24.6977, 46.7319]]', 60))
    # New streets (Riyadh)
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('Olaya Street', 24.6896, 46.6850, '[[24.6896, 46.6850], [24.6996, 46.6950]]', 40))
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('Imam Saud Bin Abdulaziz Road', 24.7612, 46.6985, '[[24.7612, 46.6985], [24.7712, 46.7085]]', 70))
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('Prince Mohammed Bin Salman Road', 24.6532, 46.7152, '[[24.6532, 46.7152], [24.6632, 46.7252]]', 60))
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('Al Rajhi Road', 24.7321, 46.6234, '[[24.7321, 46.6234], [24.7421, 46.6334]]', 50))
    cursor.execute('INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES (?, ?, ?, ?, ?)',
                   ('Makkah Al Mukarramah Road', 24.6778, 46.6490, '[[24.6778, 46.6490], [24.6878, 46.6590]]', 80))
    conn.commit()
    conn.close()

init_db()

@app.route('/api/streets')
def get_streets():
    lat = float(request.args.get('lat', 24.7136))
    lon = float(request.args.get('lon', 46.6753))
    radius = float(request.args.get('radius', 0.01))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, coords, maxspeed 
        FROM streets 
        WHERE abs(lat - ?) <= ? AND abs(lon - ?) <= ?
    """, (lat, radius, lon, radius))
    streets = cursor.fetchall()
    conn.close()
    result = [{'name': row[0], 'coords': eval(row[1]), 'maxspeed': row[2]} for row in streets]
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)