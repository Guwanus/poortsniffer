import socket
import concurrent.futures

def scan_port(ip, port):
    """Probeert een poort op het opgegeven IP-adres te openen."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return port if s.connect_ex((ip, port)) == 0 else None

def port_sniffer(ip, start_port=1, end_port=1024, max_threads=1000):
    """Scant de opgegeven poorten op het IP-adres met multi-threading."""
    open_ports = []
    print(f"Scannen van {ip} voor open poorten ({start_port}-{end_port})...")

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                print(f"Poort {port} is open.")
                open_ports.append(port)

    if open_ports:
        print("Open poorten:", open_ports)
    else:
        print("Geen open poorten gevonden.")

if __name__ == "__main__":
    target_ip = input("Voer het IP-adres in dat je wilt scannen: ")
    start_port = int(input("Voer de startpoort in: ") or 1)
    end_port = int(input("Voer de eindpoort in: ") or 1024)
    
    if start_port > end_port or start_port < 1 or end_port > 65535:
        print("Ongeldig poortbereik. Voer een geldig bereik in (1-65535).")
    else:
        port_sniffer(target_ip, start_port, end_port)