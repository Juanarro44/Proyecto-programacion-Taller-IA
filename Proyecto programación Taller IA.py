import random
import tkinter as tk
from tkinter import messagebox

# Definir funciones

def crea_tablero(fil, col, val, forma):
    '''Crea una matriz triangular con las filas y columnas y valor que le pasemos'''
    tablero = []
    for i in range(fil):
        tablero.append([])
        if forma == "equilatero":
            col_max = i + 1
        elif forma == "isosceles":
            col_max = min(i + 1, fil - i)
        elif forma == "escaleno":
            col_max = 2 * (i + 1) - 1
        else:
            col_max = col

        for j in range(col_max):
            tablero[i].append(val)

    return tablero

def coloca_minas(tablero, minas, fil, col, forma):
    '''Coloca en el tablero que le pasemos el número de minas que le pasemos'''
    minas_ocultas = []
    numero = 0
    while numero < minas:
        y = random.randint(0, fil - 1)
        if forma == "escaleno":
            x_max = 2 * (y + 1) - 1
        elif forma == "equilatero":
            x_max = y + 1
        elif forma == "isosceles":
            x_max = min(y + 1, fil - y)
        else:
            x_max = col

        x = random.randint(0, x_max - 1)

        if len(tablero[y]) <= x:
            tablero[y].extend([0] * (x - len(tablero[y]) + 1))
            
        if tablero[y][x] != 9:
            tablero[y][x] = 9
            numero += 1
            minas_ocultas.append((y, x))
    return tablero, minas_ocultas

def coloca_pistas(tablero, fil, col, forma):
    '''Recorre el tablero y pone el número de minas vecinas que tiene cada casilla'''
    for y in range(fil):
        if forma == "equilatero":
            col_max = y + 1
        elif forma == "isosceles":
            col_max = min(y + 1, fil - y)
        elif forma == "escaleno":
            col_max = 2 * (y + 1) - 1
        else:
            col_max = col

        for x in range(col_max):
            if tablero[y][x] != 9:
                minas_vecinas = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if i == 0 and j == 0:
                            continue
                        ny = y + i
                        nx = x + j

                        if 0 <= ny < fil:
                            if forma == "equilatero":
                                max_col = ny + 1
                            elif forma == "isosceles":
                                max_col = min(ny + 1, fil - ny)
                            elif forma == "escaleno":
                                max_col = 2 * (ny + 1) - 1
                            else:
                                max_col = col

                            if 0 <= nx < max_col and len(tablero[ny]) > nx and tablero[ny][nx] == 9:
                                minas_vecinas += 1

                tablero[y][x] = minas_vecinas
    return tablero

def rellenado(oculto, visible, y, x, fil, col, val):
    '''Recorre todas las casillas vecinas, y comprueba si son ceros, si es así las descubre,
    y recorre las vecinas de estas, hasta encontrar casillas con pistas, que también descubre.'''
    ceros = [(y, x)]
    while len(ceros) > 0:
        y, x = ceros.pop()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= y + i < fil and 0 <= x + j < col:
                    if visible[y + i][x + j] == val and oculto[y + i][x + j] == 0:
                        visible[y + i][x + j] = 0
                        if (y + i, x + j) not in ceros:
                            ceros.append((y + i, x + j))
                    else:
                        visible[y + i][x + j] = oculto[y + i][x + j]
    return visible

def tablero_completo(tablero, visible, fil, col, val):
    '''Comprueba si todas las casillas sin minas han sido abiertas'''
    for y in range(fil):
        for x in range(len(visible[y])):  # Recorrer solo los índices válidos de la sublista
            if tablero[y][x] != val and visible[y][x] == "-":
                return False
    return True

def actualizar_interfaz():
    '''Actualiza el texto y el color de los botones en la interfaz gráfica'''
    colores = {
        0: "#EFB810", 1: "#F08080", 2: "#4169e1", 3: "#790604", 4: "#FFB888",
        5: "#e60c05", 6: "#900C3F", 7: "#0E6655", 8: "#6400FF"  # Nuevos colores para los números del 5 al 8
    }
    for i in range(filas):
        for j in range(len(visible[i])):  # Ajustamos el rango de columnas según el tamaño de la fila actual
            if visible[i][j] == "-":
                btns[i][j].config(text="")
                btns[i][j].config(bg="#DAF7A6")  # Fondo verde claro para las celdas vacías
            elif visible[i][j] == "#":
                btns[i][j].config(text="🚩")
                btns[i][j].config(bg="#DAF7A6")  # Fondo verde claro para las celdas marcadas con bandera
            elif visible[i][j] == 9:
                btns[i][j].config(text="")  # Dejar en blanco en lugar de mostrar un asterisco
                btns[i][j].config(bg="#DAF7A6")  # Fondo verde claro para las celdas con bombas
            else:
                numero = visible[i][j]
                color = colores.get(numero, "black")  # Si el número no está en el diccionario, usa negro
                btns[i][j].config(text=str(numero), fg=color)
                btns[i][j].config(bg="#DAF7A6")  # Fondo verde claro para las celdas con números

