from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits
import math as m
import numpy as np
from matplotlib import cm

#C:/Users/tyuli/Downloads/Telegram Desktop/v523cas60s-001(1).fit

def energy():
    x_cord = int(x.get())-1
    y_cord = int(y.get())-1
    r_cord = int(r.get())
    a_cord = int(a.get())
    b_cord = int(b.get())
    file = str(dfile.get())
    hdulist = pyfits.open(f"{file}")
    hdulist.info()  # получение информ о файле
    exptime = hdulist[0].header['EXPTIME']
    value = hdulist[0].data
    value_r = 0
    n_r = 0
    for i in range(-(r_cord), (r_cord+1)):
        dy = int(m.sqrt((r_cord)**2-i**2))
        for j in range(-dy, dy+1):
            value_r += value[y_cord+j][x_cord+i]
            n_r +=1
    value_b = 0
    n_b = 0
    for i in range(-(b_cord), (b_cord+1)):
        dy = int(m.sqrt((b_cord)**2-i**2))
        for j in range(-dy, dy+1):
            value_b += value[y_cord+j][x_cord+i]
            n_b +=1
    value_a = 0
    n_a = 0
    for i in range(-(a_cord), (a_cord+1)):
        dy = int(m.sqrt((a_cord)**2-i**2))
        for j in range(-dy, dy+1):
            value_a += value[y_cord+j][x_cord+i]
            n_a +=1
    value_n = value_a - value_b
    n_n = n_a - n_b
    energy = (value_r/int(exptime)) - n_r*(value_n/(n_n*int(exptime)))
    lbl_en["text"] = str(int(energy))
    return energy
def ch_graph():
    global ch_x
    global ch_y
    global ch_3d
    ch_x = 0
    ch_y = 0
    ch_3d = 0
    if var1.get() == 1:
        ch_x = 11
    if var2.get() == 1:
        ch_y = 11
    if var3.get() == 1:
        ch_3d = 11
def graph_x():
    x_cord = int(x.get())-1
    y_cord = int(y.get())-1
    r_cord = int(r.get())
    file = str(dfile.get())
    hdulist = pyfits.open(f"{file}")
    hdulist.info()  # получение информ о файле
    value = hdulist[0].data
    cx = []
    cy = []
    vx = []
    vy = []
    for i in range(-(r_cord), (r_cord+1)):
        xx = x_cord + i
        v = value[y_cord][xx]
        cx.append(int(xx))
        vx.append(v)
        yy = y_cord + i
        v = value[yy][x_cord]
        cy.append(int(yy))
        vy.append(v)

    if ch_x == 11:
        plt.figure()
        plt.title("Зависимость энергии звезды от координаты х")
        plt.plot(cx, vx)
        plt.xlabel('координата по х')
        plt.ylabel('значение энергии')
        plt.show()

    if ch_y == 11:
        plt.figure()
        plt.title("Зависимость энергии звезды от координаты у")
        plt.plot(cy, vy)
        plt.xlabel('координата по у')
        plt.ylabel('значение энергии')
        plt.show()

    xn = np.zeros((r_cord * 2 + 1, r_cord * 2 + 1))
    yn = np.zeros((r_cord * 2 + 1, r_cord * 2 + 1))
    v = np.zeros((r_cord * 2 + 1, r_cord * 2 + 1))
    for i in range(-r_cord, r_cord + 1):
        for j in range(-r_cord, r_cord + 1):
            xxq = x_cord + i
            yyq = y_cord + j
            xn[r_cord + i][r_cord + j] += xxq
            yn[r_cord + i][r_cord + j] += yyq
    for i in range(r_cord * 2 + 1):
        for j in range(r_cord * 2 + 1):
            v[i][j] += value[int(yn[i][j])][int(xn[i][j])]

    if ch_3d == 11:
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        surf = ax.plot_surface(xn, yn, v, cmap=cm.YlGnBu)
        ax.set_xlabel("координата по x")
        ax.set_ylabel("координата по y")
        ax.set_zlabel("значение энергии")
        plt.title("Профиль 3d")
        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.show()
    hdulist.close()

root = Tk() #создаем главное окно
root.title("Данные с FITS") #заголовок окна
root.geometry("600x350") #размеры окна

f = ('Helvetica', 14)

for c in range(4):
    root.columnconfigure(index=c)
for r in range(10):
    root.rowconfigure(index=r)

main = LabelFrame(root, text='Данные', font=f,padx=10,pady=10)
main.place(x=10, y=10)

Label(main, text="Координата по х ", font=f).grid(row=0, column=0)
x = ttk.Entry(main, font=f,width=15)
x.grid(row=0, column=1)

Label(main, text="Координата по y ", font=f).grid(row=1, column=0)
y = ttk.Entry(main, font=f,width=15)
y.grid(row=1, column=1)

Label(main, text="Радиус звезды r ", font=f) .grid(row=2, column=0)
r = ttk.Entry(main, font=f,width=15)
r.grid(row=2, column=1)

Label(main, text="Внутр.радиус a  ", font=f).grid(row=3, column=0)
a = ttk.Entry(main, font=f,width=15)
a.grid(row=3, column=1)

Label(main, text="Внешн.радиус b  ", font=f).grid(row=4, column=0)
b = ttk.Entry(main, font=f,width=15)
b.grid(row=4, column=1)

file = LabelFrame(root, text='Файл', font=f, padx=10,pady=10)
file.place(x=10, y=200)

Label(file, text="Путь к файлу       ", font=f).grid(row=0, column=0)
dfile = ttk.Entry(file, font=f,width=15)
dfile.grid(row=0, column=1)

#lbl_fail = ttk.Label(text="", font=f).place(x =10, y = 280)

ttk.Separator(root,takefocus=0,orient=VERTICAL).place(x=370, y=0, relheight=1)

graph = LabelFrame(root, text="Построение графиков ", font=f, padx=10,pady=10)
graph.place(x=380, y=10)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
Checkbutton(graph, text="от Х ", font = f, variable=var1, command=ch_graph).pack(side=TOP)
Checkbutton(graph, text="от У ", font = f, variable=var2, command=ch_graph).pack(side=TOP)
Checkbutton(graph, text="3D график ", font = f, variable=var3, command=ch_graph).pack(side=TOP)
Button(graph, text="Построить графики ", font = f, command=graph_x).pack(side=TOP)

energ = LabelFrame(root, text="Энергия ", font=f, padx=10,pady=10)
energ.place(x=380, y=200)
Button(energ, text="Получить значение \nэнергии ", font = f, command=energy).pack(side=TOP)
lbl_en=ttk.Label(energ, text="Энергия = ", font=f) #padding- отступ
lbl_en.pack(side=LEFT)
lbl_en=ttk.Label(energ, text="", font=f)
lbl_en.pack(side=RIGHT)

root.mainloop()