from flask import Flask
import os
import mysql.connector

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppass"),
        database=os.getenv("DB_NAME", "hola_db"),
    )

@app.route("/")
def index():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        # Creamos una tabla de ejemplo y agregamos un registro
        cur.execute("""
            CREATE TABLE IF NOT EXISTS saludos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                texto VARCHAR(255)
            )
        """)
        cur.execute("INSERT INTO saludos (texto) VALUES ('Hola desde MySQL!')")
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM saludos")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"Hola Mundo 👋 — Conexión a MySQL OK. Filas en 'saludos': {count}"
    except Exception as e:
        return f"Hola Mundo 👋 — Error conectando a MySQL: {e}"

if __name__ == "__main__":
    # Servidor de desarrollo
    app.run(host="0.0.0.0", port=5000)
