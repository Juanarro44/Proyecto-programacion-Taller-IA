from tkinter import *
import tkinter as tk
from tkinter import ttk
import math
import numpy as np


root = Tk()
root.geometry("300x164")
root.title("Proyecto Programacion")

# Esta parte es para cuando abra el boton tasa
Label(root, text="¡Elije la opcion que estas buscando!").grid(row=0, column=0, pady=10, columnspan=2)

# Cambio de tasas 1
def tasa_fun():
    global entrada, ventana_tasa, valor_tasa, opcion_seleccionada, tasa_conocido, tasa_desconocido, entrada_conocido, entrada_desconocido
    global opcion_seleccionada_per
    tasa_final = 0
    ventana_tasa = Toplevel()
    ventana_tasa.geometry("490x250")
    ventana_tasa.title("Cambio de tasas")
    entrada = Entry(ventana_tasa)
    entrada.grid(row=1, column=0, columnspan=2)
    
    etiqueta = Label(ventana_tasa, text="Escriba el valor de la tasa en porcentaje: ").grid(row=0, columnspan=2)
    
    # Barra de opciones  
    opciones_periodicidad = ["Nominal", "Periodica"]
    opcion_seleccionada = StringVar(ventana_tasa)
    opcion_seleccionada.set(opciones_periodicidad[0])
    
    menu_desplegable = OptionMenu(ventana_tasa, opcion_seleccionada, *opciones_periodicidad)
    menu_desplegable.grid(row=1, column=2)
    
    opciones_ant_ven = ["Vencida", "Anticipada"]
    opcion_seleccionada_per = StringVar(ventana_tasa)
    opcion_seleccionada_per.set(opciones_ant_ven[0])
    menu_desplegable2 = OptionMenu(ventana_tasa, opcion_seleccionada_per, *opciones_ant_ven)
    menu_desplegable2.grid(row=1, column=3)
    
    entrada_conocido = Entry(ventana_tasa)
    entrada_conocido.grid(row=4, column=0, columnspan=2)
    etiqueta_pedir_perio = Label(ventana_tasa, text="Escriba la periodicidad conocida de la tasa en meses:").grid(row=3, column=0, columnspan=2)
    
    entrada_desconocido = Entry(ventana_tasa)
    entrada_desconocido.grid(row=6, column=0, columnspan=2)
    etiqueta_pedir_perio2 = Label(ventana_tasa, text="Escriba la periodicidad desconocida de la tasa en meses:").grid(row=5, column=0, columnspan=2)
  
    boton = Button(ventana_tasa, text="Convertir", width=20, command=obtener_valores).grid(row=10, column=0, columnspan=2)

def obtener_valores():
    valor_entrada = entrada.get()
    valor_conocido = entrada_conocido.get()
    valor_desconocido = entrada_desconocido.get()
    operacion_tasas(valor_entrada, valor_conocido, valor_desconocido)

def operacion_tasas(valor_tasa, tasa_conocido, tasa_desconocido):
    valor_tasa = float(valor_tasa)
    tasa_conocido = float(tasa_conocido)
    tasa_desconocido = float(tasa_desconocido)
    
    if opcion_seleccionada.get() == "Nominal":
        tasa_final = valor_tasa / tasa_conocido
    else:
        tasa_final = valor_tasa
    
    tasa_periodica = Label(ventana_tasa, text="Valor de la tasa periodica es: " + str(tasa_final) + "%")
    tasa_periodica.grid(row=11, column=0)
    
    tasa_cambiar_texto = tasa_periodica.cget("text").split(": ")[1].replace("%", "")
    tasa_cambiar = float(tasa_cambiar_texto) / 100
    
    if opcion_seleccionada_per.get() == "Anticipada":
        cambiada = 1 - tasa_cambiar
        tasa_ven_per = (tasa_cambiar / cambiada) * 100
    else:
        tasa_ven_per = tasa_cambiar * 100
    
    tasa_ven_per = Label(ventana_tasa, text="Valor de la tasa vencida es: " + str(tasa_ven_per) + "%")
    tasa_ven_per.grid(row=12, column=0)
    
    tasa_cambiar_texto2 = tasa_ven_per.cget("text").split(": ")[1].replace("%", "")
    tasa_cambiar_fin = float(tasa_cambiar_texto2)
    
    tasa_cambiar_fin = math.pow((1 + (tasa_cambiar_fin / 100)), (tasa_desconocido / tasa_conocido)) - 1
    tasa_cambiar_fin = tasa_cambiar_fin * 100
    
    tasa_convertida = Label(ventana_tasa, text="Valor de la tasa convertida es: " + str(tasa_cambiar_fin) + "%")
    tasa_convertida.grid(row=13, column=0)

