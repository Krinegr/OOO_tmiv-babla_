import sqlite3

sample_cards = [
    {
        'title': 'Миниатюры для D&D',
        'description': 'Пластик, 2.5 сантиметра каждая. Набор фигурок для Вашей игры. Шесть фигурок по разумной цене &#45;&#45; выбор наших покупателей.',
        'image_url': 'static/dnd-photoaidcom-cropped.png',
    },
    {
        'title': 'Warhammer 40000, "Ultramarines Marneus Calgar"',
        'description': 'Прочный материал, детализация, соответствущая канону, 13.5 сантиметров.',
        'image_url': 'static/warh-photoaidcom-cropped.png',
    },
    {
        'title': 'Warcraft 3, "Принц Артас"',
        'description': 'Винил, 25 сантиметров в высоту, идеальная детализация',
        'image_url': 'static/arthas-photoaidcom-cropped.png',
    }
]
conn = sqlite3.connect('cardsdb.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    image_url TEXT,
)
''')

for card in sample_cards:
    cursor.execute('''
    INSERT INTO cards (title, description, image_url)
    VALUES (?, ?, ?)
    ''', (card['title'], card['description'], card['image_url']))

conn.commit()
conn.close()

