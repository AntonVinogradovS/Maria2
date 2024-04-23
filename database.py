import sqlite3

# Функция для создания таблицы в базе данных
async def create_table():
    # Подключение к базе данных или ее создание, если она не существует
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # Создание таблицы payments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY,
        time_pay TEXT
    )
    ''')

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()

# Вызов функции для создания таблицы
# Функция для вставки данных в таблицу
async def insert_payment(id_, time_pay):
    # Подключение к базе данных
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # Вставка данных в таблицу
    cursor.execute('''
    INSERT OR REPLACE INTO payments (id, time_pay)
    VALUES (?, ?)
    ''', (id_, time_pay))

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()

# Функция для чтения данных из таблицы по идентификатору
async def read_payment():
    # Подключение к базе данных
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # Чтение данных из таблицы по идентификатору
    cursor.execute('''
    SELECT * FROM payments
    ''')

    # Получение результатов запроса
    payment = cursor.fetchall()
    print(payment)

    # Закрытие соединения с базой данных
    conn.close()

    return payment

# Функция для чтения данных из таблицы по идентификатору
async def read_payment_by_id(id_):
    # Подключение к базе данных
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # Чтение данных из таблицы по идентификатору
    cursor.execute('''
    SELECT * FROM payments
    WHERE id = ?
    ''', (id_,))

    # Получение результатов запроса
    payment = cursor.fetchone()
    #print(payment)

    # Закрытие соединения с базой данных
    conn.close()

    return payment

# Функция для удаления данных из таблицы по идентификатору
async def delete_payment_by_id(id_):
    # Подключение к базе данных
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    # Удаление данных из таблицы по идентификатору
    cursor.execute('''
    DELETE FROM payments
    WHERE id = ?
    ''', (id_,))

    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()
