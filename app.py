from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="", # oma käyttäjä
            password="",  # oma salasana
            database="lempdb"
        )
        cursor = conn.cursor()

        # Haetaan uusin server_time
        cursor.execute("SELECT server_time FROM server_time ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()

        if result and result[0]:
            server_time = result[0]
        else:
            server_time = "Ei aikaa tietokannassa"

    except Error as err:
        return f"""
        <h1 style='color: red;'>Tietokantavirhe</h1>
        <p>{err}</p>
        """

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    # Palautetaan HTML
    return f"""
    <html>
        <head>
            <title>Mitä kello oli joskus?</title>
            <!-- Google Fonts -->
            <link href="https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Montserrat&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Patrick Hand', sans-serif;
                    background: linear-gradient(135deg, #5f0f40, #ade8f4);
                    text-align: center;
                    margin-top: 100px;
                }}
                .card {{
                    background: white;
                    display: inline-block;
                    padding: 30px 60px;
                    border-radius: 20px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.2);
                }}
                h1 {{
                    color: #444;
                    font-family: 'Patrick Hand', sans-serif;
                }}
          </style>
        </head>
        <body>
            <div class="card">
                <h1><b>{server_time}</b></h1>
                <p>Aika on pysähtynyt 🕒</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