def jugada(y, x):
    global tablero, visible, minas_marcadas, minas_ocultas, juego_terminado
    if juego_terminado:
        return
    if y < 0 or y >= filas or x < 0 or x >= len(visible[y]):
        return

    if tablero[y][x] == 9:
        # Mostrar todas las bombas al perder
        for my, mx in minas_ocultas:
            if 0 <= my < len(visible) and 0 <= mx < len(visible[my]):
                visible[my][mx] = "@"
        actualizar_interfaz()
        messagebox.showinfo("Fin del juego", "¡Has perdido!")
        ventana.destroy()
    else:
        abrir_casillas_vacias(y, x)  # Llamar a la función corregida
    if tablero_completo(tablero, visible, filas, columnas, 9):
        juego_terminado = True
        actualizar_interfaz()
        messagebox.showinfo("Fin del juego", "¡Has ganado!")
        ventana.destroy()
    else:
        actualizar_interfaz()

def abrir_casillas_vacias(y, x):
    '''Abre las casillas adyacentes vacías de forma recursiva'''
    visible[y][x] = tablero[y][x]  # Mostrar el valor de la casilla actual
    if tablero[y][x] == 0:
        ceros = [(y, x)]
        while len(ceros) > 0:
            y, x = ceros.pop()
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    ny = y + i
                    nx = x + j
                    if 0 <= ny < filas and 0 <= nx < len(visible[ny]) and visible[ny][nx] == "-":
                        visible[ny][nx] = tablero[ny][nx]
                        if tablero[ny][nx] == 0:  # Si la casilla adyacente es 0, agregamos a la lista para seguir abriendo
                            ceros.append((ny, nx))
    return

def marca_desmarca(y, x):
    global visible, minas_marcadas
    if visible[y][x] == "-":
        visible[y][x] = "#"
        if (y, x) not in minas_marcadas:
            minas_marcadas.append((y, x))
    elif visible[y][x] == "#":
        visible[y][x] = "-"
        if (y, x) in minas_marcadas:
            minas_marcadas.remove((y, x))

def mostrar_estrella(event, y, x):
    global visible
    if visible[y][x] == "-":
        visible[y][x] = "#"
        actualizar_interfaz() # Actualizar la interfaz después de cambiar el estado
        btns[y][x].config(text="🚩") # Configuramos el texto del botón

def iniciar_juego():
    global filas, columnas, num_minas, tablero, minas_ocultas, visible, minas_marcadas, btns, juego_terminado, forma_triangulo
    juego_terminado = False
    forma_triangulo = forma_var.get()

    # Obtener la dificultad seleccionada
    dificultad = dificultad_var.get()
    if dificultad == "Fácil":
        filas = 10
        columnas = 10
        num_minas = 15
    elif dificultad == "Medio":
        filas = 12
        columnas = 12
        num_minas = 20
    elif dificultad == "Difícil":
        filas = 15
        columnas = 15
        num_minas = 40
    else:
        messagebox.showerror("Error", "Por favor, selecciona una dificultad.")
        return

    # Limpiar la ventana antes de agregar los botones
    for widget in ventana.winfo_children():
        widget.destroy()

    # Inicializar la lista visible con las dimensiones correctas
    visible = crea_tablero(filas, columnas, "-", forma_triangulo) # Ajusta las dimensiones aquí

    # Inicializar el juego con la nueva dificultad
    tablero = crea_tablero(filas, columnas, 0, forma_triangulo)
    tablero, minas_ocultas = coloca_minas(tablero, num_minas, filas, columnas, forma_triangulo)
    tablero = coloca_pistas(tablero, filas, columnas, forma_triangulo)

    # Inicializar la lista de botones
    btns = []
    for i in range(filas):
        btns.append([])
        for j in range(len(visible[i])): # Ajustamos el rango de columnas según el tamaño de la fila actual
            btn = tk.Button(ventana, text="", width=2, height=1, command=lambda y=i, x=j: jugada(y, x))
            btn.bind("<Button-3>", lambda event, y=i, x=j: mostrar_estrella(event, y, x))
            btn.grid(row=i+1, column=j, padx=1, pady=1)
            btns[i].append(btn)

    actualizar_interfaz()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Buscaminas")

# Widget para seleccionar la dificultad
dificultad_var = tk.StringVar()
dificultad_var.set("Fácil") # Valor predeterminado
dificultad_menu = tk.OptionMenu(ventana, dificultad_var, "Fácil", "Medio", "Difícil")
dificultad_menu.grid(row=0, column=0, pady=10)

# Widget para seleccionar la forma del triángulo
forma_var = tk.StringVar()
forma_var.set("equilatero") # Valor predeterminado
forma_menu = tk.OptionMenu(ventana, forma_var, "equilatero", "isosceles", "escaleno")
forma_menu.grid(row=0, column=1, pady=10)

# Botón para iniciar el juego
iniciar_btn = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
iniciar_btn.grid(row=0, column=2, pady=10)

# Variables globales
filas = 10
columnas = 10
num_minas = 20
tablero = []
minas_ocultas = []
visible = []
minas_marcadas = []
btns = []
juego_terminado = False
forma_triangulo = "equilatero"

ventana.mainloop()