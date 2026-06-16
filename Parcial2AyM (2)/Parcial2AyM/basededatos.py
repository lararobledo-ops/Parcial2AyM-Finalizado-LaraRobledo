import sqlite3

# Conectarse (si no existe, la crea)
conexion = sqlite3.connect("finanzas.db")

cursor = conexion.cursor()

# Tabla Usuario
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Tabla Movimiento
cursor.execute("""
CREATE TABLE IF NOT EXISTS movimiento (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    monto REAL NOT NULL,
    categoria TEXT NOT NULL,
    fecha TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
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

print("Base de datos creada correctamente")