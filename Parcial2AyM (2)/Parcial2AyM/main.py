import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def inicializar_db():
    conexion = sqlite3.connect("finanzas.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimiento (
        id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        monto REAL NOT NULL,
        categoria TEXT NOT NULL,
        fecha TEXT NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO usuario (nombre, email, password)
    VALUES (?, ?, ?)
    """, ("Lari", "lari@gmail.com", "1234"))

    cursor.execute("""
    INSERT OR IGNORE INTO usuario (nombre, email, password)
    VALUES (?, ?, ?)
    """, ("Admin", "admin@gmail.com", "1234"))

    conexion.commit()
    conexion.close()


# dataframe
df = pd.DataFrame(columns=[
    "Tipo",
    "Monto",
    "Categoria",
    "Fecha"
])

# ventana princial 1
inicializar_db()

ventana = tk.Tk()

ventana.title("Finanzas")
ventana.geometry("600x620")
ventana.configure(bg="green")

try:
    imagen_original = Image.open(
        os.path.join(BASE_DIR, "plata.png")
    )

    imagen_login = ImageTk.PhotoImage(
        imagen_original.resize((220, 220))
    )

    logo_label = tk.Label(
        ventana,
        image=imagen_login,
        bg="green"
    )

    logo_label.image = imagen_login
    logo_label.pack(pady=10)

except Exception as e:
    print("ERROR cargando plata.png:", e)




# ventana secundaria 2
def abrir_ventana():

    
    

    nueva = tk.Toplevel(ventana)

    

    nueva.title("Mis finanzas")
    nueva.geometry("1200x900")
    nueva.configure(bg="green")

    contenedor = ttk.Frame(nueva)
    contenedor.pack(fill="both", expand=True)


    
    canvas = tk.Canvas(contenedor, bg="green")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        contenedor,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_scrollable = tk.Frame(
        canvas,
        bg="green"
    )

    
    canvas_window = canvas.create_window(
        (0, 0),
        window=frame_scrollable,
        anchor="n"
    )

    frame_scrollable.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(canvas_window, width=e.width)
    )


    titulo = tk.Label(
        frame_scrollable,
        text="Panel de Control Financiero",
        font=("Consolas", 24, "bold"),
        bg="green",
        fg="white"
    )

    titulo.pack(pady=15)


    # CONTENEDOR FORMULARIO + IMAGEN
    frame_formulario = tk.Frame(frame_scrollable, bg="green")
    frame_formulario.pack(pady=20)

    # IZQUIERDA
    frame_campos = tk.Frame(frame_formulario, bg="green")
    frame_campos.pack(side="left", padx=30)

    # DERECHA
    frame_logo = tk.Frame(frame_formulario, bg="green")
    frame_logo.pack(side="left", padx=30)


    try:
        imagen_original = Image.open(
            os.path.join(BASE_DIR, "gastos2.png")
        )
        
        imagen_original.thumbnail((80, 80))  # tamaño final

        imagen_gastos = ImageTk.PhotoImage(
            imagen_original
        )

        logo_label = tk.Label(
            frame_logo,
            image=imagen_gastos,
            bg="green"
        )

        logo_label.image = imagen_gastos
        logo_label.pack()

    except Exception as e:
        print("ERROR:", e)


    #frame_inferior = tk.Frame(frame_scrollable, bg="green")
    

    #frame_inferior.pack(pady=5, fill="x", expand=True)

    #frame_imagen = tk.Frame(
        #frame_inferior,
        #bg="green"
    #) 

    #frame_imagen.pack(
        #side="left",
        #padx=10,
        #fill="both",
        #expand=True
    #)


    def eliminar():

        seleccionado = tabla.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un registro"
            )
            return

        valores = tabla.item(
        seleccionado[0]
        )["values"]

        tipo = valores[0]
        monto = valores[1]
        categoria = valores[2]
        fecha = valores[3]

        conexion = sqlite3.connect("finanzas.db")
        cursor = conexion.cursor()

        cursor.execute("""
        DELETE FROM movimiento
        WHERE tipo = ?
        AND monto = ?
        AND categoria = ?
        AND fecha = ?
        """, (
            tipo,
            monto,
            categoria,
             fecha
        ))

        conexion.commit()
        conexion.close()

        tabla.delete(seleccionado[0])

    #sincronizar_dataframe_con_db()

        messagebox.showinfo(
             "Éxito",
              "Registro eliminado"
        )

    def editar():

        seleccionado = tabla.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un registro"
            )
            return

        valores = tabla.item(
           seleccionado[0]
        )["values"]

        entry_tipo.delete(0, tk.END)
        entry_monto.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)

        entry_tipo.insert(0, valores[0])
        entry_monto.insert(0, valores[1])
        entry_categoria.insert(0, valores[2])
        entry_fecha.insert(0, valores[3])
    
   

 #formulario

    tk.Label(
        frame_campos,
        text="Tipo (ingreso/gasto):",
        bg="green"
    ).pack()

    entry_tipo = tk.Entry(frame_campos)
    entry_tipo.pack()


    tk.Label(
        frame_campos,
        text="Monto:",
        bg="green"
    ).pack()

    entry_monto = tk.Entry(frame_campos)
    entry_monto.pack()

    tk.Label(
        frame_campos,
        text="Categoría:",
        bg="green"
    ).pack()

    entry_categoria = tk.Entry(frame_campos)
    entry_categoria.pack()

    tk.Label(
        frame_campos,
        text="Fecha (YYYY-MM-DD):",
        bg="green"
    ).pack()
     
    
    entry_fecha = tk.Entry(frame_campos)
    entry_fecha.pack()

    def actualizar():

        seleccionado = tabla.selection()

        if not seleccionado:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un registro"
            )
            return

        valores_viejos = tabla.item(
            seleccionado[0]
        )["values"]

        tipo_viejo = valores_viejos[0]
        monto_viejo = valores_viejos[1]
        categoria_vieja = valores_viejos[2]
        fecha_vieja = valores_viejos[3]

        tipo = entry_tipo.get()
        monto = float(entry_monto.get())
        categoria = entry_categoria.get()
        fecha = entry_fecha.get()

        conexion = sqlite3.connect("finanzas.db")
        cursor = conexion.cursor()

        cursor.execute("""
        UPDATE movimiento
        SET tipo = ?,
            monto = ?,
            categoria = ?,
            fecha = ?
        WHERE tipo = ?
        AND monto = ?
        AND categoria = ?
        AND fecha = ?
        """, (
            tipo,
            monto,
            categoria,
            fecha,
            tipo_viejo,
            monto_viejo,
            categoria_vieja,
            fecha_vieja
        ))

        conexion.commit()
        conexion.close()

        tabla.item(
            seleccionado[0],
            values=(tipo, monto, categoria, fecha)
        )

        messagebox.showinfo(
            "Éxito",
            "Registro actualizado"
      )

    #tabla
    # Frame para contener tabla y scrollbar
    frame_tabla = ttk.Frame(frame_scrollable)
    frame_tabla.pack(pady=20)


    tabla = ttk.Treeview(
        frame_tabla,
        columns=("Tipo", "Monto", "Categoria", "Fecha"),
        show="headings",
        height=8
    )

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(
        frame_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=scrollbar.set)
 

    tabla.heading("Tipo", text="Tipo")
    tabla.heading("Monto", text="Monto")
    tabla.heading("Categoria", text="Categoría")
    tabla.heading("Fecha", text="Fecha")

    # Conectar scrollbar con la tabla
    scrollbar.config(command=tabla.yview)

# Ubicación de widgets
    tabla.pack(side="left")
    scrollbar.pack(side="right", fill="y")

    #tabla.pack(pady=20)

    #cargar datos existentes
    def cargar_datos():

        conexion = sqlite3.connect("finanzas.db")
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT tipo, monto, categoria, fecha
        FROM movimiento
        """)

        registros = cursor.fetchall()

        for registro in registros:

            tabla.insert(
                "",
                tk.END,
                values=registro
            )

            nuevo = {
                "Tipo": registro[0],
                "Monto": registro[1],
                "Categoria": registro[2],
                "Fecha": registro[3]
            }

            global df

            df = pd.concat(
                [df, pd.DataFrame([nuevo])],
                ignore_index=True
            )

        conexion.close()

    #ejecutar la carga
    cargar_datos()

    #función gráfico
    def mostrar_grafico():


        df_limpio = df.copy()

        df_limpio["Tipo"] = df_limpio["Tipo"].astype(str).str.strip().str.lower()
        df_limpio["Categoria"] = df_limpio["Categoria"].astype(str).str.strip()

        df_limpio["Monto"] = pd.to_numeric(df_limpio["Monto"], errors="coerce")

        df_limpio = df_limpio.dropna(subset=["Monto", "Tipo", "Categoria"])

        gastos = df_limpio[df_limpio["Tipo"] == "gasto"].copy()

        if gastos.empty:
            messagebox.showwarning("Aviso", "No hay gastos cargados")
            return

    #el dato numerico sea real
        gastos["Monto"] = pd.to_numeric(gastos["Monto"], errors="coerce")
        gastos = gastos.dropna(subset=["Monto"])

        if gastos.empty:
            messagebox.showwarning("Aviso", "No hay datos numéricos válidos")
            return

        totales = gastos.groupby("Categoria")["Monto"].sum()

        if totales.empty:
            messagebox.showwarning("Aviso", "No hay datos para graficar")
            return

        totales = totales.astype(float)

        ax = totales.plot(kind="bar")

        ax.set_title("Gastos por categoría")
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Monto")

        plt.tight_layout()
        plt.show()
    #grafico2
    
    def grafico_detorta():

        df_limpio = df.copy()

        df_limpio["Tipo"] = df_limpio["Tipo"].astype(str).str.strip().str.lower()
        df_limpio["Categoria"] = df_limpio["Categoria"].astype(str).str.strip()
        df_limpio["Monto"] = pd.to_numeric(df_limpio["Monto"], errors="coerce")

        df_limpio = df_limpio.dropna(subset=["Monto", "Tipo"])

        gastos = df_limpio[df_limpio["Tipo"] == "gasto"]

        if gastos.empty:
            messagebox.showwarning("Aviso", "No hay gastos")
            return

        totales = gastos.groupby("Categoria")["Monto"].sum()

        if totales.empty:
            messagebox.showwarning("Aviso", "Sin datos")
            return

        totales.plot.pie(autopct="%1.1f%%")

        plt.title("Distribución de gastos")
        plt.ylabel("")
        plt.show()

    #grafico 3
    def comparacion_ingresos_gastos():

        df_limpio = df.copy()

        df_limpio["Tipo"] = df_limpio["Tipo"].astype(str).str.strip().str.lower()
        df_limpio["Monto"] = pd.to_numeric(df_limpio["Monto"], errors="coerce")

        df_limpio = df_limpio.dropna(subset=["Monto", "Tipo"])

        ingresos = df_limpio[df_limpio["Tipo"] == "ingreso"]["Monto"].sum()
        gastos = df_limpio[df_limpio["Tipo"] == "gasto"]["Monto"].sum()

        plt.bar(["Ingresos", "Gastos"], [ingresos, gastos])

        plt.title("Ingresos vs Gastos")
        plt.ylabel("Monto")
        plt.show()

    #evolucion de gastos grafico 4
    def grafico_fechas():
        
        df_limpio = df.copy()

        df_limpio["Tipo"] = (
            df_limpio["Tipo"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df_limpio["Monto"] = pd.to_numeric(
            df_limpio["Monto"],
            errors="coerce"
        )

        df_limpio["Fecha"] = pd.to_datetime(
            df_limpio["Fecha"],
            errors="coerce"
        )

        df_limpio = df_limpio.dropna(
            subset=["Monto", "Fecha", "Tipo"]
        )

        gastos = df_limpio[
            df_limpio["Tipo"] == "gasto"
        ]

        if gastos.empty:
            messagebox.showwarning(
                "Aviso",
                "No hay gastos cargados"
            )
            return

        gastos_por_fecha = (
            gastos.groupby("Fecha")["Monto"]
            .sum()
            .sort_index()
        )

        if gastos_por_fecha.empty:
            messagebox.showwarning(
                "Aviso",
                "No hay datos para graficar"
            )
            return

        plt.figure(figsize=(8, 4))

        plt.plot(
            gastos_por_fecha.index,
            gastos_por_fecha.values,
            marker="o"
        )

        plt.title("Evolución de gastos")
        plt.xlabel("Fecha")
        plt.ylabel("Monto gastado")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    #grafico de gastos por mes, grafico 5
    def grafico_mensual():


        df_limpio = df.copy()

        df_limpio["Tipo"] = (
            df_limpio["Tipo"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df_limpio["Monto"] = pd.to_numeric(
            df_limpio["Monto"],
            errors="coerce"
        )

        df_limpio["Fecha"] = pd.to_datetime(
            df_limpio["Fecha"],
            errors="coerce"
        )

        df_limpio = df_limpio.dropna(
            subset=["Monto", "Fecha", "Tipo"]
        )

        ingresos = df_limpio[
            df_limpio["Tipo"] == "ingreso"
        ].copy()

        if ingresos.empty:
            messagebox.showwarning(
                "Aviso",
                "No hay ingresos cargados"
            )
            return

        ingresos["Mes"] = (
            ingresos["Fecha"]
            .dt.to_period("M")
            .astype(str)
        )

        sueldo_mes = (
            ingresos.groupby("Mes")["Monto"]
            .sum()
            .sort_index()
        )

        if sueldo_mes.empty:
            messagebox.showwarning(
                "Aviso",
                "No hay datos para graficar"
            )
            return

        plt.figure(figsize=(8, 5))

        plt.barh(
            sueldo_mes.index,
            sueldo_mes.values
        )

        plt.title("Ingresos por mes")
        plt.xlabel("Monto")
        plt.ylabel("Mes")

        plt.tight_layout()
        plt.show()

    #guardar datos
    def guardar():

        global df

        tipo = entry_tipo.get()

        monto_texto = entry_monto.get()

        categoria = entry_categoria.get()

        fecha = entry_fecha.get()

        #validaciones
        if tipo == "" or monto_texto == "":

            messagebox.showerror(
                "Error",
                "Completa los campos obligatorios"
            )

            return

        try:
            monto = float(monto_texto)

        except ValueError:

            messagebox.showerror(
                "Error",
                "El monto debe ser numérico"
            )

            return


        #guardar en SQLite
        conexion = sqlite3.connect("finanzas.db")
        cursor = conexion.cursor()

        id_usuario = 1  #id fijo para este ejemplo

        cursor.execute("""
        INSERT INTO movimiento
        (id_usuario, tipo, monto, categoria, fecha)
        VALUES (?, ?, ?, ?, ?)
        """, (
            id_usuario,
            tipo,
            monto,
            categoria,
            fecha
       ))

        conexion.commit()
        conexion.close()

        #agregar fila a la tabla
        tabla.insert(
            "",
            tk.END,
            values=(tipo, monto, categoria, fecha)
        )

        nuevo = {
            "Tipo": tipo,
            "Monto": monto,
            "Categoria": categoria,
            "Fecha": fecha
        }

        #agregar al dataframe
        df = pd.concat(
            [df, pd.DataFrame([nuevo])],
            ignore_index=True
        )

        print(df)

        messagebox.showinfo(
            "Guardado",
            "Registro guardado correctamente"
        )

        #limpiar campos
        entry_tipo.delete(0, tk.END)

        entry_monto.delete(0, tk.END)

        entry_categoria.delete(0, tk.END)

        entry_fecha.delete(0, tk.END)
    

    frame_botones = tk.Frame(frame_scrollable, bg="green")
    frame_botones.pack(pady=15)
    
    #BOTONESSSS
    #boton guardar
    tk.Button(
        frame_botones,
        text="Guardar",
        command=guardar,
        bg="lightblue"
    ).pack(side="left",padx=5)

    #boton grafico

    tk.Button(
    frame_botones,
    text="Eliminar",
    command=eliminar,
    bg="salmon"
    ).pack(side="left",padx=5)

    tk.Button(
    frame_botones,
    text="Editar",
    command=editar,
    bg="khaki"
    ).pack(side="left",padx=5)

    tk.Button(
    frame_botones,
    text="Actualizar",
    command=actualizar,
    bg="orange"
    ).pack(side="left",padx=5)

    texto_info = tk.Label(
    frame_scrollable,
    text="Panel de gráficos",
    font=("Consolas", 12
    , "bold"),
    bg="green"
    )

    texto_info.pack(pady=10)

    #botones nuevos
    # CONTENEDOR GENERAL
    frame_inferior = tk.Frame(frame_scrollable, bg="green")
    frame_inferior.pack(pady=10, fill="both", expand=True)

# BOTONES A LA IZQUIERDA
    frame_nuevos_botones = tk.Frame(
       frame_inferior,
       bg="green",
    )
    frame_nuevos_botones.pack(
        anchor="center",
        #side="left",
        pady=10,
    )


# IMAGEN A LA DERECHA
    frame_imagen = tk.Frame(
        frame_inferior,
        bg="green"
    )
    frame_imagen.pack(
        side="left",
        padx=30
    )

    #gráfico de balance entre ingresos y gastos del mes actual
    tk.Button(
    frame_nuevos_botones,
    text="Gastos por categoria",
    command=mostrar_grafico
    ).pack(pady=5, anchor="center")

    #grafico de todos los gastos que hubo en la semana 
    tk.Button(
    frame_nuevos_botones,
    text="Grafico de distribución de gastos",
    command=grafico_detorta
    ).pack(pady=5, anchor="center")

    #Comparacion de ingresos vs gastos del mes actual
    tk.Button(
    frame_nuevos_botones,
    text="Comparación ingresos vs gastos",
    command=comparacion_ingresos_gastos
    ).pack(pady=5, anchor="center")

    #1er grafico que hice, con las categorias y sus gastos generales
    tk.Button(
    frame_nuevos_botones,
    text="Evolución de gastos",
    command=grafico_fechas
    ).pack(pady=5, anchor="center")

    #gastos totales de cada mes
    tk.Button(
    frame_nuevos_botones,
    text="Evolución de ingresos",
    command=grafico_mensual
    ).pack(pady=5, anchor="center")


#login
def enviar():

    usuario = entry_usuario.get()

    password = entry_password.get()

    conexion = sqlite3.connect("finanzas.db")

    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id_usuario, nombre
    FROM usuario
    WHERE email = ? AND password = ?
    """, (usuario, password))

    usuario_encontrado = cursor.fetchone()

    conexion.close()

    if usuario_encontrado:

        nombre = usuario_encontrado[1]

        resultado.config(
        text=f"Bienvenido {nombre}"
        )

        abrir_ventana()

    else:

        messagebox.showerror(
            "Error",
            "Credenciales incorrectas"
    )    
  

#encabezado
encabezado = tk.Label(
    ventana,
    text="Bienvenido a su aplicación Tus Finanzas",
    font=("Consolas", 16, "bold"),
    bg="lightblue"
)

encabezado.pack(pady=15)


#formulario login
form_frame = tk.Frame(
    ventana,
    bg="green"
)

form_frame.pack(pady=20)

tk.Label(
    form_frame,
    text="Email:",
    bg="green"
).grid(row=0, column=0)

entry_usuario = tk.Entry(
    form_frame,
    width=35
)

entry_usuario.grid(row=0, column=1)

tk.Label(
    form_frame,
    text="Contraseña:",
    bg="green"
).grid(row=1, column=0)

entry_password = tk.Entry(
    form_frame,
    show="*",
    width=35
)

entry_password.grid(row=1, column=1)

resultado = tk.Label(
    ventana,
    text="",
    bg="green"
)

resultado.pack(pady=10)

#botón ingresar
tk.Button(
    ventana,
    text="Ingresar",
    command=enviar,
    bg="lightblue"
).pack(pady=15)

#ejecutar app
ventana.mainloop()




