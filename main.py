import hashlib # для паролей
import my_function
import bd_sql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk     # подключю пакет ttk
import tempfile, base64, zlib
from PIL import Image, ImageTk


#cоздаём таблицу
bd_sql.sql_execute(bd_sql.table)

def insert_data_bottom(event):
    insert_data()

def clear_table():

    res1 = my_function.get_list_order()
    if res1:
        # если таблица не пуста(res1) и пользователь дал согласие - удаляем и ощищаем в окне
        if my_function.clear_table():
            # Очистка поля ввода
            order.delete(0, END)

            # очистка таблицы поля удаление данных
            for item in tree.get_children():
                tree.delete(item)

            # обнуляе Итоги
            result['text'] = f"Итого: 0.0 р."
    else:
        messagebox.showinfo('Удаление таблицы', 'Разве! Таблица сейчас пуста :-))')

# удаление выбранной строки
def clear_selected():
    id_select = tree.selection()
    if id_select:
        item = tree.item(id_select)
        res =messagebox.askokcancel("Удаление строки", f"Вы точно хотите удалить строку с суммой {item['values'][2]}р.?")
        if res:
            # удаляем строку если пользователь согласился
            id_selct = item['values'][0]
            #print(id_selct)
            res_sql = my_function.dell_row(id_selct)
            if res_sql:
                tree.delete(id_select)

                # Обновление итоговых данных внизу окна
                all_sum = my_function.get_all_sum()
                # для очистки None из бд
                all_sum1 = []
                if any(all_sum):
                    for x in all_sum:
                        if x is None:
                            all_sum1.append(0)
                            continue
                        all_sum1.append(x)
                    result['text'] = f"Итого: {round(all_sum1[0], 2)} р.,: Cтоловая: {round(all_sum1[1], 2)}р., походов: {all_sum1[2]}. Буфет: {round(all_sum1[3], 2)}р., походов: {all_sum1[4]}"

                # если пусто при выборке
                else:
                    result['text']="Итого: 0.0р."

    # если ничего не выбрано
    else:
        messagebox.showinfo('Удаление строки', 'Выберите строку для удаления')



def insert_data():

    # получение из формы
    order_get = order.get()

    # получение данных от радиокнопок
    select_zatrata = selected_zatrata.get()
    select_zatrata = {'stolovka':'Столовая', 'bufet':'Буфет'}[select_zatrata]
    #print(select_zatrata)

    if order_get:
        # записываю и назад возвращая последний для вставки в таблицу
        order_one1 = my_function.insert_data(order_get[0:5], select_zatrata)
        #print(order_one1)

        # Очистка поля ввода
        order.delete(0, END)

        # если пользователь ввел данные в нужно формате то вставляем в таблицу на окне
        #if not order_one1:
        if order_one1 != False:
            tree.insert("", END, values=order_one1)

            # Обновление итоговых данных внизу окна
            all_sum = my_function.get_all_sum()
            # для очистки None из бд
            all_sum1 = []
            if any(all_sum):
                for x in all_sum:
                    if x is None:
                        all_sum1.append(0)
                        continue
                    all_sum1.append(x)
            result['text']=f"Итого: {round(all_sum1[0],2)} р.,: Cтоловая: {round(all_sum1[1],2)}р., походов: {all_sum1[2]}. Буфет: {round(all_sum1[3],2)}р., походов: {all_sum1[4]}"
            #result['text']=f"Итого: {all_sum} р."
            #print(order_one1[2])
            #all_summ_add = float(all_summ)+order_one1[2]
            #print(all_summ_add)

        # очистка таблицы для изменённых
        #for item in tree.get_children():
        #    tree.delete(item)

        # заново вставка значений в таблицу
        #for order_one in orders_one:
            #tree.insert("", END, values=order_one)
    else:
        messagebox.showinfo('Добавление записи ', 'Нет данных для сохранения!')




ICON = zlib.decompress(base64.b64decode("eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc="))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, "wb") as icon_file:
    icon_file.write(ICON)

root = Tk()
root.title("Копейка 2.0  -=ITVokirtep=-")
root.geometry("570x460")
root.minsize(570,460)
root.maxsize(670,560)
root.iconbitmap(default=ICON_PATH)

ttk.Style().configure("TLabel",  font="helvetica 10", foreground="#004D40", padding=5, background="sky blue")
ttk.Style().configure("TButton",  font="helvetica 9", foreground="#004D40", padding=5)
ttk.Style().configure("TEntry",  font="helvetica 9", foreground="#004D40", padding=5)


