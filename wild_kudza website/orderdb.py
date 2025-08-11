import sqlite3


conn = sqlite3.connect('orders.db')


c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS content (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             idblock TEXT,
             short_title TEXT,
             img TEXT,
             altimg TEXT,
             title TEXT,
             contenttext TEXT,
             author TEXT,
             timestampdata DATETIME)''')


c.execute('''CREATE TABLE IF NOT EXISTS orders (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             house TEXT,
             figure TEXT,
             googledoclink TEXT)''')

conn.close()