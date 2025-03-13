import socket
import concurrent.futures
import pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)

# Database configuratie
DB_SERVER = 'GUWAN\SQLEXPRESS'   
DB_DATABASE = 'poortsniffer' 
DB_USERNAME = 'snifferwriteonly'
DB_PASSWORD = 'Welkom01'

def connect_database():
    """Maakt verbinding met de MSSQL-database."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD}"
        )
        return conn
    except Exception as e:
        print(f"Fout bij verbinden met de database: {e}")
        return None

def save_to_database(ip, port):
    """Slaat een open poort op in de MSSQL database."""
    conn = connect_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO OpenPorts (ip_address, port, scan_time) VALUES (?, ?, GETDATE())",
                (ip, port)
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Fout bij opslaan in database: {e}")
        finally:
            conn.close()

def scan_port(ip, port):
    """Probeert een poort op het opgegeven IP-adres te openen."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            save_to_database(ip, port)  # Sla open poort op in de database
            return port
    return None

def port_sniffer(ip, start_port=1, end_port=65535, max_threads=1000):
    """Scant de opgegeven poorten op het IP-adres en slaat open poorten op in MSSQL."""
    open_ports = []
    print(f"Scannen van {ip} voor open poorten ({start_port}-{end_port})...")

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)

    return open_ports

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        target_ip = request.form["ip"]
        start_port = int(request.form["start_port"])
        end_port = int(request.form["end_port"])

        if start_port > end_port or start_port < 1 or end_port > 65535:
            results = "Ongeldig poortbereik. Voer een geldig bereik in (1-65535)."
        else:
            results = port_sniffer(target_ip, start_port, end_port)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)