frame_top = LabelFrame(root)
frame_top = LabelFrame(text="Внесение сумм")


name_label = ttk.Label(frame_top, text="Введите cумму затрат:")
name_label.grid(row=0,column=1, padx=5)

order = ttk.Entry(frame_top, width=10)
order.bind("<Return>", insert_data_bottom)
order.grid(row=0, column=2, padx=2)


btn_add = ttk.Button(frame_top, text="Добавить", command=insert_data) # создаем кнопку из пакета ttk
btn_add.grid(row=0, column=3, ipadx=15, sticky='nswe')


# для фото если рядом есть то берём, иначе пропускаем
try:
    image = Image.open('wallet.png')
    img = image.resize((60, 60))
    my_img=ImageTk.PhotoImage(img)
    label=Label(frame_top, image=my_img)
    label.grid(row=0, rowspan=2, column=4,  padx=[40, 0])
except Exception:
    pass


#btn_clear = ttk.Button(frame_top, text="Очистить", command=clear_table) # создаем кнопку из пакета ttk
#btn_clear.grid(row=0, column=4,  padx=10 )

#--------start chekboks----------

selected_zatrata = StringVar(value="stolovka") # по умолчанию будет выбран элемент с value=stolovka

chboks_stolovka = ttk.Radiobutton(frame_top, text="Столовая", value="stolovka", variable=selected_zatrata)
chboks_stolovka.grid( row=1, columnspan=3, padx=5, pady=[5, 0], sticky=W )

chboks_bufet = ttk.Radiobutton(frame_top, text="Буфет", value="bufet", variable=selected_zatrata)
chboks_bufet.grid(row=1, columnspan=3, padx=110, pady=[5, 0], sticky=W )


#----------------tree---------start-----------

# получение все покупок
orders_all = my_function.get_list_order()


frame_center = LabelFrame(root)
frame_center = LabelFrame(text="Таблица")

#--------start ----- dell --- order----------
id_dell = ttk.Button(frame_center, text="Удалить", command=clear_selected)
id_dell.grid(row=0, column=2,  padx=2, pady=[10, 0], sticky='ne')

btn_clear = ttk.Button(frame_center, text="Очистить", command=clear_table) # создаем кнопку из пакета ttk
btn_clear.grid(row=0, column=2,  padx=2, pady=[50, 10], sticky='n')

# определяем столбцы
columns = ("id","data", "cost", "bufet")

tree = ttk.Treeview(frame_center, columns=columns, show="headings")
tree.grid( row=0, column=0, pady=10, padx=5, ipady=5, ipadx=4, sticky="nsew")


# определяем заголовки
tree.heading("id", text="id", anchor=N)
tree.heading("data", text="Дата", anchor=N)
tree.heading("cost", text="Сумма", anchor=N)
tree.heading("bufet", text="Столовая\Буфет", anchor=E)

tree.column("#1", stretch=NO,anchor=E,  width=30)
tree.column("#2", stretch=NO,  width=150)
tree.column("#3", stretch=NO, anchor=E, width=100)
tree.column("#4", stretch=NO, anchor=E, width=120)


# добавляем данные в таблицу окна
for order_one in orders_all:
    tree.insert("", END, values=order_one)

# добавляем вертикальную прокрутку
scrollbar = ttk.Scrollbar(frame_center, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

#------------------ ИТОГО-------------
# получение итого по всем затратам
all_summ = my_function.get_all_sum()

#all_sum = all_summ  if all_summ not in [None, 0, 0.0]  else 0.0
all_sum1 = []
if any(all_summ):
    for x in all_summ:
        if x is None:
            all_sum1.append(0)
            continue
        all_sum1.append(x)

    result = ttk.Label(text=f"Итого: {round(all_sum1[0],2)} р.,: Столовая: {round(all_sum1[1],2)}р., походов: {all_sum1[2]}. Буфет: {round(all_sum1[3],2)}р., походов: {all_sum1[4]}", font=('helvetica', 9), background='#ccc')
    result.grid(row=3, columnspan=2, column=0, padx=[5, 5], pady=[0, 10], sticky='nsew')
else:
    result = ttk.Label(text=f"Итого: 0.0р.",  background='#ccc')
    result.grid(row=3, columnspan=2, column=0, padx=[5, 5], pady=[0, 10], sticky='nsew')

#-----------------

frame_top.grid(row=0, column=0, pady=10, padx=5, ipady=5, ipadx=4, sticky='nsew')
frame_center.grid(row=1, column=0, pady=10, padx=5, ipady=5, ipadx=4, sticky="nsew")


root.mainloop()





