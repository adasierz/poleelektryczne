from tkinter import *
from tkinter import messagebox
from tkinter import ttk as tkk
from tkinter import Tk, Frame, Canvas, Scrollbar, LabelFrame, Label
from mpl_toolkits.mplot3d import axes3d
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import inf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# STALE
# wartosc pi: np.pi
global e0
global Energia
e0 = (1/36/np.pi)/10**(-9)
Energia=0

r1, r2, N = 0, 0, 0
q = []
e_q=[]
xq=[]
e_x=[]
yq=[]
e_y=[]
zq=[]
e_z=[]

# ramka 1
def pobierz_rN():
    global r1, r2, N, e_q

    r1_value = e_r1.get()
    r2_value = e_r2.get()

    try:
        r1 = float(r1_value)
        r2 = float(r2_value)
        N = int(e_N.get())

        if r1 >= r2:
            messagebox.showerror("Błąd", "Niepoprawne wartości. r1 powinno być mniejsze od r2.")
            e_r1.delete(0, END)
            e_r2.delete(0, END)
        else:
            myButton1.grid_forget()

            # Druga ramka
            dane2 = LabelFrame(container, bd=1, relief="solid")
            dane2.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            dane3 = LabelFrame(container, bd=1, relief="solid")
            dane3.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            myButton2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
            Label(dane2).grid(row=0, column=1)
            Label(dane3).grid(row=0, column=1)

            # tekst przy okienkach
            wartq = Label(dane2, text="Podaj wartości kolejnych ładunków:", anchor="center")
            wartq.grid(row=0, column=0, columnspan=5)
            polozenieq = Label(dane3, text="Określ położenie kolejnych ładunków (x, y, z):", anchor="center")
            polozenieq.grid(row=0, column=0, columnspan=5)

            for i in range(N):
                Label(dane2, text=i + 1).grid(row=i + 1, column=0, sticky="e")
                entry = Entry(dane2)
                entry.grid(row=i + 1, column=2, sticky="w")
                e_q.append(entry)

                Label(dane3, text=i + 1).grid(row=i + 1, column=0, sticky="e")
                entry1 = Entry(dane3)
                entry1.grid(row=i + 1, column=3, sticky="w")
                e_x.append(entry1)
                entry2 = Entry(dane3)
                entry2.grid(row=i + 1, column=4, sticky="w")
                e_y.append(entry2)
                entry3 = Entry(dane3)
                entry3.grid(row=i + 1, column=5, sticky="w")
                e_z.append(entry3)
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawne wartości. r1 i r2 powinny być liczbami.")

    for widget in dane2.grid_slaves():
        widget.grid_configure(padx=10)

# ramka 2
def pobierz_q():
    global q, e_q, e_x, e_y, e_z, xq, yq, zq

    temp_q = []  # Inicjalizacja tymczasowej listy
    temp_xq = []
    temp_yq = []
    temp_zq = []

    for j in range(N):
        entry_e_x = float(e_x[j].get())  # Pobranie wartości z pola wprowadzania i konwersja na float
        entry_e_y = float(e_y[j].get())
        entry_e_z = float(e_z[j].get())
        if entry_e_x > r2 or entry_e_x < r1:
            messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości powinny zawierać się w przedziale r1 do r2.")
            e_x[j].delete(0, END)  # Wyczyszczenie pola wprowadzania
        if entry_e_y > r2 or entry_e_y < r1:
            messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości powinny zawierać się w przedziale r1 do r2.")
            e_y[j].delete(0, END)  # Wyczyszczenie pola wprowadzania
        if entry_e_z > r2 or entry_e_z < r1:
            messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości powinny zawierać się w przedziale r1 do r2.")
            e_z[j].delete(0, END)  # Wyczyszczenie pola wprowadzania
        else:
            for i in range(N):
                try:
                    q_value = float(e_q[i].get())
                    temp_q.append(q_value)
                except ValueError:
                    messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości ładunków powinny być liczbami.")
                    e_q[i].delete(0, END)
                    return  # Przerwij funkcję w przypadku błędu

                try:
                    xq_value = float(e_x[i].get())
                    temp_xq.append(xq_value)
                except ValueError:
                    messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości ładunków powinny być liczbami.")
                    e_x[i].delete(0, END)
                    return

                try:
                    yq_value = float(e_y[i].get())
                    temp_yq.append(yq_value)
                except ValueError:
                    messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości ładunków powinny być liczbami.")
                    e_y[i].delete(0, END)
                    return

                try:
                    zq_value = float(e_z[i].get())
                    temp_zq.append(zq_value)
                except ValueError:
                    messagebox.showerror("Błąd", "Niepoprawne wartości. Wartości ładunków powinny być liczbami.")
                    e_z[i].delete(0, END)
                    return
            q = temp_q
            xq = temp_xq
            yq = temp_yq
            zq = temp_zq

            wykresy()