tasa_boton = Button(root, text="Tasa", width=20, height=2, command=tasa_fun).grid(row=1, column=0, columnspan=1)

# Anualidades 2
def calcular_pago_mensual(principal, tasa_anual, años):
    tasa_mensual = tasa_anual / 12 / 100
    num_pagos = años * 12
    pago_mensual = principal * (tasa_mensual * (1 + tasa_mensual)**num_pagos) / ((1 + tasa_mensual)**num_pagos - 1)
    return pago_mensual

def generar_tabla_amortizacion(principal, tasa_anual, años):
    tasa_mensual = tasa_anual / 12 / 100
    num_pagos = años * 12
    pago_mensual = calcular_pago_mensual(principal, tasa_anual, años)
    
    saldo = principal
    tabla_amortizacion = []
    
    for i in range(num_pagos):
        interes = saldo * tasa_mensual
        capital = pago_mensual - interes
        saldo -= capital
        tabla_amortizacion.append((i + 1, pago_mensual, capital, interes, saldo))
    
    return tabla_amortizacion

def calcular_amortizacion_anua():
    principal = float(entry_principal_anua.get())
    tasa_anual = float(entry_tasa_anual_anua.get())
    años = int(entry_años_anua.get())

    pago_mensual = calcular_pago_mensual(principal, tasa_anual, años)
    label_pago_mensual_anua.config(text=f'Pago mensual: {pago_mensual:.2f}')

    tabla = generar_tabla_amortizacion(principal, tasa_anual, años)

    total_pagado = sum(row[1] for row in tabla)
    label_total_pagado_anua.config(text=f'Total pagado: {total_pagado:.2f}')

    for i in mostrar_anua.get_children():
        mostrar_anua.delete(i)

    for fila in tabla:
        mostrar_anua.insert('', tk.END, values=fila) 

def anua_fun():
    global entry_principal_anua, entry_tasa_anual_anua, entry_años_anua, label_pago_mensual_anua, label_total_pagado_anua, mostrar_anua

    ventana_anua = tk.Toplevel(root)
    ventana_anua.geometry("1050x500")
    ventana_anua.title("Cálculo de anualidades")

    frame_anua = tk.Frame(ventana_anua)
    frame_anua.pack(padx=10, pady=10)

    tk.Label(frame_anua, text="Monto del préstamo:").grid(row=0, column=0, sticky='e')
    entry_principal_anua = tk.Entry(frame_anua)
    entry_principal_anua.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_anua, text="Tasa de interés anual (%):").grid(row=1, column=0, sticky='e')
    entry_tasa_anual_anua = tk.Entry(frame_anua)
    entry_tasa_anual_anua.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_anua, text="Duración del préstamo (años):").grid(row=2, column=0, sticky='e')
    entry_años_anua = tk.Entry(frame_anua)
    entry_años_anua.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(frame_anua, text="Calcular", command=calcular_amortizacion_anua).grid(row=3, column=0, columnspan=2, pady=10)

    label_pago_mensual_anua = tk.Label(frame_anua, text="Pago mensual: ")
    label_pago_mensual_anua.grid(row=4, column=0, columnspan=2)

    label_total_pagado_anua = tk.Label(frame_anua, text="Total pagado: ")
    label_total_pagado_anua.grid(row=5, column=0, columnspan=2)

    columnas = ('Mes', 'Pago Mensual', 'Capital', 'Intereses', 'Saldo')

    mostrar_anua = ttk.Treeview(frame_anua, columns=columnas, show='headings')
    for col in columnas:
        mostrar_anua.heading(col, text=col)
        mostrar_anua.grid(row=6, column=0, columnspan=2)

anua_boton = Button(root, text="Anualidades", width=20, height=2, command=anua_fun).grid(row=2, column=0, columnspan=1)

# Gradientes 3

