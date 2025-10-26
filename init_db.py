import sqlite3

#Connecting to existing database file
conn = sqlite3.connect("/Users/prithikavenkatesh/smart-desk-assistant/app/tracker.db")
cursor = conn.cursor()

#Create the events table if it doesn't already exist
cursor.execute("""
               CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               emotion TEXT NOT NULL,
               emotion_conf REAL,
               timestamp TEXT NOT NULL
               );
            """)

conn.commit()
conn.close()

print("Table 'events' created successfully!")