def wykresy():
    x = np.linspace(r1, r2, 5)
    y = np.linspace(r1, r2, 5)
    z = np.linspace(r1, r2, 5)

    X, Y, Z = np.meshgrid(x, y, z)

    Ex = np.zeros((len(x), len(y), len(z)))
    Ey = np.zeros((len(x), len(y), len(z)))
    Ez = np.zeros((len(x), len(y), len(z)))
    V = np.zeros((len(x), len(y), len(z)))

    for n in range(0, N):
        ex = np.zeros((len(x), len(y), len(z)))
        ey = np.zeros((len(x), len(y), len(z)))
        ez = np.zeros((len(x), len(y), len(z)))
        v = np.zeros((len(x), len(y), len(z)))

        for i in range(0, len(x)):
            for j in range(0, len(y)):
                for k in range(0, len(z)):
                    dr = math.sqrt((x[i] - xq[n]) ** 2 + (y[j] - yq[n]) ** 2 + (z[k] - zq[n]) ** 2)
                    if dr < (x[1] - x[0]) / 100:
                        continue
                    else:
                        rx = ((x[i] - xq[n]))
                        ry = ((y[j] - yq[n]))
                        rz = ((z[k] - zq[n]))
                        ex[i][j][k] = 1 / (4 * np.pi * e0) * q[n] / (dr ** 3) * rx
                        ey[i][j][k] = 1 / (4 * np.pi * e0) * q[n] / (dr ** 3) * ry
                        ez[i][j][k] = 1 / (4 * np.pi * e0) * q[n] / (dr ** 3) * rz
                        v[i][j][k] = 1 / (4 * np.pi * e0) * q[n] / dr
                        X[i][j][k] = x[i]
                        Y[i][j][k] = y[j]
                        Z[i][j][k] = z[k]
                        Ex[i][j][k] += ex[i][j][k]
                        Ey[i][j][k] += ey[i][j][k]
                        Ez[i][j][k] += ez[i][j][k]
                        V[i][j][k] += v[i][j][k]

    for m in range(0, N):
        for n in range(0, N):
            if m is not n:
                global Energia
                Energia = Energia + q[m] * 1 / (4 * np.pi * e0) * q[n] / math.sqrt(
                    (xq[n] - xq[m]) ** 2 + (yq[n] - yq[m]) ** 2 + (zq[n] - zq[m]) ** 2)

    dajenergie()
    przedzial = abs(r2 - r1) # dla przedzialu kolo 50 jest spoko dlugosc 5; przedzial 400 malo widoczne
    przedzial1 =  math.floor(math.log10(przedzial)) + 1
    max_q = max(q)  # Znajduje największą wartość w liście q
    rzad_q_max = math.floor(math.log10(max_q)) + 1
    strzalka = 0.5*10**(przedzial1-1) + rzad_q_max*0
    print(strzalka, rzad_q_max, max_q)
    # wykresy
    fig = plt.figure()

    # pierwszy wykres - strzałki
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_xlabel('x', labelpad=20)
    ax1.set_ylabel('y', labelpad=20)
    ax1.set_zlabel('z', labelpad=20)
    ax1.quiver(X, Y, Z, Ex, Ey, Ez, length=strzalka, normalize=True )

    # drugi wykres
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_xlabel('x', labelpad=20)
    ax2.set_ylabel('y', labelpad=20)
    ax2.set_zlabel('z', labelpad=20)
    # ax2.plot_surface(X, Y, Z, V, cmap='viridis')
    ax2.scatter(X, Y, Z, c=V.flatten(), edgecolor="face", alpha=0.5, marker="o", cmap="magma", linewidth=0, s=50)

    plt.show()

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def dajenergie():
    dane4 = LabelFrame(container, bd=1, relief="solid")
    dane4.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
    Label(dane4).grid(row=0, column=1)
    en = Label(dane4, text="Energia układu [J]: " + str(Energia), anchor="center")
    en.grid(row=0, column=0, columnspan=5)

    for widget in dane4.grid_slaves():
        widget.grid_configure(padx=10)

#-----------------------------------------------------------------------------------------------------------------------
# okno
root = Tk()
root.title("Symulacja pola elektrycznego")
root.geometry("550x800")
root.iconbitmap("ikona.ico")

# Tworzenie kontenera typu Canvas
canvas = Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# scrollbar
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Konfiguracja przewijania Canvas przy użyciu scrollbaru
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', on_configure)

# Tworzenie ramki wewnątrz Canvas
container = Frame(canvas)
canvas.create_window((0, 0), window=container, anchor="nw")

# Pierwsza ramka
dane = LabelFrame(container, text="Dane", bd=1, relief="solid")
dane.grid(row=0, column=0, padx=10, pady=10)

# Wyśrodkowanie
root.update_idletasks()  # Zastosuj zmiany
width = root.winfo_width()  # Szerokość okna
height = root.winfo_height()  # Wysokość okna
x = (width - canvas.winfo_width()) // 2  # Oblicz położenie x kontenera
y = (height - canvas.winfo_height()) // 2  # Oblicz położenie y kontenera
canvas.configure(scrollregion=canvas.bbox("all"))
canvas.create_window((x, y), window=container, anchor="nw")


# tekst przy okienkach
przedzial = Label(dane, text="Podaj minimalną (r1) i maksymalną (r2) wartość jaką mogą osiągnąć współrzędne x, y, z: ")
przedzial.grid(row=0, column=0, columnspan=5)
wart_r1 = Label(dane, text="r1: ")
wart_r1.grid(row=1, column=1)
wart_r2 = Label(dane, text="r2: ")
wart_r2.grid(row=1, column=3)

ladunki = Label(dane, text="Wybierz liczbę ładunków (1-10): ")
ladunki.grid(row=2, column=0, columnspan=5)
wart_N = Label(dane, text="N: ")
wart_N.grid(row=3,column=1)

# wprowadzane dane (okienka)
e_r1 = Entry(dane, exportselection=0)
e_r1.grid(row=1, column=2)
e_r2 = Entry(dane, exportselection=0)
e_r2.grid(row=1, column=4)

e_N = Spinbox(dane, from_=1, to=10)
e_N.grid(row=3, column=2)

# Tworzenie ramki na przyciski
buttons_frame = Frame(container)
buttons_frame.grid(row=1, column=0, pady=10)
# Przyciski
myButton1 = Button(buttons_frame, text="Zatwierdź", command=pobierz_rN)
myButton1.grid(row=0, column=0, padx=10)

myButton2 = Button(container, text="Zatwierdź", command=pobierz_q)

root.mainloop()