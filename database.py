import sqlite3

def update_db():
    conn = sqlite3.connect('speedradio.db')
    cursor = conn.cursor()
    
    # Add more streets (Riyadh examples)
    cursor.execute('''
        INSERT OR IGNORE INTO streets (name, lat, lon, coords, maxspeed) VALUES
        ('King Abdullah Road', 24.6877, 46.7219, '[[24.6877, 46.7219], [24.6977, 46.7319]]', 60),
        ('Prince Turki Road', 24.7436, 46.6583, '[[24.7436, 46.6583], [24.7536, 46.6683]]', 50)
    ''')
    
    conn.commit()
    conn.close()
    print("Database updated with more streets!")

if __name__ == '__main__':
    update_db()