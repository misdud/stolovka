import sqlite3
from tkinter import messagebox


path = 'stolobka.db'


table = '''
    CREATE TABLE IF NOT EXISTS "orders" (
	"id" INTEGER NOT NULL,
	"date" TEXT NOT NULL,
	"cost" REAL NOT NULL,
	"zatrata" TEXT DEFAULT 'Столовая',
	PRIMARY KEY("id" AUTOINCREMENT)
)
'''


def sql_execute(sql, params=None):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(sql)

        connection.commit()
        cursor.close()
        connection.close()



    except sqlite3.Error as e:
        messagebox.showerror("Error execute sql", e)
        cursor.close()
        connection.close()
    finally:
        pass
        # делаем файл скрытым +
        #subprocess.call(['attrib', '+h', path])


def sql_execute_get_last_id(sql):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()

        cursor.execute(sql)
        connection.commit()

        res_last_id = cursor.lastrowid

        cursor.close()

        return res_last_id
    except sqlite3.Error as e:
        messagebox.showerror("Error execute sql", e)
        cursor.close()
        connection.close()



#con = sqlite3.connect("my_database.db")
#cursor = con.cursor()
#cursor.execute("INSERT INTO orders(date, 'order', bufet) VALUES ('1', 111125.0, 0)")
#con.commit()


# получаем все данные из таблицы people
#cursor.execute("SELECT * FROM orders")
#print(cursor.fetchall())
#cursor.close()





