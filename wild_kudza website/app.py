import logging

from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import hashlib
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = 'labubu'

@app.route('/sign.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Пароли не совпадают!', 'danger')
            return redirect(url_for('register'))

        try:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            if c.fetchone():
                flash('Пользователь с таким именем уже существует', 'danger')
                return redirect(url_for('register'))

            # Добавление нового пользователя
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, hashed_password))

            conn.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('admin_login'))

        except Exception as e:
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')
            return redirect(url_for('register'))

        finally:
            conn.close()

    return render_template('sign.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_admin'):
            flash('Требуется авторизация администратора', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin.html')


@app.route('/')
def home():
    try:
        conn = sqlite3.connect('cardsdb.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, image_url FROM cards')
        cards = cursor.fetchall()
        card_list = []
        for card in cards:
            card_list.append({
                'title': card[0],
                'description': card[1],
                'image_url': card[2]
            })

        return render_template('cards.html', card_list=card_list)

    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении карточек из базы данных: {e}")
        return render_template('cards.html', card_list=[])

    finally:
        if 'conn' in locals():
            conn.close()





@app.route('/orderform.html')
def order():
    return render_template('orderform.html')


# логин в админ-панель
@app.route('/login.html', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        try:

            # Получаем пользователя из базы
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()

            if user:
                stored_password = user[2]  # Пароль находится в третьем столбце
                # Проверяем хеш пароля
                input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

                if input_hash == stored_password:
                    session['logged_in'] = True
                    session['username'] = username
                    session['is_admin'] = True
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(url_for('admin_panel'))

            flash('Неверное имя пользователя или пароль', 'danger')

        except Exception as e:
            flash(f'Ошибка при входе: {str(e)}', 'danger')

        finally:
            conn.close()

    return render_template('login.html')


@app.route('/admin.html', methods=['GET', 'POST'])
def new_card():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_url = request.form.get('image_url')



        if not title:
            flash('Название карточки не может быть пустым!', 'error')
            return redirect(url_for('new_card'))

        conn = sqlite3.connect('cardsdb.db')
        cursor = conn.cursor()

        try:

            cursor.execute('''
                    INSERT INTO cards (title, description, image_url)
                VALUES (?, ?, ?)
            ''', (title, description, image_url))
            conn.commit()
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            flash(f'Ошибка при создании карточки: {e}', 'error')
            return redirect(url_for('new_card'))
        finally:
            if conn:
                conn.close()



    return render_template('admin.html')



# Страница админ панели
@app.route('/admin_panel')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_admin'):
            flash('Требуется авторизация администратора', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/orderform.html', methods=['GET', 'POST'])
def handle_order():
    if request.method == 'POST':
        name = request.form.get('names')
        house = request.form.get('house')
        figure = request.form.get('order')
        googledoclink = request.form.get('googledoclink')

        try:
            connn = sqlite3.connect('orders.db')
            c = connn.cursor()
            c.execute('INSERT INTO orders (name, house, figure, googledoclink) VALUES (?, ?, ?, ?)',
                     (name, house, figure, googledoclink))

            connn.commit()
            flash('Ваш заказ успешно оформлен!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash(f'Ошибка при оформлении заказа: {str(e)}', 'danger')
            return redirect(url_for('order'))

        finally:
            connn.close()

    return redirect(url_for('order'))

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Вы вышли из системы')
    return redirect(url_for('home'))


@app.route('/admin/orders')
@login_required
def view_orders():
    try:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()

        # Получаем все заказы из базы данных
        cursor.execute('SELECT id, name, house, figure, googledoclink FROM orders ORDER BY id DESC')
        orders = cursor.fetchall()

        return render_template('adminorder.html', orders=orders)

    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении заказов: {e}")
        flash('Ошибка при загрузке заказов', 'danger')
        return render_template('adminorder.html', orders=[])

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=8080)