def calcular_anualidades_crecientes(principal, tasa_anual, tasa_crecimiento, años):
    tasa_mensual = tasa_anual / 12 / 100
    tasa_crec_mensual = tasa_crecimiento / 12 / 100
    num_pagos = años * 12
    saldo = principal
    tabla_grad = []
    
    # Verificar si las tasas son iguales para evitar división por cero
    if tasa_mensual == tasa_crec_mensual:
        pago_inicial = principal / num_pagos  # Una aproximación sencilla si las tasas son iguales
    else:
        pago_inicial = principal * (tasa_mensual - tasa_crec_mensual) / (1 - (1 + tasa_crec_mensual) / (1 + tasa_mensual))  # Aprox inicial del pago

    for i in range(num_pagos):
        interes = saldo * tasa_mensual
        cuota = pago_inicial * ((1 + tasa_crec_mensual) ** i)
        capital = cuota - interes
        saldo -= capital
        tabla_grad.append((i + 1, cuota, capital, interes, saldo))

    return tabla_grad

def calcular_grad():
    principal = float(entry_principal_grad.get())
    tasa_anual = float(entry_tasa_anual_grad.get())
    tasa_crecimiento = float(entry_tasa_crec_grad.get())
    años = int(entry_años_grad.get())

    tabla = calcular_anualidades_crecientes(principal, tasa_anual, tasa_crecimiento, años)

    total_pagado = sum(row[1] for row in tabla)
    label_total_pagado_grad.config(text=f'Total pagado: {total_pagado:.2f}')

    for i in mostrar_grad.get_children():
        mostrar_grad.delete(i)

    for fila in tabla:
        mostrar_grad.insert('', tk.END, values=fila)

def grad_fun():
    global entry_principal_grad, entry_tasa_anual_grad, entry_tasa_crec_grad, entry_años_grad, label_total_pagado_grad, mostrar_grad

    ventana_grad = Toplevel(root)
    ventana_grad.geometry("1050x500")
    ventana_grad.title("Calculo de gradientes")

    frame_grad = tk.Frame(ventana_grad)
    frame_grad.pack(padx=10, pady=10)

    tk.Label(frame_grad, text="Monto del préstamo:").grid(row=0, column=0, sticky='e')
    entry_principal_grad = tk.Entry(frame_grad)
    entry_principal_grad.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_grad, text="Tasa de interés anual (%):").grid(row=1, column=0, sticky='e')
    entry_tasa_anual_grad = tk.Entry(frame_grad)
    entry_tasa_anual_grad.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_grad, text="Tasa de crecimiento anual (%):").grid(row=2, column=0, sticky='e')
    entry_tasa_crec_grad = tk.Entry(frame_grad)
    entry_tasa_crec_grad.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_grad, text="Duración del préstamo (años):").grid(row=3, column=0, sticky='e')
    entry_años_grad = tk.Entry(frame_grad)
    entry_años_grad.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(frame_grad, text="Calcular", command=calcular_grad).grid(row=4, column=0, columnspan=2, pady=10)

    label_total_pagado_grad = tk.Label(frame_grad, text="Total pagado: ")
    label_total_pagado_grad.grid(row=5, column=0, columnspan=2)

    columns_grad = ('mes', 'pago', 'capital', 'interes', 'saldo')
    mostrar_grad = ttk.Treeview(ventana_grad, columns=columns_grad, show='headings')
    mostrar_grad.heading('mes', text='Mes')
    mostrar_grad.heading('pago', text='Pago')
    mostrar_grad.heading('capital', text='Capital')
    mostrar_grad.heading('interes', text='Interés')
    mostrar_grad.heading('saldo', text='Saldo')

    mostrar_grad.pack(padx=10, pady=10)

grad_boton = Button(root, text="Gradientes", width=20, height=2, command=grad_fun).grid(row=3, column=0, columnspan=1)





# TIR 4
from tkinter import *

def calcular_tir(flujos_de_caja):
    # Tasa inicial de prueba
    guess = 0.1
    
    # Función para calcular el valor presente neto (VPN) dado una tasa de descuento
    def calcular_vpn(flujos_de_caja, tasa_descuento):
        return sum([flujo / (1 + tasa_descuento) ** indice for indice, flujo in enumerate(flujos_de_caja)])
    
    # Implementación del método de aproximación de Newton-Raphson para encontrar la TIR
    epsilon = 0.0001
    max_iter = 1000
    i = 0
    while True:
        vpn = calcular_vpn(flujos_de_caja, guess)
        derivada = (calcular_vpn(flujos_de_caja, guess + epsilon) - vpn) / epsilon
        # Manejar el caso donde la derivada es cercana a cero
        if abs(derivada) < epsilon:
            break
        guess = guess - vpn / derivada
        if abs(vpn) < epsilon or i >= max_iter:
            break
        i += 1
    
    return guess

