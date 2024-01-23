import bd_sql
import my_date
from tkinter import messagebox
import sqlite3
import subprocess



path = 'stolobka.db'

# получаем дату
cur_date_time = my_date.my_current_datetame()
#print(cur_date_time)

#cоздаём таблицу
bd_sql.sql_execute(bd_sql.table)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def clear_table():
    res = messagebox.askokcancel('Очистка таблицы', 'После очистки таблицы \nданные не возможно будет восстоновить!\nПродолжить? ')
    #print(res)
    # Ecли соглаcны удалять данные - удаляем
    if res:
        query_1 = "DELETE FROM  'orders'"
        bd_sql.sql_execute(query_1)

        # очистка автоинкремента
        query_2 = "DELETE FROM SQLITE_SEQUENCE WHERE name = 'orders'"

        bd_sql.sql_execute(query_2)

        # делаем файл скрытым +
        subprocess.call(['attrib', '+h', path])

    return res
        #получение всех после очистки
        #return get_list_order()


def insert_data(ordr_get,select_zatrata):

    get_order = ordr_get
    if get_order:
        # если есть запитая то меняем
        if ',' in get_order:
            get_order = get_order.replace(',', '.')
        if is_number(get_order):
            cost_clear = round(float(get_order), 2)
            cur_date_time = my_date.my_current_datetame()

            query = f"INSERT INTO orders (date, cost, zatrata) VALUES (\'{cur_date_time}\', \'{cost_clear}\', \'{select_zatrata}\')"
            res = bd_sql.sql_execute_get_last_id(query)

            # получаем заново только последнего для перересовки
            query1 = f"SELECT * FROM orders WHERE id = {res}"
            order_one = get_last_order(query1)

            return order_one
        else:
            messagebox.showwarning('Вставка в таблицу', "Нужно указать сумму")

            # если пользователь ввел не цифры, тогда данные в таблице не обновляем
            return False

    else:
        messagebox.showwarning('Вставка в таблицу', "Нет данных для вставки")
        return False



def get_list_order():

    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM orders')
        row = cursor.fetchall()
        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error select orders!", e)
        cursor.close()
        connection.close()

    return row



def get_last_order(sql):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error select orders!", e)
        cursor.close()
        connection.close()
    return row


def get_all_sum():
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute("SELECT sum(cost) FROM orders")
        total_sum = cursor.fetchone()[0]
        cursor.execute("SELECT sum(cost) FROM orders WHERE zatrata = 'Столовая' ")
        stolovka_sum = cursor.fetchone()[0]
        cursor.execute("SELECT sum(cost) FROM orders WHERE zatrata = 'Буфет' ")
        bufet_sum = cursor.fetchone()[0]
        cursor.execute("SELECT count(id) FROM orders WHERE zatrata = 'Столовая'")
        stolovka_count = cursor.fetchone()[0]
        cursor.execute("SELECT count(id) FROM orders WHERE zatrata = 'Буфет'")
        bufet_count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error select orders!", e)
        cursor.close()
        connection.close()
    return (total_sum, stolovka_sum,  stolovka_count, bufet_sum, bufet_count)


def dell_row(id_selct):
    sql = 'cc'
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM orders WHERE id={id_selct}")
        cursor.close()
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error dell row!", e)
        cursor.close()
        connection.close()
    return True