def tir_fun():
    ventana_tir = Toplevel()
    ventana_tir.geometry("400x300")
    ventana_tir.title("Cálculo de TIR")
    
    Label(ventana_tir, text="Ingrese los flujos de caja separados por comas:").pack(pady=10)
    entry_flujos_de_caja = Entry(ventana_tir, width=50)
    entry_flujos_de_caja.pack(pady=10)
    
    def calcular_y_mostrar_tir():
        flujos_str = entry_flujos_de_caja.get()
        try:
            flujos_de_caja = list(map(float, flujos_str.split(',')))
            tir = calcular_tir(flujos_de_caja)
            label_tir_resultado.config(text=f"TIR: {tir:.4f}")
        except ValueError:
            label_tir_resultado.config(text="Error: Asegúrese de ingresar números separados por comas.")
    
    Button(ventana_tir, text="Calcular TIR", command=calcular_y_mostrar_tir).pack(pady=10)
    
    label_tir_resultado = Label(ventana_tir, text="")
    label_tir_resultado.pack(pady=10)


TIR_boton = Button(root, text="TIR", width=20, height=2, command=tir_fun)
TIR_boton.grid(row=1, column=1, columnspan=1)




#Rentabilidad CDT 5

def depre_fun():
    ventana_depre = Toplevel()
    ventana_depre.geometry("350x200")
    ventana_depre.title("Cálculo de rentabilidad en CDT")

    # Función para calcular la rentabilidad del CDT
    def calcular_rentabilidad():
        try:
            tasa_cdt = float(entry_tasa_cdt.get()) / 100  # Convertir a decimal
            monto_depositado = float(entry_monto_depositado.get())
            tiempo = float(entry_tiempo.get())
            tiempo_en_meses = tiempo if var_tiempo.get() == "Años" else tiempo / 12

            # Fórmula para calcular la rentabilidad
            rentabilidad = monto_depositado * (1 + tasa_cdt) ** tiempo_en_meses - monto_depositado
            total_final = monto_depositado * (1 + tasa_cdt) ** tiempo_en_meses

            label_rentabilidad.config(text=f"La rentabilidad del CDT es: {rentabilidad:.2f}")
            label_total_final.config(text=f"El total de dinero al final es: {total_final:.2f}")
        except ValueError:
            label_rentabilidad.config(text="Por favor, introduce valores numéricos válidos.")

    # Etiquetas y campos de entrada
    Label(ventana_depre, text="Tasa del CDT (%):").grid(row=0, column=0)
    entry_tasa_cdt = Entry(ventana_depre)
    entry_tasa_cdt.grid(row=0, column=1)

    Label(ventana_depre, text="Monto depositado:").grid(row=1, column=0)
    entry_monto_depositado = Entry(ventana_depre)
    entry_monto_depositado.grid(row=1, column=1)

    Label(ventana_depre, text="Tiempo:").grid(row=2, column=0)
    entry_tiempo = Entry(ventana_depre)
    entry_tiempo.grid(row=2, column=1)
    
    var_tiempo = StringVar()
    var_tiempo.set("Años")
    tiempo_options = ["Años", "Meses"]
    tiempo_menu = OptionMenu(ventana_depre, var_tiempo, *tiempo_options)
    tiempo_menu.grid(row=2, column=2)

    # Botón para calcular la rentabilidad
    Button(ventana_depre, text="Calcular Rentabilidad", command=calcular_rentabilidad).grid(row=3, columnspan=3)

    # Etiqueta para mostrar la rentabilidad calculada
    label_rentabilidad = Label(ventana_depre, text="")
    label_rentabilidad.grid(row=4, columnspan=3)

    # Etiqueta para mostrar el total de dinero al final
    label_total_final = Label(ventana_depre, text="")
    label_total_final.grid(row=5, columnspan=3)

Depreciacion_boton = Button(root, text="Rentabilidad CDT", width=20, height=2, command=depre_fun).grid(row=2, column=1, columnspan=1)





#Estado de Resultados  6

def flujo_de_caja_fun():
    ventana_portafolio = Toplevel()
    ventana_portafolio.geometry("600x500")
    ventana_portafolio.title("Estado de Resultados")
    
    def calcular_estado_resultados():
        # Obtiene los valores ingresados por el usuario
        try:
            ventas = float(ventas_entry.get())
            costos_ventas = float(costos_ventas_entry.get())
            gastos_operativos = float(gastos_operativos_entry.get())
            gastos_financieros = float(gastos_financieros_entry.get())
            otros_ingresos = float(otros_ingresos_entry.get())
            otros_gastos = float(otros_gastos_entry.get())
            impuestos = float(impuestos_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")
            return

        # Calcula los valores del estado de resultados
        utilidad_bruta = ventas - costos_ventas
        utilidad_operacional = utilidad_bruta - gastos_operativos
        utilidad_antes_impuestos = utilidad_operacional + otros_ingresos - gastos_financieros - otros_gastos
        utilidad_neta = utilidad_antes_impuestos - impuestos

        # Muestra los resultados al usuario
        resultado_text.config(state="normal")
        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, f"Utilidad bruta: {utilidad_bruta:.2f}\n")
        resultado_text.insert(tk.END, f"Utilidad operacional: {utilidad_operacional:.2f}\n")
        resultado_text.insert(tk.END, f"Utilidad antes de impuestos: {utilidad_antes_impuestos:.2f}\n")
        resultado_text.insert(tk.END, f"Utilidad neta: {utilidad_neta:.2f}\n")

        if utilidad_neta > 0:
            resultado_text.insert(tk.END, "La empresa cuenta con ganancias.\n")
        elif utilidad_neta < 0:
            resultado_text.insert(tk.END, "La empresa cuenta con pérdidas.\n")
        resultado_text.config(state="disabled")

    # Encabezado
    header_label = tk.Label(ventana_portafolio, text="Estado de Resultados")
    header_label.pack()

    # Sub encabezado
    periodicidad_label = tk.Label(ventana_portafolio, text="Periodicidad del estado de resultados:")
    periodicidad_label.pack()

    # Datos de entrada
    ventas_label = tk.Label(ventana_portafolio, text="Ventas:")
    ventas_label.pack()
    ventas_entry = tk.Entry(ventana_portafolio)
    ventas_entry.pack()

    costos_ventas_label = tk.Label(ventana_portafolio, text="Costos de ventas:")
    costos_ventas_label.pack()
    costos_ventas_entry = tk.Entry(ventana_portafolio)
    costos_ventas_entry.pack()

    gastos_operativos_label = tk.Label(ventana_portafolio, text="Gastos operativos:")
    gastos_operativos_label.pack()
    gastos_operativos_entry = tk.Entry(ventana_portafolio)
    gastos_operativos_entry.pack()

    gastos_financieros_label = tk.Label(ventana_portafolio, text="Gastos financieros:")
    gastos_financieros_label.pack()
    gastos_financieros_entry = tk.Entry(ventana_portafolio)
    gastos_financieros_entry.pack()

    otros_ingresos_label = tk.Label(ventana_portafolio, text="Otros ingresos:")
    otros_ingresos_label.pack()
    otros_ingresos_entry = tk.Entry(ventana_portafolio)
    otros_ingresos_entry.pack()

    otros_gastos_label = tk.Label(ventana_portafolio, text="Otros gastos:")
    otros_gastos_label.pack()
    otros_gastos_entry = tk.Entry(ventana_portafolio)
    otros_gastos_entry.pack()

    impuestos_label = tk.Label(ventana_portafolio, text="Impuestos:")
    impuestos_label.pack()
    impuestos_entry = tk.Entry(ventana_portafolio)
    impuestos_entry.pack()

    # Botón para calcular el estado de resultados
    calcular_button = tk.Button(ventana_portafolio, text="Calcular", command=calcular_estado_resultados)
    calcular_button.pack()

    # Resultado
    resultado_label = tk.Label(ventana_portafolio, text="Resultado:")
    resultado_label.pack()
    resultado_text = tk.Text(ventana_portafolio, height=10, width=50, state="disabled")
    resultado_text.pack()

Portafolio_boton = Button(root, text="Estado de Resultados", width=20, height=2, command=flujo_de_caja_fun).grid(row=3, column=1, columnspan=1) 


root.mainloop()
